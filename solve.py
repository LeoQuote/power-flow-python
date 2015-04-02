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
