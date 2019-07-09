import cv2
import time
import os
import sys
import pymysql
import logging
import numpy as np
import datetime
import multiprocessing
from multiprocessing import Process,Queue,Pool
from lib.init import Universal_value
import matplotlib.pyplot as plt

class Main(Universal_value):
    def __init__(self, camera_num, dial_num , frame_num1, frame_num2):
        Universal_value.__init__(self)

        self.camera_num = camera_num
        self.dial_num = dial_num
        self.frame_num1 = frame_num1
        self.frame_num2 = frame_num2
        self.q = Queue()
        self.plot = multiprocessing.Process(target= (self.plotConfidence), args = (self.q, ))

        # print(self.list_map['0-4'])

    def readImage(self):
        result = []
        # for i in range(self.frame_num1, self.frame_num2+1):
        imagePath = 'video/%s/%s/%s.jpg' % (self.camera_num, self.dial_num, i)
        # imagePath = '6.jpg'
        # print(imagePath)
        try:
            image = cv2.imread(imagePath)
            # print(i)
            # print(image.shape)
            # cv2.imwrite('confidenceLevelTest/%s_%s_%s.jpg'%(self.camera_num, self.dial_num, i),image)
            # exit()
            newImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # print(newImage)
            # print(newImage.shape)
            newImage1 = (cv2.resize(newImage, (30,30))/255.0)
            newImage2 = (cv2.resize(newImage, (164,164))/255.0).reshape(164, 164, 1)

            print(newImage1)
            result.append(newImage2)
    
        except Exception as e:
            print(e)
        return result

    def error_data(self, result_datas):
        n = 0
        for i in result_datas:
            try:
                if abs(result_datas[n+1]-result_datas[n]) > 30:
                    result_datas[n+1] = int(result_datas[n])
            except:
                pass
            n += 1
        return result_datas


    def prediction(self):
        inputValue = self.readImage()
        from test_googlenet import gnet
        result = list(gnet.predict_label(inputValue))
        a = self.list_map['%s-%s' % (self.camera_num, self.dial_num)][4]
        result = list(map(lambda result : float('%.2f'%(float(result) * a)), result))
        # resultFilter = self.error_data
        # print('结果为:', result)
        credibilityDis = list(gnet.predict_label2(inputValue))          
        self.q.put(credibilityDis)
        self.plot.start()
        # print('置信度分布为:', credibilityDis)
        maxCredibilityDis = list(map(max, credibilityDis))
        # print('置信度为', maxCredibilityDis)
        # result2 = list(map(str, result))
        # dic = {}
        for i in range(len(result)):
            print('结果为:', result[i],',')
            print('对应的置信度为:', maxCredibilityDis[i])

        # for i in range(len(result2)):
        #     dic['%s-%s'%(result2[i], i)] = maxCredibilityDis[i]
        # print('识别结果及相应的置信度为:', dic)
        return credibilityDis

    def plotConfidence(self, q):
        credibilityDis = self.q.get(True)
        for i in range(len(credibilityDis)):
            plt.ylim(0,max(credibilityDis[i]) + 0.002) 
            plt.plot(credibilityDis[i])
            plt.savefig('confidenceLevelTest/confidenceLevelTest_%s_%s_%s' % (self.camera_num, self.dial_num, i + self.frame_num1))  
            plt.cla()
        # print(credibilityDis)

if __name__ == '__main__':
    # a = 1/120
    # print(a)
    # exit()
    camera_num = 0
    dial_num = 4
    frame_num1 = 1476
    frame_num2 = 1520
    main = Main(camera_num, dial_num, frame_num1, frame_num2)
    main.prediction()
    # main.readImage()

