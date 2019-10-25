import sys
import serial
import re
import binascii
import _thread
import time
import serial.tools.list_ports
from UI1 import Ui_MainWindow
from PyQt5 import QtWidgets







class PC_software(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(PC_software,self).__init__()
        self.setupUi(self)

        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.ser.bytesize = 8  # 设置数据位
        self.ser.stopbits = 1  # 设置停止位
        self.ser.parity = "N"  # 设置校验位
        self.pushButton_4.clicked.connect(self.Clear_text)
        self.pushButton.clicked.connect(self.Screach_COM)
        self.pushButton_2.clicked.connect(self.Clink_COM)
        self.pushButton_3.clicked.connect(self.Data_Send)
        self.Screach_COM()
    def Clear_text(self):
        self.textEdit.clear()
        self.textBrowser.clear()
    def Screach_COM(self):
        self.comboBox.clear()
        port_list = list(serial.tools.list_ports.comports())
        com_numbers = len(port_list)
        p1 = re.compile(r'[(](.*?)[)]', re.S)
        for i in range(com_numbers):
            com_list = str(port_list[i])
            com_name = re.findall(p1, com_list)
            com_name = str(com_name)
            strlist = com_name.split("'")
            self.comboBox.addItem(strlist[1])
    def Clink_COM(self):
        self.ser.port = self.comboBox.currentText()
        if self.ser.is_open == True :
            self.ser.close()
            self.pushButton_2.setText('打开串口')
        else:
            self.ser.open()
            self.pushButton_2.setText('关闭串口')
    def Data_Send(self):
        if self.ser.is_open == True:
            self.ser.write((self.textEdit.toPlainText()+'\r\n').encode('gbk'))
            #self.ser.write(str(binascii.b2a_hex(self.textEdit.toPlainText()))) #尝试编写HEX发送—失败
    def Data_Recive(self):

         while True:
             if self.ser.is_open == True:
                self.RC_data = self.ser.read_all()
                if self.RC_data != b'':
                   #print('receive',self.RC_data.decode("gbk"))
                    self.textBrowser.insertPlainText(self.RC_data.decode("UTF-8"))
                    self.textBrowser.moveCursor(self.textBrowser.textCursor().End)  # 文本框显示到底部




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    myshow = PC_software()
    myshow.show()
    _thread.start_new_thread(myshow.Data_Recive,())
    sys.exit(app.exec_())


