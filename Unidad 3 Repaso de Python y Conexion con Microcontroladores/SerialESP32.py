import sys
import time
import serial
from serial.tools import list_ports
from pathlib import Path
from PySide6.QtCore import QFile, QIODevice, Qt, QTimer, Signal, QObject
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QPushButton, QCheckBox, QLabel, QComboBox, QTextEdit, QMessageBox, QWidget, QLCDNumber, QPlainTextEdit, QTextEdit, QSpinBox, QVBoxLayout
import json
import csv
import os
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

plt.style.use("dark_background")

class GraphWindow(QWidget):
    update_signal = Signal(int)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gráfico LDR")
        self.setGeometry(100, 100, 640, 480)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.data_x = []
        self.data_y = []

        self.update_signal.connect(self.add_new_value)
    
    def add_new_value(self, value):
        timestamp = time.strftime("%H:%M:%S")
        
        self.data_x.append(timestamp)
        self.data_y.append(value)

        if len(self.data_x) > 20:
            self.data_x.pop(0)
            self.data_y.pop(0)

        self.ax.clear()
        self.ax.plot(self.data_x, self.data_y, marker="o", linestyle="-", color="b")
        self.ax.set_title("Valores del LDR")
        self.ax.set_xlabel("Tiempo")
        self.ax.set_ylabel("LDR %")
        self.ax.grid()
        self.ax.tick_params(axis='x', rotation=45)

        self.canvas.draw()


class TallerESP32:
    def __init__(self):
        self.graph_window = None
        self.serial_connection = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.read_serial_data)
        self.cargar_ui() 
        self.refresh_ports()

    def cargar_ui(self):
        ui_path = Path(__file__).parent / "HMI.ui"
        if not ui_path.exists():
            print(f"Error: No se encontró el archivo {ui_path}")
            sys.exit(-1)
        
        ui_file = QFile(str(ui_path))
        if not ui_file.open(QIODevice.ReadOnly):
            print("Error al abrir el archivo:", ui_file.errorString())
            sys.exit(-1)
        
        loader = QUiLoader()
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        if self.ui is None:
            print("Error al cargar la interfaz.")
            sys.exit(-1)
        
        self.refresh_button = self.ui.findChild(QPushButton, "Reset_btn")
        self.connect_button = self.ui.findChild(QPushButton, "Connect_btn")
        self.label = self.ui.findChild(QLabel, "label")
        self.combobox = self.ui.findChild(QComboBox, "Ports_btn")
        self.text_edit = self.ui.findChild(QTextEdit, "textEdit")
        self.ExcludeEvents = self.ui.findChild(QCheckBox, "ExcludeEvents")
        self.groups = self.ui.findChild(QWidget, "Grupos")
        self.group_ldr = self.ui.findChild(QWidget, "LDR_Group")
        self.group_lcd = self.ui.findChild(QWidget, "LCD_Group")
        self.group_interrupt = self.ui.findChild(QWidget, "Interrupt_Group")
        self.group_control = self.ui.findChild(QWidget, "Control_Group")
        self.en_ldr = self.ui.findChild(QCheckBox, "LDR_En")
        self.en_lcd = self.ui.findChild(QCheckBox, "LCD_En")
        self.en_interrupt = self.ui.findChild(QCheckBox, "Interrupt_En")
        self.en_control = self.ui.findChild(QCheckBox, "Control_En")
        self.ValueLDR = self.ui.findChild(QLCDNumber, "ValueLDR")

        self.ValueTemp = self.ui.findChild(QLCDNumber, "ValueTemp")
        self.SetTemp_btn = self.ui.findChild(QPushButton, "SetTemp_btn")
        self.SetPoint_spin = self.ui.findChild(QSpinBox, "SetPoint_spin")
        self.ShowDisplayLDR = self.ui.findChild(QCheckBox, "ShowDisplayLDR")
        self.ShowDisplayLCD = self.ui.findChild(QCheckBox, "ShowDisplayLCD")
        self.ShowDisplayInterrupt = self.ui.findChild(QCheckBox, "ShowDisplayInterrupt")
        self.ShowDisplayTemp = self.ui.findChild(QCheckBox, "ShowDisplayTemp")

        self.textEdit_2 = self.ui.findChild(QTextEdit, "textEdit_2")

        self.ShowLCD = self.ui.findChild(QPushButton, "ShowLCD")
        self.ClearLCD = self.ui.findChild(QPushButton, "ClearLCD")
        self.TextoLCD = self.ui.findChild(QPlainTextEdit, "TextoLCD")

        
        self.refresh_button.clicked.connect(self.refresh_ports)
        self.combobox.currentTextChanged.connect(self.check_selected_port)
        self.connect_button.clicked.connect(self.toggle_connection)

        self.ShowLCD.clicked.connect(self.MostrarLCD)
        self.ClearLCD.clicked.connect(self.BorrarLCD)

        self.SetTemp_btn.clicked.connect(self.SetTemp)

        self.en_ldr.stateChanged.connect(self.enableGroups)
        self.en_lcd.stateChanged.connect(self.enableGroups)
        self.en_interrupt.stateChanged.connect(self.enableGroups)
        self.en_control.stateChanged.connect(self.enableGroups)
        self.ShowDisplayTemp.stateChanged.connect(self.enableGroups)
        self.ShowDisplayLDR.stateChanged.connect(self.enableGroups)
        self.ShowDisplayInterrupt.stateChanged.connect(self.enableGroups)

        self.connect_button.setEnabled(False)
        self.connect_button.setText("Conectar")
    
    def refresh_ports(self):
        self.combobox.clear()
        ports = list_ports.comports()
        port_names = [port.device for port in ports]
        self.combobox.addItems(port_names)
        self.connect_button.setEnabled(bool(port_names))
    
    def check_selected_port(self, port):
        self.connect_button.setEnabled(bool(port))
    
    def toggle_connection(self):
        if self.serial_connection is None or not self.serial_connection.is_open:
            selected_port = self.combobox.currentText()
            if not selected_port:
                self.label.setText("No se ha seleccionado ningún puerto.")
                return
            try:
                self.label.setText("Conectando...")
                self.label.repaint()
                if self.serial_connection and self.serial_connection.is_open:
                    self.serial_connection.close()
                    time.sleep(1)
                self.serial_connection = serial.Serial(selected_port, 250000, timeout=0.1)
                id_command = {"cmd": "ID?"}
                json_cmd = json.dumps(id_command) + "\n"

                response = b""
                start_time = time.time()

                while time.time() - start_time < 5:
                    self.serial_connection.write(json_cmd.encode("utf-8"))
                    time.sleep(0.5) 

                    if self.serial_connection.in_waiting:
                        response = self.serial_connection.read(self.serial_connection.in_waiting)
                        break 

                if not response:
                    QMessageBox.critical(self.ui, "Error de conexión",
                        "No se puede conectar a este dispositivo. Intente de nuevo.")
                    self.serial_connection.close()
                    self.serial_connection = None
                    self.label.setText("Desconectado")
                    self.groups.setEnabled(False)
                    return

                try:
                    response_obj = json.loads(response.decode("utf-8").strip())
                except Exception as e:
                    QMessageBox.critical(self.ui, "Error de conexión", 
                        f"No se pudo decodificar la respuesta JSON.\nError: {e}")
                    self.serial_connection.close()
                    self.serial_connection = None
                    self.label.setText("Desconectado")
                    self.groups.setEnabled(False)
                    return

                expected_id = "ESP32_31125"
                if response_obj.get("id") != expected_id:
                    QMessageBox.critical(self.ui, "Error de conexión", 
                        f"El dispositivo en {selected_port} no es el esperado.\nRespuesta: {json.dumps(response_obj)}")
                    self.serial_connection.close()
                    self.serial_connection = None
                    self.label.setText("Desconectado")
                    self.groups.setEnabled(False)
                    return

                self.label.setText(f"Conectado a {selected_port}")
                self.connect_button.setText("Desconectar")
                self.timer.start(50)
                print(f"Conectado a {selected_port} a 250000 baudios")
                self.label.setText(expected_id)
                self.groups.setEnabled(True)

            except serial.SerialException as e:
                self.label.setText("Error al conectar")
                print(f"Error al conectar al puerto {selected_port}: {e}")

        else:
            self.timer.stop()
            self.serial_connection.close()
            self.serial_connection = None
            self.label.setText("Desconectado")
            self.connect_button.setText("Conectar")
            print("Desconectado")
            self.groups.setEnabled(False)
            if self.text_edit:
                self.text_edit.clear()

    def read_serial_data(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                bytes_available = self.serial_connection.in_waiting
                if bytes_available:
                    raw_data = self.serial_connection.read(bytes_available)

                    try:
                        data = raw_data.decode("utf-8", errors="ignore").strip()
                        message_obj = json.loads(data)
                        json_message = json.dumps(message_obj, indent=2)

                        if "LDR" in message_obj:
                            value = message_obj["LDR"]
                            if value < 0 or value > 999:
                                value = -1
                            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                            self.save_to_csv(timestamp, value)
                            self.ValueLDR.display(value)

                            if self.graph_window:
                                self.graph_window.update_signal.emit(value)

                        if "TEMP" in message_obj:
                            value = message_obj["TEMP"]
                            if value > 999:
                                value = 999
                            self.ValueTemp.display(value)

                        if "BUTTON" in message_obj:
                            if message_obj["BUTTON"]:
                                if self.textEdit_2.toPlainText() == "Activado":
                                    None
                                else:
                                    self.textEdit_2.append("Activado") 
                            else:
                                self.textEdit_2.clear()

                    except json.JSONDecodeError:
                        json_message = f"Datos no válidos o incompletos: {raw_data.hex(' ')}" 

                    if self.text_edit:
                        if (not self.ExcludeEvents.isChecked()):
                            self.text_edit.clear()
                        else:
                            hex_message = json_message.encode("utf-8").hex()
                            formatted_hex = " ".join(hex_message[i:i+2] for i in range(0, len(hex_message), 2))  # Formato con espacios
                            self.text_edit.append(formatted_hex)
                            # self.text_edit.append(json_message)
                    else:
                        print(json_message)

            except Exception as e:
                print(f"Error al leer datos del serial: {e}")
    
    def enableGroups(self):
        enabled_features = {
            "ldr": str(self.en_ldr.isChecked()).lower(),
            "lcd": str(self.en_lcd.isChecked()).lower(),
            "button": str(self.en_interrupt.isChecked()).lower(),
            "temp": str(self.en_control.isChecked()).lower(),
            "show_ldr": str(self.ShowDisplayLDR.isChecked()).lower(),
            "show_lcd": str(self.ShowDisplayLCD.isChecked()).lower(),
            "show_temp": str(self.ShowDisplayTemp.isChecked()).lower(),
            "show_button": str(self.ShowDisplayInterrupt.isChecked()).lower()
        }

        self.group_ldr.setEnabled(self.en_ldr.isChecked())

        if self.en_ldr.isChecked():
            if self.graph_window is None:
                self.graph_window = GraphWindow()
            self.graph_window.show()
        else:
            if self.graph_window:
                self.graph_window.close()
        
        if self.en_lcd.isChecked():
            self.ShowDisplayLDR.setEnabled(self.en_ldr.isChecked())
            self.ShowDisplayLCD.setEnabled(self.en_lcd.isChecked())
            self.ShowDisplayInterrupt.setEnabled(self.en_interrupt.isChecked())
            self.ShowDisplayTemp.setEnabled(self.en_control.isChecked())

            if self.ShowDisplayTemp.isChecked() or self.ShowDisplayLDR.isChecked() or self.ShowDisplayInterrupt.isChecked():
                self.group_lcd.setEnabled(False)
            else:
                self.group_lcd.setEnabled(True)
        else:
            self.ShowDisplayLDR.setEnabled(False)
            self.ShowDisplayLCD.setEnabled(False)
            self.ShowDisplayInterrupt.setEnabled(False)
            self.ShowDisplayTemp.setEnabled(False)

        self.group_interrupt.setEnabled(self.en_interrupt.isChecked())
        self.group_control.setEnabled(self.en_control.isChecked())

        if self.serial_connection and self.serial_connection.is_open:
            try:
                json_cmd = json.dumps({"cmd": "CONFIG", **enabled_features}) + "\n"
                self.serial_connection.write(json_cmd.encode("utf-8"))
                print("Enviado al ESP32:", json_cmd)
            except Exception as e:
                print(f"Error al enviar JSON: {e}")

    def MostrarLCD(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                texto = self.TextoLCD.toPlainText().strip()
                linea1 = texto[:16]
                linea2 = texto[16:32] if len(texto) > 16 else ""

                json_cmd = json.dumps({"cmd": "LCD", "line1": linea1, "line2": linea2}) + "\n"
                self.serial_connection.write(json_cmd.encode("utf-8"))
                print("Enviado al ESP32:", json_cmd)
            except Exception as e:
                print(f"Error al enviar JSON: {e}")


    def BorrarLCD(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                json_cmd = json.dumps({"cmd": "LCD", "line1": "", "line2": ""}) + "\n"
                self.serial_connection.write(json_cmd.encode("utf-8"))
                print("Enviado al ESP32:", json_cmd)
            except Exception as e:
                print(f"Error al enviar JSON: {e}")

    def SetTemp(self):
        if self.serial_connection and self.serial_connection.is_open:
            try:
                setpoint = self.SetPoint_spin.value()
                json_cmd = json.dumps({"cmd": "SetTemp", "setpoint": setpoint}) + "\n"
                self.serial_connection.write(json_cmd.encode("utf-8"))
                print("Enviado al ESP32:", json_cmd)
            except Exception as e:
                print(f"Error al enviar JSON: {e}")

    def save_to_csv(self, timestamp, ldr_value):
        script_dir = os.path.dirname(os.path.abspath(__file__)) 
        file_name = os.path.join(script_dir, "ldr_data.csv") 
        
        with open(file_name, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([timestamp, ldr_value])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_instance = TallerESP32()
    app_instance.ui.setWindowFlags(app_instance.ui.windowFlags() | Qt.Window)
    app_instance.ui.show()
    app.exec()