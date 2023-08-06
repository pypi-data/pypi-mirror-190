import codified_json as cjson
import json

# Copy/pasted from the "forecast example" at the bottom of this "weatherapi" website:
# - https://www.weatherapi.com/
json_file = 'tests/weather_forecast.json'
with open(json_file, 'r') as f:
    weather_data = json.load(f)

filename = 'tests/weather_forecast_structs_array.codf.json'
with open(filename, 'r') as f:
    cjson_str = f.read()

filename2 = 'tests/weather_forecast.codf.json'
with open(filename2, 'r') as f:
    cjson_str2 = f.read()


def test_as_str():
    assert cjson.as_str(weather_data, structures_as_array=True) == cjson_str
    assert cjson.as_str(weather_data) == cjson_str2


def test_parse_str():
    assert cjson.parse_str(cjson_str) == weather_data
    assert cjson.parse_str(cjson_str2) == weather_data


def test_read_from_file():
    newfilename = 'tests/tmp/test.codf.json'
    cjson.write_to_file(weather_data, newfilename)
    assert cjson.read_from_file(newfilename) == weather_data


def test_read_from_compressed_bytes_file():
    newfilename = 'tests/tmp/test.codf.json.gz'
    cjson.write_to_compressed_bytes_file(weather_data, newfilename)
    assert cjson.read_from_compressed_bytes_file(newfilename) == weather_data
