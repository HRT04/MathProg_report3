import numpy as np
import pandas as pd
# [a1, a2, ... , an, 定数]
inpt_sub1 = np.array([[1, -1, 2, 8], [2, -3, -1, 1]])
inpt_sub2 = np.array([[1, 2, 14], [1, 1, 8], [3, 1, 18]])
inpt_sub3 = np.array([[1, -1, 1], [-2, 1, 2], [1, -2, 1]])
inpt_z1= np.array([-1, -1, -1, 0])
inpt_z2 = np.array([-2, -1, 0])
inpt_z3 = np.array([-1, -1, 0])

# 引数: p...制約条件のx1, x2, ... ,xnの係数, 目的関数のxnの係数 
def simplex(p, z):
    # データ用意
    ps = p.shape
    col = []
    ind = []
    data = np.vstack([p, z])
    zero_c = np.zeros(p.shape[1])
    zero_i = np.zeros(p.shape[0])
    for i1 in range(1, ps[0]+ps[1]):   # column, index 作成
        if i1 < ps[1]:
            col.append("x" + str(i1))
        else:
            ind.append("x" + str(i1))
    col.append("constant")
    ind.append("Z")
    # DataFrame作成
    df = pd.DataFrame(data, columns=col, index=ind)
    print(df)
    print()
    z_zero = False
    z_mi = False
    
    # 停止条件1
    while not np.all(df.loc["Z"].to_list() >= zero_c):
        min_column = df.loc["Z"].idxmin()
        # Z行内での最小の値の列データ
        min_colval = df[min_column][:-1]
        num = df["constant"][:-1]
        # PE
        for ii, i2 in enumerate((num/min_colval).to_list()):
            if i2 > 0:
                if ii == 0:
                    hirei_min = i2
                    hirei_ind = ii
                elif i2 < hirei_min:
                    hirei_min = i2
                    hirei_ind = ii
        
        old_df = df[min_column].copy()
        
        # PE演算
        pe = df[min_column][hirei_ind]
        df.iloc[[hirei_ind]] = df.iloc[[hirei_ind]]/pe
        x_pe = df.iloc[[hirei_ind]].copy()
        for i3 in range(df.shape[0]):
            if i3 == hirei_ind:
                continue
            else:     
                df.iloc[i3] = df.iloc[i3] - x_pe * old_df[i3]
        
        # 列名、行名交換
        new_index = df.index.tolist()
        new_columns = df.columns.tolist()

        new_index[hirei_ind] = min_colval.name
        new_columns[df.columns.get_loc(min_column)] = df.index[hirei_ind]
        df.index = new_index
        df.columns = new_columns

        min_column = df.loc["Z"].idxmin()
        # Z行内での最小の値の列データ
        min_colval = df[min_column][:-1]
        z_zero = np.all(min_colval.to_list() == zero_i)
        z_mi = np.all(min_colval.to_list() < zero_i)
        
        print(df)
        print()
        # 停止条件2
        if (z_zero):
            print("選ばれた列の値が全て0なので、最適解は存在しない")
            exit()
        elif (z_mi):
            print("選ばれた列の値が全て負の値なので、最適解は存在しない")
            exit()
    for i4 in range(df.shape[0]):
        if i4 == df.shape[0] - 1:
            print("の時\n{0} = {1}\n".format(df.index.to_list()[i4], df["constant"][i4]))
        else:
            print("{0} = {1}".format(df.index.to_list()[i4], df["constant"][i4]))

# 結果表示
print("練習課題1")
simplex(inpt_sub1, inpt_z1)
print("練習課題2")
simplex(inpt_sub2, inpt_z2)
print("練習課題3")
simplex(inpt_sub3, inpt_z3)

