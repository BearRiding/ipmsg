import sys 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import core
import feiQCoreData
import feiQSendMsg
import feiQRecv
import feiQTcp

class Example(QWidget):
    def __init__(self):
        super().__init__()
        core.start()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle("Draw text")

        btn1 = QPushButton("上线", self)
        btn1.move(30, 50)

        btn2 = QPushButton("下线", self)
        btn2.move(150, 50)
      
        btn1.clicked.connect(self.btUpClicked)
        btn2.clicked.connect(self.btOffClicked)
                
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Event sender')
        self.show()
        
        
    def btUpClicked(self):      
        feiQSendMsg.send_broadcast_online_msg()
        
        
    def btOffClicked(self):      
        feiQSendMsg.send_broadcast_offline_msg()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())