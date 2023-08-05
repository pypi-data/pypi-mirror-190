from nazca4sdk.sdk import SDK
import time

sdk = SDK(False)

start_time = time.time()
data = sdk.variable_over_time('H-M', ['Flow V1'], 30, 'DAY')
print(type(data))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(data))

start_time = time.time()
dask_data = sdk.variable_over_time('H-M', ['Flow V1'], 30, 'DAY', dask=True)
print('----------------------')
print(type(dask_data))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(dask_data))

start_time = time.time()
data_day = data = sdk.variable_over_day('H-M', ['Flow V1'], '2023-01-01T10:00:00', '2023-01-19T10:00:00')
print('----------------------')
print(type(data_day))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(data_day))

start_time = time.time()
data_dask_day = sdk.variable_over_day('H-M', ['Flow V1'], '2023-01-01T10:00:00', '2023-01-19T10:00:00', dask=True)
print('----------------------')
print(type(data_dask_day))
print("--- %s seconds ---" % round((time.time() - start_time), 2))
print(len(data_dask_day))
