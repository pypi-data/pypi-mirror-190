"""
Functions for managing incremental imports on an RDG.
"""
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional

from katana_enterprise.distributed import single_host
from katana_enterprise.remote import import_data
from katana_enterprise.remote.aio.import_data import Operation
from katana_enterprise.remote.sync_wrappers import Graph

__all__ = [
    "SourceSystem",
    "upsert_incremental_node_source",
    "upsert_incremental_edge_source",
    "remove_incremental_source",
    "incremental_refresh",
]


class EntityKind(Enum):
    Nodes = "nodes"
    Edges = "edges"


class SourceSystem(Enum):
    Delta = "Delta"


PandasOrDaskDataFrame = Any  # Not type checking this, but it's useful for documentation.


@dataclass
class ChangeDataFeedEntry:
    """
    Describes one step in a change data feed. It's a single DataFrame.
    The records can be loaded in any order, and they all represent the same operation.
    """

    # Representing versions is up to the data sources.
    # The version can be omitted if this entry does not complete any version.
    # (It will still be loaded.)
    version: Optional[Any]
    df: PandasOrDaskDataFrame
    operation: Operation
    may_be_empty: bool  # TODO: Remove this when DataFrameImporter supports empty inputs.


def _import_df(graph: Graph, operation: Operation, df: PandasOrDaskDataFrame, kind: EntityKind, **kwargs):
    """
    Imports a change data table into the graph.

    :param kwargs: Passed to the DataFrameImporter.
    """
    with import_data.DataFrameImporter(graph) as dfi:
        if kind is EntityKind.Nodes:
            dfi.nodes_dataframe(df, **kwargs)
        elif kind is EntityKind.Edges:
            dfi.node_id_property_name(kwargs.pop("id_column"))
            dfi.edges_dataframe(df, **kwargs)
        else:
            raise ValueError(f"Kind must be 'EntityKind.Nodes' or 'EntityKind.Edges'. Got '{kind}'.")
        if operation is Operation.Insert:
            dfi.insert()
        elif operation is Operation.Update:
            dfi.update()
        elif operation is Operation.Delete:
            dfi.delete()
        else:
            raise ValueError(f"Unexpected operation: {operation}")


# A graph property with this name is used to store the configured sources and their current status.
_METADATA_PROPERTY = "incremental-data-sources"


def _get_metadata(graph: Graph):
    try:
        return single_host(graph.get_graph_property(_METADATA_PROPERTY))
    except LookupError:
        return None


def _set_metadata(graph: Graph, metadata):
    graph.upsert_graph_property(_METADATA_PROPERTY, metadata)


def _upsert_incremental_source(
    graph: Graph, source_id: str, system: SourceSystem, path: str, kind: EntityKind, **kwargs,
):
    """
    Configures an incremental data source for this graph.

    :param source_id: This string will identify this source. You can re-run this function
        with the same source_id and different configuration to make changes.
    :param system: The name of the system that has this source. One of: "DELTA"
    :param path: The path to the source table in the format used by the source system.
    :param kind: Nodes or edges.
    :param kwargs: Passed to the DataFrameImporter.
    """
    sources = graph.run(_get_metadata) or {}
    old = sources.get(source_id)
    source = dict(
        id=source_id, system=system.value, path=path, kind=kind.value, kwargs=kwargs,
        loaded_version=old["loaded_version"] if old else 0,
    )
    if source != old:
        sources[source_id] = source
        graph.run(lambda g: _set_metadata(g, sources))


def upsert_incremental_node_source(graph: Graph, source_id: str, system: SourceSystem, path: str, **kwargs):
    """
    Configures an incremental data source for nodes of this graph.

    :param source_id: This string will identify this source. You can re-run this function
        with the same source_id and different configuration to make changes.
    :param system: The name of the system that has this source. One of: "DELTA"
    :param path: The path to the source table in the format used by the source system.
    :param kwargs: Passed to the DataFrameImporter.
    """
    _upsert_incremental_source(graph, source_id, system, path, EntityKind.Nodes, **kwargs)


def upsert_incremental_edge_source(graph: Graph, source_id: str, system: SourceSystem, path: str, **kwargs):
    """
    Configures an incremental data source for edges of this graph.

    :param source_id: This string will identify this source. You can re-run this function
        with the same source_id and different configuration to make changes.
    :param system: The name of the system that has this source. One of: "DELTA"
    :param path: The path to the source table in the format used by the source system.
    :param kwargs: Passed to the DataFrameImporter.
    """
    _upsert_incremental_source(graph, source_id, system, path, EntityKind.Edges, **kwargs)


def remove_incremental_source(graph: Graph, source_id: str):
    """
    Removes a previously defined incremental data source.
    """
    sources = graph.run(_get_metadata) or {}
    del sources[source_id]
    graph.run(lambda g: _set_metadata(g, sources))


def incremental_refresh(graph: Graph):
    """
    Checks all configured incremental data sources for this graph and loads anything new.
    """
    sources = graph.run(_get_metadata)
    if sources is None:
        raise ValueError(f"No incremental sources configured on graph {graph}")
    todo = list(sources.values())
    for source in sorted(todo, key=lambda s: s["kind"], reverse=True):  # Update nodes before edges.
        cdf = _load_table_cdf(source)
        for e in cdf:
            if not e.may_be_empty or len(e.df) > 0:
                _import_df(graph, e.operation, e.df, EntityKind(source["kind"]), **source["kwargs"])
            # Update last version at every step to make sure we can recover from errors where we left off.
            if e.version is not None:
                source["loaded_version"] = e.version
            graph.run(lambda g: _set_metadata(g, sources))


def _load_table_cdf(source) -> List[ChangeDataFeedEntry]:
    """
    Dispatches the loading to the right data source.
    """
    loaded_version = source["loaded_version"]
    system = SourceSystem(source["system"])
    path = source["path"]
    if system is SourceSystem.Delta:
        return _load_delta_sharing_cdf(path, loaded_version)
    else:
        sid = source["id"]
        raise ValueError(f"Incremental data source {sid} uses an unsupported system: {system}")


def _split_mixed(
    df: PandasOrDaskDataFrame, column: str, insert_label: str, delete_label: str, update_label: str
) -> List[ChangeDataFeedEntry]:
    """
    Delta has mixed ("cdc") tables that contain records that can be inserts/updates/deletes independently.
    This function splits up such a table into separate ChangeDataFeedEntries.
    """
    res = []
    updates = df.query(f"{column} == '{update_label}'").drop(columns=column)
    deletes = df.query(f"{column} == '{delete_label}'").drop(columns=column)
    inserts = df.query(f"{column} == '{insert_label}'").drop(columns=column)
    # The order is important: updates and deletes are idempotent. Conclude the version with the inserts.
    return [
        ChangeDataFeedEntry(None, updates, Operation.Update, may_be_empty=True),
        ChangeDataFeedEntry(None, deletes, Operation.Delete, may_be_empty=True),
        ChangeDataFeedEntry(None, inserts, Operation.Insert, may_be_empty=True),
    ]


def _load_delta_sharing_cdf(path, loaded_version) -> List[ChangeDataFeedEntry]:
    # Optional import. Only needed for Delta Sharing tables.
    import dask_deltasharing

    source_version = dask_deltasharing.get_latest_table_version(path)
    if source_version <= loaded_version:
        return []
    res = []
    cdf = dask_deltasharing.load_as_dask_changes(
        path, starting_version=loaded_version + 1, ending_version=source_version,
    )
    for version, change, df in cdf:
        if change == "add":
            res.append(ChangeDataFeedEntry(version, df, Operation.Insert, may_be_empty=False))
        elif change == "remove":
            res.append(ChangeDataFeedEntry(version, df, Operation.Delete, may_be_empty=False))
        elif change == "cdc":
            split = _split_mixed(
                df,
                column="_change_type",
                insert_label="insert",
                delete_label="delete",
                update_label="update_postimage",
            )
            if split:
                split[-1].version = version  # Only set the version number after the last step.
                res.extend(split)
        else:
            raise ValueError(f"Incremental data source {path} returned unexpected change: {change}")
    return res


def get_or_create_graph(client, name, **kwargs):
    matches = client.find_graphs_by_name(name)
    if len(matches) == 0:
        return client.create_graph(name=name, **kwargs)
    elif len(matches) == 1:
        return matches[0]
    else:
        raise ValueError(f"Multiple graphs found named {name}")