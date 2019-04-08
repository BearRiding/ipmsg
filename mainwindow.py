# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(364, 689)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.btnOnline = QtWidgets.QPushButton(self.centralWidget)
        self.btnOnline.setGeometry(QtCore.QRect(40, 20, 99, 27))
        self.btnOnline.setObjectName("btnOnline")
        self.btnOffline = QtWidgets.QPushButton(self.centralWidget)
        self.btnOffline.setGeometry(QtCore.QRect(210, 20, 99, 27))
        self.btnOffline.setObjectName("btnOffline")
        self.ipCombo = QtWidgets.QComboBox(self.centralWidget)
        self.ipCombo.setGeometry(QtCore.QRect(40, 80, 221, 25))
        self.ipCombo.setObjectName("ipCombo")
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setGeometry(QtCore.QRect(30, 160, 281, 91))
        self.textEdit.setObjectName("textEdit")
        self.textLabel = QtWidgets.QLabel(self.centralWidget)
        self.textLabel.setGeometry(QtCore.QRect(30, 130, 91, 17))
        self.textLabel.setObjectName("textLabel")
        self.btnSendMsg = QtWidgets.QPushButton(self.centralWidget)
        self.btnSendMsg.setGeometry(QtCore.QRect(210, 270, 99, 27))
        self.btnSendMsg.setObjectName("btnSendMsg")
        self.btnSendFile = QtWidgets.QPushButton(self.centralWidget)
        self.btnSendFile.setGeometry(QtCore.QRect(40, 270, 99, 27))
        self.btnSendFile.setObjectName("btnSendFile")
        self.textLabel2 = QtWidgets.QLabel(self.centralWidget)
        self.textLabel2.setGeometry(QtCore.QRect(30, 320, 81, 17))
        self.textLabel2.setObjectName("textLabel2")
        self.ReceiveLabel = QtWidgets.QLabel(self.centralWidget)
        self.ReceiveLabel.setGeometry(QtCore.QRect(30, 350, 311, 91))
        self.ReceiveLabel.setText("")
        self.ReceiveLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.ReceiveLabel.setObjectName("ReceiveLabel")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(0, 450, 351, 192))
        self.listWidget.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralWidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 364, 29))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.btnOnline.setText(_translate("MainWindow", "上线"))
        self.btnOffline.setText(_translate("MainWindow", "下线"))
        self.textLabel.setText(_translate("MainWindow", "要发送的消息"))
        self.btnSendMsg.setText(_translate("MainWindow", "发送消息"))
        self.btnSendFile.setText(_translate("MainWindow", "发送文件"))
        self.textLabel2.setText(_translate("MainWindow", "接受的消息"))


