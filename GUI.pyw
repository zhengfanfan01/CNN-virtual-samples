from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
from subprocess import run
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pylab as pl
from scipy.optimize import leastsq
from scipy.integrate import *
import warnings
import matplotlib.backends.backend_qt5agg
import math
import sys
import numpy as np
from multiprocessing import Process, Queue
import datetime
import os
import pymysql
import time
from subprocess import run
from usemodel_alexnet import Main

# a = Main() 

# print(a.allParam)
# exit()


pl.mpl.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
pl.mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


class runRec():
    def recongnize(self):
        run("python useAlexnet.py", shell = False)

class Window(QtWidgets.QWidget):
    param = [0, 0, 0]

    def __init__(self):
        super(Window, self).__init__()


        self.list_map = {'0-0': [u'油压,上游过滤器,A侧【2 LHQ650LP】', u'压力', 'bar', 10, 0.1],
                         '0-1': [u'油压,下游过滤器,A侧【2 LHQ651LP】', u'压力', 'bar', 10, 0.1],
                         '0-2': [u'油压,上游过滤器,B侧【2 LHQ652LP】', u'压力', 'bar', 10, 0.1],
                         '0-3': [u'油压,下游过滤器,B侧【2 LHQ653LP】', u'压力', 'bar', 10, 0.1],
                         '0-4': [u'燃油压力上游过滤器【2 LHQ600LP】', u'压力', 'bar', 6, 0.05],
                         '0-5': [u'燃油压力下游过滤器【2 LHQ601LP】', u'压力', 'bar', 6, 0.05],
                         '0-6': [u'混合空气压力A侧【2 LHQ800LP】', u'压力', 'bar', 4, 0.05],
                         '0-7': [u'混合空气压力A侧【2 LHQ801LP】', u'压力', 'bar', 4, 0.05],

                         '1-0': [u'发动机水入口压力【2 LHQ700LP】', u'压力', 'bar', 10, 0.1],
                         '1-1': [u'发动机水入口温度【2 LHQ700LT】', u'温度', '℃', 120, 1],
                         '1-2': [u'发动机油入口温度A侧【2 LHQ650LT】', u'温度', '℃', 120, 1],
                         '1-3': [u'发动机油入口温度B侧【2 LHQ652LT】', u'温度', '℃', 120, 1],
                         '1-4': [u'发动机水入口温度【2 LHQ700LT】', u'温度', '℃', 120, 1],
                         '1-5': [u'混合空气温度A侧【2 LHQ800LT】', u'温度', '℃', 120, 1],
                         '1-6': [u'混合空气温度B侧【2 LHQ801LT】', u'温度', '℃', 120, 1],

                         '2-0': [u'油压,上游过滤器,A侧【2 LHQ150LP】', u'压力', 'bar', 10, 0.1],
                         '2-1': [u'油压,下游过滤器,A侧【2 LHQ151LP】', u'压力', 'bar', 10, 0.1],
                         '2-2': [u'油压,上游过滤器,B侧【2 LHQ152LP】', u'压力', 'bar', 10, 0.1],
                         '2-3': [u'油压,下游过滤器,B侧【2 LHQ153LP】', u'压力', 'bar', 10, 0.1],
                         '2-4': [u'燃油压力上游过滤器【2 LHQ100LP】', u'压力', 'bar', 6, 0.05],
                         '2-5': [u'燃油压力下游过滤器【2 LHQ101LP】', u'压力', 'bar', 6, 0.05],
                         '2-6': [u'混合空气压力A侧【2 LHQ300LP】', u'压力', 'bar', 4, 0.05],
                         '2-7': [u'混合空气压力A侧【2 LHQ301LP】', u'压力', 'bar', 4, 0.05],

                         '3-0': [u'发动机水入口压力【2 LHQ200LP】', u'压力', 'bar', 10, 0.1],
                         '3-1': [u'发动机水入口温度【2 LHQ200LT】', u'温度', '℃', 120, 1],
                         '3-2': [u'发动机油入口温度A侧【2 LHQ150LT】', u'温度', '℃', 120, 1],
                         '3-3': [u'发动机油入口温度B侧【2 LHQ152LT】', u'温度', '℃', 120, 1],
                         '3-4': [u'发动机水入口温度【2 LHQ203LT】', u'温度', '℃', 120, 1],
                         '3-5': [u'混合空气温度A侧【2 LHQ300LT】', u'温度', '℃', 120, 1],
                         '3-6': [u'混合空气温度B侧【2 LHQ301LT】', u'温度', '℃', 120, 1],


                         # '表盘编号'[标题名称，Y坐标名称，单位，量程最大值，比例]
                         }

        # BH5000系统中的几项标准参数                 
        self.a = Main()  
        self.listCompany = []
        self.listFactory = []
        self.listPlant = []
        self.listCompany.append(self.a.allParam['Company'])
        self.listFactory.append(self.a.allParam['Factory'])
        self.listPlant.append(self.a.allParam['Plant'])
        # self.listMiddleware = ['127.0.0.1']

        '''网格布局'''
        gridLayout = QtWidgets.QGridLayout()

        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.button = QtWidgets.QPushButton('历史曲线')
        gridLayout.addWidget(self.button, 8, 7, 1, 1)
        font0 = QtGui.QFont()
        font0.setFamily("楷体")
        font0.setPointSize(12)
        self.button.setFont(font0)

        self.titleLbl = QtWidgets.QLabel(u"核电应急柴油机模拟仪表识别系统", self)
        self.titleLbl.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.titleLbl.setAlignment(Qt.AlignCenter)
        gridLayout.addWidget(self.titleLbl, 0, 1, 1, 6)
        font0 = QtGui.QFont()
        font0.setFamily("楷体")
        font0.setPointSize(24)
        self.titleLbl.setFont(font0)

        self.company = QtWidgets.QLabel(u"请选择公司", self)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.company.setFont(font)
        self.company.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.company.setFrameShadow(QtWidgets.QFrame.Sunken)
        gridLayout.addWidget(self.company, 5, 0, 1, 1)

        self.companySelect = QtWidgets.QComboBox(self)
        gridLayout.addWidget(self.companySelect, 5, 1, 1, 1)
        font3 = QtGui.QFont()
        font3.setFamily("宋体")
        font3.setPointSize(10)
        self.companySelect.setFont(font3)
        self.companySelect.setEditable(True)
        # self.listCompany = ['大亚湾核电', '宁德核电']
        for i in range(len(self.listCompany)):
            self.companySelect.addItem(self.listCompany[i])
        _translate = QtCore.QCoreApplication.translate

        self.factory = QtWidgets.QLabel(u"请选择厂区", self)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.factory.setFont(font)
        self.factory.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.factory.setFrameShadow(QtWidgets.QFrame.Sunken)
        gridLayout.addWidget(self.factory, 6, 0, 1, 1)

        self.factorySelect = QtWidgets.QComboBox(self)
        gridLayout.addWidget(self.factorySelect, 6, 1, 1, 1)
        font3 = QtGui.QFont()
        font3.setFamily("宋体")
        font3.setPointSize(10)
        self.factorySelect.setFont(font3)
        self.factorySelect.setEditable(True)
        # self.listFactory = ['1号反应堆', '2号反应堆']
        for i in range(len(self.listFactory)):
            self.factorySelect.addItem(self.listFactory[i])
        _translate = QtCore.QCoreApplication.translate

        self.plant = QtWidgets.QLabel(u"请选择设备", self)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.plant.setFont(font)
        self.plant.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plant.setFrameShadow(QtWidgets.QFrame.Sunken)
        gridLayout.addWidget(self.plant, 7, 0, 1, 1)

        self.plantSelect = QtWidgets.QComboBox(self)
        gridLayout.addWidget(self.plantSelect, 7, 1, 1, 1)
        font3 = QtGui.QFont()
        font3.setFamily("宋体")
        font3.setPointSize(10)
        self.plantSelect.setFont(font3)
        self.plantSelect.setEditable(True)
        # self.listPlant = ['应急柴油机1号', '应急柴油机2号']
        for i in range(len(self.listPlant)):
            self.plantSelect.addItem(self.listPlant[i])
        _translate = QtCore.QCoreApplication.translate

        self.runtime = QtWidgets.QLabel(u"运行时间", self)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.runtime.setFont(font)
        self.runtime.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.runtime.setFrameShadow(QtWidgets.QFrame.Sunken)
        gridLayout.addWidget(self.runtime, 5, 2, 1, 1)

        self.timeShow = QtWidgets.QLineEdit(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.timeShow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("仿宋")
        font.setPointSize(14)
        self.timeShow.setFont(font)        
        gridLayout.addWidget(self.timeShow, 5, 3, 1, 1)

        self.recongnizeBtn = QtWidgets.QPushButton(u"开始识别")
        gridLayout.addWidget(self.recongnizeBtn, 6, 2, 1, 1)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.recongnizeBtn.setFont(font)
        self.recongnizeBtn.clicked.connect(self.timer)
        self.recongnizeBtn.clicked.connect(self.changeLabel)
        self.recongnizeBtn.clicked.connect(self.recongnize)

        self.quitBtn = QtWidgets.QPushButton('退出', self)
        gridLayout.addWidget(self.quitBtn, 6, 3, 1, 1)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.quitBtn.setFont(font)
        self.quitBtn.clicked.connect(self.quit)


        self.cameraLbl = QtWidgets.QLabel(u"摄像头编号")
        gridLayout.addWidget(self.cameraLbl, 5, 4, 1, 1)
        font3 = QtGui.QFont()
        font3.setFamily("楷体")
        font3.setPointSize(12)
        self.cameraLbl.setFont(font3)
        self.cameraLbl.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.cameraLbl.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.cameraSelect = QtWidgets.QComboBox(self)
        gridLayout.addWidget(self.cameraSelect, 5, 5, 1, 1)
        font3 = QtGui.QFont()
        font3.setFamily("宋体")
        font3.setPointSize(10)
        self.cameraSelect.setFont(font3)
        self.cameraSelect.setEditable(True)
        for i in range(4):
            self.cameraSelect.addItem("")
        _translate = QtCore.QCoreApplication.translate
        self.cameraSelect.setCurrentText(_translate("", "1"))
        for i in range(4):
            self.cameraSelect.setItemText(i, _translate("", "%s" % (i+1)))
        self.cameraSelect.currentIndexChanged['int'].connect(self.judge)

        self.startTime = QtWidgets.QLabel(u"起始时间")
        gridLayout.addWidget(self.startTime, 5, 6, 1, 1)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.startTime.setFont(font)
        self.startTime.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.startTime.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.startTimeSelect = QtWidgets.QDateTimeEdit(self)
        start_time_default = time.localtime()
        self.startTimeSelect.setDateTime(QtCore.QDateTime(QtCore.QDate(
            start_time_default.tm_year, start_time_default.tm_mon, start_time_default.tm_mday), QtCore.QTime(start_time_default.tm_hour-1, start_time_default.tm_min, start_time_default.tm_sec)))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.startTimeSelect.setFont(font)
        gridLayout.addWidget(self.startTimeSelect, 5, 7, 1, 1)

        self.dialLbl = QtWidgets.QLabel(u"仪表编号")
        gridLayout.addWidget(self.dialLbl, 6, 4, 1, 1)
        font4 = QtGui.QFont()
        font4.setFamily("楷体")
        font4.setPointSize(12)
        self.dialLbl.setFont(font4)
        self.dialLbl.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.dialLbl.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.dialSelect = QtWidgets.QComboBox(self)
        gridLayout.addWidget(self.dialSelect, 6, 5, 1, 1)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(10)
        self.dialSelect.setFont(font)
        self.dialSelect.setEditable(True)

        for i in range(8):
            self.dialSelect.addItem("")
        _translate = QtCore.QCoreApplication.translate

        self.dialSelect.setCurrentText(_translate("", "1"))
        for i in range(8):
            self.dialSelect.setItemText(i, _translate("", "%s" % (i+1)))


        self.stopTime = QtWidgets.QLabel(u"终止时间")
        gridLayout.addWidget(self.stopTime, 6, 6, 1, 1)
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(12)
        self.stopTime.setFont(font)
        self.stopTime.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stopTime.setFrameShadow(QtWidgets.QFrame.Sunken)

        self.stopTimeSelect = QtWidgets.QDateTimeEdit(self)
        self.stopTimeSelect.setDateTime(QtCore.QDateTime(QtCore.QDate(
            start_time_default.tm_year, start_time_default.tm_mon, start_time_default.tm_mday), QtCore.QTime(23, 59, 59)))
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(12)
        self.stopTimeSelect.setFont(font)
        gridLayout.addWidget(self.stopTimeSelect, 6, 7, 1, 1)

        gridLayout.addWidget(self.toolbar, 8, 0, 1, 8)
        gridLayout.addWidget(self.canvas, 9, 0, 1, 8)

        self.setLayout(gridLayout)

        self.setWindowTitle(u"核电应急柴油机模拟仪表识别系统")
        self.resize(600, 600)

        '''初始时间参数设置'''
        self.timeShow.setText('0:00:00')

        '''初始化定时器'''
        self.timerCal = QTimer()  # 初始化一个定时器
        self.timerCal.setInterval(1000)
        '''计数器'''
        self.i = 1
        self.m = 1
        '''识别主进程'''
        runRecStart = runRec()
        self.runRec = Process(target = runRecStart.recongnize, args=())

    def quit(self):
        if self.i % 2 == 0:
            self.runRec.terminate()
            os.system("taskkill/im python.exe -f")
            sys.exit()
        elif self.i % 2 == 1:
            sys.exit()

    def judge(self):
        if self.cameraSelect.currentIndex() == 0 or self.cameraSelect.currentIndex() == 2:
            self.dialSelect.clear()
            for i in range(8):
                self.dialSelect.addItem("")
                _translate = QtCore.QCoreApplication.translate
                self.dialSelect.setItemText(i, '%s' % (i+1))


        else:
            self.dialSelect.clear()
            for i in range(7):
                self.dialSelect.addItem("")
                _translate = QtCore.QCoreApplication.translate
                self.dialSelect.setItemText(i, '%s' % (i+1))


    def operate(self):
        timeInterval = str(datetime.datetime.now() - time_init)[0:7]
        self.timeShow.setText(timeInterval)

    def timer(self):
        if self.i == 1:
            global time_init

            time_init = datetime.datetime.now()

            self.timerCal.start()  # 设置计时间隔并启动
            self.timerCal.timeout.connect(self.operate)  # 计时结束调用operate()方法


    def changeLabel(self):
        if self.i % 2 == 1:
            self.recongnizeBtn.setText("暂停")
            self.quitBtn.setText("结束并退出")
        elif self.i % 2 == 0:
            self.recongnizeBtn.setText("开始识别")
            self.quitBtn.setText("退出")
        self.i += 1


    def recongnize(self):
        if self.i % 2 == 0:
            self.runRec.start()
        else:
            self.runRec.terminate()
            os.system("taskkill/im python.exe -f")
            runRecStart = runRec()
            self.runRec = Process(target = runRecStart.recongnize, args=())

    def draw(self):
        camera_num = int(self.cameraSelect.currentText())
        dial_num = int(self.dialSelect.currentText())

        time_start = self.startTimeSelect.dateTime().toPyDateTime()
        time_stop = self.stopTimeSelect.dateTime().toPyDateTime()

        time_start = time.mktime(time_start.timetuple())
        time_stop = time.mktime(time_stop.timetuple())
        
        ax = self.figure.add_subplot(1, 1, 1)
        ax.clear()
        plt.grid(True)  # 添加网格
        plt.ion()  # interactive mode on
        
        result = self.read_data_db(
            camera_num-1, dial_num-1, time_start, time_stop)
        plt.ylim(0, self.list_map['%s-%s' % (camera_num-1, dial_num-1)][3])
        ax.set_title('Camera %s, Dial %s' % (camera_num-1, dial_num-1))
        ax.set_title(u'%s' % self.list_map[
                     '%s-%s' % (camera_num-1, dial_num-1)][0])
        ax.set_xlabel('时间')
        ax.set_ylabel('%s (%s)' % (self.list_map['%s-%s' % (camera_num-1, dial_num-1)][
                      1], self.list_map['%s-%s' % (camera_num-1, dial_num-1)][2]))
        if len(result) == 0:
            print('无数据')
        else:
            data = []
            x_ticks_index = []
            date_time_index = []
            index = 0
            try:
                for i in range(len(result) - 1):
                    one_data = list(map(int, result[i][2].split()))
                    data += (one_data)
                    x_ticks_index.append(index)
                    index += len(one_data)
                    each_time1 = result[i][0]
                    each_time2 = result[i+1][0]
                    interval = each_time2 - each_time1
                    for n in range(10):
                        date_time_index.append(time.strftime(
                        "%H:%M:%S", time.localtime(result[i][0] + n*(interval/10))))
                data = np.array(
                    data)*self.list_map['%s-%s' % (camera_num - 1, dial_num - 1)][4]
                data = list(data)
                ax.plot(data)
                new_date_time_index = []
                
                for i in range(10):
                    new_date_time_index.append(date_time_index[int(i*LEN/10)])

                ax.set_xticks(new_date_time_index)
                plt.legend()
                self.canvas.draw()
            except Exception as e:
                print(e)


    def read_data_db(self, camera_num, dial_num, time_start, time_stop):
        conn = pymysql.connect(user='root', passwd='bhxz2017', db='bhxz')
        cursor = conn.cursor()

        if time.strftime('%Y-%m-%d', time.localtime(time_start)) == time.strftime('%Y-%m-%d', time.localtime(time_stop)):
            db_name = time.strftime('data%Y%m%d', time.localtime(time_start))
            sql = r'SELECT * FROM %s WHERE time>=%s and time<=%s and name="%s-%s"' % (
                db_name, time_start, time_stop, camera_num, dial_num)
            print('1:', sql)
        elif (time_stop - time_start) <= 24*60*60:
            db_name_0 = time.strftime('data%Y%m%d', time.localtime(time_start))
            db_name_1 = time.strftime('data%Y%m%d', time.localtime(time_stop))
            sql = r'SELECT * FROM {0} WHERE time>={1} and name="{2}-{3}" UNION ALL SELECT * FROM {4} WHERE time<={5} and name="{2}-{3}"'.format(
                db_name_0, time_start, camera_num, dial_num, db_name_1, time_stop)
            print('2', sql)
        else:
            db_name_0 = time.strftime('data%Y%m%d', time.localtime(time_start))
            db_name_1 = time.strftime('data%Y%m%d', time.localtime(time_stop))
            time_stop = time_start + 24*60*60
            sql = r'SELECT * FROM {0} WHERE time>={1} and name="{2}-{3}" UNION ALL SELECT * FROM {4} WHERE time<={5} and name="{2}-{3}"'.format(
                db_name_0, time_start, camera_num, dial_num, db_name_1, time_stop)
            print('3', sql)
        try:
            cursor.execute(sql)
            conn.commit()
            result = cursor.fetchall()
        except:
            print('无所选时间历史数据!!')
            result = []
            # print(result)
        finally:
            conn.close()
        return result

    # 捕捉窗口关闭事件
    def closeEvent(self, event):
        if self.i % 2 == 0:
            self.runRec.terminate()
            os.system("taskkill/im python.exe -f")
            sys.exit()
        elif self.i % 2 == 1:
            sys.exit()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    m = Window()
    m.show()
    app.exec_()
    sys.exit(app.exec_())
    
