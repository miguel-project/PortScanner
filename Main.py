import sys
from PyQt5.QtWidgets import QApplication
from Scanner import Scanner
from Sorter import Sorter
from ExcelExporter import ExcelExporter
from PortScannerGUI import PortScannerGUI

if __name__ == "__main__":
    app = QApplication(sys.argv)


    scanner = Scanner()
    sorter = Sorter()
    excel_exporter = ExcelExporter()

    
    gui = PortScannerGUI(scanner, sorter, excel_exporter)
    gui.show()

    sys.exit(app.exec_())