# -*- coding:utf-8 -*-
from PyQt5.QtWidgets import QMainWindow, QApplication
from untitled import Ui_MainWindow
import os, time, sys, re
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import pymysql



flog = 0

class Main(QMainWindow, Ui_MainWindow):  # 如果你是用Widget创建的窗口，这里会不同
    # class Main(QWidget,Ui_Form):

    def __init__(self):
        super(Main, self).__init__()
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.Save_datebase)
        self.pushButton_3.clicked.connect(self.DB_Search)
        self.pushButton_4.clicked.connect(self.Printinfo_picture)



    def Read_dd_2(self):
        Edit_datetime = self.dateTimeEdit_2.text().replace('/', '-', 1) + ':00'
        Edit_datetime = Edit_datetime.replace(':', '+', 1)
        Edit_dict = {'Year': Edit_datetime[0:4],
                     'Mon': Edit_datetime[(Edit_datetime.index('-') + 1):(Edit_datetime.index('/'))],
                     'Day': Edit_datetime[(Edit_datetime.index('/') + 1):(Edit_datetime.index(' '))],
                     'Hour': Edit_datetime[(Edit_datetime.index(' ') + 1):(Edit_datetime.index('+'))],
                     'Min': Edit_datetime[(Edit_datetime.index('+') + 1):(Edit_datetime.index(':'))],
                     'Sec': '00'}
        if len(Edit_dict['Mon']) == 1:
            Edit_dict['Mon'] = '0' + Edit_dict['Mon']
        if len(Edit_dict['Day']) == 1:
            Edit_dict['Day'] = '0' + Edit_dict['Day']
        if len(Edit_dict['Hour']) == 1:
            Edit_dict['Hour'] = '0' + Edit_dict['Hour']
        if len(Edit_dict['Min']) == 1:
            Edit_dict['Min'] = '0' + Edit_dict['Min']
        return datetime.datetime.strptime(
            Edit_dict['Year'] + Edit_dict['Mon'] + Edit_dict['Day'] + Edit_dict['Hour'] + Edit_dict['Min'] + \
            Edit_dict['Sec'], "%Y%m%d%H%M%S")

    def Read_dd(self):
        Edit_datetime = self.dateTimeEdit.text().replace('/', '-', 1) + ':00'
        Edit_datetime = Edit_datetime.replace(':', '+', 1)
        Edit_dict = {'Year': Edit_datetime[0:4],
                     'Mon': Edit_datetime[(Edit_datetime.index('-') + 1):(Edit_datetime.index('/'))],
                     'Day': Edit_datetime[(Edit_datetime.index('/') + 1):(Edit_datetime.index(' '))],
                     'Hour': Edit_datetime[(Edit_datetime.index(' ') + 1):(Edit_datetime.index('+'))],
                     'Min': Edit_datetime[(Edit_datetime.index('+') + 1):(Edit_datetime.index(':'))],
                     'Sec': '00'}
        if len(Edit_dict['Mon']) == 1:
            Edit_dict['Mon'] = '0' + Edit_dict['Mon']
        if len(Edit_dict['Day']) == 1:
            Edit_dict['Day'] = '0' + Edit_dict['Day']
        if len(Edit_dict['Hour']) == 1:
            Edit_dict['Hour'] = '0' + Edit_dict['Hour']
        if len(Edit_dict['Min']) == 1:
            Edit_dict['Min'] = '0' + Edit_dict['Min']
        return  datetime.datetime.strptime(
            Edit_dict['Year'] + Edit_dict['Mon'] + Edit_dict['Day'] + Edit_dict['Hour'] + Edit_dict['Min'] + \
            Edit_dict['Sec'], "%Y%m%d%H%M%S")

    def Handle_datetime(self , dateTimeEdit):
        Edit_datetime = dateTimeEdit.replace('/', '-', 1) + ':00'
        Edit_datetime = Edit_datetime.replace(':', '+', 1)
        Edit_dict = {'Year': Edit_datetime[0:4],
                     'Mon': Edit_datetime[(Edit_datetime.index('-') + 1):(Edit_datetime.index('/'))],
                     'Day': Edit_datetime[(Edit_datetime.index('/') + 1):(Edit_datetime.index(' '))],
                     'Hour': Edit_datetime[(Edit_datetime.index(' ') + 1):(Edit_datetime.index('+'))],
                     'Min': Edit_datetime[(Edit_datetime.index('+') + 1):(Edit_datetime.index(':'))],
                     'Sec': '00'}
        if len(Edit_dict['Mon']) == 1:
            Edit_dict['Mon'] = '0' + Edit_dict['Mon']
        if len(Edit_dict['Day']) == 1:
            Edit_dict['Day'] = '0' + Edit_dict['Day']
        if len(Edit_dict['Hour']) == 1:
            Edit_dict['Hour'] = '0' + Edit_dict['Hour']
        if len(Edit_dict['Min']) == 1:
            Edit_dict['Min'] = '0' + Edit_dict['Min']
        return datetime.datetime.strptime(
            Edit_dict['Year'] + Edit_dict['Mon'] + Edit_dict['Day'] + Edit_dict['Hour'] + Edit_dict['Min'] + \
            Edit_dict['Sec'], "%Y%m%d%H%M%S")


    def Str_Compare(self , str_line):
        if str(str_line[2:3]).find(self.lineEdit.text()) and str(str_line[8:9]).find(self.lineEdit_2.text()):
            return 1
        else :
            if str(str_line[2:3]).find(self.lineEdit.text()):
                self.textEdit_2.append("未匹配到ID号")
            if str(str_line[8:9]).find(self.lineEdit_2.text()):
                self.textEdit_2.append("未匹配到区站号")
            return 0

    def DI_check(self , str_line ):
        global flog
        a = ''.join(str_line[7:8])
        b = self.comboBox.currentText()
        if a == b:
            return 1
        else:
            self.textEdit_2.append("第"+str(flog)+"未找DI")
            return 0

    def ID_ckeck(self, str_line ):
        global folg
        a =  ''.join(str_line[8:9])
        b = self.lineEdit_2.text()
        if a == b:
            return 1
        else:
            self.textEdit_2.append("第"+str(flog)+"未找ID")
            return 0

    def frame_check(self, str_line ):
        global flog
        a = ''.join(str_line[10:11])
        b =  self.comboBox_2.currentText()
        if a == b:
            return 1
        else:
            self.textEdit_2.append("第"+str(flog)+"未找数据帧")
            return 0

    def StatNum_check(self, str_line ):
        a = ''.join(str_line[2:3])
        b = self.lineEdit.text()
        if a == b:
            return 1
        else:
            self.textEdit_2.append("第"+str(flog)+"未找到台站号")
            return 0

    def datetime_check(self , str_line  , dd_jure , dd_inter ):
        global dd
        global dd_pull
        global dd_Miss
        global flog
        global dd_first
        global dd_jurefirst
        dd_2 = self.Handle_dd_2()
        #if flog == 0:
            #dd_jurefirst = self.Handle_dd_jure(str_line)
        if dd <= dd_jure and dd<=dd_2 :
            if int((dd_jure - dd).seconds/60)%dd_inter == 0 :
                dd = dd_jure
                return 1
            else :
                while dd < dd_jure:
                    dd = dd +datetime.timedelta(minutes=dd_inter)
                return 0

        else:
            return 0
    def Handle_dd_jure(self , str_line):
        return datetime.datetime.strptime(''.join(str_line[9:10]), '%Y%m%d%H%M%S')
    def read_asNULL(self , str_line):
        global flog
        g_MessageDict[str(flog)] = ['NULL']
        flog = flog+1
        g_MessageDict[str(flog)] = str_line[9:10]
    def readfile_asline(self , str_line ):
        global g_MessageLine
        g_MessageLine = g_MessageLine+str_line[2:3]+str_line[7:8]+ str_line[8:9]+ str_line[10:11]+ str_line[9:10]+str_line[10:]
        return

    def Read_combox_3(self):
        a = int(self.comboBox_3.currentIndex())
        if a == 0:
            return 1
        if a == 1:
            return 5
        if a == 2:
            return 10
        if a == 3:
            return 60

    def Handle_MessageLine(self):
        global g_MessageLine
        MessageLine = g_MessageLine
        dd = self.Handle_dd()
        dd_2 = self.Handle_dd_2()
        dd_len = int((dd_2 - dd).seconds/60)
        i = 0

        while i <= dd_len:
            if datetime.datetime.strptime(str(MessageLine[i]), '%Y%m%d%H%M%S') == dd:
                dd = dd + datetime.timedelta(minutes=1)
                i = i+1
            else:
                dd_Message = datetime.datetime.strptime(str(MessageLine[i]), '%Y%m%d%H%M%S')
                list_len = int((dd_Message - dd).seconds/60)
                list = [0]*list_len
                dd = datetime.datetime.strptime(MessageLine[i], '%Y%m%d%H%M%S')
                MessageLine[i:i] = list
                i = i + list_len

        return MessageLine

        
    def save_SQL_asline(self, line , str_line):
        # 打开数据库连接-填入你Mysql的账号密码和端口
        conn = pymysql.connect('localhost', 'root', '2667885', "wetherdate", charset='utf8')
        # 使用 cursor() 方法创建一个游标对象 cursor
        mycursor = conn.cursor()
        time = datetime.datetime.strptime(str(str_line[9]), '%Y%m%d%H%M%S')

        try:
            sql = "INSERT INTO `wetherdate`.`all_log` (area, DInum, IDnum, frame, datetime, date) VALUES (%s,%s,%s,%s,%s,%s)"
            val = (str_line[2] , str_line[7] , str_line[8],str_line[10],time,line)
            mycursor.execute(sql, val)
            # 调用
            # sql='select * from zljob'
            # 执行sql语句
            conn.commit()

        except Exception:
            # 发生错误时回滚
            conn.rollback()
            print('发生异常')
            # 关闭数据库连接
        mycursor.close()
        conn.close()


    def Save_datebase(self):
        #dd_inter = datetime.datetime.strptime(str(self.Read_combox_3()), "%S")
        dd_inter = self.Read_combox_3()
        global dd
        global dd_2
        global g_MessageDict
        global flog
        global dd_jurefirst
        global dd_first
        global fiog
        global End_identification
        End_identification = 0
        dd = self.Handle_datetime(self.dateTimeEdit.text())
        dd_2 = self.Handle_datetime(self.dateTimeEdit_2.text())
        if len(self.lineEdit.text()) == 0 or len(self.lineEdit_2.text()) == 0:
            if len(self.lineEdit.text()) == 0:
                self.textEdit_2.append("提示：请输入区站号")
            if len(self.lineEdit_2.text()) == 0:
                self.textEdit_2.append("提示：请输入ID号")

        else:
            if os.path.isfile('ReceivedTofile-TCPSERVER-2019_11_5_10-04-51.DAT'):
                self.textEdit_2.append("验证文件成功")
                file = open('ReceivedTofile-TCPSERVER-2019_11_5_10-04-51.DAT', mode='r+', encoding='UTF-8')
                flog = 0
                for line in file.readlines() :
                    flog = flog + 1
                    if len(line) != 0:
                        str_line = line.strip().split(',')
                        if len(str_line) >= 11:
                            if self.Str_Compare(str_line):
                                dd_jure = self.Handle_dd_jure(str_line)
                                if ( self.ID_ckeck(str_line )) and (self.DI_check(str_line )) and (self.frame_check(str_line)) and (self.StatNum_check(str_line )):
                                    self.save_SQL_asline(line , str_line)
                                    print(str(flog))

                            else:
                                break
                file.close()
                self.textEdit_2.append(str(flog))

            else:
                self.textEdit.append('未找到文件，请放到根目录下')

    def Printinfo_picture(self):
        # 以0.2为间隔均匀采样
        t = np.arange(0., 5., 0.2)
        # 'r--':红色的需要;'bs':蓝色方块;'g^':绿色三角
        plt.plot(t, t, 'r--', t, t ** 2, 'bs', t, t ** 3, 'g^')
        plt.show()
    def DB_Search(self):
        beg_time = self.Read_dd()
        end_time = self.Read_dd_2()
        mydb = pymysql.connect(
            host="localhost",
            user="root",
            passwd="2667885",
            database="wetherdate"
        )
        mycursor = mydb.cursor()
        sql = "SELECT * FROM all_log WHERE datetime >= '%s' and datetime <='%s'"%(beg_time, end_time)
        mycursor.execute(sql)
        myresult = mycursor.fetchall()  # fetchall() 获取所有记录

        self.textEdit_2.append(str(myresult))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Main()
    main.show()
    sys.exit(app.exec_())
    #6666
