import random
import time

from influxdb_client import Point

from influxdb_client.client.write_api import SYNCHRONOUS
from db_connect import generate_failure, change_state

from influxdb_client.client import influxdb_client

token = "IcnSAex8pK2KWaZlk_dLqKlaSCOgvDBPscjkDwx493iMYSyXQCqgNZ422NfPUwUeIARgccR7NBxt0Mv6Uv5Q-A=="
org = "MIREA"
url = "http://127.0.0.1:8086"

write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)

bucket="PCB"

write_api = write_client.write_api(write_options=SYNCHRONOUS)

query_api = write_client.query_api()

plate_num_1 = 0.0
plate_num_2 = 0.0
plate_num_3 = 0.0
done_plates = 0
paste_cnt = 452.0
clean_liq = 490.0
clean_liq_level = 125
defend_liq = 600.0
components = 120000.0

def generate_data():

    for value in range(2000):

        for i in range(1, 12):
            change_state(i, 7)

        temp_1 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_1")
            .field("Value", random.uniform(95, 130))
        )
        temp_2 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_2")
            .field("Value", random.uniform(150, 170))
        )

        temp_3 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_3")
            .field("Value", random.uniform(170, 230))
        )

        temp_4 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_4")
            .field("Value", random.uniform(210, 230))
        )

        temp_5 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_5")
            .field("Value", random.uniform(100, 230))
        )

        temp_printer = (
            Point("Printer")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature")
            .field("Value", random.uniform(30, 32))
        )

        temp_cleaner = (
            Point("Cleaner")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature")
            .field("Value", random.uniform(30, 32))
        )

        axis_printer = (
            Point("Printer")
            .tag("Type", "Sensor")
            .tag("Name", "Axis")
            .field("Value", float(random.randint(1, 1024)))
        )

        pres = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Pressure")
            .field("Value", random.uniform(1, 3))
        )

        speed = (
            Point("Conveys")
            .tag("Type", "Sensor")
            .tag("Name", "Speed")
            .field("Value", random.uniform(0.5, 2))
        )

        global components
        components -= 10
        component_pick = (
            Point("Pick_and_Place")
            .tag("Type", "Sensor")
            .tag("Name", "Components")
            .field("Value", components)
        )

        axis_pick = (
            Point("Pick_and_Place")
            .tag("Type", "Sensor")
            .tag("Name", "Axis")
            .field("Value", float(random.randint(1, 1024)))
        )
        

        if value % 150 == 0:
            global plate_num_1
            if (plate_num_1 > 100):
                plate_num_1 = 0
            plate_num_1 += 1
            fullness_1 = (
                Point("Conveys")
                .tag("Type", "Sensor")
                .tag("Name", "Plates_1")
                .field("Value", float(plate_num_1))
            )
            generate_failure(1, 4, "нанесения паяльной пасты.")
            state_changer(4)
        
        if value % 160 == 0:
            global plate_num_2
            if (plate_num_2 > 100):
                plate_num_2 = 0
            plate_num_2 += 1
            fullness_2 = (
                Point("Conveys")
                .tag("Type", "Sensor")
                .tag("Name", "Plates_2")
                .field("Value", float(plate_num_2))
            )
            generate_failure(2, 6, "пайки в печи.")
        
        if value % 350 == 0:
            global plate_num_3
            if (plate_num_3 > 100):
                plate_num_3 = 0
            plate_num_3 += 1
            fullness_3 = (
                Point("Conveys")
                .tag("Type", "Sensor")
                .tag("Name", "Plates_3")
                .field("Value", float(plate_num_3))
            )
            generate_failure(3, 6, "финального теста.")
            

        if value % 4 == 0:
            global paste_cnt
            paste_cnt -= 0.01
            solder = (
                Point("Printer")
                .tag("Type", "Sensor")
                .tag("Name", "SolderPaste")
                .field("Value", float(paste_cnt))
            )
            state_changer(1)

        
        if value % 6 == 0:
            global clean_liq
            clean_liq -= 0.06
            cleaner = (
                Point("Cleaner")
                .tag("Type", "Sensor")
                .tag("Name", "CleaningLiquid")
                .field("Value", float(clean_liq))
            )
            global clean_liq_level
            clean_liq_level -= 0.15
            liq_level_cleaner = (
            Point("Cleaner")
            .tag("Type", "Sensor")
            .tag("Name", "LiqLevel")
            .field("Value", float(clean_liq_level))
            )
            state_changer(2)
        
        if value % 8 == 0:
            global defend_liq
            defend_liq -= 0.2
            defender = (
                Point("Defender")
                .tag("Type", "Sensor")
                .tag("Name", "DefendLiquid")
                .field("Value", float(defend_liq))
            )
            state_changer(3)
        
        if value % 60 == 0:
            global done_plates
            done_plates += 1
            plates = (
                Point("Conveys")
                .tag("Type", "Sensor")
                .tag("Name", "DonePlates")
                .field("Value", float(done_plates))
            )

        defend_axis = (
            Point("Defender")
            .tag("Type", "Sensor")
            .tag("Name", "DefendAxis")
            .field("Value", float(random.randint(1, 1024)))
        )      

        write_api.write(bucket="PCB", org="MIREA", record=temp_1)
        write_api.write(bucket="PCB", org="MIREA", record=temp_2)
        write_api.write(bucket="PCB", org="MIREA", record=temp_3)
        write_api.write(bucket="PCB", org="MIREA", record=temp_4)
        write_api.write(bucket="PCB", org="MIREA", record=temp_5)

        write_api.write(bucket="PCB", org="MIREA", record=temp_printer)
        write_api.write(bucket="PCB", org="MIREA", record=axis_printer)

        write_api.write(bucket="PCB", org="MIREA", record=temp_cleaner)

        write_api.write(bucket="PCB", org="MIREA", record=liq_level_cleaner)

        write_api.write(bucket="PCB", org="MIREA", record=pres)

        write_api.write(bucket="PCB", org="MIREA", record=speed)

        write_api.write(bucket="PCB", org="MIREA", record=fullness_1)
        write_api.write(bucket="PCB", org="MIREA", record=fullness_2)
        write_api.write(bucket="PCB", org="MIREA", record=fullness_3)

        write_api.write(bucket="PCB", org="MIREA", record=solder)

        write_api.write(bucket="PCB", org="MIREA", record=cleaner)

        write_api.write(bucket="PCB", org="MIREA", record=defender)
        write_api.write(bucket="PCB", org="MIREA", record=defend_axis)

        write_api.write(bucket="PCB", org="MIREA", record=component_pick)
        write_api.write(bucket="PCB", org="MIREA", record=axis_pick)

        write_api.write(bucket="PCB", org="MIREA", record=plates)

        time.sleep(1)

def state_changer(num):
    if num == 1:
        change_state(3, 7)
        change_state(4, 1)
        change_state(5, 1)
        change_state(6, 1)
        change_state(7, 4)
        change_state(8, 1)
        change_state(9, 1)
        change_state(10, 1)
        change_state(11, 1)
    elif num == 2:
        change_state(3, 7)
        change_state(4, 9)
        change_state(5, 13)
        change_state(6, 14)
        change_state(7, 5)
        change_state(8, 13)
        change_state(9, 11)
        change_state(10, 12)
        change_state(11, 13)
    elif num == 3:
        change_state(1, 10)
        change_state(3, 7)
        change_state(4, 13)
        change_state(5, 7)
        change_state(6, 7)
        change_state(7, 6)
        change_state(8, 7)
        change_state(9, 7)
        change_state(10, 7)
        change_state(11, 7)
    elif num == 4:
        change_state(3,10)

def change_params(zone, value):

    if zone == 1:
        temp_1 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_1")
            .field("Value", value)
        )
        write_api.write(bucket="PCB", org="MIREA", record=temp_1)
        
    elif zone == 2:
        temp_2 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_2")
            .field("Value", value)
        )
        write_api.write(bucket="PCB", org="MIREA", record=temp_2)

    elif zone == 3:
        temp_3 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_3")
            .field("Value", value)
        )
        write_api.write(bucket="PCB", org="MIREA", record=temp_3)

    elif zone == 4:
        temp_4 = (
            Point("Oven")
            .tag("Type", "Sensor")
            .tag("Name", "Temperature_4")
            .field("Value", value)
        )
        write_api.write(bucket="PCB", org="MIREA", record=temp_4)

    elif zone == 5:
        for i in range(0, 6):
            temp_5 = (
                Point("Oven")
                .tag("Type", "Sensor")
                .tag("Name", "Temperature_5")
                .field("Value", value)
            )
            write_api.write(bucket="PCB", org="MIREA", record=temp_5)
    
    time.sleep(1)

if __name__ == "__main__":
    generate_data()