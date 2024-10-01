import UI.Ui_tool, sys
from PyQt5.QtWidgets import QWidget, QApplication

def main():
    app = QApplication(sys.argv)
    win = QWidget()
    ui = UI.Ui_tool.Ui_Form()
    ui.setupUi(win)
    win.show()
    sys.exit(app.exec_())