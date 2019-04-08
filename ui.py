import sys 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import core
import feiQCoreData
import feiQSendMsg
import feiQRecv
import os
import feiQTcp
import time
from mainwindow import Ui_MainWindow

class tUpdateUI(QThread):

    _signal = pyqtSignal(str)

    def __init__(self):
        super(tUpdateUI, self).__init__()

    def run(self):
        while True:
            self._signal.emit("write OK")
            time.sleep(1)

    def callback(self, msg):
        # print('callback')
        pass

class myui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        core.start()
        super(myui, self).__init__(parent)
        self.setupUi(self)
        self.btnOffline.setVisible(False)
        self.btnOffline.clicked.connect(self.btOffClicked)
        self.btnOnline.clicked.connect(self.btUpClicked)
        self.btnSendMsg.clicked.connect(self.btnMsgClicked)
        self.btnSendFile.clicked.connect(self.btnFileClicked)
        self.listWidget.clicked.connect(self.btnDownload)
        self.flushBegin()
        self.user_list = list()
        self.receives = list()
        self.download_file_list = list()

    def flushBegin(self):
        self.tupdate = tUpdateUI()
        self.tupdate._signal.connect(self.flush)
        self.tupdate.start()

    def flush(self):
        i = 0
        for x in self.user_list:
            i = i + 1
            if x not in feiQCoreData.user_list:
                self.user_list.remove(x)
                self.ipCombo.removeItem(i)
        for x in feiQCoreData.user_list:
            if x not in self.user_list:
                self.user_list.append(x)
                self.ipCombo.addItem(x['host_name'], x['ip'])
        if feiQRecv.message is not 'null':
            tempstr = self.ReceiveLabel.text() + '\n' + feiQRecv.message
            self.ReceiveLabel.setText(tempstr)
            feiQRecv.message = 'null'
            print(tempstr)

        i = 0
        self.listWidget.clear()
        for x in feiQCoreData.download_file_list:
            file_name = x['file_name'].split('/')
            self.listWidget.addItem(str(i) + ' ' + str(x['dest_ip']) + ' ' + file_name[-1])
            i = i + 1

    def btnDownload(self, item):
        print(454)
        file_info = dict()
        file_info['type'] = "download_file"
        file_info['data'] = feiQCoreData.download_file_list[item.row()]
        feiQCoreData.file_info_queue.put(file_info)
        print('down')

    def btUpClicked(self):
        feiQSendMsg.send_broadcast_online_msg()
        print(self.textEdit.toPlainText())
        self.btnOffline.setVisible(True)
        
    def btOffClicked(self):      
        feiQSendMsg.send_broadcast_offline_msg()

    def btnMsgClicked(self):
        feiQSendMsg.send_msg_2_ip(self.ipCombo.currentData(), self.textEdit.toPlainText())
    
    def btnFileClicked(self):
        filename = QFileDialog.getOpenFileName()
        print(filename, type(filename), filename[0])
        feiQSendMsg.send_file_2_ip(self.ipCombo.currentData(), filename[0])
    


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = myui()
    ex.show()
    sys.exit(app.exec_())
    core.start()