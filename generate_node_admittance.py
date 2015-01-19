#!/usr/bin/env python3
# coding=utf-8
import csv
from numpy import *
#第一次打开文件,统计最大的节点数
with open('data.csv',newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    arraySize=4
    for row in spamreader:
        if int(row['toport'])>arraySize:
            arraySize=int(row['toport'])
        if int(row['fromport'])>arraySize:
            arraySize=int(row['fromport'])
    print('最大值为',arraySize)
#第二次打开文件,形成导纳矩阵
with open('data.csv',newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    Ybus=zeros((arraySize,arraySize),complex)
    for row in spamreader:
        #print('in!')
        #print(int(a[1]))
        fromport=int(row['fromport'])-1
        #print('来源',fromport)
        toport=int(row['toport'])-1
        Z=complex(float(row['R']),float(row['X']))
        BOrK=float(row['BOrK'])
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
def outputToFile(array,fileName):
    with open(fileName,'w',newline='') as outputFile:
        writer=csv.writer(outputFile)
        writer.writerows(array)
outputToFile(Ybus,'Ybus.csv')
facterTable=Ybus.copy()
#下三角消元
for k in range(arraySize-1):
    oneOverkk=1/facterTable[k,k]
    for i in range(k+1,arraySize):
        for j in range(k+1,arraySize):
            facterTable[i,j]-=facterTable[i,k]*facterTable[k,j]*oneOverkk
        facterTable[i,k]=0
    print(facterTable)

print(facterTable)
#对角元规格化
for i in range(arraySize):
    #倒数存放对角元
    facterTable[i,i]=1/facterTable[i,i]
    for j in range(i+1,arraySize):
        #规格化其他元素
        facterTable[i,j]*=facterTable[i,i]
#print a
outputToFile(facterTable,'facterTable.csv')

'''
file_object = open('data.csv')
try:
    all_the_text = file_object.read(  )
finally:
    file_object.close(  )
'''
