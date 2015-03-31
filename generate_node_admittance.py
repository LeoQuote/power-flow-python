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
'''
y_busRealImag=zeros((y_bus_size,y_bus_size*2),float)
for i in range(y_bus_size):
    for j in range(y_bus_size):
        y_busRealImag[i,j*2]=y_bus[i,j].real
        y_busRealImag[i,j*2+1]=y_bus[i,j].imag
'''
e = [1, 1, 1.1, 1.05]
f = [0, 0, 0, 0]
#电压初值
n = y_bus_size-1
pv_point=2
m = pv_point
jacobi_array = zeros((n, n), float)
while(unfinished()):
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
outputToFile(y_bus, 'y_bus.csv')
facter_table=y_bus.copy()
# 下三角消元
for k in range(y_bus_size - 1):
    oneOverkk=1 / facter_table[k, k]
    for i in range(k + 1, y_bus_size):
        for j in range(k + 1, y_bus_size):
            facter_table[i,
    j] -= facter_table[i,
    k] * facter_table[k,
     j] * oneOverkk
        facter_table[i, k]=0
    # print(facter_table)

print(facter_table)
# 对角元规格化
for i in range(y_bus_size):
    # 倒数存放对角元
    facter_table[i, i]=1 / facter_table[i, i]
    for j in range(i + 1, y_bus_size):
        # 规格化其他元素
        facter_table[i, j] *= facter_table[i, i]
# print a
outputToFile(facter_table, 'facter_table.csv')
# 初始化Z阵和f阵, 详见电力系统分析上册 90页
z_bus=zeros((y_bus_size, y_bus_size), complex)
for j in range(y_bus_size - 1, -1, -1):
    f=[]
    f += [0] * j
    h=f.copy()
    f += [1]
    for i in range(j + 1, y_bus_size):
        f += [0]
        for k in range(j, i):
            # print(j,i,k)
            # 临时变量temp,存储l f 的乘积
            f[i] -= facter_table[k, i] * f[k]
    # print(f)
    for i in range(j, y_bus_size):
        h += [f[i] * facter_table[i, i]]
    # print(h)
    # print(f,j)
    for i in range(y_bus_size - 1, -1, -1):
        z_bus[i, j]=h[i]
        # print(i,j)
        for k in range(i + 1, y_bus_size):
            # print('in!')
            z_bus[i, j] -= facter_table[i, k] * z_bus[k, j]
outputToFile(z_bus, 'z_bus.csv')
'''
file_object = open('data.csv')
try:
    all_the_text = file_object.read(  )
finally:
    file_object.close(  )
'''
