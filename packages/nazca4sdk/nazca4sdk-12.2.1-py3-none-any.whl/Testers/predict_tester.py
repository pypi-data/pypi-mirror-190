from nazca4sdk.sdk import SDK

sdk = SDK(False)

print(sdk.predict('symulator', 'V1', 15, 'MINUTE', 3, 'min', 'prophet'))
