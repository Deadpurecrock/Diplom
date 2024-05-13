import mysql.connector

mydb = mysql.connector.connect(user = 'root',
                                password = '123054', 
                                host = '127.0.0.1', 
                                database = 'diplom')

cursor = mydb.cursor()

### Названия датчиков
def get_sensor_oven():
    cursor.execute("SELECT s.name, ps.type FROM sensor AS s JOIN parameter AS p ON s.Parameter_id_Par = p.id_Par JOIN Parameter_Standard AS ps ON p.Parameter_Standard_id_PS = ps.id_PS WHERE s.Equipment_id_E = 7")
    result = cursor.fetchall()
    return result

def get_sensor_printer():
    cursor.execute("SELECT s.name, ps.type FROM sensor AS s JOIN parameter AS p ON s.Parameter_id_Par = p.id_Par JOIN Parameter_Standard AS ps ON p.Parameter_Standard_id_PS = ps.id_PS WHERE s.Equipment_id_E = 4")
    result = cursor.fetchall()
    return result

def get_sensor_cleaner():
    cursor.execute("SELECT s.name, ps.type FROM sensor AS s JOIN parameter AS p ON s.Parameter_id_Par = p.id_Par JOIN Parameter_Standard AS ps ON p.Parameter_Standard_id_PS = ps.id_PS WHERE s.Equipment_id_E = 9")
    result = cursor.fetchall()
    return result

def get_sensor_defender():
    cursor.execute("SELECT s.name, ps.type FROM sensor AS s JOIN parameter AS p ON s.Parameter_id_Par = p.id_Par JOIN Parameter_Standard AS ps ON p.Parameter_Standard_id_PS = ps.id_PS WHERE s.Equipment_id_E = 10")
    result = cursor.fetchall()
    return result

def get_sensor_pick_place():
    cursor.execute("SELECT s.name, ps.type FROM sensor AS s JOIN parameter AS p ON s.Parameter_id_Par = p.id_Par JOIN Parameter_Standard AS ps ON p.Parameter_Standard_id_PS = ps.id_PS WHERE s.Equipment_id_E = 6")
    result = cursor.fetchall()
    return result

def get_sensor_pick_place():
    cursor.execute("SELECT s.name, ps.type FROM sensor AS s JOIN parameter AS p ON s.Parameter_id_Par = p.id_Par JOIN Parameter_Standard AS ps ON p.Parameter_Standard_id_PS = ps.id_PS WHERE s.Equipment_id_E = 6")
    result = cursor.fetchall()
    return result

### Названия ресурсов
def get_resource_printer():
    cursor.execute("SELECT r.name, rs.type FROM Resource AS r JOIN Resource_Standard AS rs ON r.Resource_Standard_id_RS = rs.id_RS JOIN Equipment AS e ON r.id_R = e.Resource_id_R WHERE e.id_E = 4")
    result = cursor.fetchall()
    return result

def get_resource_cleaner():
    cursor.execute("SELECT r.name, rs.type FROM Resource AS r JOIN Resource_Standard AS rs ON r.Resource_Standard_id_RS = rs.id_RS JOIN Equipment AS e ON r.id_R = e.Resource_id_R WHERE e.id_E = 9")
    result = cursor.fetchall()
    return result

def get_resource_pick_place():
    cursor.execute("SELECT r.name, rs.type FROM Resource AS r JOIN Resource_Standard AS rs ON r.Resource_Standard_id_RS = rs.id_RS JOIN Equipment AS e ON r.id_R = e.Resource_id_R WHERE e.id_E = 6")
    result = cursor.fetchall()
    return result

def get_resource_defender():
    cursor.execute("SELECT r.name, rs.type FROM Resource AS r JOIN Resource_Standard AS rs ON r.Resource_Standard_id_RS = rs.id_RS JOIN Equipment AS e ON r.id_R = e.Resource_id_R WHERE e.id_E = 10")
    result = cursor.fetchall()
    return result

### Названия состояний AOI
def get_aois_states():
    cursor.execute("SELECT e.name, s.name FROM State AS s JOIN Equipment AS e ON s.id_S = e.State_id_S WHERE e.id_E = 5 OR e.id_E = 8 OR e.id_E = 11")
    result = cursor.fetchall()
    return result

def get_aois_failures():
    cursor.execute("SELECT name, description, date FROM Terminal_Record")
    result = cursor.fetchall()
    return result


def get_errors():
    cursor.execute("SELECT name, date, description FROM Error_Log")
    result = cursor.fetchall()
    return result

def get_conveys_params():
    cursor.execute("SELECT d.serial, dt.type FROM Device AS d JOIN Device_Type AS dt ON d.Device_Type_id_DT = dt.id_DT WHERE d.id_Dev = 7 OR d.id_Dev = 9")
    result = cursor.fetchall()
    return result

def get_users():
    cursor.execute("SELECT login, password FROM User")
    result = cursor.fetchall()
    return result


def generate_failure(n, id_E, fail):
    cursor.execute(f"INSERT INTO Terminal_Record(name, date, description, Equipment_id_E) VALUES ('Брак платы буффер №{n}', NOW(), 'Плата не прошла проверку после {fail}', {id_E})")
    cursor.execute("COMMIT")

def change_state(id_E, state):
    cursor.execute(f"UPDATE Equipment SET State_id_S = '{state}' WHERE id_E = {id_E}")
    cursor.execute("COMMIT")



if __name__ == "__main__":
    # print(get_sensor_oven())
    # print(get_conveys_params())
    # print(get_users())
    # print(get_aois_states())
    # print(get_resource_defender())
    print(get_aois_failures())

    '''
    ('Брак платы буффер №1', 'Плата не прошла проверку после нанесения паяльной пасты.', datetime.datetime(2024, 5, 12, 3, 30, 24))
    '''