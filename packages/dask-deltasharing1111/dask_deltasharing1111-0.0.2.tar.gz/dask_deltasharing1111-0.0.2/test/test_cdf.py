"""Test for accessing change tables."""
import dask_deltasharing as dds

T = "test/test-profile.json#lynxkite-dev.default.silvertable"
v = dds.get_latest_table_version(T)
for action, df in dds.load_as_dask_changes(T, starting_version=4, ending_version=v):
    print(action)
    print(df.compute())
