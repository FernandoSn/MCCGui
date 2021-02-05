import os
from PyQt5 import QtCore, QtGui, QtWidgets

from mcculw import ul
from mcculw.enums import InterfaceType

import Board as Bd
import Gfx


class Ui_settings_wnd(QtWidgets.QMainWindow):

    SettingsFileName = "mymccsettings.txt"

    def __init__(self,parent):
        
        super().__init__(parent)
        
        self.setObjectName("settings_wnd")
        self.resize(331, 414)
        self.setMinimumSize(QtCore.QSize(331, 414))
        self.setMaximumSize(QtCore.QSize(331, 414))
        
        self.settings_wid = QtWidgets.QWidget(self)
        self.settings_wid.setObjectName("settings_wid")
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowMaximizeButtonHint, False)
        self.onlyInt = QtGui.QIntValidator()
        
        self.viswnd_lab = QtWidgets.QLabel(self.settings_wid)
        self.viswnd_lab.setGeometry(QtCore.QRect(10, 60, 61, 16))
        self.viswnd_lab.setObjectName("viswnd_lab")
        
        self.samrate_lab = QtWidgets.QLabel(self.settings_wid)
        self.samrate_lab.setGeometry(QtCore.QRect(10, 90, 61, 16))
        self.samrate_lab.setObjectName("samrate_lab")
        
        self.chan_lab = QtWidgets.QLabel(self.settings_wid)
        self.chan_lab.setGeometry(QtCore.QRect(10, 150, 61, 16))
        self.chan_lab.setObjectName("chan_lab")
        
        self.resp_check = QtWidgets.QCheckBox(self.settings_wid)
        self.resp_check.setGeometry(QtCore.QRect(10, 210, 121, 17))
        self.resp_check.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.resp_check.setObjectName("resp_check")
        self.resp_check.setChecked(False)
        
        self.ok_push = QtWidgets.QPushButton(self.settings_wid)
        self.ok_push.setGeometry(QtCore.QRect(70, 340, 75, 23))
        self.ok_push.setObjectName("ok_push")
        
        self.cancel_push = QtWidgets.QPushButton(self.settings_wid)
        self.cancel_push.setGeometry(QtCore.QRect(190, 340, 75, 23))
        self.cancel_push.setObjectName("cancel_push")
        
        self.range_lab = QtWidgets.QLabel(self.settings_wid)
        self.range_lab.setEnabled(True)
        self.range_lab.setGeometry(QtCore.QRect(10, 120, 61, 16))
        self.range_lab.setObjectName("range_lab")
        
        self.chan_le = QtWidgets.QLineEdit(self.settings_wid)
        self.chan_le.setGeometry(QtCore.QRect(80, 150, 31, 20))
        self.chan_le.setObjectName("chan_le")
        self.chan_le.setValidator(self.onlyInt)
        
        self.range_cb = QtWidgets.QComboBox(self.settings_wid)
        self.range_cb.setGeometry(QtCore.QRect(80, 120, 69, 22))
        self.range_cb.setObjectName("range_cb")
        self.range_cb.addItem("±2")
        self.range_cb.addItem("±5")
        self.range_cb.addItem("±10")
        
        self.viswnd_cb = QtWidgets.QComboBox(self.settings_wid)
        self.viswnd_cb.setGeometry(QtCore.QRect(80, 60, 61, 22))
        self.viswnd_cb.setObjectName("viswnd_cb")
        self.viswnd_cb.addItem("2")
        self.viswnd_cb.addItem("5")
        self.viswnd_cb.addItem("10")
        self.viswnd_cb.addItem("20")
        self.viswnd_cb.addItem("30")
        
        self.chanresp_lab = QtWidgets.QLabel(self.settings_wid)
        self.chanresp_lab.setGeometry(QtCore.QRect(10, 240, 61, 16))
        self.chanresp_lab.setObjectName("chanresp_lab")
        
        self.chanresp_le = QtWidgets.QLineEdit(self.settings_wid)
        self.chanresp_le.setGeometry(QtCore.QRect(80, 240, 31, 20))
        self.chanresp_le.setObjectName("chanresp_le")
        self.chanresp_le.setValidator(self.onlyInt)
        self.chanresp_le.setDisabled(True)
        
        self.board_lab = QtWidgets.QLabel(self.settings_wid)
        self.board_lab.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.board_lab.setObjectName("board_lab")
        
        self.board_cb = QtWidgets.QComboBox(self.settings_wid)
        self.board_cb.setGeometry(QtCore.QRect(80, 10, 121, 22))
        self.board_cb.setObjectName("board_cb")
        
        self.samrate_cb = QtWidgets.QComboBox(self.settings_wid)
        self.samrate_cb.setGeometry(QtCore.QRect(80, 90, 69, 22))
        self.samrate_cb.setObjectName("samrate_cb")
        self.samrate_cb.addItem("1000")
        self.samrate_cb.addItem("2000")
        self.samrate_cb.addItem("4000")
        self.samrate_cb.addItem("6000")
        self.samrate_cb.addItem("8000")
        self.samrate_cb.addItem("10000")
        self.samrate_cb.addItem("14000")
        self.samrate_cb.addItem("20000")
        self.samrate_cb.addItem("30000")
        
        self.setCentralWidget(self.settings_wid)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 331, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.setWindowModality(QtCore.Qt.WindowModal)

        self.retranslateUi()
        self.discoverBoards()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.resp_check.clicked.connect(self.resp_check_proc)
        self.loadSettings()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("settings_wnd", "MainWindow"))
        self.viswnd_lab.setText(_translate("settings_wnd", "Window (S)"))
        self.samrate_lab.setText(_translate("settings_wnd", "Rate (Hz)"))
        self.chan_lab.setText(_translate("settings_wnd", "Channels"))
        self.resp_check.setText(_translate("settings_wnd", "Respiration detection"))
        self.ok_push.setText(_translate("settings_wnd", "OK"))
        self.cancel_push.setText(_translate("settings_wnd", "Cancel"))
        self.range_lab.setText(_translate("settings_wnd", "Range (V)"))
        self.chanresp_lab.setText(_translate("settings_wnd", "Channel"))
        self.board_lab.setText(_translate("settings_wnd", "Board"))

    def discoverBoards(self):

        ul.ignore_instacal()
        self.inventory = ul.get_daq_device_inventory(InterfaceType.ANY)

        if len(self.inventory)>0:
            for device in self.inventory:
                self.board_cb.addItem(device.product_name + "(" + device.unique_id + ")")
        else:
            self.board_cb.addItem("Board not found")
            self.board_cb.setDisabled(True)
            self.viswnd_cb.setDisabled(True)
            self.chan_le.setDisabled(True)
            self.range_cb.setDisabled(True)
            self.samrate_cb.setDisabled(True)
            self.resp_check.setDisabled(True)
            self.ok_push.setDisabled(True)

    def loadSettings(self):

        if os.path.exists(self.SettingsFileName):

            SettingsFile = open(self.SettingsFileName,"r")
            SettingsStr = SettingsFile.read()

            idx1 = SettingsStr.find("window")
            idx1 = SettingsStr.find("=",idx1)
            idx2 = SettingsStr.find(",",idx1)
            val = int(SettingsStr[idx1 + 1: idx2])
            if val in Gfx.Canvas._VISWND:
                self.viswnd_cb.setCurrentIndex(Gfx.Canvas._VISWND.index(val))

            idx1 = SettingsStr.find("rate")
            idx1 = SettingsStr.find("=", idx1)
            idx2 = SettingsStr.find(",", idx1)
            val = int(SettingsStr[idx1 + 1: idx2])
            if val in Bd.Board._SAMPLINGFR:
                self.samrate_cb.setCurrentIndex(Bd.Board._SAMPLINGFR.index(val))

            idx1 = SettingsStr.find("range")
            idx1 = SettingsStr.find("=", idx1)
            idx2 = SettingsStr.find(",", idx1)
            val = int(SettingsStr[idx1 + 1: idx2])
            if val in Bd.Board._VRANGE:
                self.range_cb.setCurrentIndex(Bd.Board._VRANGE.index(val))

            idx1 = SettingsStr.find("channels")
            idx1 = SettingsStr.find("=", idx1)
            idx2 = SettingsStr.find(",", idx1)
            if idx1+1 == idx2 or idx1 == -1 or idx2 == -1:
                self.chan_le.setText(str(1))
            else:
                val = int(SettingsStr[idx1 + 1: idx2])
                self.chan_le.setText(str(val))

            idx1 = SettingsStr.find("chanresp")
            idx1 = SettingsStr.find("=", idx1)
            idx2 = SettingsStr.find(",", idx1)
            if idx1+1 == idx2 or idx1 == -1 or idx2 == -1:
                self.chanresp_le.setText(str(1))
            else:
                val = int(SettingsStr[idx1 + 1: idx2])
                self.chanresp_le.setText(str(val))

            SettingsFile.close()

    def saveSettings(self,Session):
        Session.a = 2
        SettingsFile = open(self.SettingsFileName, "w")

        SettingsFile.write("window=" + str(Gfx.Canvas._VISWND[self.viswnd_cb.currentIndex()]) + ",\n")
        SettingsFile.write("rate=" + str(Bd.Board._SAMPLINGFR[self.samrate_cb.currentIndex()]) + ",\n")
        SettingsFile.write("range=" + str(Bd.Board._VRANGE[self.range_cb.currentIndex()]) + ",\n")
        SettingsFile.write("channels=" + self.chan_le.text() + ",\n")
        SettingsFile.write("chanresp=" + self.chanresp_le.text() + ",\n")
        SettingsFile.write("board=" + self.board_cb.currentText() + ",\n")

        SettingsFile.close()

        Session.Descriptor = self.inventory[self.board_cb.currentIndex()]
        Session.BoardNum = self.board_cb.currentIndex()
        Session.VRange = Bd.Board._VRANGE[self.range_cb.currentIndex()]
        Session.SRate = Bd.Board._SAMPLINGFR[self.samrate_cb.currentIndex()]
        Session.Channels = int(self.chan_le.text())
        Session.VisWindowLength = Gfx.Canvas._VISWND[self.viswnd_cb.currentIndex()]
        Session.RespON = self.resp_check.isChecked()
        Session.BoardStr = self.board_cb.currentText()
        if Session.RespON:
            Session.RespCh = int(self.chanresp_le.text())


    def resp_check_proc(self):

        if self.resp_check.isChecked():
            self.chanresp_le.setEnabled(True)

        else:
            self.chanresp_le.setDisabled(True)