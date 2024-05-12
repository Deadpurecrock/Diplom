import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

token = "IcnSAex8pK2KWaZlk_dLqKlaSCOgvDBPscjkDwx493iMYSyXQCqgNZ422NfPUwUeIARgccR7NBxt0Mv6Uv5Q-A=="
org = "MIREA"
url = "http://127.0.0.1:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="PCB"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

query_api = write_client.query_api()


def get_oven_params():
    param_name = ["Temperature_1", "Temperature_2","Temperature_3", "Temperature_4", "Temperature_5", "Pressure"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "PCB")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Oven")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org="MIREA")
        param_values[name] = table[0].records[0].get_value()
    return param_values

def get_convey_params():
    param_name = ["Speed", "Plates_1", "Plates_2", "Plates_3"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "PCB")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Conveys")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org="MIREA")
        param_values[name] = table[0].records[0].get_value()
    return param_values

def get_printer_params():
    param_name = ["Axis", "SolderPaste", "Temperature"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "PCB")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Printer")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org="MIREA")
        param_values[name] = table[0].records[0].get_value()
    return param_values


def get_defender_params():
    param_name = ["DefendAxis", "DefendLiquid"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "PCB")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Defender")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org="MIREA")
        param_values[name] = table[0].records[0].get_value()
    return param_values


def get_cleaner_params():
    param_name = ["Temperature", "LiqLevel", "CleaningLiquid"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "PCB")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Cleaner")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org="MIREA")
        param_values[name] = table[0].records[0].get_value()
    return param_values

def get_pick_params():
    param_name = ["Axis", "Components"]
    param_values = {}
    for name in param_name:
        query = f"""from(bucket: "PCB")
  |> range(start: -10s, stop: now())
  |> filter(fn: (r) => r["_measurement"] == "Pick_and_Place")
  |> filter(fn: (r) => r["Type"] == "Sensor")
  |> filter(fn: (r) => r["Name"] == "{name}")
  |> filter(fn: (r) => r["_field"] == "Value")
  |> last()"""
        table = query_api.query(query, org="MIREA")
        param_values[name] = table[0].records[0].get_value()
    return param_values




if __name__ == "__main__":
    # print(get_oven_params())
    # print(get_convey_params())
    print(get_pick_params())
