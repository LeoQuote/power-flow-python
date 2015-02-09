#!/usr/bin/env python3
# coding=utf-8
import csv
#from numpy import *
from scipy import sparse
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
    Ybus=sparse.lil_matrix((arraySize,arraySize),dtype=complex)
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
            Ybus[fromport,fromport]+=Y
            Ybus[toport,toport]+=Y/(BOrK*BOrK)
            Ybus[toport,fromport]=Ybus[fromport,toport]=-Y/BOrK
        else:
            BOrK=complex(0,BOrK)
            Ybus[fromport,fromport]+=Y+BOrK
            Ybus[toport,toport]+=Y+BOrK
            Ybus[fromport,toport]=Ybus[toport,fromport]=-Y
#定义个输出数组到csv文件的函数,以后会用到好多次
def outputToFile(array,fileName):
    with open(fileName,'w',newline='') as outputFile:
        writer=csv.writer(outputFile)
        writer.writerows(array)
outputToFile(Ybus.toarray(),'Ybus.csv')
print(Ybus.toarray())
facterTable=sparse.triu(Ybus)
facterTable=sparse.lil_matrix(facterTable)
print(facterTable)
#对角元规格化
for i in range(arraySize):
    #倒数存放对角元
    facterTable[i,i]=1/facterTable[i,i]
    for j in range(i+1,arraySize):
        #规格化其他元素
        facterTable[i,j]*=facterTable[i,i]
#print a
outputToFile(facterTable.toarray(),'facterTable.csv')
'''
#初始化Z阵和f阵, 详见电力系统分析上册 90页
Zbus=zeros((arraySize,arraySize),complex)
for j in range(arraySize-1,-1,-1):
    f=[]
    f+=[0]*j
    h=f.copy()
    f+=[1]
    for i in range(j+1,arraySize):
        f+=[0]
        for k in range(j,i):
            #print(j,i,k)
            #临时变量temp,存储l f 的乘积
            f[i]-=facterTable[k,i]*f[k]
    #print(f)
    for i in range(j,arraySize):
        h+=[f[i]*facterTable[i,i]]
    #print(h)
    #print(f,j)
    for i in range(arraySize-1,-1,-1):
        Zbus[i,j]=h[i]
        #print(i,j)
        for k in range(i+1,arraySize):
            #print('in!')
            Zbus[i,j]-=facterTable[i,k]*Zbus[k,j]
outputToFile(Zbus,'Zbus.csv')
'''
'''
file_object = open('data.csv')
try:
    all_the_text = file_object.read(  )
finally:
    file_object.close(  )
'''
