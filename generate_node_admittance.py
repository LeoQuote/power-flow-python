#!/usr/bin/env python3
# coding=utf-8
import csv
from numpy import *
#第一次打开文件,统计最大的节点数
with open('data.csv',newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    arraySize=4
    for row in spamreader:
        a=list(row)
        print(int(a[1]))
        if int(a[0])>arraySize:
            arraySize=int(a[0])
        if int(a[1])>arraySize:
            arraySize=int(a[1])
    print('最大值为',arraySize)
#第二次打开文件,形成导纳矩阵
with open('data.csv',newline='') as csvfile:
    spamreader = csv.reader(csvfile)
    Ybus=zeros((arraySize,arraySize),complex)
    for row in spamreader:
        #print('in!')
        a=list(row)
        #print(int(a[1]))
        fromport=int(a[0])-1
        #print('来源',fromport)
        toport=int(a[1])-1
        Z=complex(float(a[2]),float(a[3]))
        BOrK=float(a[4])
        Y=1/Z
        if BOrK>0.85 :
            #如果大于0.85,认为是变压器,做相关变换
            #print(Z)
            #print(Y)
            Ybus[fromport,toport]+=Y
            Ybus[toport,toport]+=Y/(BOrK*BOrK)
            Ybus[toport,fromport]=Ybus[fromport,toport]=-Y/BOrK
        else:
            BOrK=complex(0,BOrK)
            Ybus[fromport,fromport]+=Y+BOrK
            Ybus[toport,toport]+=Y+BOrK
            Ybus[fromport,toport]=Ybus[toport,fromport]=-Y
with open('Ybus.csv','w',newline='') as YbusFile:
    writer=csv.writer(YbusFile)
    writer.writerows(Ybus)
print(Ybus)
#print a
'''
file_object = open('data.csv')
try:
    all_the_text = file_object.read(  )
finally:
    file_object.close(  )
'''
