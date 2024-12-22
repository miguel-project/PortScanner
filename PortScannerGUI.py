from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QProgressBar, QFileDialog, QRadioButton, QGroupBox, QApplication
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt

class PortScannerGUI(QWidget):
    def __init__(self, scanner, sorter, excel_exporter):
        super().__init__()
        self.scanner = scanner
        self.sorter = sorter
        self.excel_exporter = excel_exporter
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Port Scanner")
        self.setWindowIcon(QIcon("resources/logo.png"))

        
        logo_label = QLabel(self)
        pixmap = QPixmap("resources/app_image.png")
        logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
        logo_label.setAlignment(Qt.AlignCenter)


        ip_label = QLabel("Inserisci l'indirizzo IP:")
        self.ip_input = QLineEdit()


        port_range_label = QLabel("Inserisci il range di porte (es. 1-1024):")
        self.start_port_input = QLineEdit()
        self.start_port_input.setPlaceholderText("Porta iniziale")
        self.end_port_input = QLineEdit()
        self.end_port_input.setPlaceholderText("Porta finale")


        protocol_label = QLabel("Seleziona il protocollo:")
        self.protocol_group = QGroupBox("Protocollo")
        self.tcp_radio = QRadioButton("TCP")
        self.udp_radio = QRadioButton("UDP")
        self.both_radio = QRadioButton("Entrambi")
        self.tcp_radio.setChecked(True)

        protocol_layout = QVBoxLayout()
        protocol_layout.addWidget(self.tcp_radio)
        protocol_layout.addWidget(self.udp_radio)
        protocol_layout.addWidget(self.both_radio)
        self.protocol_group.setLayout(protocol_layout)


        scan_button = QPushButton("Avvia Scansione")
        scan_button.clicked.connect(self.start_scan)

        sort_button = QPushButton("Ordina Risultati")
        sort_button.clicked.connect(self.sort_results)

        export_button = QPushButton("Esporta in Excel")
        export_button.clicked.connect(self.export_to_excel)


        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setAlignment(Qt.AlignCenter)

        self.results_output = QTextEdit()
        self.results_output.setReadOnly(True)


        layout = QVBoxLayout()
        layout.addWidget(logo_label)
        layout.addWidget(ip_label)
        layout.addWidget(self.ip_input)
        layout.addWidget(port_range_label)

        port_layout = QHBoxLayout()
        port_layout.addWidget(self.start_port_input)
        port_layout.addWidget(self.end_port_input)
        layout.addLayout(port_layout)

        layout.addWidget(protocol_label)
        layout.addWidget(self.protocol_group)
        layout.addWidget(scan_button)
        layout.addWidget(sort_button)
        layout.addWidget(export_button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.results_output)

        self.setLayout(layout)

    def start_scan(self):
        target = self.ip_input.text().strip()
        start_port = self.start_port_input.text().strip()
        end_port = self.end_port_input.text().strip()

        if not target:
            self.results_output.setText("Per favore, inserisci un indirizzo IP valido.")
            return
        if not start_port.isdigit() or not end_port.isdigit():
            self.results_output.setText("Per favore, inserisci un range di porte valido.")
            return

        start_port, end_port = int(start_port), int(end_port)

        if start_port < 1 or end_port > 65535 or start_port > end_port:
            self.results_output.setText("Per favore, inserisci un range di porte valido (1-65535).")
            return

        protocols_to_scan = []
        if self.tcp_radio.isChecked():
            protocols_to_scan.append("TCP")
        if self.udp_radio.isChecked():
            protocols_to_scan.append("UDP")
        if self.both_radio.isChecked():
            protocols_to_scan = ["TCP", "UDP"]

        self.results_output.setText(f"Scansione in corso per {target}...\n")
        self.progress_bar.setValue(0)
        total_ports = end_port - start_port + 1

        for i, port in enumerate(range(start_port, end_port + 1)):
            for protocol in protocols_to_scan:
                if protocol == "TCP":
                    self.scanner.scan_tcp(target, port)
                elif protocol == "UDP":
                    self.scanner.scan_udp(target, port)
            progress = int(((i + 1) / total_ports) * 100)
            self.progress_bar.setValue(progress)

        self.results_output.append("Scansione completata!")
        self.progress_bar.setValue(100)

    def sort_results(self):
        results = self.scanner.get_results()
        if not results:
            self.results_output.setText("Non ci sono risultati da ordinare. Esegui prima una scansione.")
            return

        sorted_results = self.sorter.sort_results(results)

        self.results_output.setText("Risultati ordinati (solo porte aperte):\n")
        for port, protocol, proto_type, status in sorted_results:
            self.results_output.append(f"Porta {port}: {status} ({proto_type} - {protocol})")

    def export_to_excel(self):
        results = self.scanner.get_results()
        if not results:
            self.results_output.setText("Non ci sono risultati da esportare.")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Salva come Excel", "", "Excel Files (*.xlsx);;All Files (*)", options=options)

        if file_path:
            message = self.excel_exporter.export_to_excel(results, file_path)
            self.results_output.append(message)