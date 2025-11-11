import numpy as np


# 碱基配对
def match(a, b):
    score = 0

    if (a == 'A' or a == 'a'):
        if (b == 'A' or b == 'a'):
            score = 1
    if (a == 'A' or a == 'a'):
        if (b == 'C' or b == 'C'):
            score = 2
    if (a == 'A' or a == 'a'):
        if (b == 'G' or b == 'g'):
            score = 3
    if (a == 'A' or a == 'a'):
        if (b == 'U' or b == 'u'):
            score = 4
    if (a == 'C' or a == 'c'):
        if (b == 'A' or b == 'a'):
            score = 5
    if (a == 'C' or a == 'c'):
        if (b == 'C' or b == 'c'):
            score = 6
    if (a == 'C' or a == 'c'):
        if (b == 'G' or b == 'g'):
            score = 7
    if (a == 'C' or a == 'c'):
        if (b == 'U' or b == 'u'):
            score = 8
    if (a == 'G' or a == 'g'):
        if (b == 'A' or b == 'a'):
            score = 9
    if (a == 'G' or a == 'g'):
        if (b == 'C' or b == 'c'):
            score = 10
    if (a == 'G' or a == 'g'):
        if (b == 'G' or b == 'g'):
            score = 11
    if (a == 'G' or a == 'g'):
        if (b == 'U' or b == 'u'):
            score = 12
    if (a == 'U' or a == 'u'):
        if (b == 'A' or b == 'a'):
            score = 13
    if (a == 'U' or a == 'u'):
        if (b == 'C' or b == 'c'):
            score = 14
    if (a == 'U' or a == 'u'):
        if (b == 'G' or b == 'g'):
            score = 15
    if (a == 'U' or a == 'u'):
        if (b == 'U' or b == 'u'):
            score = 16

    return score


# 构建配对矩阵
def stem1(s):
    stem = np.zeros((len(s), len(s)))
    for i in range(0, len(s)):
        for j in range(0, len(s)):
            stem[i][j] = match(s[i], s[j])
    return stem


# 碱基对与理化性质相对应
def f_dimer(stem, s):
    stem1 = stem
    stem2 = stem1.copy()
    stem3 = stem1.copy()
    stem4 = stem1.copy()
    stem5 = stem1.copy()
    stem6 = stem1.copy()
    stem7 = stem1.copy()
    stem8 = stem1.copy()
    stem9 = stem1.copy()
    stem10 = stem1.copy()
    stem_all = []
    s = s
    dimer = np.array(
        [[-0.83, -0.14, 0.55, -0.14, -1.87, 0.78, 0.55, 0.55, 1.47, 0.37, 0.78, -0.14, 0.09, 1.47, -1.87, -0.83],
         [-0.67, -1.64, 0, -0.62, 0.62, 0.09, 1.6, 0, 0.4, -1.07, 1.6, -1.64, 0.98, 0.4, 0.62, -0.67],
         [-1.13, 1.5, -0.79, -0.96, 0.48, -0.53, 2.09, -0.79, 0.14, 0.14, -0.53, 1.5, -0.62, 0.14, 0.48, -1.13],
         [1.34, 0.49, 0.12, 0.87, 0.33, -1.36, -1.95, 0.12, -0.94, 0.71, -1.36, 0.49, 0.39, -0.94, 0.33, 1.34],
         [-1.84, 0.54, 0.09, 0.98, 0.83, -0.2, -0.8, 0.09, 1.28, -0.65, -0.2, 0.54, -0.95, 1.28, 0.83, -1.84],
         [-0.26, 0.34, -0.86, 0.93, -0.26, 0.34, -2.65, -0.86, 0.34, 2.13, 0.34, 0.34, 0.34, 0.34, -0.26, -0.26],
         [1.72, -0.27, 0.13, 0.61, 0.15, -1.13, 0.06, 0.13, -0.72, -1.77, -1.13, -0.27, 1.34, -0.72, 0.15, 1.72],
         [0.95, -0.31, 0.82, 1.42, -0.57, -0.88, 0.79, 0.82, -1.82, -1.72, -0.88, -0.31, 0.27, -0.31, 0.82, 0.95],
         [0.29, 0.23, 0.1, -0.83, -0.17, 2.02, -0.97, 0.1, -0.04, -1.83, 2.02, 0.23, -1.23, -0.04, -0.17, 0.29],
         [1.35, -0.26, 0.28, 1.35, 0.14, -1.34, -0.13, 0.28, -0.53, -2.01, -1.34, -0.26, 1.08, -0.26, 0.28, 1.35]])

    dimer = dimer + 10

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num1 = int(stem1[i][j])
            if stem1[i][j] == 0:
                continue
            else:
                stem1[i][j] = dimer[0][num1 - 1]
    if(len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem1[i][j]
        stem1 = b
    stem_all.append(stem1)
    print(stem1)
    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num2 = int(stem2[i][j])
            if stem2[i][j] == 0:
                continue
            else:
                stem2[i][j] = dimer[1][num2 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem2[i][j]
        stem2 = b
    stem_all.append(stem2)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num3 = int(stem3[i][j])
            if stem3[i][j] == 0:
                continue
            else:
                stem3[i][j] = dimer[2][num3 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem3[i][j]
        stem3 = b
    stem_all.append(stem3)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num4 = int(stem4[i][j])
            if stem4[i][j] == 0:
                continue
            else:
                stem4[i][j] = dimer[3][num4 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem4[i][j]
        stem4 = b
    stem_all.append(stem4)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num5 = int(stem5[i][j])
            if stem5[i][j] == 0:
                continue
            else:
                stem5[i][j] = dimer[4][num5 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem5[i][j]
        stem5 = b
    stem_all.append(stem5)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num6 = int(stem6[i][j])
            if stem6[i][j] == 0:
                continue
            else:
                stem6[i][j] = dimer[5][num6 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem6[i][j]
        stem6 = b
    stem_all.append(stem6)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num7 = int(stem7[i][j])
            if stem7[i][j] == 0:
                continue
            else:
                stem7[i][j] = dimer[6][num7 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem7[i][j]
        stem7 = b
    stem_all.append(stem7)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num8 = int(stem8[i][j])
            if stem8[i][j] == 0:
                continue
            else:
                stem8[i][j] = dimer[7][num8 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem8[i][j]
        stem8 = b
    stem_all.append(stem8)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num9 = int(stem9[i][j])
            if stem9[i][j] == 0:
                continue
            else:
                stem9[i][j] = dimer[8][num9 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem9[i][j]
        stem9 = b
    stem_all.append(stem9)

    for i in range(0, len(s)):
        for j in range(0, len(s)):
            num10 = int(stem10[i][j])
            if stem10[i][j] == 0:
                continue
            else:
                stem10[i][j] = dimer[9][num10 - 1]
    if (len(s) < 32):
        b = np.zeros((32, 32))
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                b[i][j] = stem10[i][j]
        stem10 = b
    stem_all.append(stem10)

    return stem_all


# 记录二级结构配对碱基的坐标
def f_rna(target):
    target = list(target)
    local = []
    for i in range(0, len(target)):
        if target[i] == ")":
            for j in range(i - 1, -1, -1):
                if target[j] == "(":
                    local.append([i, j])
                    target[i] = "."
                    target[j] = "."
                    break
    return local


# 二级结构转换成矩阵并与理化性质相对应
def rna_str(local, s):
    local = local
    s = list(s)
    stem = np.zeros((len(s), len(s)))
    for i in range(0, len(local)):
        a, b = local[i]
        sorce = match(s[a], s[b])
        stem[a][b] = sorce
    stem_dimer = f_dimer(stem, s)
    return stem_dimer


# 将点括号转换成0、1
def target(s):
    a = f_rna(s)
    b = (np.ones([len(s), len(s)])/100) * 99
    for i in a:
        b[i[0], i[1]] = 0.01
        b[i[1], i[0]] = 0.01
    return b

