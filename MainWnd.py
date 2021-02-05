from PyQt5 import QtCore, QtGui, QtWidgets
import SettingsWnd as SW
import Session as Sn
import mcculw
import Gfx

class Ui_MainWindow(QtWidgets.QMainWindow):

    SettingsReady = False
    Session = Sn.Session()
    Playing = False
    Recording = False

    def __init__(self):

        super().__init__()
        self.setObjectName("MainWnd")
        self.resize(788, 378)
        self.setMinimumSize(QtCore.QSize(788, 378))

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        self.axis_check = QtWidgets.QCheckBox(self.centralwidget)
        self.axis_check.setMinimumSize(QtCore.QSize(45, 23))
        self.axis_check.setMaximumSize(QtCore.QSize(45, 23))
        self.axis_check.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.axis_check.setObjectName("axis_check")
        self.axis_check.setChecked(False)
        self.gridLayout.addWidget(self.axis_check, 0, 0, 1, 1)

        self.play_pb = QtWidgets.QPushButton(self.centralwidget)
        self.play_pb.setMinimumSize(QtCore.QSize(75, 23))
        self.play_pb.setMaximumSize(QtCore.QSize(75, 23))
        self.play_pb.setObjectName("play_pb")
        self.gridLayout.addWidget(self.play_pb, 0, 1, 1, 1)

        self.record_pb = QtWidgets.QPushButton(self.centralwidget)
        self.record_pb.setMinimumSize(QtCore.QSize(75, 23))
        self.record_pb.setMaximumSize(QtCore.QSize(75, 23))
        self.record_pb.setObjectName("record_pb")
        self.gridLayout.addWidget(self.record_pb, 0, 2, 1, 1)

        self.filename_lb = QtWidgets.QLabel(self.centralwidget)
        self.filename_lb.setMinimumSize(QtCore.QSize(47, 13))
        self.filename_lb.setMaximumSize(QtCore.QSize(47, 13))
        self.filename_lb.setObjectName("filename_lb")
        self.gridLayout.addWidget(self.filename_lb, 0, 3, 1, 1)

        self.filename_le = QtWidgets.QLineEdit(self.centralwidget)
        self.filename_le.setMinimumSize(QtCore.QSize(431, 20))
        self.filename_le.setObjectName("filename_le")
        self.gridLayout.addWidget(self.filename_le, 0, 4, 1, 1)

        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setMinimumSize(QtCore.QSize(0, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 768, 417))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.scrollAreaWidgetContents)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.gridLayout.addWidget(self.scrollArea, 1, 0, 1, 5)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 788, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.SettingsWnd = SW.Ui_settings_wnd(self)
        self.SettingsWnd.show()
        self.SettingsWnd.ok_push.clicked.connect(self.settings_ok_push_proc)
        self.SettingsWnd.cancel_push.clicked.connect(self.settings_cancel_push_proc)
        self.play_pb.clicked.connect(self.play_push_proc)
        self.record_pb.clicked.connect(self.record_push_proc)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWnd", "MCC Gui"))
        self.axis_check.setText(_translate("MainWnd", "Axis"))
        self.play_pb.setText(_translate("MainWnd", "Play"))
        self.record_pb.setText(_translate("MainWnd", "Record"))
        self.filename_lb.setText(_translate("MainWnd", "File name"))


    def settings_ok_push_proc(self):

        try:
            #The order for calling these methods matter!!
            self.SettingsWnd.saveSettings(self.Session)
            self.Session.createBoard()
            self.Session.myBoard.testBoard()
            self.createCanvases()
            self.SettingsWnd.close()

        except mcculw.ul.ULError as e:
            self.MCCExceptionHandler(e)
            self.SettingsWnd.close()
            self.close()

    def settings_cancel_push_proc(self):

        self.SettingsWnd.close()
        self.close()

    def MCCExceptionHandler(self,e):

        error_msg = QtWidgets.QMessageBox()
        error_msg.setIcon(QtWidgets.QMessageBox.Critical)
        error_msg.setWindowTitle("MCC Exception")
        error_msg.setText("Error code: " + str(e.errorcode))
        error_msg.setInformativeText(e.message)
        error_msg.exec_()

    def createCanvases(self):
        self.Ch_labs = []
        for x in range(self.Session.myBoard.Channels):

            self.Ch_labs.append(QtWidgets.QLabel(self.scrollAreaWidgetContents))
            self.Ch_labs[x].setMinimumSize(QtCore.QSize(21, 16))
            self.Ch_labs[x].setMaximumSize(QtCore.QSize(21, 16))
            self.Ch_labs[x].setObjectName("Ch " + str(x) + " label")
            self.Ch_labs[x].setText("Ch " + str(x))
            self.gridLayout_2.addWidget(self.Ch_labs[x], x, 0, 1, 1)

            self.Session.Canvases.append(
                Gfx.Canvas(self.Session.myBoard.SRate * self.Session.VisWindowLength
                           ,self.scrollAreaWidgetContents, width=701, height=71)
            )
            self.Session.Canvases[x].setMinimumSize(QtCore.QSize(701, 71))
            self.Session.Canvases[x].setMaximumSize(QtCore.QSize(16777215, 121))
            self.Session.Canvases[x].setObjectName("Ch " + str(x) + " canvas")
            self.gridLayout_2.addWidget(self.Session.Canvases[x], x, 1, 1, 1)

    def play_push_proc(self):

        if self.Playing:

            self.play_pb.setText("Play")
            self.Playing = False
            self.Recording = False

            self.Session.StopAcquisition()
            self.record_pb.setDisabled(False)
            self.filename_le.setDisabled(False)
            self.axis_check.setDisabled(False)

        else:

            self.play_pb.setText("Stop")
            self.Playing = True
            self.Recording = False

            self.record_pb.setDisabled(True)
            self.filename_le.setDisabled(True)
            self.axis_check.setDisabled(True)

            self.SetCanvasAxis()

            self.Session.AcquireData()

    def record_push_proc(self):

        if self.Recording:

            self.record_pb.setText("Record")
            self.Playing = False
            self.Recording = False
            self.Session.isRecording = self.Recording

            self.Session.StopAcquisition()
            self.play_pb.setDisabled(False)
            self.filename_le.setDisabled(False)
            self.axis_check.setDisabled(False)

        else:

            self.record_pb.setText("Stop")
            self.Playing = True
            self.Recording = True
            self.Session.isRecording = self.Recording
            self.Session.FileName = self.filename_le.text()

            self.play_pb.setDisabled(True)
            self.filename_le.setDisabled(True)
            self.axis_check.setDisabled(True)

            #self.SetCanvasAxis()

            self.Session.AcquireData()

    def SetCanvasAxis(self):

        for Canvas in self.Session.Canvases:
            Canvas.AxisON = self.axis_check.isChecked()

    def closeEvent(self, event):
        self.Session.EndSession()


