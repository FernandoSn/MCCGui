import sys
import MainWnd

app = MainWnd.QtWidgets.QApplication(sys.argv)
ui = MainWnd.Ui_MainWindow()
ui.show()
sys.exit(app.exec_())