import socket
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit
from PyQt5.QtCore import Qt

class PortScannerApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Port Scanner")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout()

        self.label = QLabel("Inserisci l'IP di destinazione:", self)
        self.layout.addWidget(self.label)
        self.target_input = QLineEdit(self)
        self.layout.addWidget(self.target_input)
        self.scan_button = QPushButton("Avvia scansione", self)
        self.scan_button.clicked.connect(self.start_scan)
        self.layout.addWidget(self.scan_button)
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        self.setLayout(self.layout)

    def start_scan(self):
        target_ip = self.target_input.text()
        if not target_ip:
            self.result_text.append("Errore! Inserisci un IP valido!")
            return
        if target_ip:
            self.result_text.clear()
            self.result_text.append(f"Avviando la scansione su {target_ip} ...\n")
            self.scan_ports(target_ip)

    def scan_ports(self, target_ip):
        open_ports = []
        for port in range(1, 1000):
            result = self.check_port(target_ip, port)
            if result:
                open_ports.append(port)

        if open_ports:
            self.result_text.append(f"Porte aperte su {target_ip}: \n{', '.join(map(str, open_ports))}")
        else:
            self.result_text.append(f"Nessuna porta aperta trovata su {target_ip}")

    def check_port(self, target_ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target_ip, port))
        sock.close()
        return result == 0


if __name__ == '__main__':
    app = QApplication([])

    window = PortScannerApp()
    window.show()

    app.exec_()