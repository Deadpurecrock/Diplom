
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic
from windows.main_window import Ui_MainWindow
from windows.login import Ui_Login_Page
from windows.oven_zones_edit import Ui_Oven_page
import sys
from db_connect import get_sensor_oven, get_errors, get_conveys_params, get_users, get_sensor_printer, get_sensor_cleaner, get_sensor_defender, get_sensor_pick_place, get_aois_states
from db_connect import get_resource_printer, get_resource_cleaner, get_resource_pick_place, get_resource_defender, get_aois_failures
from influx_connect import get_oven_params, get_convey_params, get_printer_params, get_cleaner_params, get_defender_params, get_pick_params, get_done_plates
from generator import change_params as generator_change

def change_widget(self, n):
    self.ui.pages_TP.setCurrentIndex(n)


def check_login(window, login, password):
    
    key = (login, password)

    if key in get_users():
        print(f"Login of user: {login} - successful!")
        window.setHidden(True)
        window.main.show()
    else:
        print("error")


def stop_process(self):
    self.ui.lamp_loader.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_printer.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_oven.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_spi.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_aoi.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_collector_1.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_collector_2.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_collector_3.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_plate_tester.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_pick_place.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_cleaner.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_defender.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))
    self.ui.lamp_plate_tester.setPixmap(QtGui.QPixmap("./client/images/red_light.png"))

    msg = QtWidgets.QMessageBox()
    msg.setWindowTitle("STOP")
    msg.setText("Процесс остановлен!")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.exec_()


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.oven_edit = OvenPage()

        self.ui.but_oven.clicked.connect(lambda: change_widget(self, 0))
        self.ui.but_conveys.clicked.connect(lambda: change_widget(self, 1))
        self.ui.but_loader.clicked.connect(lambda: change_widget(self, 1))
        self.ui.but_collector_1.clicked.connect(lambda: change_widget(self, 1))
        self.ui.but_collector_2.clicked.connect(lambda: change_widget(self, 1))
        self.ui.but_collector_3.clicked.connect(lambda: change_widget(self, 1))
        self.ui.but_printer.clicked.connect(lambda: change_widget(self, 2))
        self.ui.but_spi.clicked.connect(lambda: change_widget(self, 3))
        self.ui.but_aoi.clicked.connect(lambda: change_widget(self, 3))
        self.ui.but_plate_tester.clicked.connect(lambda: change_widget(self, 3))
        self.ui.but_pick_place.clicked.connect(lambda: change_widget(self, 4))
        self.ui.but_cleaner.clicked.connect(lambda: change_widget(self, 5))
        self.ui.but_defender.clicked.connect(lambda: change_widget(self, 6))
        
        self.ui.but_stop.clicked.connect(lambda: stop_process(self))

        self.ui.but_oven_edit.clicked.connect(lambda: self.oven_edit_win())

        self.ui.table_oven.setColumnWidth(0, 300)
        self.ui.table_oven.setColumnWidth(1, 200)

        self.ui.table_conv.setColumnWidth(0, 165)
        self.ui.table_conv.setColumnWidth(1, 200)
        self.ui.table_conv.setColumnWidth(2, 122)
        self.ui.table_conv.setColumnWidth(3, 146)

        self.ui.table_spi_ban.setColumnWidth(0, 212)
        self.ui.table_spi_ban.setColumnWidth(1, 220)
        self.ui.table_spi_ban.setColumnWidth(2, 181)

        self.ui.table_spi.setColumnWidth(0, 309)
        self.ui.table_spi.setColumnWidth(1, 352)

        self.ui.table_oven_2.setColumnWidth(0, 345)
        self.ui.table_oven_2.setColumnWidth(1, 252)
        self.ui.table_oven_2.setColumnWidth(2, 96)

        self.ui.table_conv_2.setColumnWidth(0, 253)
        self.ui.table_conv_2.setColumnWidth(1, 243)
        self.ui.table_conv_2.setColumnWidth(2, 96)

        self.ui.table_pick_material.setColumnWidth(0, 253)
        self.ui.table_pick_material.setColumnWidth(1, 243)
        self.ui.table_pick_material.setColumnWidth(2, 96)

        self.ui.table_pick_material_2.setColumnWidth(0, 253)
        self.ui.table_pick_material_2.setColumnWidth(1, 243)
        self.ui.table_pick_material_2.setColumnWidth(2, 96)

        self.ui.table_pick_material_3.setColumnWidth(0, 253)
        self.ui.table_pick_material_3.setColumnWidth(1, 243)
        self.ui.table_pick_material_3.setColumnWidth(2, 96)

        self.ui.table_pick_sensor.setColumnWidth(0, 345)
        self.ui.table_pick_sensor.setColumnWidth(1, 252)
        self.ui.table_pick_sensor.setColumnWidth(2, 96)
        
        self.ui.table_pick_sensor_2.setColumnWidth(0, 345)
        self.ui.table_pick_sensor_2.setColumnWidth(1, 252)
        self.ui.table_pick_sensor_2.setColumnWidth(2, 96)

        self.ui.table_pick_sensor_3.setColumnWidth(0, 345)
        self.ui.table_pick_sensor_3.setColumnWidth(1, 252)
        self.ui.table_pick_sensor_3.setColumnWidth(2, 96)

        self.ui.table_oven_err.setColumnWidth(0, 275)
        self.ui.table_oven_err.setColumnWidth(1, 370)
        self.ui.table_oven_err.setColumnWidth(2, 189)

        self.ui.table_conv_err.setColumnWidth(0, 163)
        self.ui.table_conv_err.setColumnWidth(1, 193)
        self.ui.table_conv_err.setColumnWidth(2, 180)

        self.ui.table_prnt_err.setColumnWidth(0, 163)
        self.ui.table_prnt_err.setColumnWidth(1, 193)
        self.ui.table_prnt_err.setColumnWidth(2, 180)

        self.ui.table_spi_err.setColumnWidth(0, 163)
        self.ui.table_spi_err.setColumnWidth(1, 193)
        self.ui.table_spi_err.setColumnWidth(2, 180)

        self.ui.table_pick_err.setColumnWidth(0, 163)
        self.ui.table_pick_err.setColumnWidth(1, 193)
        self.ui.table_pick_err.setColumnWidth(2, 180)

        self.ui.table_pick_err_2.setColumnWidth(0, 163)
        self.ui.table_pick_err_2.setColumnWidth(1, 193)
        self.ui.table_pick_err_2.setColumnWidth(2, 180)

        self.ui.table_pick_err_3.setColumnWidth(0, 163)
        self.ui.table_pick_err_3.setColumnWidth(1, 193)
        self.ui.table_pick_err_3.setColumnWidth(2, 180)

        self.ui.table_oven.setEnabled(False)

        self.lamps_light()

        self.oven_table_titles()
        
        self.printer_table_titles()
        self.printer_resource_table_titles()

        self.cleaner_table_titles()
        self.cleaner_resource_table_titles()

        self.aoi_table_titles()

        self.defender_table_titles()
        self.defender_resource_table_titles()

        self.pick_place_table_titles()
        self.pick_resource_table_titles()

        

        self.errors = []
        self.bans = []
        self.get_convey_params()
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.get_params)
        self.timer.start()

    def display_plates(self):
        result = get_done_plates()
        self.ui.lcd_done.display(int(result['DonePlates']))

    def get_params(self):
        ##  Обновляемые функции
        self.error_table_refresh()
        self.oven_table_refresh()
        self.conveys_table_resresh()
        self.ban_table_refresh()
        self.printer_table_refresh()
        self.cleaner_table_refresh()
        # self.aoi_table_refresh()
        self.defender_table_refresh()
        self.pick_table_refresh()
        self.display_plates()

    def printer_table_refresh(self):
        result = get_printer_params()
        print("РТ Параметры Принтера", result)

        self.ui.table_oven_2.setItem (0, 1, QtWidgets.QTableWidgetItem(str(round(result['Temperature'], 3))))
        if (result['SolderPaste'] <10):
            self.ui.table_oven_2.setItem(1, 1, QtWidgets.QTableWidgetItem('Заканчивается'))
        else:
            self.ui.table_oven_2.setItem(1, 1, QtWidgets.QTableWidgetItem('В наличии'))
        self.ui.table_oven_2.setItem(2, 1, QtWidgets.QTableWidgetItem(str(round(result['Axis']))))
        self.ui.table_conv_2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(round(result['SolderPaste'], 3))))

    def pick_table_refresh(self):
        result = get_pick_params()
        print(result)
        self.ui.table_pick_sensor.setItem (0, 1, QtWidgets.QTableWidgetItem(str(round(result['Axis'], 3))))
        if (result['Components'] < 100):
            self.ui.table_pick_sensor.setItem(1, 1, QtWidgets.QTableWidgetItem('Заканчивается'))
        else:
            self.ui.table_pick_sensor.setItem(1, 1, QtWidgets.QTableWidgetItem('В наличии'))
        self.ui.table_pick_material.setItem(0, 1, QtWidgets.QTableWidgetItem(str(round(result['Components'], 3))))

    def cleaner_table_refresh(self):
        result = get_cleaner_params()
        print(result)
        self.ui.table_pick_sensor_2.setItem (0, 1, QtWidgets.QTableWidgetItem(str(round(result['Temperature'], 3))))
        if (result['CleaningLiquid'] < 10):
            self.ui.table_pick_sensor_2.setItem(1, 1, QtWidgets.QTableWidgetItem('Заканчивается'))
        else:
            self.ui.table_pick_sensor_2.setItem(1, 1, QtWidgets.QTableWidgetItem('В наличии'))
        
        self.ui.table_pick_sensor_2.setItem (2, 1, QtWidgets.QTableWidgetItem(str(round(result['LiqLevel'], 3))))
        self.ui.table_pick_material_2.setItem(0, 1, QtWidgets.QTableWidgetItem(str(round(result['CleaningLiquid'], 3))))
    
    def defender_table_refresh(self):
        result = get_defender_params()
        print(result)
        self.ui.table_pick_sensor_3.setItem (0, 1, QtWidgets.QTableWidgetItem(str(round(result['DefendAxis'], 3))))
        if (result['DefendLiquid'] < 10):
            self.ui.table_pick_sensor_3.setItem(1, 1, QtWidgets.QTableWidgetItem('Заканчивается'))
        else:
            self.ui.table_pick_sensor_3.setItem(1, 1, QtWidgets.QTableWidgetItem('В наличии'))
        
        self.ui.table_pick_material_3.setItem(0, 1, QtWidgets.QTableWidgetItem(str(round(result['DefendLiquid'], 3))))
        pass

    def oven_edit_win(self):
        self.oven_edit.show()
    
    def conveys_table_resresh(self):
        result = get_convey_params()
        print(result)
        for i in range(0, 12):
            self.ui.table_conv.setItem(i, 2, QtWidgets.QTableWidgetItem(str(round(result['Speed'], 3))))
            self.ui.table_conv.setItem(i, 3, QtWidgets.QTableWidgetItem('-'))

        for i in range (0, 4):
            self.ui.table_conv.setItem(i+11, 2, QtWidgets.QTableWidgetItem(str(round(result['Speed'], 3))))
        
        self.ui.table_conv.setItem(13, 2, QtWidgets.QTableWidgetItem(str(round(result['Speed'], 3))))
        self.ui.table_conv.setItem(14, 2, QtWidgets.QTableWidgetItem(str(round(result['Speed'], 3))))
        self.ui.table_conv.setItem(11, 3, QtWidgets.QTableWidgetItem(str(result['Plates_1'])))
        self.ui.table_conv.setItem(12, 3, QtWidgets.QTableWidgetItem(str(result['Plates_2'])))
        self.ui.table_conv.setItem(13, 3, QtWidgets.QTableWidgetItem(str(result['Plates_3'])))
        
    def get_convey_params(self):
        for i in range(0, 14):
            self.ui.table_conv.insertRow(i)
        result = get_conveys_params()
        print("Параметры конвейера nonRT:", result)
        models = []
        types = []
        for i, j in enumerate(result):
                    models.append(j[0])
                    types.append(j[1])
        
        k = int(str(models[0])[-2:])
        l = int(str(models[1])[-1:])

        print("ЧИСЛА", k, l)

        for i in range(1, k+1):
            self.ui.table_conv.setItem(i-1, 0, QtWidgets.QTableWidgetItem(f"M0VE-{i}"))
            self.ui.table_conv.setItem(i-1, 1, QtWidgets.QTableWidgetItem(str(types[0])))
        for i in range(1, l+1):
            self.ui.table_conv.setItem(i+k-1, 0, QtWidgets.QTableWidgetItem(f"GR4B-{i}"))
            self.ui.table_conv.setItem(i+k-1, 1, QtWidgets.QTableWidgetItem(str(types[1])))

    def oven_table_titles(self):
        for i in range(0, 6):
            self.ui.table_oven.insertRow(i)
        result = get_sensor_oven()        
        print("Параметры печи nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_oven.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_oven.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))

    def printer_table_titles(self):
        for i in range(0, 3):
            self.ui.table_oven_2.insertRow(i)
        result = get_sensor_printer()
        print("Параметры принтера nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_oven_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_oven_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))

    def printer_resource_table_titles(self):
        for i in range(0, 1):
            self.ui.table_conv_2.insertRow(i)
        result = get_resource_printer()
        print("Материалы принтера nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_conv_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_conv_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))

    def cleaner_table_titles(self):
        for i in range(0, 2):
            self.ui.table_pick_sensor_2.insertRow(i)
        result = get_sensor_cleaner()
        print("Параметры чистильника nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_pick_sensor_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_pick_sensor_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))
    
    def cleaner_resource_table_titles(self):
        for i in range(0, 1):
            self.ui.table_pick_material_2.insertRow(i)
        result = get_resource_cleaner()
        print("Ресурсы очистителя nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_pick_material_2.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_pick_material_2.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))

    def pick_place_table_titles(self):
        for i in range(0, 2):
            self.ui.table_pick_sensor.insertRow(i)
        result = get_sensor_pick_place()
        print("Параметры подборщика nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_pick_sensor.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_pick_sensor.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))
    
    def pick_resource_table_titles(self):
        for i in range(0, 1):
            self.ui.table_pick_material.insertRow(i)
        result = get_resource_pick_place()
        print("Материалы подборщика nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_pick_material.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_pick_material.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))

    def defender_table_titles(self):
        for i in range(0, 2):
            self.ui.table_pick_sensor_3.insertRow(i)
        result = get_sensor_defender()
        print("Параметры защитника nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_pick_sensor_3.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_pick_sensor_3.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))
    
    def defender_resource_table_titles(self):
        for i in range(0, 1):
            self.ui.table_pick_material_3.insertRow(i)
        result = get_resource_defender()
        print("Ресурсы защитника nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_pick_material_3.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_pick_material_3.setItem(i, 2, QtWidgets.QTableWidgetItem(str(j[1])))

    def aoi_table_titles(self):
        for i in range(0, 3):
            self.ui.table_spi.insertRow(i)
        result = get_aois_states()
        print("Параметры AOI nonRT:", result)
        for i, j in enumerate(result):
            self.ui.table_spi.setItem(i, 0, QtWidgets.QTableWidgetItem(str(j[0])))
            self.ui.table_spi.setItem(i, 1, QtWidgets.QTableWidgetItem(str(j[1])))

    def error_table_refresh(self):
        result = get_errors()
        print(result)
        for i in result:
            if (i) not in self.errors:
                self.errors.append(i)

                self.ui.table_oven_err.insertRow(self.ui.table_oven_err.rowCount())
                self.ui.table_oven_err.setItem(self.ui.table_oven_err.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_oven_err.setItem(self.ui.table_oven_err.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_oven_err.setItem(self.ui.table_oven_err.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))

                self.ui.table_conv_err.insertRow(self.ui.table_conv_err.rowCount())
                self.ui.table_conv_err.setItem(self.ui.table_conv_err.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_conv_err.setItem(self.ui.table_conv_err.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_conv_err.setItem(self.ui.table_conv_err.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))
                
                self.ui.table_prnt_err.insertRow(self.ui.table_prnt_err.rowCount())
                self.ui.table_prnt_err.setItem(self.ui.table_prnt_err.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_prnt_err.setItem(self.ui.table_prnt_err.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_prnt_err.setItem(self.ui.table_prnt_err.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))

                self.ui.table_spi_err.insertRow(self.ui.table_spi_err.rowCount())
                self.ui.table_spi_err.setItem(self.ui.table_spi_err.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_spi_err.setItem(self.ui.table_spi_err.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_spi_err.setItem(self.ui.table_spi_err.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))

                self.ui.table_pick_err.insertRow(self.ui.table_pick_err.rowCount())
                self.ui.table_pick_err.setItem(self.ui.table_pick_err.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_pick_err.setItem(self.ui.table_pick_err.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_pick_err.setItem(self.ui.table_pick_err.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))

                self.ui.table_pick_err_2.insertRow(self.ui.table_pick_err_2.rowCount())
                self.ui.table_pick_err_2.setItem(self.ui.table_pick_err_2.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_pick_err_2.setItem(self.ui.table_pick_err_2.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_pick_err_2.setItem(self.ui.table_pick_err_2.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))

                self.ui.table_pick_err_3.insertRow(self.ui.table_pick_err_3.rowCount())
                self.ui.table_pick_err_3.setItem(self.ui.table_pick_err_3.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_pick_err_3.setItem(self.ui.table_pick_err_3.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_pick_err_3.setItem(self.ui.table_pick_err_3.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[2])))
    
    def oven_table_refresh(self):
        result = get_oven_params()
        print(result)
        for i, (j,k) in enumerate(result.items()):
            self.ui.table_oven.setItem(i, 1, QtWidgets.QTableWidgetItem(str(round(k,3))))

    def ban_table_refresh(self):
        result = reversed(get_aois_failures())
        for i in result:
            if (i) not in self.bans:
                self.bans.append(i)
                self.ui.table_spi_ban.insertRow(self.ui.table_spi_ban.rowCount())
                self.ui.table_spi_ban.setItem(self.ui.table_spi_ban.rowCount()-1, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.ui.table_spi_ban.setItem(self.ui.table_spi_ban.rowCount()-1, 1, QtWidgets.QTableWidgetItem(str(i[1])))
                self.ui.table_spi_ban.setItem(self.ui.table_spi_ban.rowCount()-1, 2, QtWidgets.QTableWidgetItem(str(i[2])))



    def lamps_light(self):
        self.ui.lamp_loader.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_printer.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_oven.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_spi.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_aoi.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_collector_1.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_collector_2.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_collector_3.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_plate_tester.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_pick_place.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_cleaner.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_defender.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))
        self.ui.lamp_plate_tester.setPixmap(QtGui.QPixmap("./client/images/green_light.png"))


class LoginPage(QMainWindow):    
    def __init__(self):
        super(LoginPage, self).__init__()
        self.main = MainWindow()
        self.ui = Ui_Login_Page()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(lambda: check_login(self, self.ui.line_login.text(), self.ui.line_password.text()))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            check_login(self, self.ui.line_login.text(), self.ui.line_password.text())

class OvenPage(QMainWindow):
    def __init__(self):
        super(OvenPage, self).__init__()
        self.ui = Ui_Oven_page()
        self.ui.setupUi(self)
        self.ui.bu_ok_z1.clicked.connect(lambda: self.set_zone_params(self.ui.line_chng_z1.text(), 1))
        self.ui.bu_ok_z2.clicked.connect(lambda: self.set_zone_params(self.ui.line_chng_z2.text(), 2))
        self.ui.bu_ok_z3.clicked.connect(lambda: self.set_zone_params(self.ui.line_chng_z3.text(), 3))
        self.ui.bu_ok_z4.clicked.connect(lambda: self.set_zone_params(self.ui.line_chng_z4.text(), 4))
        self.ui.bu_ok_z5.clicked.connect(lambda: self.set_zone_params(self.ui.line_chng_z5.text(), 5))

        self.get_zone_params()

        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.get_zone_params)
        self.timer.start()
    
    def timed_functions(self):
        self.get_zone_params() 


    def get_zone_params(self):
        result = get_oven_params()
        for i, (j,k) in enumerate(result.items()):
            if j == "Temperature_1":
                self.ui.lcd_z1.display(float(round(k,3)))
            if j == "Temperature_2":
                self.ui.lcd_z2.display(float(round(k,3)))
            if j == "Temperature_3":
                self.ui.lcd_z3.display(float(round(k,3)))
            if j == "Temperature_4":
                self.ui.lcd_z4.display(float(round(k,3)))
            if j == "Temperature_5":
                self.ui.lcd_z5.display(float(round(k,3)))

    def set_zone_params(self, new_param, zone):   
        param = float(str(new_param))
        generator_change(zone, param)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    loginwin = LoginPage()
    loginwin.show()
    sys.exit(app.exec_())    