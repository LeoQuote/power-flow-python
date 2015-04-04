#!/usr/bin/env python3
# coding=utf-8
import csv
from numpy import *
# 第一次打开文件,统计最大的节点数
with open('data.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    y_bus_size = 4
    for row in spamreader:
        if int(row['to_port']) > y_bus_size:
            y_bus_size = int(row['to_port'])
        if int(row['from_port']) > y_bus_size:
            y_bus_size = int(row['from_port'])
    print('最大值为', y_bus_size)
# 第二次打开文件,形成导纳矩阵
with open('data.csv', newline='') as csvfile:
    spamreader = csv.DictReader(csvfile)
    y_bus = zeros((y_bus_size, y_bus_size), complex)
    for row in spamreader:
        # print('in!')
        # print(int(a[1]))
        from_port = int(row['from_port']) - 1
        # print('来源',from_port)
        to_port = int(row['to_port']) - 1
        Z = complex(float(row['R']), float(row['X']))
        b_or_k = float(row['b_or_k'])
        Y = 1 / Z
        if b_or_k > 0.85:
            # 如果大于0.85,认为是变压器,做相关变换
            # print(Z)
            # print(Y)
            y_bus[from_port, from_port] += Y
            y_bus[to_port, to_port] += Y / (b_or_k * b_or_k)
            y_bus[to_port, from_port] = y_bus[from_port, to_port] = -Y / b_or_k
        else:
            b_or_k = complex(0, b_or_k)
            y_bus[from_port, from_port] += Y + b_or_k
            y_bus[to_port, to_port] += Y + b_or_k
            y_bus[from_port, to_port] = y_bus[to_port, from_port] = -Y
# 定义个输出数组到csv文件的函数,以后会用到好多次


def outputToFile(array, fileName):
    with open(fileName, 'w', newline='') as outputFile:
        writer = csv.writer(outputFile)
        writer.writerows(array)
print(y_bus)
e = [1, 1, 1.1, 1.05]
f = [0, 0, 0, 0]
p = [-0.3,-0.55,0.5]
q = [-0.18,-0.13,0]
v = [0,0,1.1]
#电压初值
n = y_bus_size-1
pv_point=2
m = pv_point
jacobi_array = zeros((2*n, 2*n), float)
calc_times=1
global DELTA_P,DELTA_Q,DELTA_V
def unfinished():
    for i in range(m):
        DELTA_P[i]+=p[i]
        for j in range(y_bus_size):
            DELTA_P[i]+= -e[i]*(y_bus[i,j].real*e[j]-y_bus[i,j].imag*f[j]) - f[i](y_bus[i,j].real*f[j]+y_bus[i,j].imag*e[j])
            
    if calc_times==1:
        return 1
    elif calc_times>100:
        return 0
    else :
        return 1

while(unfinished()):
    print('这是第',calc_times,'次迭代')
    calc_times+=1
    for i in range(m):
        for j in range(n):
            jacobi_array[2*i, 2*j]= - y_bus[i,j].real * e[i] - y_bus[i,j].imag *f[i]
            jacobi_array[2*i, 2*j+1 ] = - y_bus[i,j].real * f[i] + y_bus[i,j].imag*e[i]
            jacobi_array[2*i+1,2*j] =  jacobi_array[2*i, 2*j+1 ]
            jacobi_array[2*i+1,2*j+1] = jacobi_array[2*i,2*j]
        injection_current= 1+2j
        jacobi_array[2*i,2*i]+= injection_current.imag
        jacobi_array[2*i,2*i+1]+=injection_current.real
        jacobi_array[2*i+1,2*i]+=injection_current.real
        jacobi_array[2*i+1,2*i+1]+= -injection_current.imag
    for i in range (m,n):
        for j in range(n):
            jacobi_array[2*i, 2*j]= - y_bus[i,j].real * e[i] - y_bus[i,j].imag *f[i]
            jacobi_array[2*i, 2*j+1 ] = - y_bus[i,j].real * f[i] + y_bus[i,j].imag*e[i]
        injection_current= 1+2j
        jacobi_array[2*i,2*i]+= injection_current.imag
        jacobi_array[2*i,2*i+1]+=injection_current.real
        jacobi_array[2*i+1,2*i]= - 2*e[i]
        jacobi_array[2*i+1,2*i+1]= -2*f[i]
    print('形成雅各比矩阵如下',"\n",jacobi_array)
    #solving the matrix
    
