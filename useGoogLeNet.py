# -*- coding: utf-8 -*-
"""
Created on Mon Jul 17 09:49:27 2017

@author: caiwd

##from picture get dial

##num is a list ,every param is the number dials of every lines

##input : a opencv read array
"""
import cv2
import time
import os
import sys
# import pymysql
import logging
import numpy as np
import datetime
import multiprocessing
from multiprocessing import Process,Queue,Pool

from lib.init import Universal_value


log_file = "./log.log"
formats = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename = log_file, level = logging.DEBUG, format = formats)


class Main(Universal_value):
    def __init__(self):
        Universal_value.__init__(self)
        # print(type(self.list_map['0-4'][4]))
        # exit()
        self.itera = 0
        self.minRadius = 150
        self.maxRadius=int(1.2*self.minRadius)
        self.quene_list()

        last_images ={}
        logging.info('启动系统！')

        # try:
        #     conn = pymysql.connect(user='root', passwd='', db='bhxz')
        # except:
        #     print("连接数据库错误!")
        #     logging.error("连接数据库错误!")
        #     time.sleep(10)
        #     os._exit(0)
        # cursor = conn.cursor()
        # now_time = time.strftime("%Y%m%d", time.localtime())
        # try:
        #     # sql = 'CREATE TABLE data{} (DateTime varchar(50), Name varchar(10), Value varchar(10))'.format(now_time)
        #     sql = 'CREATE TABLE data{} (DateTime varchar(50), StartIndex varchar(10), Value float(30), Company varchar(100), Factory varchar(100), Plant varchar(100), Middleware varchar(20), Port varchar(10), KeepSecond varchar(20), Type varchar(10), CHANNID varchar(10), Source varchar(20))'.format(now_time)
        #     cursor.execute(sql) 
        #     conn.commit()
        #     logging.info('新建表[data%s]'%now_time)
        # except:
        #     logging.info('表[data%s]已存在'%now_time)
        # finally:
        #     conn.close()
        for camera_num in range(self.camera_nums):
            self.empty_piclist(camera_num)
            for dial_num in range(self.dial_num_list[camera_num][0]+self.dial_num_list[camera_num][1]):
                exec('self.match_%s_%s = True'%(camera_num,dial_num))
                new_img = cv2.imread(r'template/%s_%s.jpg'%(camera_num,dial_num),0)
                exec('self.temp_{0}_{1} = (cv2.resize(new_img,self.pic_size)/255.0).reshape((self.pic_size[0],self.pic_size[0],1))'.format(camera_num,dial_num))
        

    def empty_piclist(self,camera_num):
        for dial_num in range(self.dial_num_list[camera_num][0]+self.dial_num_list[camera_num][1]):
            exec('self.memory_pic_%s_%s = []'%(camera_num,dial_num))        

    def quene_list(self):
        self.q_result_socket = multiprocessing.Queue(20)
        self.q_result_db = multiprocessing.Queue()
        self.q_result_data = multiprocessing.Queue()
        for camera_num in range(self.camera_nums):
            exec('self.q_readvideo_%s = multiprocessing.Queue()'%camera_num)
            exec('self.q_pic_%s = multiprocessing.Queue()'%camera_num)
            exec('self.start_time_{} = multiprocessing.Queue()'.format(camera_num))
    

    # def sift_match(self,img1_gray,camera_num,dial_num):##sift特征点检测，判断表盘表盘是否被遮挡
    #     img2 = cv2.imread(r'template\%s_%s.jpg'%(camera_num,dial_num))
    #     img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)    
    #     sift= cv2.xfeatures2d.SIFT_create()
    #     kp1,des1 = sift.detectAndCompute(img1_gray, None)
    #     kp2,des2 = sift.detectAndCompute(img2_gray, None)  
    #     # BFmatcher with default parms  
    #     bf = cv2.BFMatcher(cv2.NORM_L2)  
    #     matches = bf.knnMatch(des1, des2, k=2)
    #     ratio = 0.45
    #     mkp1,mkp2 = [],[] 
    #     for m in matches:  
    #         if len(m) == 2 and m[0].distance < m[1].distance * ratio:  
    #             m = m[0]  
    #             mkp1.append( kp1[m.queryIdx] )  
    #     p1 = np.float32([kp.pt for kp in mkp1])
    #     #if len(p1)>
    #     return p1

    # def sift_match2(self, img1_gray, camera_num, dial_num):

    #     global last_images
    #     lstrKey = 'template\%s_%s.jpg'%(camera_num,dial_num)
    #     image_old = None

    #     kernel_size = 5
    #     gauss_gray1 = cv2.GaussianBlur(img1_gray, (kernel_size, kernel_size), 0)

    #     if lstrKey in last_images:
    #         image_old = last_images[lstrKey]
    #     else :
    #         image_old = cv2.imread(r'template\%s_%s.jpg'%(camera_num,dial_num))
    #         image_old = cv2.cvtColor(image_old, cv2.COLOR_BGR2GRAY)

    #         image_old = cv2.GaussianBlur(image_old, (kernel_size, kernel_size), 0)
    #         last_images[lstrKey] = image_old

    #     frameDelta = cv2.absdiff(gauss_gray1, image_old)
    #     thresh = cv2.threshold(frameDelta, 7, 255, cv2.THRESH_BINARY)[1]
    #     thresh = cv2.dilate(thresh, None, iterations=2)

    #     _, contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #     lbMaskFound = 0
    #     for c in contours:
    #         if cv2.contourArea(c) < 200:
    #             continue
    #         lbMaskFound = 1
    #         break

    #     last_images[lstrKey] = gauss_gray1

    #     if(lbMaskFound):
    #         return  0
    #     else:
    #         return  1
    #     return 0

    
    def init(self):###初始化操作
        for camera_num in range(self.camera_nums):
            # cap = cv2.VideoCapture('rtsp://admin:bhxz2017@%s:554/h264/ch1/main/av_stream'%self.ip_address[camera_num])
            # video_path = os.path.join(os.getcwd(), '%s.avi'%camera_num)
            print('hhh')
            cap = cv2.VideoCapture('%s.avi'%camera_num)
            success, frame = cap.read()
            print(frame)
            if success:
                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.resize(frame,(1800,1080))
                if os.path.exists('coordinate.ini'):
                    with open('coordinate.ini','r') as f:
                        lines = len(f.readlines())
                        if (lines == self.camera_nums):
                            pass
                        elif (lines >= self.camera_nums):
                            f.close()
                            os.remove('coordinate.ini')
                            self.get_coordinate(camera_num,frame_gray)
                        else :
                            self.get_coordinate(camera_num,frame_gray)
                else :
                    self.get_coordinate(camera_num,frame_gray)
                xyr = self.read_coordinate(camera_num)
                n = 0
                for i in xyr:
                    cv2.rectangle(frame,((i[0]-i[2]),(i[1]-i[2])),((i[0]+i[2]),(i[1]+i[2])),(0,255,155),5)
                    template_img = cv2.resize(frame[(i[1]-i[2]):(i[1]+i[2]),(i[0]-i[2]):(i[0]+i[2])],(224,224))
                    cv2.imwrite('template/%s_%s.jpg'%(camera_num,n),template_img)
                    logging.info('[%s-%s]保存模板图片'%(camera_num+1,n+1))
                    n += 1
                show_img = cv2.resize(frame, None, fx = 0.3, fy = 0.3)
                cv2.imshow('Detection',show_img)
                cv2.waitKey(0)
                cv2.imwrite('%s.jpg'%camera_num,frame)
            else:
                #print ("[NO.%s] @%s Can't Connect To Camera!"%(camera_num,self.ip_address[camera_num]))
                logging.info("[NO.%s] @%s Can't Connect To Camera!"%(camera_num,self.ip_address[camera_num]))
                time.sleep(20)
                os._exit(0)


    def read_coordinate(self,camera_num):###读取初始化时候检测到的表盘位置坐标
        import re
        xyr = []
        with open('coordinate.ini','r') as f:
            for lines in range(camera_num+1):
                a = f.readline().strip('\n')
            coordinate = list(x for x in re.split(r'[\[\]]',a) if x)
            for i in coordinate:
                xyr.append(list(map(int,i.split(','))))
        logging.info('[%s]读取表盘位置坐标成功'%(camera_num+1))
        return xyr
    

    def get_coordinate(self,camera_num,img):###自动检测圆形表盘区域，初始化调试的时候使用，以后截取的表盘区域固定为在这次初始化检测到的坐标
        from functools import reduce
        circles_xyr = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,2*self.minRadius,param1=50,param2=30,minRadius=self.minRadius,maxRadius=self.maxRadius)
        dial_num = self.dial_num_list[camera_num][0]+self.dial_num_list[camera_num][1]
        xyr = circles_xyr[0][:dial_num]
        xyr = sorted(xyr,key=lambda xyr:xyr[1])
        xyr_0 = xyr[:self.dial_num_list[camera_num][0]]
        xyr_1 = xyr[self.dial_num_list[camera_num][0]:]
        xyr_0 = sorted(xyr_0,key=lambda xyr_0:xyr_0[0])
        xyr_1 = sorted(xyr_1,key=lambda xyr_1:xyr_1[0])
        sorted_xyr = xyr_0 + xyr_1
        means_radius = int(reduce((lambda x,y:x+y),sorted_xyr)[2]/(self.dial_num_list[camera_num][0]+self.dial_num_list[camera_num][1]))
        for i in sorted_xyr:
            i = list(map(int,i))
            i[2] = means_radius
            with open('coordinate.ini','a') as f:
                f.write(str(i))
        with open('coordinate.ini','a') as f:
            f.write('\n')

        
    def readvideo(self,camera_num):##读取摄像头的rtsp数据流
        while True:
            # cap = cv2.VideoCapture('rtsp://admin:bhxz2017@%s:554/h264/ch1/main/av_stream'%self.ip_address[camera_num])
            print('hei')
            cap = cv2.VideoCapture('%s.avi'%camera_num)
            success,frame_video=cap.read()
            logging.info('[%s]已连接至摄像头'%camera_num)
            i = 0
            while success:
                now = datetime.datetime.now().strftime('%Y%m%d %H:%M:%S.%f')
                exec('self.start_time_{}.put(now)'.format(camera_num))
                frame_video = cv2.cvtColor(frame_video, cv2.COLOR_BGR2GRAY)
                frame_video = cv2.resize(frame_video,(1800,1080))
                exec('self.q_readvideo_%s.put(frame_video)'%camera_num)
                success,frame_video = cap.read()
                time.sleep(0.12)
                i += 1
                if i == self.batch_size:
                    i = 0
            logging.error('[%s] Read Video Stream ERROR!!！'%camera_num)
            break

    def dail_pic_to_memory(self,xyr,img,camera_num):####截取单张图片上的表盘部分，并放在队列中等待GPU识别
        n = 0
        for i in xyr:
            i = list(map(int,i))
            new_img = img[(i[1]-i[2]):(i[1]+i[2]),(i[0]-i[2]):(i[0]+i[2])]
            if True:
                new_img = (cv2.resize(new_img,self.pic_size)/255.0).reshape((self.pic_size[0],self.pic_size[0],1))
                exec("self.memory_pic_%s_%s.append(new_img)"%(camera_num,n))
            else:
                exec("self.memory_pic_{0}_{1}.append(self.temp_{0}_{1})".format(camera_num,n))
            n += 1   
        self.itera += 1
        if self.itera == self.batch_size:
            self.itera = 0
            dial_nums = self.dial_num_list[camera_num][0]+self.dial_num_list[camera_num][1]
            for dial_num in range(dial_nums):
                exec("self.q_pic_%s.put(self.memory_pic_%s_%s)"%(camera_num,camera_num,dial_num))
                # time.sleep(0.2)
            self.empty_piclist(camera_num)

            
    def video_image(self,camera_num):
        p_video = multiprocessing.Process(target = self.readvideo,args = (camera_num,))
        p_video.start()
        while eval('self.q_readvideo_%s.empty()'%camera_num):
            time.sleep(0.1)
        exec('self.xyr_%s = self.read_coordinate(camera_num)'%camera_num)
        xyr = eval('self.xyr_%s'%camera_num)
        print ('[%s] 初始化完成!!!'%(camera_num+1))
        logging.info('[%s] 初始化完成!!!'%(camera_num+1))
        i = 0
        while True:

            frame = eval('self.q_readvideo_%s.get()'%camera_num)
            self.dail_pic_to_memory(xyr,frame,camera_num)
            i += 1


    def all_camera(self):###启动多个摄像头同时识别
        for camera_num in range(self.camera_nums):
            multiprocessing.Process(target=self.video_image,args = (camera_num,)).start()
            

    def save_result_db(self,data):

        last_time = data['time'][-1][0][0:8]

        now_time = datetime.datetime.now().strftime("%Y%m%d")


         
        times = data['time']
        data.pop('time')        
        datas = [(times,y,data[y]) for y in data]        
        try:
            for i in range(len(datas)):
                for j in range(len(datas[i][2])):                                       
                    eachData = datas[i][2][j]
                    name = datas[i][1]
                    value = float('%.2f' % (float(eachData) * self.list_map[name][4]))                      
                    time = datas[i][0][j][0]
                    time = time[:4] + '-' + time[4:6] + '-' + time[6:]
                    newName = self.oppositeDic[name]                                           
                    self.allParam['DateTime'] = time
                    self.allParam['StartIndex'] = newName
                    self.allParam['Value'] = value                    
                    self.q_result_socket.put(self.allParam)


        except Exception as e:
            print(e)
        
                
        

    def save_db(self):
        while True:
            all_camera_datas = self.q_result_db.get()
            self.save_result_db(all_camera_datas)

    def send_socket(self):
        
        
        import pika
        import socket
        import json
        ###############生产者队列##################
        # connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
        # channel = connection.channel()
        # channel.queue_declare(queue ='dse_packet')  # 如果队列没有创建，就创建这个队列
        while True:
            datas = self.q_result_socket.get()
            send_data = json.dumps(datas, indent = 1, ensure_ascii = False)
            print(send_data)
            # channel.basic_publish(exchange = '',
            #                       routing_key ='dse_packet',   # 指定队列的关键字为，这里是队列的名字
            #                       body = send_data)  # 往队列里发的消息内容
        # print(" [x] Sent 'Hello World!'")
        connection.close()

    def error_data(self,result_datas):
        n = 0
        for i in result_datas:
            try:
                if abs(result_datas[n+1]-result_datas[n]) > 8:
                    result_datas[n+1] = int(result_datas[n])
            except:
                pass
            n += 1
        return result_datas


    def result_data(self):
        while True:
            all_camera_datas = self.q_result_data.get()
            keys = all_camera_datas.keys()
            # classLen = all_camera_datas['classLen']
            for i in keys:
                if i == 'time':
                    continue
                result_datas = all_camera_datas[i]
                # result_datas = self.error_data(result_datas)
                all_camera_datas[i] = list(result_datas)

            if len(all_camera_datas) > 1:
                self.q_result_db.put(all_camera_datas)
   


    def tensorflow_gpu(self):###调用模型进行识别，GPU识别部分
        from test_googlenet import gnet
        print('gent')
        #from lib.Alexnet import model2
        #model = model2()
        
        p_server = multiprocessing.Process(target= (self.send_socket), args = ())
        p_server.start()
        print('socket')
        #p_server.join()
        
        p_save_db = multiprocessing.Process(target= (self.save_db), args = ())
        p_save_db.start()
        print('db')
        #p_save_db.join()

        p_result_data = multiprocessing.Process(target = (self.result_data),args = ())
        p_result_data.start()
        print('result')
        
        while True:
            for camera_num in range(self.camera_nums):
                all_camera_datas = {}
                qsizes = eval('self.q_pic_%s.qsize()'%camera_num)

                if qsizes == 0:
                    continue
                else:
                    q_pic_size = eval('self.q_readvideo_%s.qsize()'%camera_num)
                    print('[%s] %s组图片待识别,%s张图片待处理'%(camera_num+1, qsizes, q_pic_size))
                    try:
                        times = []
                        for i in range(self.batch_size):
                            time = eval('(self.start_time_%s.get(),3)'%camera_num)
                            # print('时间', time)
                            times.append(time)
                        # print(times)
                        all_camera_datas['time'] = times
                    except Exception as e:
                        print(e)
                        # pass
                for dial_num in range(self.dial_num_list[camera_num][0] + self.dial_num_list[camera_num][1]):
                    try:
                        # value = eval('self.q_pic_%s.get(True, 0.5)'%(camera_num))
                        value = eval('self.q_pic_%s.get(True, 0.5)'%(camera_num))
                        # print('第一个输入值为:', (value)[0])
                    except:
                        logging.info('[%s-%s] 无数据....'%(camera_num+1,dail_num+1))
                        continue
                    
                    # print(value)
                    result_datas = list(gnet.predict_label(value))

                    result_datas = list(map(str, result_datas))

                    # 根据置信度判断是否被遮挡
                    credibilityDis = list(gnet.predict_label2(value))      
                    newResult = []
                    name = '%s-%s'%(camera_num, dial_num)
                    # classLen = self.list_map[name]
                    for i in range(self.batch_size):
                        upLimit = max(credibilityDis[i])
                        average = 1/(len(credibilityDis[i]))
                        if upLimit > (2 * average):
                            newResult.append(result_datas[i])                
                    # result_datas = model.use_model(value, camera_num, dial_num)
                    all_camera_datas[name] = newResult
                    # all_camera_datas['classLen'] = classLen
                self.q_result_data.put(all_camera_datas)


       
if __name__ == '__main__':
    start = Main()
    if start.Initialization:
        start.init()
    p_pic = multiprocessing.Process(target=start.tensorflow_gpu)
    p_pic.start()
    start.all_camera()









    
