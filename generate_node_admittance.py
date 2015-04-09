#!/usr/bin/env python3
# coding=utf-8
import csv
import time
start = time.clock()
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
            y_bus[to_port, from_port
            ] = y_bus[from_port, to_port] = -Y / b_or_k
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
v = [0,0,1.21]
#电压初值
n = y_bus_size-1
pv_point=2
m = pv_point
calc_times=1
def unfinished():
    global DELTA_P,DELTA_Q,DELTA_V
    DELTA_P=p.copy()
    DELTA_Q=q.copy()
    DELTA_V=v.copy()
    for i in range(m):
        for j in range(y_bus_size):
            gmb = y_bus[i,j].real * e[j] - y_bus[i,j].imag * f[j]
            gpb = y_bus[i,j].real * f[j] + y_bus[i,j].imag * e[j]
            #以上分别代表 Gij-Bij 和 Gij + Bij(电力系统分析下册 P58 11-46,11-47)
            DELTA_P[i]+= - e[i] * gmb - f[i] * gpb
            DELTA_Q[i]+= - f[i] * gmb + e[i] * gpb
    for i in range(m,n):
        for j in range(y_bus_size):
            gmb = y_bus[i,j].real * e[j] - y_bus[i,j].imag * f[j]
            gpb = y_bus[i,j].real * f[j] + y_bus[i,j].imag * e[j]
            #以上分别代表 Gij-Bij 和 Gij + Bij(电力系统分析下册 P58 11-46,11-47)
            DELTA_P[i]+= - e[i] * gmb - f[i] * gpb
        DELTA_V[i]+= - e[i] * e[i] - f[i] * f[i]
    max_delta = max(DELTA_P+DELTA_Q+DELTA_V,key=abs)
    print ('最大不平衡量',max_delta)
    if calc_times==1:
        return 1
    if calc_times > 100:
        return 0
    elif abs(max_delta) < 0.000001:
        return 0
    else :
        return 1

def swap_rows(arr, frm, to):
    arr[[frm, to],:] = arr[[to, frm],:]

def swap_cols(arr, frm, to):
    arr[:,[frm, to]] = arr[:,[to, frm]]

while(unfinished()):
    print('这是第',calc_times,'次迭代')
    calc_times+=1
    jacobi_array = zeros((2*n, 2*n), float)
    for i in range(m):
        #以下形成非对角元
        for j in range(n):
            jacobi_array[2*i, 2*j
            ]= - y_bus[i,j].real * e[i] - y_bus[i,j].imag *f[i]
            jacobi_array[2*i, 2*j+1 
            ] = - y_bus[i,j].real * f[i] + y_bus[i,j].imag*e[i]
            jacobi_array[2*i+1,2*j] =  jacobi_array[2*i, 2*j+1 ]
            jacobi_array[2*i+1,2*j+1] = - jacobi_array[2*i,2*j]
        #以下形成对角元
        sigma_gmb=0
        sigma_gpb=0
        for k in range(y_bus_size):
            sigma_gmb += y_bus[i,k].real * e[k] - y_bus[i,k].imag * f[k]
            sigma_gpb += y_bus[i,k].real * f[k] + y_bus[i,k].imag * e[k]
        jacobi_array[2*i,2*i] += - sigma_gmb
        jacobi_array[2*i,2*i+1] += - sigma_gpb
        jacobi_array[2*i+1,2*i] += sigma_gpb
        jacobi_array[2*i+1,2*i+1] += -sigma_gmb
    for i in range (m,n):
        #以下形成非对角元
        for j in range(n):
            jacobi_array[2*i, 2*j
            ] = - y_bus[i,j].real * e[i] - y_bus[i,j].imag *f[i]
            jacobi_array[2*i, 2*j+1 
            ] = - y_bus[i,j].real * f[i] + y_bus[i,j].imag*e[i]
        jacobi_array[2*i+1,2*i]= - 2*e[i]
        jacobi_array[2*i+1,2*i+1]= -2*f[i]
        #以下形成对角元
        sigma_gmb=0
        sigma_gpb=0
        for k in range(y_bus_size):
            sigma_gmb += y_bus[i,k].real * e[k] - y_bus[i,k].imag * f[k]
            sigma_gpb += y_bus[i,k].real * f[k] + y_bus[i,k].imag * e[k]
        jacobi_array[2*i,2*i] += - sigma_gmb
        jacobi_array[2*i,2*i+1] += - sigma_gpb
        
        
    print('形成雅各比矩阵如下',"\n",jacobi_array)
    #先调整矩阵使最大值在对角线上,并加负号
    for i in range(n):
        swap_rows(jacobi_array,2*i,2*i+1)
    jacobi_array = -jacobi_array 
    #以下解方程
    
    #下三角消元
    
    jacobi_array_size=2*n
    delta_v = [0]*jacobi_array_size
    delta_w = [0]*jacobi_array_size
    for i in range(m):
        delta_w[2*i] = DELTA_Q[i]
        delta_w[2*i+1] = DELTA_P[i]
    for i in range(m,n):
        delta_w[2*i] = DELTA_V[i]
        delta_w[2*i+1] = DELTA_P[i]
    for k in range(jacobi_array_size-1):
        one_over_kk=1/jacobi_array[k,k]
        for i in range(k+1,jacobi_array_size):
            for j in range(k+1,jacobi_array_size):
                jacobi_array[i,j]-= jacobi_array[i,k] * jacobi_array[k,j]*one_over_kk
            delta_w[i] -= jacobi_array[i,k] * delta_w[k] * one_over_kk
            jacobi_array[i,k]=0
    print(jacobi_array,"\n",delta_w)
    
    #解方程  jacobi_array *delta_v = delta_w
    #回代
    for i in range(jacobi_array_size-1,-1,-1):
        delta_v[i] = delta_w[i]
        for j in range(i+1,jacobi_array_size):
            delta_v[i] -= jacobi_array[i,j] * delta_v[j]
        delta_v[i] = delta_v[i]/jacobi_array[i,i]
        
    print(delta_v)
    
    #修正
    for i in range(n):
        e[i] += delta_v[2*i]
        f[i] += delta_v[2*i+1]
print(e,f)
print ('耗时',time.clock()-start)
    

