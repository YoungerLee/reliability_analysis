from reilability_main import MainWindow
from PyQt5.QtWidgets import QApplication
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.showMaximized()
    sys.exit(app.exec_())
