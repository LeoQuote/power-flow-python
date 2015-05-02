# power-flow-python[![Build Status](https://travis-ci.org/LeoQuote/power-flow-python.svg?branch=master)](https://travis-ci.org/LeoQuote/power-flow-python)
用python写的矩阵消去和潮流计算程序

###运行环境
* Ubuntu 12.04
* Python 3.4.0
* Numpy 1.8.0
* Scipy 0.13.3-1 

###程序设计
1. 读取csv文件里的节点参数生成节点导纳矩阵
2. 做三角分解,得到单位上三角矩阵U和对角线矩阵D,两矩阵可以储存在一个因子矩阵内,节省空间
3. 用线性方程的直接解法对节点导纳矩阵求逆,得到节点阻抗矩阵

###To-do
1. 稀疏矩阵的引入.
2. 实际的潮流计算.
