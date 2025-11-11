import random
from test1 import out
from collections import Counter
# 求解出自由能
def lowerpower(ss, Structures):
    RNA = ss
    str1 = ss
    structures1 = Structures
    str3 = list(structures1)
    structures = list(structures1)
    # 设置第二个列表的目的是为了针对((((....XXXXXXX......XXXXXX...."))))".....XXXXX，引号部分的处理
    structures2 = list(structures1)
    # 每一个数组的第一个位置是发夹环的茎环结构中的茎区中的碱基对数目(a)
    a = 0
    a1 = 0
    # 每一个数组的第二个位置是发夹环的环区左侧第一个‘（’位置(b)
    b = 0
    # 每一个数组的第三个位置是发夹环的环区右侧第一个‘）’位置(c)
    c = 0
    # 每一个数组的第四个位置是发夹环的环区未配对的碱基数目(d)
    d = 0
    # 每一个数组的第五个位置是发夹环的茎环结构的起始位置(e)
    e = 0
    # 每一个数组的第六个位置是发夹环的茎环结构的终止位置(f)
    f = 0
    l = 0
    all = []
    # 先将Q，X，D在序列中进行标记
    for i in range(0, len(structures)):
        # 先找到序列中的第一个")"
        if (structures[i] == ')' and structures2[i] != 'Y'):
            # 标记好这个位置
            c = i
            r = 0
            # 对于标记的第一个")"，在这个位置向左开始遍历，用来统计发夹环的左括号数
            for k in range(c, -1, -1):
                # 当找到发夹环左侧的第一个"("位置时，对b进行赋值
                if (structures[k] == '(' and structures[k + 1] == '.'):
                    b = k
                    r = 1
                # 这一步是为了统计发夹环的左括号数
                if (structures[k] == '('):
                    a1 = a1 + 1
                # 当找到发夹环的最左侧时终止这次循环
                if ((structures[k] == '.' and structures[k + 1] == '(') or (
                        structures[k] == ')' and structures[k + 1] == '(') or (
                        structures[k] == 'X' and structures[k + 1] == '(')):
                    break
                # 当找到序列第一个位置时终止循环
                if (structures[k] == '(' and k == 0 and r == 0):
                    b = k
                    break
            # 对于标记的位置从右开始遍历，用来统计发夹环的右括号数
            for q in range(c, len(structures)):
                # 当找到序列的最后一个位置时停止遍历
                if (q == len(structures) - 1):
                    a = a + 1
                    break
                # 进行右括号数的统计
                if (structures[q] == ')'):
                    a = a + 1
                # 找到右括号的终止位置时停止遍历
                if ((structures[q] == ')' and structures[q + 1] == '.') or (
                        structures[q] == ')' and structures[q + 1] == '(')):
                    break
            # 选择左括号数（a1）和右括号数（a2）中最小的数
            if (a1 == a or a1 < a):
                a1 = a1
            elif (a1 > a):
                a1 = a
            # 计算出发夹环茎区结构的起始位置
            e = b - a1 + 1
            # 计算出发夹环茎区结构的终止位置
            f = c + a1 - 1
            # 计算出发夹环中的游离碱基数目
            d = c - b - 1
            # 将所得数据添加到发夹环列表中
            all.append([a1, b, c, d, e, f])
            # 将发夹环茎区结构的起始位置到终止位置置为X
            for i in range(e, f + 1):
                structures[i] = 'X'
            # 对于这样的结构((((....XXXXXXX......XXXXXX...."))))".....XXXXX，对于引号前面的茎区标记完X后悔从后面接着遍历寻找“）”，这时需要跳过这个"))))"去寻找下一个茎区
            l = 0
            # 从发夹环茎区的最后一个位置开始寻找，直到找到下一个发夹环茎区的起始位置然后将这个位置标记起来，中间所有的碱基在第二个列表中置为Y
            for s in range(f + 1, len(structures)):
                if (structures[s] == '('):
                    l = 1
                    break
                structures2[s] = 'Y'
            a1 = 0
            a = 0
            b = 0
            c = 0
            d = 0
            e = 0
            f = 0
            # 如果发现没有左括号就说明后面没有茎区了，整个结束
            if (l == 0):
                break
    # k1是'.'的个数
    k1 = 0
    # k2是总的碱基个数
    k2 = 0
    local = 0
    local2 = 0
    look = 0
    look2 = 0
    stop = 0
    # 先判断是不是多分枝环，如果是的话执行下面的操作
    if (len(all) >= 2):
        # 对每一个发夹环茎区单独进行判断
        for i in range(0, len(all)):
            # k1是'.'的个数
            k1 = 0
            # k2是总的碱基个数
            k2 = 0
            local = 0
            local2 = 0
            look = 0
            look2 = 0
            stop = 0
            # 先判断是不是最后一个位置
            if ((i + 1) < len(all)):
                # 计算两个发夹环之间的'.'的个数
                for j in range(all[i][5] + 1, all[i + 1][4]):
                    # 统计两个发夹环茎区的碱基个数和'.'的个数
                    # 添加一个判断'D'的条件的目的是因为如果k1=k2，说明两个发夹环之间全是‘.’
                    # 然后从list(i,5)-1（前一个发夹环的起始位置）处开始向左遍历，查找相邻的‘.’，直到找到的是非‘.’的位置，然后将‘.’置成‘D’；
                    # 从list(i+1,6)+1（后一个发夹环的终止位置）处开始向右遍历，查找相邻的‘.’，直到找到的是非‘.’的位置，然后将‘.’置成‘D’；
                    # 经过上面的操作后可能在对下一个茎区之间存在一定的影响(下一个茎区之间的'.'被置为'D')
                    if (structures[j] == '.' or structures[j] == 'D'):
                        k1 = k1 + 1
                        k2 = k2 + 1
                    else:
                        k2 = k2 + 1
                # 如果茎区间的碱基数等于'.'的个数，先将两个发夹环茎区之间的'.'置换成'D'
                # 从list(i,5)-1（前一个发夹环的起始位置）处开始向左遍历，查找相邻的‘.’，直到找到的是非‘.’的位置，然后将‘.’置成‘D’；
                # 从list(i+1,6)+1（后一个发夹环的终止位置）处开始向右遍历，查找相邻的‘.’，直到找到的是非‘.’的位置，然后将‘.’置成‘D’；
                if (k1 == k2):
                    for j in range(all[i][5] + 1, all[i + 1][4]):
                        structures[j] = 'D'
                    for j in range(all[i][4] - 1, -1, -1):
                        if (structures[j] == '.'):
                            structures[j] = 'D'
                        else:
                            break
                    for j in range(all[i + 1][5] + 1, len(structures)):
                        if (structures[j] == '.'):
                            structures[j] = 'D'
                        else:
                            break
                # 如果k1!=k2说明中间出现了')'或者'('
                # ...XXXXX...(((..XXXXX..)))... => ...XXXXXDDD(((..XXXXX..)))...(stem(j) == '.' && stem(j-1) == 'X' )
                # ...(((..XXXXX..)))...XXXXX... => ...(((..XXXXX..)))DDDXXXXX...(stem(j) == '.' &&stem(j-1) == ')' )
                if (k1 != k2):
                    q1 = 0
                    q2 = 0
                    w1 = 0
                    w2 = 0
                    # 找到前一个茎区最右边的')'或者'X'的位置
                    for j in range(all[i + 1][4] - 1, -1, -1):
                        if ((structures[j] == ')' and structures[j + 1] == '(') or (
                                structures[j] == 'X' and structures[j + 1] == '(') or (
                                structures[j] == ')' and structures[j + 1] == 'X')):
                            stop = j
                            break
                        if ((structures[j] == '.' or structures[j] == 'D') and (
                                structures[j - 1] == ')' or structures[j - 1] == 'X')):
                            local = j
                            break
                    if (local == 0):
                        # 处理前一个茎区
                        if (structures[stop] == 'X'):
                            for j in range(all[i][4] - 1, -1, -1):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
                        else:
                            p = 0
                            for j in range(stop, -1, -1):
                                if (structures[j] == ')'):
                                    p = p + 1
                                if (structures[j] == '('):
                                    p = p - 1
                                if (p == 0):
                                    look2 = j
                                    break
                            for j in range(look2 - 1, -1, -1):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
                        # 处理后一个茎区

                        if (structures[stop + 1] == 'X'):
                            for j in range(all[i + 1][5] + 1, len(structures)):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
                        else:
                            p = 0
                            for j in range(stop + 1, len(structures)):
                                if (structures[j] == '('):
                                    p = p + 1
                                if (structures[j] == ')'):
                                    p = p - 1
                                if (p == 0):
                                    look2 = j
                                    break
                            for j in range(look2 + 1, len(structures)):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'

                    else:
                        # 从找到的位置向后直到'('或者'X'
                        for l in range(local, len(structures)):
                            if (structures[l] == '(' or structures[l] == 'X'):
                                local2 = l
                                break
                            structures[l] = 'D'
                        # 第二种方法
                        # 在两个发夹环之间找到第一个D
                        look = local
                        if (structures[look - 1] == 'X'):
                            for j in range(all[i][4] - 1, -1, -1):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
                        else:
                            # 在local的前一个位置进行遍历统计左括号和右括号的个数，遇到右括号时＋1，遇到左括号时-1
                            p = 0
                            for j in range(look - 1, -1, -1):
                                if (structures[j] == ')'):
                                    p = p + 1
                                if (structures[j] == '('):
                                    p = p - 1
                                if (p == 0):
                                    look2 = j
                                    break
                            for j in range(look2 - 1, -1, -1):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
                        # 在两个发夹环之间找到最后一个个D
                        look = local2
                        if (structures[look] == 'X'):
                            for j in range(all[i + 1][5] + 1, len(structures)):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
                        else:
                            # 在local2的后一个位置进行遍历统计左括号和右括号的个数。遇到右括号时+1 ， 遇到左括号时-1
                            p = 0
                            for j in range(look, len(structures)):
                                if (structures[j] == '('):
                                    p = p + 1
                                if (structures[j] == ')'):
                                    p = p - 1
                                if (p == 0):
                                    look2 = j
                                    break
                            for j in range(look2 + 1, len(structures)):
                                if (structures[j] != '.'):
                                    break
                                if (structures[j] == '.'):
                                    structures[j] = 'D'
            k1 = 0
            k2 = 0
    else:
        aa = 0
        for i in all:
            for j in range(i[1] - 1, -1, -1):
                if (structures[j] == '('):
                    aa = 1
                    break
        if (aa == 0):
            for i in range(0, len(structures)):
                if (structures[i] == '.'):
                    structures[i] = 'D'
    local = 0
    # 将游离碱基置为'Q'，分别从序列的从左向右和从右向左进行遍历，直到遇到不为'.'的位置
    for i in range(0, len(structures)):
        if (structures[i] == 'X'):
            break
        if (structures[i] == '('):
            local = i
            break
    if (local != 0):
        for i in range(local - 1, -1, -1):
            structures[i] = 'Q'
    local = 0
    for j in range(len(structures) - 1, -1, -1):
        if (structures[j] == 'X'):
            break
        if (structures[j] == ')'):
            local = j + 1
            break
    if (local != 0):
        for i in range(local, len(structures)):
            structures[i] = 'Q'
    # 当前茎区中的发夹环的左侧的凸环或内环中的碱基数
    k1 = 0
    # 当前茎区中的发夹环的右侧的凸环或内环中的碱基数
    k2 = 0
    # 当前茎区中的发夹环的左侧的'.'的数目
    k_1 = 0
    # 当前茎区中的发夹环的右侧的'.'的数目
    k_2 = 0
    # 当前茎区中的发夹环的左侧的'('的数目
    n1 = 0
    # 当前茎区中的发夹环的右侧的')'的数目
    n2 = 0
    # 将每一个内环的碱基数添加进去
    inner = []
    # 将每一个内环的碱基添加进去
    inner_V = []
    # 将每一个凸环的碱基数添加进去
    convex = []
    # 将每一个凸环的碱基添加进去
    convex_V = []
    # 对每一个发夹环茎区单独进行计算
    for i in all:
        # 当发夹环茎区的起始位置在第一个(XXXXXXDDDD)
        # 当前发夹环茎区的起始的前一个位置和终止的后一个位置不是'.'(DDDXXXXXDDD)
        # 当前发夹环茎区的终止位置是在序列的最后一个位置时
        # 以上情况跳过本次循环
        if ((i[4] == 0) or (
                (i[5] == len(structures) - 1) or ((structures[i[4] - 1] != '.') and (structures[i[5] + 1] != '.')))):
            continue
        # 先进行一次预判断
        # 当前发夹环茎区的起始位置的前一个位置或者终止位置的后一个位置不是'.'
        # 说明此时存在凸环，进行相应的计算
        stop = 0
        if (structures[i[4] - 1] != '.' or structures[i[5] + 1] != '.'):
            # 设置一个列表用于保存碱基
            V = []
            # 从当前发夹环茎区的起始位置的前一个位置进行判断
            for j in range(i[4] - k_1 - n1 - 1, -1, -1):
                # 当前位置是'.'时，设置为R，当前凸环中碱基的数量+1(k1)
                # 发夹环茎区左侧统计的'.'的数量+1(k_1)
                if (structures[j] == '.'):
                    structures[j] = 'R'
                    k1 = k1 + 1
                    k_1 = k_1 + 1
                    V.insert(0, RNA[j])
                # 当遍历到序列的最左侧时停止这次循环
                if (j == 0):
                    n1 = n1 + 1
                    break
                # 当遍历到不为'('的位置时停止这次循环
                if (structures[j] == '(' and structures[j - 1] == '.'):
                    n1 = n1 + 1
                    break
                # 当遍历到终止位置时
                if (structures[j] == '(' and (
                        structures[j - 1] == 'D' or structures[j - 1] == 'Q' or structures[j - 1] == 'X' or structures[
                    j - 1] == ')')):
                    n1 = n1 + 1
                    break
                # 当遍历到'('时，n1+1
                if (structures[j] == '('):
                    n1 = n1 + 1
            # 从当前发夹环茎区的终止位置的后一个位置进行判断
            for j in range(i[5] + k_2 + n2 + 1, len(structures)):
                # 当前位置是'.'时，设置为R，当前凸环中碱基的数量+1(k2)
                # 发夹环茎区右侧统计的'.'的数量+1(k_2)
                if (structures[j] == '.'):
                    structures[j] = 'R'
                    k2 = k2 + 1
                    k_2 = k_2 + 1
                    V.append(RNA[j])
                # 当遍历到序列的最右侧时停止这次循环
                if (j == len(structures) - 1):
                    n2 = n2 + 1
                    break
                # 当遍历到不为')'的位置时停止这次循环
                if (structures[j] == ')' and (
                        structures[j + 1] == '.' or structures[j + 1] == 'D' or structures[j + 1] == 'Q' or structures[
                    j + 1] == 'X' or structures[j + 1] == '(')):
                    n2 = n2 + 1
                    break
                # 当遍历到'('时，n1+1
                if (structures[j] == ')'):
                    n2 = n2 + 1
            # 将这个凸环的碱基数添加进数组中
            convex.append(k1 + k2)
            k1 = 0
            k2 = 0
            # 将凸环的碱基添加进数组中
            convex_V.append(V)
        # 当前发夹环茎区的起始位置的前一个位置和终止位置的后一个位置是'.'
        # 说明此时存在内环，进行相应的计算
        if (structures[i[4] - 1] == '.' and structures[i[5] + 1] == '.'):
            # 设置一个列表用于保存碱基
            V = []
            # 从当前发夹环茎区的起始位置的前一个位置进行判断
            for j in range(i[4] - k_1 - n1 - 1, -1, -1):
                # 当前位置是'.'时，设置为R，当前内环中碱基的数量+1(k1)
                # 发夹环茎区左侧统计的'.'的数量+1(k_1)
                if (structures[j] == '.'):
                    structures[j] = 'R'
                    k1 = k1 + 1
                    k_1 = k_1 + 1
                    # 将碱基添加进列表中
                    V.insert(0, RNA[j])
                # 当遍历到序列的最左侧时停止这次循环
                if (j == 0):
                    n1 = n1 + 1
                    break
                # 当遍历到不为'('的位置时停止这次循环
                if (structures[j] == '(' and (
                        structures[j - 1] == '.' or structures[j - 1] == 'D' or structures[j - 1] == 'Q' or structures[
                    j - 1] == 'X' or structures[j - 1] == ')')):
                    n1 = n1 + 1
                    break
                # 当遍历到'('时，n1+1
                if (structures[j] == '('):
                    n1 = n1 + 1
            # 从当前发夹环茎区的终止位置的后一个位置进行判断
            for j in range(i[5] + k_2 + n2 + 1, len(structures)):
                # 当前位置是'.'时，设置为R，当前内环中碱基的数量+1(k2)
                # 发夹环茎区右侧统计的'.'的数量+1(k_2)
                if (structures[j] == '.'):
                    structures[j] = 'R'
                    k2 = k2 + 1
                    k_2 = k_2 + 1
                    V.append(RNA[j])
                # 当遍历到序列的最右侧时停止这次循环
                if (j == len(structures) - 1):
                    n2 = n2 + 1
                    break
                # 当遍历到不为')'的位置时停止这次循环
                if (structures[j] == ')' and (
                        structures[j + 1] == '.' or structures[j + 1] == 'D' or structures[j + 1] == 'Q' or structures[
                    j + 1] == 'X' or structures[j + 1] == '(')):
                    n2 = n2 + 1
                    break
                # 当遍历到')'时，n2+1
                if (structures[j] == ')'):
                    n2 = n2 + 1
            # 将这个内环的碱基数添加进数组中
            inner.append(k1 + k2)
            # 更新参数用于进行下一次的计算
            k1 = 0
            k2 = 0
            # 将内环的碱基添加进数组中
            inner_V.append(V)
        # 开始对于n1,n2进行判断
        while (True):
            # 当前左侧的位置在序列初始位置并且发夹环左侧括号数目和右侧括号数目相等时，说明这个茎区已经计算完成，终止循环
            if ((i[4] - k_1 - n1) == 0):
                break
            # 当前右侧的位置在序列末尾位置并且发夹环左侧括号数目和右侧括号数目相等时，说明这个茎区已经计算完成，终止循环
            if ((i[5] + k_2 + n2) == len(structures) - 1):
                break
            # 当前左侧位置为X并且发夹环左侧括号数目和右侧括号数目相等时，说明这个茎区已经计算完成，终止循环
            if (structures[i[4] - k_1 - n1 - 1] == 'X' or structures[i[4] - k_1 - n1 - 1] == 'Q' or structures[
                i[4] - k_1 - n1 - 1] == 'D' or (
                    structures[i[4] - k_1 - n1 - 1] == '(' and structures[i[4] - k_1 - n1 - 2] == ')')):
                if (n1 <= n2):
                    break
            if (structures[i[5] + k_2 + n2 + 1] == 'X' or structures[i[5] + k_2 + n2 + 1] == 'Q' or structures[
                i[5] + k_2 + n2 + 1] == 'D' or (
                    structures[i[5] + k_2 + n2] == ')' and structures[i[5] + k_2 + n2 + 1] == '(')):
                if (n2 <= n1):
                    break
            # 当左括号和右括号的数目相等时，进行的步骤和前面的步骤相同
            if (n1 == n2):
                V = []
                for j in range(i[4] - k_1 - n1 - 1, -1, -1):
                    if (structures[j] == '.'):
                        structures[j] = 'R'
                        k1 = k1 + 1
                        k_1 = k_1 + 1
                        V.insert(0, RNA[j])
                    if (j == 0):
                        n1 = n1 + 1
                        break
                    if (structures[j] == '(' and (
                            structures[j - 1] == '.' or structures[j - 1] == 'D' or structures[j - 1] == 'Q' or
                            structures[j - 1] == 'X' or structures[j - 1] == ')')):
                        n1 = n1 + 1
                        break
                    if (structures[j] == '('):
                        n1 = n1 + 1
                for j in range(i[5] + k_2 + n2 + 1, len(structures)):
                    if (structures[j] == '.'):
                        structures[j] = 'R'
                        k2 = k2 + 1
                        k_2 = k_2 + 1
                        V.append(RNA[j])
                    if (j == len(structures) - 1):
                        n2 = n2 + 1
                        break
                    if (structures[j] == ')' and (
                            structures[j + 1] == '.' or structures[j + 1] == 'D' or structures[j + 1] == 'Q' or
                            structures[j + 1] == 'X' or structures[j + 1] == '(')):
                        n2 = n2 + 1
                        break
                    if (structures[j] == ')'):
                        n2 = n2 + 1
                if ((k1 + k2) > 0):
                    inner.append(k1 + k2)
                    inner_V.append(V)
                k1 = 0
                k2 = 0
            # 当左括号的数目大于右括号的数目时，只需要进行右侧的计算，计算过程和前面的相同
            elif (n1 > n2):
                V = []
                for j in range(i[5] + k_2 + n2 + 1, len(structures)):
                    if (structures[j] == '.'):
                        structures[j] = 'R'
                        k2 = k2 + 1
                        k_2 = k_2 + 1
                        V.append(RNA[j])
                    if (j == len(structures) - 1):
                        n2 = n2 + 1
                        break
                    if (structures[j] == ')' and (
                            structures[j + 1] == '.' or structures[j + 1] == 'D' or structures[j + 1] == 'Q' or
                            structures[j + 1] == 'X' or structures[j + 1] == '(')):
                        n2 = n2 + 1
                        break
                    if (structures[j] == ')'):
                        n2 = n2 + 1
                if ((k1 + k2) > 0):
                    convex.append(k1 + k2)
                    convex_V.append(V)
                k1 = 0
                k2 = 0
            # 当左括号的数目小于右括号的数目时，只需要进行左侧的计算，计算过程和前面的相同
            elif (n1 < n2):
                V = []
                for j in range(i[4] - k_1 - n1 - 1, -1, -1):
                    if (structures[j] == '.'):
                        structures[j] = 'R'
                        k1 = k1 + 1
                        k_1 = k_1 + 1
                        V.insert(0, RNA[j])
                    if (j == 0):
                        n1 = n1 + 1
                        break
                    if (structures[j] == '(' and (
                            structures[j - 1] == '.' or structures[j - 1] == 'D' or structures[j - 1] == 'Q' or
                            structures[j - 1] == 'X' or structures[j - 1] == ')')):
                        n1 = n1 + 1
                        break
                    if (structures[j] == '('):
                        n1 = n1 + 1
                if ((k1 + k2) > 0):
                    convex.append(k1 + k2)
                    convex_V.append(V)
                k1 = 0
                k2 = 0
        # 当前茎区处理到遇到遇到不同括号，X，Q，D时，例如：当向左遍历遇到不同括号，X，Q，D时，如果左括号数量小于右括号时，进行如下操作
        # 先判断n1和n2的大小，例如：n1 > n2，将n1向右后退(n1 - n2)个左括号，并记录下当前的位置e，右侧边缘的位置为i[5] + k_2 + n2
        # 将(e , (i[5] + k_2 + n2))范围内当前的整个茎区变为‘E’，然后进行下一个茎区的处理
        # 最后将所有参数置0，用来计算下一个茎区
        k1 = 0
        k2 = 0
        k_1 = 0
        k_2 = 0
        n1 = 0
        n2 = 0
        # print(structures)
    aaa = 0
    for i in range(0, len(structures)):
        if (structures[i] == '.'):
            aaa = 1
            break
    if (aaa == 1):
        # 先判断是不是处理的仅仅只是茎区的一部分
        structure = list(structures)
        structure2 = list(structures)
        # 右括号的第一个位置
        local = 0
        # 右括号的个数
        a = 0
        # 右括号的终止位置
        b = 0
        # 左括号的个数(总的括号数)
        a1 = 0
        # 左括号的第一个位置
        c = 0
        # 左侧的起始位置
        e = 0
        # 右侧的起始位置
        f = 0
        l = 0
        allin = []
        for j in range(0, len(structure)):
            if (structure[j] == 'X'):
                structure[j] = 'E'
        while (True):
            m = 0
            for j in range(0, len(structure)):
                if (structure[j] == '(' or structure[j] == ')'):
                    m = 1
                    break
            if (m != 1):
                break
            RNA2 = ""
            for k in structure:
                RNA2 = RNA2 + k
            structure2 = list(RNA2)
            structure = list(RNA2)
            for i in range(0, len(structure)):
                if (structure[i] == ')' and structure2[i] != 'Y'):
                    # if(structure[i] == ')'):
                    local = i
                    for j in range(local, len(structure)):
                        if (j == len(structure) - 1):
                            a = a + 1
                            b = j
                            break
                        if ((structure[j] == ')' and structure[j + 1] == '.') or (
                                structure[j] == ')' and structure[j + 1] == '(') or (
                                structure[j] == ')' and structure[j + 1] == 'X') or (
                                structure[j] == ')' and structure[j + 1] == 'Q') or (
                                structure[j] == ')' and structure[j + 1] == 'D') or (
                                structure[j] == ')' and structure[j + 1] == 'E')):
                            a = a + 1
                            break
                        if (structure[j] == ')'):
                            a = a + 1
                    r = 0
                    for j in range(local, -1, -1):
                        if (j == 0):
                            a1 = a1 + 1
                            break
                        if (structure[j] == '(' and structure[j + 1] != '.' and r != 1):
                            c = j
                            r = 1
                        if ((structure[j] == '(' and structure[j - 1] == '.') or (
                                structure[j] == '(' and structure[j - 1] == ')') or (
                                structure[j] == '(' and structure[j - 1] == 'X') or (
                                structure[j] == '(' and structure[j - 1] == 'Q') or (
                                structure[j] == '(' and structure[j - 1] == 'D') or (
                                structure[j] == '(' and structure[j - 1] == 'E')):
                            a1 = a1 + 1
                            break
                        if (structure[j] == '('):
                            a1 = a1 + 1
                    if (a1 >= a):
                        a1 = a
                    elif (a1 < a):
                        a1 = a1
                    # e = c - a1 + 1
                    # f = local + a1 - 1
                    p = a1
                    for j in range(local, len(structure)):
                        if (structure[j] == ')'):
                            p = p - 1
                        if (p == 0):
                            f = j
                            break
                    p = a1
                    for j in range(c, -1, -1):
                        if (structure[j] == '('):
                            p = p - 1
                        if (p == 0):
                            e = j
                            break
                    allin.append([e, f])
                    for j in range(e, f + 1):
                        structure[j] = 'E'
                    # l = 0
                    # 从发夹环茎区的最后一个位置开始寻找，直到找到下一个发夹环茎区的起始位置然后将这个位置标记起来，中间所有的碱基在第二个列表中置为Y
                    for s in range(f + 1, len(structure)):
                        if (structure[s] == '('):
                            l = 1
                            break
                        structure2[s] = 'Y'
                    # 右括号的第一个位置
                    local = 0
                    # 右括号的个数
                    a = 0
                    # 右括号的终止位置
                    b = 0
                    # 左括号的个数(总的括号数)
                    a1 = 0
                    # 左括号的第一个位置
                    c = 0
                    # 左侧的起始位置
                    e = 0
                    # 右侧的起始位置
                    f = 0
                    # 如果发现没有左括号就说明后面没有茎区了，整个结束
                    if (l == 0):
                        break
            for i in allin:
                # 当发夹环茎区的起始位置在第一个(XXXXXXDDDD)
                # 当前发夹环茎区的起始的前一个位置和终止的后一个位置不是'.'(DDDXXXXXDDD)
                # 当前发夹环茎区的终止位置是在序列的最后一个位置时
                # 以上情况跳过本次循环
                if ((i[0] == 0) or ((i[1] == len(structure) - 1) or (
                        (structure[i[0] - 1] != '.') and (structure[i[1] + 1] != '.')))):
                    continue
                # 先进行一次预判断
                # 当前发夹环茎区的起始位置的前一个位置或者终止位置的后一个位置不是'.'
                # 说明此时存在凸环，进行相应的计算
                if (structure[i[0] - 1] != '.' or structure[i[1] + 1] != '.'):
                    # 设置一个列表用于保存碱基
                    V = []
                    # 从当前发夹环茎区的起始位置的前一个位置进行判断
                    for j in range(i[0] - k_1 - n1 - 1, -1, -1):
                        # 当前位置是'.'时，设置为R，当前凸环中碱基的数量+1(k1)
                        # 发夹环茎区左侧统计的'.'的数量+1(k_1)
                        if (structure[j] == '.'):
                            structure[j] = 'R'
                            k1 = k1 + 1
                            k_1 = k_1 + 1
                            V.insert(0, RNA[j])
                        # 当遍历到序列的最左侧时停止这次循环
                        if (j == 0):
                            n1 = n1 + 1
                            break
                        # 当遍历到不为'('的位置时停止这次循环
                        if ((structure[j] == '(' and (structure[j - 1] == '.') or structure[j - 1] == 'D' or structure[
                            j - 1] == 'Q' or structure[j - 1] == 'X')):
                            n1 = n1 + 1
                            break
                        # 当遍历到'('时，n1+1
                        if (structure[j] == '('):
                            n1 = n1 + 1
                    # 从当前发夹环茎区的终止位置的后一个位置进行判断
                    for j in range(i[1] + k_2 + n2 + 1, len(structure)):
                        # 当前位置是'.'时，设置为R，当前凸环中碱基的数量+1(k2)
                        # 发夹环茎区右侧统计的'.'的数量+1(k_2)
                        if (structure[j] == '.'):
                            structure[j] = 'R'
                            k2 = k2 + 1
                            k_2 = k_2 + 1
                            V.append(RNA[j])
                        # 当遍历到序列的最右侧时停止这次循环
                        if (j == len(structure) - 1):
                            n2 = n2 + 1
                            break
                        # 当遍历到不为')'的位置时停止这次循环
                        if ((structure[j] == ')' and (structure[j + 1] == '.') or structure[j + 1] == 'D' or structure[
                            j + 1] == 'Q' or structure[j + 1] == 'X')):
                            n2 = n2 + 1
                            break
                        # 当遍历到'('时，n1+1
                        if (structure[j] == ')'):
                            n2 = n2 + 1
                    # 将这个凸环的碱基数添加进数组中
                    convex.append(k1 + k2)
                    k1 = 0
                    k2 = 0
                    # 将凸环的碱基添加进数组中
                    convex_V.append(V)
                # 当前发夹环茎区的起始位置的前一个位置和终止位置的后一个位置是'.'
                # 说明此时存在内环，进行相应的计算
                if (structure[i[0] - 1] == '.' and structure[i[1] + 1] == '.'):
                    # 设置一个列表用于保存碱基
                    V = []
                    # 从当前发夹环茎区的起始位置的前一个位置进行判断
                    for j in range(i[0] - k_1 - n1 - 1, -1, -1):
                        # 当前位置是'.'时，设置为R，当前内环中碱基的数量+1(k1)
                        # 发夹环茎区左侧统计的'.'的数量+1(k_1)
                        if (structure[j] == '.'):
                            structure[j] = 'R'
                            k1 = k1 + 1
                            k_1 = k_1 + 1
                            # 将碱基添加进列表中
                            V.insert(0, RNA[j])
                        # 当遍历到序列的最左侧时停止这次循环
                        if (j == 0):
                            n1 = n1 + 1
                            break
                        # 当遍历到不为'('的位置时停止这次循环
                        if ((structure[j] == '(' and (structure[j - 1] == '.') or structure[j - 1] == 'D' or structure[
                            j - 1] == 'Q' or structure[j - 1] == 'X')):
                            n1 = n1 + 1
                            break
                        # 当遍历到'('时，n1+1
                        if (structure[j] == '('):
                            n1 = n1 + 1
                    # 从当前发夹环茎区的终止位置的后一个位置进行判断
                    for j in range(i[1] + k_2 + n2 + 1, len(structure)):
                        # 当前位置是'.'时，设置为R，当前内环中碱基的数量+1(k2)
                        # 发夹环茎区右侧统计的'.'的数量+1(k_2)
                        if (structure[j] == '.'):
                            structure[j] = 'R'
                            k2 = k2 + 1
                            k_2 = k_2 + 1
                            V.append(RNA[j])
                        # 当遍历到序列的最右侧时停止这次循环
                        if (j == len(structure) - 1):
                            n2 = n2 + 1
                            break
                        # 当遍历到不为')'的位置时停止这次循环
                        if ((structure[j] == ')' and (structure[j + 1] == '.') or structure[j + 1] == 'D' or structure[
                            j + 1] == 'Q' or structure[j + 1] == 'X')):
                            n2 = n2 + 1
                            break
                        # 当遍历到')'时，n2+1
                        if (structure[j] == ')'):
                            n2 = n2 + 1
                    # 将这个内环的碱基数添加进数组中
                    inner.append(k1 + k2)
                    # 更新参数用于进行下一次的计算
                    k1 = 0
                    k2 = 0
                    # 将内环的碱基添加进数组中
                    inner_V.append(V)
                # 开始对于n1,n2进行判断
                while (True):
                    # 当前左侧的位置在序列初始位置并且发夹环左侧括号数目和右侧括号数目相等时，说明这个茎区已经计算完成，终止循环
                    if ((i[0] - k_1 - n1) == 0):
                        break
                    # 当前右侧的位置在序列末尾位置并且发夹环左侧括号数目和右侧括号数目相等时，说明这个茎区已经计算完成，终止循环
                    if ((i[1] + k_2 + n2) == len(structures) - 1):
                        break
                    # 当前左侧位置为X并且发夹环左侧括号数目和右侧括号数目相等时，说明这个茎区已经计算完成，终止循环
                    if (structures[i[0] - k_1 - n1 - 1] == 'X' or structures[i[0] - k_1 - n1 - 1] == 'Q' or structures[
                        i[0] - k_1 - n1 - 1] == 'D' or (
                            structures[i[0] - k_1 - n1 - 1] == '(' and structures[i[0] - k_1 - n1 - 2] == ')')):
                        if (n1 <= n2):
                            break
                    if (structures[i[1] + k_2 + n2 + 1] == 'X' or structures[i[1] + k_2 + n2 + 1] == 'Q' or structures[
                        i[1] + k_2 + n2 + 1] == 'D' or (
                            structures[i[1] + k_2 + n2] == ')' and structures[i[1] + k_2 + n2 + 1] == '(')):
                        if (n2 <= n1):
                            break
                    # 当左括号和右括号的数目相等时，进行的步骤和前面的步骤相同
                    if (n1 == n2):
                        V = []
                        for j in range(i[0] - k_1 - n1 - 1, -1, -1):
                            if (structure[j] == '.'):
                                structure[j] = 'R'
                                k1 = k1 + 1
                                k_1 = k_1 + 1
                                V.insert(0, RNA[j])
                            if (j == 0):
                                n1 = n1 + 1
                                break
                            if ((structure[j] == '(' and (structure[j - 1] == '.') or structure[j - 1] == 'D' or
                                 structure[j - 1] == 'Q' or structure[j - 1] == 'X')):
                                n1 = n1 + 1
                                break
                            if (structure[j] == '('):
                                n1 = n1 + 1
                        for j in range(i[1] + k_2 + n2 + 1, len(structure)):
                            if (structure[j] == '.'):
                                structure[j] = 'R'
                                k2 = k2 + 1
                                k_2 = k_2 + 1
                                V.append(RNA[j])
                            if (j == len(structure) - 1):
                                n2 = n2 + 1
                                break
                            if ((structure[j] == ')' and (structure[j + 1] == '.') or structure[j + 1] == 'D' or
                                 structure[j + 1] == 'Q' or structure[j + 1] == 'X')):
                                n2 = n2 + 1
                                break
                            if (structure[j] == ')'):
                                n2 = n2 + 1
                        if ((k1 + k2) > 0):
                            inner.append(k1 + k2)
                            inner_V.append(V)
                        k1 = 0
                        k2 = 0
                    # 当左括号的数目大于右括号的数目时，只需要进行右侧的计算，计算过程和前面的相同
                    elif (n1 > n2):
                        V = []
                        for j in range(i[1] + k_2 + n2 + 1, len(structure)):
                            if (structure[j] == '.'):
                                structure[j] = 'R'
                                k2 = k2 + 1
                                k_2 = k_2 + 1
                                V.append(RNA[j])
                            if (j == len(structure) - 1):
                                n2 = n2 + 1
                                break
                            if ((structure[j] == ')' and (structure[j + 1] == '.') or structure[j + 1] == 'D' or
                                 structure[j + 1] == 'Q' or structure[j + 1] == 'X')):
                                n2 = n2 + 1
                                break
                            if (structure[j] == ')'):
                                n2 = n2 + 1
                        if ((k1 + k2) > 0):
                            convex.append(k1 + k2)
                            convex_V.append(V)
                        k1 = 0
                        k2 = 0
                    # 当左括号的数目小于右括号的数目时，只需要进行左侧的计算，计算过程和前面的相同
                    elif (n1 < n2):
                        V = []
                        for j in range(i[0] - k_1 - n1 - 1, -1, -1):
                            if (structure[j] == '.'):
                                structure[j] = 'R'
                                k1 = k1 + 1
                                k_1 = k_1 + 1
                                V.insert(0, RNA[j])
                            if (j == 0):
                                n1 = n1 + 1
                                break
                            if ((structure[j] == '(' and (structure[j - 1] == '.') or structure[j - 1] == 'D' or
                                 structure[j - 1] == 'Q' or structure[j - 1] == 'X')):
                                n1 = n1 + 1
                                break
                            if (structure[j] == '('):
                                n1 = n1 + 1
                        if ((k1 + k2) > 0):
                            convex.append(k1 + k2)
                            convex_V.append(V)
                        k1 = 0
                        k2 = 0
                # 最后将所有参数置0，用来计算下一个茎区
                k1 = 0
                k2 = 0
                k_1 = 0
                k_2 = 0
                n1 = 0
                n2 = 0
                allin = []
                bbb = 0
                for j in range(0, len(structure)):
                    if (structure[j] == '.'):
                        bbb = 1
                        break
                if (bbb == 0):
                    break
            bbb = 0
            for j in range(0, len(structure)):
                if (structure[j] == '.'):
                    bbb = 1
                    break
            if (bbb == 0):
                break
    str1 = ss
    str2 = Structures
    str3 = list(str2)
    a = 0
    b = []
    c = []
    d = 0
    for i in range(0, len(str1)):
        if (str3[i] == ')'):
            for j in range(i - 1, -1, -1):
                if (str3[j] == '.'):
                    a = a + 1
                if (str3[j] == '('):
                    break
            for j in range(i, len(str1)):
                if ((j == len(str1) - 1) or (str3[j] == ')' and str3[j + 1] != ')') or (
                        str3[j - a - 1 - d] == '(' and str3[j - a - 2 - d] != '(')):
                    c.insert(0, str1[j - a - 1 - d] + str1[j])
                    str3[j - a - 1 - d] = '.'
                    str3[j] = '.'
                    break
                if (str3[j] == ')' and str3[j - a - 1 - d] == '('):
                    c.insert(0, str1[j - a - 1 - d] + str1[j])
                    str3[j - a - 1 - d] = '.'
                    str3[j] = '.'
                d = d + 2
            b.append(c)
            c = []
            a = 0
            d = 0
    RNA3 = ""
    for i in structures:
        if (i == '.'):
            RNA3 = RNA3 + 'R'
        else:
            RNA3 = RNA3 + i
    Multi_branched_power = 0
    Multi_branched = list(RNA3)
    for j in range(0, len(Multi_branched)):
        leftpair = 0
        rightpair = 0
        muti_ring = 0
        Multi_branched_count = 0
        Start = 0
        End = 0
        innerleft = 0
        block = 0
        if (Multi_branched[j] == ')'):
            for k in range(j, len(Multi_branched)):
                if (k == len(Multi_branched) - 1 and Multi_branched[k] == ')'):
                    End = k
                    rightpair = rightpair + 1
                    break
                if (Multi_branched[k] == 'D' or Multi_branched[k] == '(' or Multi_branched[k] == 'Q' or Multi_branched[
                    k] == 'X' or Multi_branched[k] == 'E'):
                    End = k - 1
                    break
                if (Multi_branched[k] == ')'):
                    rightpair = rightpair + 1
            for k in range(j, -1, -1):
                if (k == 0 and Multi_branched[k] == '('):
                    leftpair = leftpair + 1
                    Start = k
                    break
                if (Multi_branched[k] == '(' and Multi_branched[k + 1] != '(' and block == 0):
                    block = 1
                    innerleft = k
                if (Multi_branched[k] == '(' and (
                        Multi_branched[k - 1] == 'D' or Multi_branched[k - 1] == 'Q' or Multi_branched[k - 1] == ')' or
                        Multi_branched[k - 1] == 'X' or Multi_branched[k - 1] == 'E')):
                    leftpair = leftpair + 1
                    Start = k
                    break
                if (Multi_branched[k] == 'D'):
                    muti_ring = 1
                    Multi_branched_count = Multi_branched_count + 1
                if (Multi_branched[k] == '('):
                    leftpair = leftpair + 1
            if (leftpair > rightpair):
                New_Start = 0
                for k in range(innerleft, -1, -1):
                    if (Multi_branched[k] == '('):
                        rightpair = rightpair - 1
                    if (rightpair <= 0):
                        New_Start = k
                        break
                Start = New_Start
            elif (rightpair > leftpair):
                New_End = 0
                for k in range(j, len(Multi_branched)):
                    if (Multi_branched[k] == ')'):
                        leftpair = leftpair - 1
                    if (leftpair <= 0):
                        New_End = k
                        break
                End = New_End
            if (muti_ring == 1):
                Multi_branched_power = Multi_branched_power + 2
                if (Multi_branched_count == 1):
                    Multi_branched_power = Multi_branched_power + 0.2
                elif (Multi_branched_count > 1 and Multi_branched_count < 11):
                    Multi_branched_power = Multi_branched_power + 0.1 + 0.1 * Multi_branched_count
                elif (Multi_branched_count >= 11):
                    Multi_branched_power = Multi_branched_power + 1.2
            for k in range(Start, End + 1):
                Multi_branched[k] = 'E'
    power = 0
    for i in b:
        for j in range(0, len(i)):
            if (j == len(i) - 1):
                break
            if (i[j] == 'AU' and i[j + 1] == 'AU'):
                power = power - 0.9
            if (i[j] == 'AU' and i[j + 1] == 'UA'):
                power = power - 1.3
            if (i[j] == 'AU' and i[j + 1] == 'GC'):
                power = power - 2.4
            if (i[j] == 'AU' and i[j + 1] == 'CG'):
                power = power - 2.1
            if (i[j] == 'AU' and i[j + 1] == 'GU'):
                power = power - 1.3
            if (i[j] == 'AU' and i[j + 1] == 'UG'):
                power = power - 1
            if (i[j] == 'UA' and i[j + 1] == 'AU'):
                power = power - 1.1
            if (i[j] == 'UA' and i[j + 1] == 'UA'):
                power = power - 0.9
            if (i[j] == 'UA' and i[j + 1] == 'GC'):
                power = power - 2.2
            if (i[j] == 'UA' and i[j + 1] == 'CG'):
                power = power - 2.1
            if (i[j] == 'UA' and i[j + 1] == 'GU'):
                power = power - 1.4
            if (i[j] == 'UA' and i[j + 1] == 'UG'):
                power = power - 0.6
            if (i[j] == 'GC' and i[j + 1] == 'AU'):
                power = power - 2.1
            if (i[j] == 'GC' and i[j + 1] == 'UA'):
                power = power - 2.1
            if (i[j] == 'GC' and i[j + 1] == 'GC'):
                power = power - 3.3
            if (i[j] == 'GC' and i[j + 1] == 'CG'):
                power = power - 2.4
            if (i[j] == 'GC' and i[j + 1] == 'GU'):
                power = power - 2.1
            if (i[j] == 'GC' and i[j + 1] == 'UG'):
                power = power - 1.4
            if (i[j] == 'CG' and i[j + 1] == 'AU'):
                power = power - 2.2
            if (i[j] == 'CG' and i[j + 1] == 'UA'):
                power = power - 2.4
            if (i[j] == 'CG' and i[j + 1] == 'GC'):
                power = power - 3.4
            if (i[j] == 'CG' and i[j + 1] == 'CG'):
                power = power - 3.3
            if (i[j] == 'CG' and i[j + 1] == 'GU'):
                power = power - 2.5
            if (i[j] == 'CG' and i[j + 1] == 'UG'):
                power = power - 1.5
            if (i[j] == 'GU' and i[j + 1] == 'AU'):
                power = power - 0.6
            if (i[j] == 'GU' and i[j + 1] == 'UA'):
                power = power - 1
            if (i[j] == 'GU' and i[j + 1] == 'GC'):
                power = power - 1.5
            if (i[j] == 'GU' and i[j + 1] == 'CG'):
                power = power - 1.4
            if (i[j] == 'GU' and i[j + 1] == 'GU'):
                power = power - 0.5
            if (i[j] == 'GU' and i[j + 1] == 'UG'):
                power = power + 0.3
            if (i[j] == 'UG' and i[j + 1] == 'AU'):
                power = power - 1.4
            if (i[j] == 'UG' and i[j + 1] == 'UA'):
                power = power - 1.3
            if (i[j] == 'UG' and i[j + 1] == 'GC'):
                power = power - 2.5
            if (i[j] == 'UG' and i[j + 1] == 'CG'):
                power = power - 2.1
            if (i[j] == 'UG' and i[j + 1] == 'GU'):
                power = power + 1.3
            if (i[j] == 'UG' and i[j + 1] == 'UG'):
                power = power - 0.5
    power2 = 0
    count = [0.5, 0.5, 0.5, 1.7, 1.8, 2, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3, 3, 3.1, 3.1, 5, 5, 5, 5, 5, 5]
    for i in inner:
        if (i > 24):
            power2 = power2 + 5
        else:
            power2 = power2 + count[i - 1]
    power3 = 0
    count1 = [3.8, 2.8, 3.2, 3.6, 4, 4.4, 4.6, 4.7, 4.8, 4.9, 5, 5.1, 5.2, 5.3, 5.4, 5.4, 5.5, 5.5, 8, 9, 10, 11, 12,
              13, 14, 15, 16, 17, 18, 19, 20]
    for i in convex:
        if (i > 31):
            power3 = power3 + 20
        else:
            power3 = power3 + count1[i - 1]
    power4 = 0
    count2 = [0, 0, 5.7, 5.6, 5.6, 5.4, 5.9, 5.6, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 6.9, 7, 7.1, 7.1, 9, 10, 11, 12, 13, 14,
              15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
              41, 42, 43, 44, 45]
    for i in all:
        if (i[3] > 55):
            power4 = power4 + 45
        else:
            power4 = power4 + count2[i[3] - 1]
    hair = []
    allhair = []
    for i in all:
        for j in range(i[1] + 1, i[2]):
            hair.append(str1[j])
        allhair.append(hair)
        hair = []
    power5 = 0
    if (len(ss) >= 65 and len(ss) <= 90):
        p = 0
        for i in structures:
            if (i == 'D'):
                p = p + 1
        power5 = p * 0.2
    # power1 = power + power2 + power3 + power4 + power5 + Multi_branched_power
    power1 = power + power2 + power3 + power4 + power5 + Multi_branched_power
    if (len(ss) >= 65 and len(ss) <= 90):
        return power1,len(all)
    else:
        return power1

#长度在110以内的处理
def peiduijuzhen(f, str1):
    file = open(f, "r")
    content = file.readlines()
    Amm = []
    for i in content:
        Amm.append(i[:-1])
    B = []
    for i in Amm:
        lst = i.split(",")
        result = [float(item) for item in lst]
        B.append(result)
    s = str1
    if (len(s) < 32):
        A = []
        d = []
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                d.append(B[i][j])
            A.append(d)
            d = []

        a = len(A)
        b = len(A[0])
        for i in range(0, a):
            for j in range(0, b):
                if (A[i][j] > 0.985500):
                    A[i][j] = 0
                elif (A[i][j] <= 0.985500):
                    if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                            (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                            (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                        if (abs(i - j) > 2):
                            A[i][j] = 1
                        else:
                            A[i][j] = 0
                    else:
                        A[i][j] = 0
        i = 0
        j = len(A[0]) - 1
        ii = 0
        jj = 0
        # 找到上三角斜对角线上第一个等于1的位置
        while (True):
            if (i > 2):
                break
            if (A[i][j] == 1):
                ii = i
                jj = j
                break
            i = i + 1
            j = j - 1
        # 在斜对角线上向右上角遍历
        i = ii
        j = jj
        while (True):
            i = i - 1
            j = j + 1
            if (i < 0):
                break
            if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                    (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                    (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                if (abs(i - j) > 2):
                    A[i][j] = 1
            else:
                break
        # 在上三角斜对角线上向左下角遍历
        i = ii
        j = jj
        while (True):
            i = i + 1
            j = j - 1
            if (i < 0):
                break
            if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                    (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                    (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                if ((len(s) % 2 == 1 and abs(i - j) > 3) or (len(s) % 2 == 0 and abs(i - j) > 4)):
                    A[i][j] = 1
                else:
                    break
            else:
                break
        i = len(A[0]) - 1
        j = 0
        ii = 0
        jj = 0
        # 找到下三角斜对角线上第一个等于1的位置
        while (True):
            if (j > 2):
                break
            if (A[i][j] == 1):
                ii = i
                jj = j
                break
            i = i - 1
            j = j + 1
        # 在下三角斜对角线上向左下角遍历
        i = ii
        j = jj
        while (True):
            i = i + 1
            j = j - 1
            if (j < 0):
                break
            if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                    (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                    (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                if (abs(i - j) > 2):
                    A[i][j] = 1
            else:
                break
        # 在下三角斜对角线上向右上角遍历
        i = ii
        j = jj
        while (True):
            i = i - 1
            j = j + 1
            if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                    (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                    (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                if ((len(s) % 2 == 1 and abs(i - j) > 3) or (len(s) % 2 == 0 and abs(i - j) > 4)):
                    A[i][j] = 1
                else:
                    break
            else:
                break
        # 先将上三角区域斜对角线上的茎区挑选出来,只添加配对最多的茎区
        i = 0
        j = len(A[0]) - 1
        ii = 0
        jj = 0
        while (True):
            if (i > 2):
                break
            if (A[i][j] == 1):
                if (A[i + 1][j - 1] == 0):
                    i = i + 1
                    j = j - 1
                    continue
                elif (A[i + 1][j - 1] == 1):
                    ii = i
                    jj = j
                    break
            i = i + 1
            j = j - 1
        # print(ii)
        # print(jj)
        w = []
        count1 = 0
        if (jj != 0):
            i = ii
            j = jj
            q = []
            while (i >= 0 and j < len(A[0]) and A[i][j] == 1):
                count1 = count1 + 1
                q = [i, j]
                w.append(q)
                i = i + 1
                j = j - 1
        qqq = '.' * len(A[0])
        qqq = list(qqq)
        for q in w:
            qqq[q[0]] = '('
            qqq[q[1]] = ')'
        qq1 = ''
        for q in qqq:
            qq1 = qq1 + q
        # 再对下三角区域进行处理
        i = len(A[0]) - 1
        j = 0
        ii = 0
        jj = 0
        while (True):
            if (i < len(A[0]) - 3):
                break
            if (A[i][j] == 1):
                if (A[i - 1][j + 1] == 0):
                    i = i - 1
                    j = j + 1
                    continue
                elif (A[i - 1][j + 1] == 1):
                    ii = i
                    jj = j
                    break
            i = i - 1
            j = j + 1
        w = []
        count2 = 0
        if (ii != 0):
            i = ii
            j = jj
            q = []
            while (i >= 0 and j < len(A[0]) and A[i][j] == 1):
                count2 = count2 + 1
                q = [i, j]
                w.append(q)
                i = i - 1
                j = j + 1
        qqq = '.' * len(A[0])
        qqq = list(qqq)
        for q in w:
            qqq[q[1]] = '('
            qqq[q[0]] = ')'
        qq2 = ''
        for q in qqq:
            qq2 = qq2 + q
        ww = []
        if (count1 >= count2):
            ww.append(qq1)
        elif (count1 < count2):
            ww.append(qq2)
        c = 1
        w = []
        for i in range(0, a):
            for j in range(c, b):
                q = []
                count = 0
                if (A[i][j] == 1):
                    z = i
                    x = j
                    while z >= 0 and x < b and (A[z][x] == 1):
                        q.append([z, x])
                        count = count + 1
                        z = z - 1
                        x = x + 1
                if count >= 2:
                    w.append(q)
            c = c + 1
        Structure = []
        for i in w:
            s = ['.'] * a
            for j in i:
                s[j[0]] = '('
                s[j[1]] = ')'
            l = ''
            for k in s:
                l = l + k
            Structure.append(l)
        c = 1
        w = []
        for i in range(0, a):
            for j in range(c, b):
                q = []
                count = 0
                if (A[j][i] == 1):
                    z = i
                    x = j
                    while x < b and z >= 0 and (A[x][z] == 1):
                        q.append([z, x])
                        count = count + 1
                        x = x + 1
                        z = z - 1
                if (count >= 2):
                    w.append(q)
            c = c + 1
        Structure1 = []
        for i in w:
            s = ['.'] * a
            for j in i:
                s[j[0]] = '('
                s[j[1]] = ')'
            l = ''
            for k in s:
                l = l + k
            Structure1.append(l)
        Structure = Structure1 + Structure
        Structure = list(set(Structure))
        c = 1
        for i in range(0, len(Structure) - 1):
            count = 0
            for k in Structure[i]:
                if (k == '('):
                    count = count + 1
            for j in range(c, len(Structure)):
                s = 0
                for l in Structure[j]:
                    if (l == '('):
                        s = s + 1
                if (count < s):
                    t = Structure[j]
                    Structure[j] = Structure[i]
                    Structure[i] = t
                    count = s
            c = c + 1
        Structures = []
        for i in Structure:
            count = 0
            for j in range(0, len(i)):
                if (i[j] == '('):
                    count = 0
                if (i[j] == '.'):
                    count = count + 1
                if (i[j] == ')' and count > 2):
                    Structures.append(i)
                    break
        s = str1
        count = []
        allcount = []
        b = 0
        for i in range(0, len(Structures)):
            a = 0
            for j in range(0, len(s)):
                if (Structures[i][j] == '('):
                    a = a + 1
            if (a == b):
                count.append(Structures[i])
            if (a != b):
                b = a
                if (count != []):
                    allcount.append(count)
                count = []
                count.append(Structures[i])
        allcount.append(count)
        for structure in allcount:
            c = 1
            for i in range(0, len(structure) - 1):
                a = 0
                r = 0
                s = 0
                for j in range(0, len(structure[i])):
                    if (structure[i][j] == '(' and structure[i][j + 1] == '.' and r == 0):
                        r = 1
                    if (structure[i][j] == '.' and r == 1):
                        a = a + 1
                    if (structure[i][j] == ')'):
                        break
                for j in range(c, len(structure)):
                    count = 0
                    r = 0
                    for k in range(0, len(structure[i])):
                        if (structure[j][k] == '(' and structure[j][k + 1] == '.' and r == 0):
                            r = 1
                        if (structure[j][k] == '.' and r == 1):
                            count = count + 1
                        if (structure[j][k] == ')'):
                            break
                    if (count > a):
                        t = structure[j]
                        structure[j] = structure[i]
                        structure[i] = t
                        a = count
                c = c + 1
        Structures = []
        for i in allcount:
            for j in i:
                Structures.append(j)
        if (ww != []):
            countd = 0
            local1 = 0
            local2 = 0
            www = list(ww[0])
            for i in range(0, len(ww[0])):
                if (ww[0][i] == ')'):
                    local1 = i
                    break
            for i in range(local1, -1, -1):
                if (ww[0][i] == '.'):
                    countd = countd + 1
                if (ww[0][i] == '('):
                    local2 = i
                    break
            if (countd < 3):
                www[local1] = '.'
                www[local2] = '.'
            www1 = ''
            ww = []
            for i in www:
                www1 = www1 + i
            ww.append(www1)
            if (ww[0][0] != '(' and ww[0][len(A[0]) - 1] != ')'):
                count = 0
                for i in range(0, len(ww[0])):
                    if (ww[0][i] == '('):
                        count = count + 1
                if (count < 3):
                    ww = []
        Structures = ww + Structures
        allcome = []
        compare = []
        for i in Structures:
            s = ""
            for j in range(0, len(i)):
                if (i[j] == '(' or i[j] == ')'):
                    s = s + '1'
                elif (i[j] == '.'):
                    s = s + '0'
            allcome.append(s)
            p = 0
            q = 0
            t = 0
            for j in range(0, len(i)):
                if (j == 0 and i[j] == '('):
                    p = 0
                if (i[j] == '('):
                    t = t + 1
                if ((j == len(i) - 1) and i[j] == ')'):
                    q = len(i) - 1
                    break
                if (i[j] == ')' and i[j + 1] == '.'):
                    q = j
                    break
                if (i[j] == '.' and i[j + 1] == '('):
                    p = j + 1
                if (i[j] == ')' and i[j + 1] == '.'):
                    q = j
            compare.append([p, q, t])
        allin = []
        allStructure = []
        number = []
        for i in range(0, 1):
            s = allcome[i]
            allin.append(compare[i])
            number.append(i)
            for j in range(i + 1, len(Structures)):
                r = 0
                for a in range(0, len(Structures[0])):
                    if (allcome[i][a] == '1' and allcome[j][a] == '1'):
                        r = 1
                        break
                if (r == 1):
                    continue
                r = 0
                if (((compare[j][0] < compare[i][0]) and (
                        compare[j][1] > compare[i][0] and compare[j][1] < compare[i][1])) or (
                        (compare[j][1] > compare[i][1]) and (
                        compare[j][0] > compare[i][0] and compare[j][0] < compare[i][1]))):
                    r = 1
                if (r == 1):
                    continue
                s1 = ""
                for a in range(0, len(Structures[0])):
                    if ((allcome[i][a] == '1' and allcome[j][a] == '0') or (
                            allcome[i][a] == '0' and allcome[j][a] == '1')):
                        s1 = s1 + '1'
                    if (allcome[i][a] == '0' and allcome[j][a] == '0'):
                        s1 = s1 + '0'
                s = s1
                allin.append(compare[j])
                number.append(j)
                for k in range(j + 1, len(Structures)):
                    r = 0
                    for a in range(0, len(Structures[0])):
                        if (s[a] == '1' and allcome[k][a] == '1'):
                            r = 1
                            break
                    if (r == 1):
                        continue
                    r = 0
                    for a in allin:
                        if (((compare[k][0] < a[0]) and (compare[k][1] > a[0] and compare[k][1] < a[1])) or (
                                (compare[k][1] > a[1]) and (compare[k][0] > a[0] and compare[k][0] < a[1]))):
                            r = 1
                            break
                    if (r == 1):
                        continue
                    s1 = ""
                    for a in range(0, len(Structures[0])):
                        if ((s[a] == '1' and allcome[k][a] == '0') or (s[a] == '0' and allcome[k][a] == '1')):
                            s1 = s1 + '1'
                        if (s[a] == '0' and allcome[k][a] == '0'):
                            s1 = s1 + '0'
                    s = s1
                    allin.append(compare[k])
                    number.append(k)
                s4 = Structures[number[0]]
                for k in range(1, len(number)):
                    s5 = ""
                    s6 = Structures[number[k]]
                    for l in range(0, len(s)):
                        if (s4[l] == '.' and s6[l] == '.'):
                            s5 = s5 + '.'
                        if ((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                            s5 = s5 + '('
                        if ((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                            s5 = s5 + ')'
                    s4 = s5
                allin = []
                allin.append(compare[i])
                number = []
                number.append(i)
                s = allcome[i]
                allStructure.append(s4)
            if (len(number) == 1):
                allStructure.append(Structures[number[0]])
            allin = []
            number = []
        allStructures = []
        if (len(allStructure) == 1):
            allStructures = allStructure
        else:
            allStructures = allStructure[0:len(allStructure) - 1]
        allStructure = []
        for i in allStructures:
            allStructure.append(i)
    elif ((len(s) >= 32 and len(s) < 65) or len(s) > 90):
        if (len(s) > 90 and len(s) <= 110):
            gg = 0.988500
            pp = 2
        else:
            gg = 0.985500
            pp = 3
        A = B
        a = len(A)
        b = len(A[0])
        for i in range(0, a):
            for j in range(0, b):
                if (A[i][j] > gg):
                    A[i][j] = 0
                elif (A[i][j] <= gg):
                    if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                            (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                            (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                        if (abs(i - j) > 2):
                            A[i][j] = 1
                        else:
                            A[i][j] = 0
                    else:
                        A[i][j] = 0
        c = 1
        w = []
        for i in range(0, a):
            for j in range(c, b):
                q = []
                count = 0
                if (A[i][j] == 1):
                    z = i
                    x = j
                    while z >= 0 and x < b and (A[z][x] == 1):
                        q.append([z, x])
                        count = count + 1
                        z = z - 1
                        x = x + 1
                if count >= pp:
                    w.append(q)
            c = c + 1
        Structure = []
        for i in w:
            s = ['.'] * a
            for j in i:
                s[j[0]] = '('
                s[j[1]] = ')'
            l = ''
            for k in s:
                l = l + k
            Structure.append(l)
        c = 1
        w = []
        for i in range(0, a):
            for j in range(c, b):
                q = []
                count = 0
                if (A[j][i] == 1):
                    z = i
                    x = j
                    while x < b and z >= 0 and (A[x][z] == 1):
                        q.append([z, x])
                        count = count + 1
                        x = x + 1
                        z = z - 1
                if (count >= pp):
                    w.append(q)
            c = c + 1
        Structure1 = []
        for i in w:
            s = ['.'] * a
            for j in i:
                s[j[0]] = '('
                s[j[1]] = ')'
            l = ''
            for k in s:
                l = l + k
            Structure1.append(l)
        Structure = Structure1 + Structure
        Structure = list(set(Structure))
        c = 1
        for i in range(0, len(Structure) - 1):
            count = 0
            for k in Structure[i]:
                if (k == '('):
                    count = count + 1
            for j in range(c, len(Structure)):
                s = 0
                for l in Structure[j]:
                    if (l == '('):
                        s = s + 1
                if (count < s):
                    t = Structure[j]
                    Structure[j] = Structure[i]
                    Structure[i] = t
                    count = s
            c = c + 1

        Structures = []
        for i in Structure:
            count = 0
            for j in range(0, len(i)):
                if (i[j] == '('):
                    count = 0
                if (i[j] == '.'):
                    count = count + 1
                if (i[j] == ')' and count > 2):
                    Structures.append(i)
                    break
        s = str1
        count = []
        allcount = []
        b = 0
        for i in range(0, len(Structures)):
            a = 0
            for j in range(0, len(s)):
                if (Structures[i][j] == '('):
                    a = a + 1
            if (a == b):
                count.append(Structures[i])
            if (a != b):
                b = a
                if (count != []):
                    allcount.append(count)
                count = []
                count.append(Structures[i])
        allcount.append(count)
        for structure in allcount:
            c = 1
            for i in range(0, len(structure) - 1):
                a = 0
                r = 0
                s = 0
                for j in range(0, len(structure[i])):
                    if (structure[i][j] == '(' and structure[i][j + 1] == '.' and r == 0):
                        r = 1
                    if (structure[i][j] == '.' and r == 1):
                        a = a + 1
                    if (structure[i][j] == ')'):
                        break
                for j in range(c, len(structure)):
                    count = 0
                    r = 0
                    for k in range(0, len(structure[i])):
                        if (structure[j][k] == '(' and structure[j][k + 1] == '.' and r == 0):
                            r = 1
                        if (structure[j][k] == '.' and r == 1):
                            count = count + 1
                        if (structure[j][k] == ')'):
                            break
                    if (count > a):
                        t = structure[j]
                        structure[j] = structure[i]
                        structure[i] = t
                        a = count
                c = c + 1
        Structures = []
        for i in allcount:
            for j in i:
                Structures.append(j)
        allStructure = []
        allin = []
        p = 0
        q = 0
        if (len(Structures) == 1):
            allStructure = Structures
        if (len(Structures) > 1 and len(Structures) <= 20):
            allcome = []
            compare = []
            for i in Structures:
                s = ""
                for j in range(0, len(i)):
                    if (i[j] == '(' or i[j] == ')'):
                        s = s + '1'
                    elif (i[j] == '.'):
                        s = s + '0'
                allcome.append(s)
                p = 0
                q = 0
                t = 0
                for j in range(0, len(i)):
                    if (j == 0 and i[j] == '('):
                        p = 0
                    if (i[j] == '('):
                        t = t + 1
                    if ((j == len(i) - 1) and i[j] == ')'):
                        q = len(i) - 1
                        break
                    if (i[j] == ')' and i[j + 1] == '.'):
                        q = j
                        break
                    if (i[j] == '.' and i[j + 1] == '('):
                        p = j + 1
                    if (i[j] == ')' and i[j + 1] == '.'):
                        q = j
                compare.append([p, q, t])
            allin = []
            allStructure = []
            number = []
            for i in range(0, len(Structures)):
                s = allcome[i]
                allin.append(compare[i])
                number.append(i)
                for j in range(i + 1, len(Structures)):
                    r = 0
                    for a in range(0, len(Structures[0])):
                        if (allcome[i][a] == '1' and allcome[j][a] == '1'):
                            r = 1
                            break
                    if (r == 1):
                        continue
                    r = 0
                    if (((compare[j][0] < compare[i][0]) and (
                            compare[j][1] > compare[i][0] and compare[j][1] < compare[i][1])) or (
                            (compare[j][1] > compare[i][1]) and (
                            compare[j][0] > compare[i][0] and compare[j][0] < compare[i][1]))):
                        r = 1
                    if (r == 1):
                        continue
                    s1 = ""
                    for a in range(0, len(Structures[0])):
                        if ((allcome[i][a] == '1' and allcome[j][a] == '0') or (
                                allcome[i][a] == '0' and allcome[j][a] == '1')):
                            s1 = s1 + '1'
                        if (allcome[i][a] == '0' and allcome[j][a] == '0'):
                            s1 = s1 + '0'
                    s = s1
                    allin.append(compare[j])
                    number.append(j)
                    for k in range(j + 1, len(Structures)):
                        r = 0
                        for a in range(0, len(Structures[0])):
                            if (s[a] == '1' and allcome[k][a] == '1'):
                                r = 1
                                break
                        if (r == 1):
                            continue
                        r = 0
                        for a in allin:
                            if (((compare[k][0] < a[0]) and (compare[k][1] > a[0] and compare[k][1] < a[1])) or (
                                    (compare[k][1] > a[1]) and (compare[k][0] > a[0] and compare[k][0] < a[1]))):
                                r = 1
                                break
                        if (r == 1):
                            continue
                        s1 = ""
                        for a in range(0, len(Structures[0])):
                            if ((s[a] == '1' and allcome[k][a] == '0') or (s[a] == '0' and allcome[k][a] == '1')):
                                s1 = s1 + '1'
                            if (s[a] == '0' and allcome[k][a] == '0'):
                                s1 = s1 + '0'
                        s = s1
                        allin.append(compare[k])
                        number.append(k)
                    s4 = Structures[number[0]]
                    for k in range(1, len(number)):
                        s5 = ""
                        s6 = Structures[number[k]]
                        for l in range(0, len(s)):
                            if (s4[l] == '.' and s6[l] == '.'):
                                s5 = s5 + '.'
                            if ((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                                s5 = s5 + '('
                            if ((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                                s5 = s5 + ')'
                        s4 = s5
                    allin = []
                    allin.append(compare[i])
                    number = []
                    number.append(i)
                    s = allcome[i]
                    allStructure.append(s4)
                if (len(number) == 1):
                    allStructure.append(Structures[number[0]])
                allin = []
                number = []
        elif (len(Structures) > 20):
            allcome = []
            compare = []
            for i in Structures:
                s = ""
                for j in range(0, len(i)):
                    if (i[j] == '(' or i[j] == ')'):
                        s = s + '1'
                    elif (i[j] == '.'):
                        s = s + '0'
                allcome.append(s)
                p = 0
                q = 0
                t = 0
                for j in range(0, len(i)):
                    if (j == 0 and i[j] == '('):
                        p = 0
                    if (i[j] == '('):
                        t = t + 1
                    if ((j == len(i) - 1) and i[j] == ')'):
                        q = len(i) - 1
                        break
                    if (i[j] == ')' and i[j + 1] == '.'):
                        q = j
                        break
                    if (i[j] == '.' and i[j + 1] == '('):
                        p = j + 1
                    if (i[j] == ')' and i[j + 1] == '.'):
                        q = j
                compare.append([p, q, t])
            allin = []
            allStructure = []
            number = []
            for i in range(0, 20):
                s = allcome[i]
                allin.append(compare[i])
                number.append(i)
                for j in range(i + 1, len(Structures)):
                    r = 0
                    for a in range(0, len(Structures[0])):
                        if (allcome[i][a] == '1' and allcome[j][a] == '1'):
                            r = 1
                            break
                    if (r == 1):
                        continue
                    r = 0
                    if (((compare[j][0] < compare[i][0]) and (
                            compare[j][1] > compare[i][0] and compare[j][1] < compare[i][1])) or (
                            (compare[j][1] > compare[i][1]) and (
                            compare[j][0] > compare[i][0] and compare[j][0] < compare[i][1]))):
                        r = 1
                    if (r == 1):
                        continue
                    s1 = ""
                    for a in range(0, len(Structures[0])):
                        if ((allcome[i][a] == '1' and allcome[j][a] == '0') or (
                                allcome[i][a] == '0' and allcome[j][a] == '1')):
                            s1 = s1 + '1'
                        if (allcome[i][a] == '0' and allcome[j][a] == '0'):
                            s1 = s1 + '0'
                    s = s1
                    allin.append(compare[j])
                    number.append(j)
                    for k in range(j + 1, len(Structures)):
                        r = 0
                        for a in range(0, len(Structures[0])):
                            if (s[a] == '1' and allcome[k][a] == '1'):
                                r = 1
                                break
                        if (r == 1):
                            continue
                        r = 0
                        for a in allin:
                            if (((compare[k][0] < a[0]) and (compare[k][1] > a[0] and compare[k][1] < a[1])) or (
                                    (compare[k][1] > a[1]) and (compare[k][0] > a[0] and compare[k][0] < a[1]))):
                                r = 1
                                break
                        if (r == 1):
                            continue
                        s1 = ""
                        for a in range(0, len(Structures[0])):
                            if ((s[a] == '1' and allcome[k][a] == '0') or (s[a] == '0' and allcome[k][a] == '1')):
                                s1 = s1 + '1'
                            if (s[a] == '0' and allcome[k][a] == '0'):
                                s1 = s1 + '0'
                        s = s1
                        allin.append(compare[k])
                        number.append(k)
                    s4 = Structures[number[0]]
                    for k in range(1, len(number)):
                        s5 = ""
                        s6 = Structures[number[k]]
                        for l in range(0, len(s)):
                            if (s4[l] == '.' and s6[l] == '.'):
                                s5 = s5 + '.'
                            if ((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                                s5 = s5 + '('
                            if ((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                                s5 = s5 + ')'
                        s4 = s5
                    allin = []
                    allin.append(compare[i])
                    number = []
                    number.append(i)
                    s = allcome[i]
                    allStructure.append(s4)
                if (len(number) == 1):
                    allStructure.append(Structures[number[0]])
                allin = []
                number = []
    elif (len(s) >= 65 and len(s) <= 90):
        A = B
        A = []
        d = []
        for i in range(0, len(s)):
            for j in range(0, len(s)):
                d.append(B[i][j])
            A.append(d)
            d = []
        a = len(A)
        b = len(A[0])
        for i in range(0, a):
            for j in range(0, b):
                if (A[i][j] > 0.985500):
                    A[i][j] = 0
                elif (A[i][j] <= 0.985500):
                    if (((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or (
                            (s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or (
                            (s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                        if (abs(i - j) > 2):
                            A[i][j] = 1
                        else:
                            A[i][j] = 0
                    else:
                        A[i][j] = 0
        # 先找到短茎区
        # 针对于上三角部分
        ShortStructure = []
        longStructure = []
        c = 1
        for i in range(0, a):
            for j in range(c, b):
                q = []
                count = 0
                if (A[i][j] == 1 and (abs(i - j) + 1 <= 24)):
                    k = i
                    l = j
                    count = 0
                    while (True):
                        if (A[k][l] == 1):
                            count = count + 1
                            q.append([k, l])
                        k = k + 1
                        l = l - 1
                        if (((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or (
                                (abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3) or A[k][l] == 0):
                            break
                    if (count >= 2):
                        if ((abs(i - j) + 1 <= 20)):
                            zz = 0
                            kk = i - 1
                            ll = j + 1
                            while (zz < 2 and kk >= 0 and ll < b):
                                if ((s[kk] == 'A' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'A') or (
                                        s[kk] == 'C' and s[ll] == 'G') or (s[kk] == 'G' and s[ll] == 'C') or (
                                        s[kk] == 'G' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'G')):
                                    A[kk][ll] = 1
                                    count = count + 1
                                    q.insert(0, [kk, ll])
                                else:
                                    break
                                kk = kk - 1
                                ll = ll + 1
                                zz = zz + 1
                        while (True):
                            if ((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (
                                    s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (
                                    s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                                if (((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or (
                                        (abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3)):
                                    break
                                else:
                                    A[k][l] = 1
                                    count = count + 1
                                    q.append([k, l])
                            else:
                                break
                            k = k + 1
                            l = l - 1
                    if (count >= 3):
                        qq = '.' * len(A[0])
                        qq = list(qq)
                        for z in q:
                            qq[z[0]] = '('
                            qq[z[1]] = ')'
                            A[z[0]][z[1]] = 0
                        qq2 = ''
                        for z in qq:
                            qq2 = qq2 + z
                        ShortStructure.append(qq2)
                        short = 0
                        for z in range(0, len(qq2)):
                            if (qq2[z] == '('):
                                short = short + 1
                        st = []
                        for z in q:
                            st.append(z)
                        while (short > 3):
                            st.pop(0)
                            qq = '.' * len(A[0])
                            qq = list(qq)
                            for z in st:
                                qq[z[0]] = '('
                                qq[z[1]] = ')'
                                A[z[0]][z[1]] = 0
                            qq2 = ''
                            for z in qq:
                                qq2 = qq2 + z
                            ShortStructure.append(qq2)
                            short = short - 1
                if (A[i][j] == 1 and (abs(i - j) + 1 > 24)):
                    w = []
                    count = 0
                    z = i
                    x = j
                    while z >= 0 and x < b and (A[z][x] == 1):
                        w.append([z, x])
                        count = count + 1
                        z = z - 1
                        x = x + 1
                    if (count >= 3):
                        qq = '.' * len(A[0])
                        qq = list(qq)
                        for z in w:
                            qq[z[0]] = '('
                            qq[z[1]] = ')'
                        qq2 = ''
                        for z in qq:
                            qq2 = qq2 + z
                        longStructure.append(qq2)
            c = c + 1
        # 先找到短茎区
        # 针对于下三角部分
        c = 1
        w = []
        for i in range(0, a):
            for j in range(c, b):
                q = []
                count = 0
                if (A[j][i] == 1 and (abs(i - j) + 1 <= 24)):
                    w = [j, i]
                    k = j
                    l = i
                    count = 0
                    while (True):
                        if (A[k][l] == 1):
                            count = count + 1
                            q.append([k, l])
                        k = k - 1
                        l = l + 1
                        if (((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or (
                                (abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3) or A[k][l] == 0):
                            break
                    if (count >= 2):
                        if (abs(i - j) + 1 <= 20):
                            zz = 0
                            kk = j + 1
                            ll = i - 1
                            while (zz < 2 and kk < b and ll >= 0):
                                if ((s[kk] == 'A' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'A') or (
                                        s[kk] == 'C' and s[ll] == 'G') or (s[kk] == 'G' and s[ll] == 'C') or (
                                        s[kk] == 'G' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'G')):
                                    A[kk][ll] = 1
                                    count = count + 1
                                    q.insert(0, [kk, ll])
                                else:
                                    break
                                kk = kk + 1
                                ll = ll - 1
                                zz = zz + 1
                        while (True):
                            if ((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (
                                    s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (
                                    s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                                if (((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or (
                                        (abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3)):
                                    break
                                else:
                                    A[k][l] = 1
                                    count = count + 1
                                    q.append([k, l])
                            else:
                                break
                            k = k - 1
                            l = l + 1
                    if (count >= 3):
                        qq = '.' * len(A[0])
                        qq = list(qq)
                        for z in q:
                            qq[z[1]] = '('
                            qq[z[0]] = ')'
                            A[z[0]][z[1]] = 0
                        qq2 = ''
                        for z in qq:
                            qq2 = qq2 + z
                        ShortStructure.append(qq2)
                        short = 0
                        for z in range(0, len(qq2)):
                            if (qq2[z] == '('):
                                short = short + 1
                        st = []
                        for z in q:
                            st.append(z)
                        while (short > 3):
                            st.pop(0)
                            qq = '.' * len(A[0])
                            qq = list(qq)
                            for z in st:
                                qq[z[1]] = '('
                                qq[z[0]] = ')'
                                A[z[0]][z[1]] = 0
                            qq2 = ''
                            for z in qq:
                                qq2 = qq2 + z
                            ShortStructure.append(qq2)
                            short = short - 1
                if (A[i][j] == 1 and (abs(i - j) + 1 > 24)):
                    w = []
                    count = 0
                    z = i
                    x = j
                    while x < b and z >= 0 and (A[x][z] == 1):
                        w.append([z, x])
                        count = count + 1
                        x = x + 1
                        z = z - 1
                    if (count >= 3):
                        qq = '.' * len(A[0])
                        qq = list(qq)
                        for z in w:
                            qq[z[0]] = '('
                            qq[z[1]] = ')'
                        qq2 = ''
                        for z in qq:
                            qq2 = qq2 + z
                        longStructure.append(qq2)
            c = c + 1
        longStructure = list(set(longStructure))
        ShortStructure = list(set(ShortStructure))
        c = 1
        for i in range(0, len(ShortStructure) - 1):
            count = 0
            for k in ShortStructure[i]:
                if (k == '('):
                    count = count + 1
            for j in range(c, len(ShortStructure)):
                s = 0
                for l in ShortStructure[j]:
                    if (l == '('):
                        s = s + 1
                if (count < s):
                    t = ShortStructure[j]
                    ShortStructure[j] = ShortStructure[i]
                    ShortStructure[i] = t
                    count = s
            c = c + 1
        Structures = []
        for i in ShortStructure:
            count = 0
            for j in range(0, len(i)):
                if (i[j] == '('):
                    count = 0
                if (i[j] == '.'):
                    count = count + 1
                if (i[j] == ')' and count > 2):
                    Structures.append(i)
                    break
        s = str1
        count = []
        allcount = []
        b = 0
        for i in range(0, len(Structures)):
            a = 0
            for j in range(0, len(s)):
                if (Structures[i][j] == '('):
                    a = a + 1
            if (a == b):
                count.append(Structures[i])
            if (a != b):
                b = a
                if (count != []):
                    allcount.append(count)
                count = []
                count.append(Structures[i])
        allcount.append(count)
        for structure in allcount:
            c = 1
            for i in range(0, len(structure) - 1):
                a = 0
                r = 0
                s = 0
                for j in range(0, len(structure[i])):
                    if (structure[i][j] == '(' and structure[i][j + 1] == '.' and r == 0):
                        r = 1
                    if (structure[i][j] == '.' and r == 1):
                        a = a + 1
                    if (structure[i][j] == ')'):
                        break
                for j in range(c, len(structure)):
                    count = 0
                    r = 0
                    for k in range(0, len(structure[i])):
                        if (structure[j][k] == '(' and structure[j][k + 1] == '.' and r == 0):
                            r = 1
                        if (structure[j][k] == '.' and r == 1):
                            count = count + 1
                        if (structure[j][k] == ')'):
                            break
                    if (count > a):
                        t = structure[j]
                        structure[j] = structure[i]
                        structure[i] = t
                        a = count
                c = c + 1
        ShortStructure = []
        for i in allcount:
            for j in i:
                ShortStructure.append(j)
        c = 1
        for i in range(0, len(longStructure) - 1):
            count = 0
            for k in longStructure[i]:
                if (k == '('):
                    count = count + 1
            for j in range(c, len(longStructure)):
                s = 0
                for l in longStructure[j]:
                    if (l == '('):
                        s = s + 1
                if (count < s):
                    t = longStructure[j]
                    longStructure[j] = longStructure[i]
                    longStructure[i] = t
                    count = s
            c = c + 1
        Structures = []
        for i in longStructure:
            count = 0
            for j in range(0, len(i)):
                if (i[j] == '('):
                    count = 0
                if (i[j] == '.'):
                    count = count + 1
                if (i[j] == ')' and count > 2):
                    Structures.append(i)
                    break
        s = str1
        count = []
        allcount = []
        b = 0
        for i in range(0, len(Structures)):
            a = 0
            for j in range(0, len(s)):
                if (Structures[i][j] == '('):
                    a = a + 1
            if (a == b):
                count.append(Structures[i])
            if (a != b):
                b = a
                if (count != []):
                    allcount.append(count)
                count = []
                count.append(Structures[i])
        allcount.append(count)
        for structure in allcount:
            c = 1
            for i in range(0, len(structure) - 1):
                a = 0
                r = 0
                s = 0
                for j in range(0, len(structure[i])):
                    if (structure[i][j] == '(' and structure[i][j + 1] == '.' and r == 0):
                        r = 1
                    if (structure[i][j] == '.' and r == 1):
                        a = a + 1
                    if (structure[i][j] == ')'):
                        break
                for j in range(c, len(structure)):
                    count = 0
                    r = 0
                    for k in range(0, len(structure[i])):
                        if (structure[j][k] == '(' and structure[j][k + 1] == '.' and r == 0):
                            r = 1
                        if (structure[j][k] == '.' and r == 1):
                            count = count + 1
                        if (structure[j][k] == ')'):
                            break
                    if (count > a):
                        t = structure[j]
                        structure[j] = structure[i]
                        structure[i] = t
                        a = count
                c = c + 1
        longStructure = []
        for i in allcount:
            for j in i:
                longStructure.append(j)
        allStructure = []
        if (len(longStructure) < 20):
            lenS = len(longStructure)
        else:
            lenS = 20
        for ii in range(0, lenS):
            Structures = []
            longS = []
            longS.append(longStructure[ii])
            Structures = longS + ShortStructure
            Structures
            allcome = []
            compare = []
            for i in Structures:
                s = ""
                for j in range(0, len(i)):
                    if (i[j] == '(' or i[j] == ')'):
                        s = s + '1'
                    elif (i[j] == '.'):
                        s = s + '0'
                allcome.append(s)
                p = 0
                q = 0
                t = 0
                for j in range(0, len(i)):
                    if (j == 0 and i[j] == '('):
                        p = 0
                    if (i[j] == '('):
                        t = t + 1
                    if ((j == len(i) - 1) and i[j] == ')'):
                        q = len(i) - 1
                        break
                    if (i[j] == ')' and i[j + 1] == '.'):
                        q = j
                        break
                    if (i[j] == '.' and i[j + 1] == '('):
                        p = j + 1
                    if (i[j] == ')' and i[j + 1] == '.'):
                        q = j
                compare.append([p, q, t])
            allin = []
            number = []
            for i in range(0, 1):
                s = allcome[i]
                allin.append(compare[i])
                number.append(i)
                for j in range(i + 1, len(Structures)):
                    r = 0
                    for a in range(0, len(Structures[0])):
                        if (allcome[i][a] == '1' and allcome[j][a] == '1'):
                            r = 1
                            break
                    if (r == 1):
                        continue
                    r = 0
                    if (((compare[j][0] < compare[i][0]) and (
                            compare[j][1] > compare[i][0] and compare[j][1] < compare[i][1])) or (
                            (compare[j][1] > compare[i][1]) and (
                            compare[j][0] > compare[i][0] and compare[j][0] < compare[i][1]))):
                        r = 1
                    if (r == 1):
                        continue
                    s1 = ""
                    for a in range(0, len(Structures[0])):
                        if ((allcome[i][a] == '1' and allcome[j][a] == '0') or (
                                allcome[i][a] == '0' and allcome[j][a] == '1')):
                            s1 = s1 + '1'
                        if (allcome[i][a] == '0' and allcome[j][a] == '0'):
                            s1 = s1 + '0'
                    s = s1
                    allin.append(compare[j])
                    number.append(j)
                    for k in range(j + 1, len(Structures)):
                        r = 0
                        for a in range(0, len(Structures[0])):
                            if (s[a] == '1' and allcome[k][a] == '1'):
                                r = 1
                                break
                        if (r == 1):
                            continue
                        r = 0
                        for a in allin:
                            if (((compare[k][0] < a[0]) and (compare[k][1] > a[0] and compare[k][1] < a[1])) or (
                                    (compare[k][1] > a[1]) and (compare[k][0] > a[0] and compare[k][0] < a[1]))):
                                r = 1
                                break
                        if (r == 1):
                            continue
                        s1 = ""
                        for a in range(0, len(Structures[0])):
                            if ((s[a] == '1' and allcome[k][a] == '0') or (s[a] == '0' and allcome[k][a] == '1')):
                                s1 = s1 + '1'
                            if (s[a] == '0' and allcome[k][a] == '0'):
                                s1 = s1 + '0'
                        s = s1
                        allin.append(compare[k])
                        number.append(k)
                    s4 = Structures[number[0]]
                    for k in range(1, len(number)):
                        s5 = ""
                        s6 = Structures[number[k]]
                        for l in range(0, len(s)):
                            if (s4[l] == '.' and s6[l] == '.'):
                                s5 = s5 + '.'
                            if ((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                                s5 = s5 + '('
                            if ((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                                s5 = s5 + ')'
                        s4 = s5
                    allin = []
                    allin.append(compare[i])
                    number = []
                    number.append(i)
                    s = allcome[i]
                    allStructure.append(s4)
                if (len(number) == 1):
                    allStructure.append(Structures[number[0]])
                allin = []
                number = []
    return allStructure

# 长度在111到140之间的处理
def Processing_of_111(data1 , f):
    file = open(f, "r")
    content = file.readlines()
    Amm = []
    for i in content:
        Amm.append(i[:-1])
    A = []
    for i in Amm:
        lst = i.split(",")
        result = [float(item) for item in lst]
        A.append(result)
    s = data1
    a = len(A)
    b = len(A[0])
    for i in range(0 , a):
        for j in range(0 , b):
            if(A[i][j] > 0.988500):
                A[i][j] = 0
            elif(A[i][j] <= 0.988500):
                if(((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or ((s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or ((s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                    if(abs(i - j) > 2):
                        A[i][j] = 1
                    else:
                        A[i][j] = 0
                else:
                    A[i][j] = 0
    # 对配对矩阵进行茎区扩展
    # 针对上三角矩阵
    c = 1
    for i in range(0 , a):
        for j in range(c , b):
            count = 0
            if(A[i][j] == 1):
                k = i
                l = j
                count = 0
                while(True):
                    if(A[k][l] == 1):
                        count = count + 1
                    k = k + 1
                    l = l - 1
                    if(((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3) or A[k][l] == 0):
                        break
                if(count >= 2):
                    kk = i - 1
                    ll = j + 1
                    while(kk >= 0 and ll < b):
                        if((s[kk] == 'A' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'A') or (s[kk] == 'C' and s[ll] == 'G') or (s[kk] == 'G' and s[ll] == 'C') or (s[kk] == 'G' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'G')):
                            A[kk][ll] = 1
                        else:
                            break
                        kk = kk - 1
                        ll = ll + 1
                    while(True):
                        if((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                            if(((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3)):
                                break
                            else:
                                A[k][l] = 1
                        else:
                            break
                        k = k + 1
                        l = l - 1
        c = c + 1
    # 针对下三角矩阵
    c = 1
    for i in range(0 , a):
        for j in range(c , b):
            count = 0
            if(A[j][i] == 1):
                k = j
                l = i
                count = 0
                while(True):
                    if(A[k][l] == 1):
                        count = count + 1
                    k = k - 1
                    l = l + 1
                    if(((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3) or A[k][l] == 0):
                        break
                if(count >= 2):
                    kk = j + 1
                    ll = i - 1
                    while(kk < b and ll >= 0):
                        if((s[kk] == 'A' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'A') or (s[kk] == 'C' and s[ll] == 'G') or (s[kk] == 'G' and s[ll] == 'C') or (s[kk] == 'G' and s[ll] == 'U') or (s[kk] == 'U' and s[ll] == 'G')):
                            A[kk][ll] = 1
                            count = count + 1
                        else:
                            break
                        kk = kk + 1
                        ll = ll - 1
                    while(True):
                        if((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                            if(((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3)):
                                break
                            else:
                                A[k][l] = 1
                                count = count + 1
                        else:
                            break
                        k = k - 1
                        l = l + 1
        c = c + 1
    # 形成茎区
    # 针对上三角矩阵
    c = 1
    allStructure = []
    for i in range(0 , a):
        for j in range(c , b):
            q1 = []
            q2 = []
            count = 0
            if(A[i][j] == 1):
                k = i
                l = j
                count = 0
                while(True):
                    if(A[k][l] == 1):
                        count = count + 1
                        q1.append([k , l])
                        q2.append([k , l])
                    k = k + 1
                    l = l - 1
                    if(((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3) or A[k][l] == 0):
                        break
                if(count >= 2):
                    qq = ['.'] * len(A[0])
                    for z in q1:
                        qq[z[0]] = '('
                        qq[z[1]] = ')'
                    qq2 = ''
                    for z in qq:
                        qq2 = qq2 + z
                    allStructure.append(qq2)
                    q1.pop(0)
                    q2.pop()
                    while(len(q1) >= 2):
                        qqq1 = ['.'] * len(A[0])
                        qqq2 = ['.'] * len(A[0])
                        for z in q1:
                            qqq1[z[0]] = '('
                            qqq1[z[1]] = ')'
                        qq2 = ''
                        for z in qqq1:
                            qq2 = qq2 + z
                        allStructure.append(qq2)
                        for z in q2:
                            qqq2[z[0]] = '('
                            qqq2[z[1]] = ')'
                        qq2 = ''
                        for z in qqq2:
                            qq2 = qq2 + z
                        allStructure.append(qq2)
                        q1.pop(0)
                        q2.pop()
        c = c + 1
    # 针对下三角矩阵
    c = 1
    for i in range(0 , a):
        for j in range(c , b):
            q1 = []
            q2 = []
            count = 0
            if(A[j][i] == 1):
                k = j
                l = i
                count = 0
                while(True):
                    if(A[k][l] == 1):
                        count = count + 1
                        q1.append([k , l])
                        q2.append([k , l])
                    k = k - 1
                    l = l + 1
                    if(((abs(i - j) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(i - j) + 1) % 2 == 0 and abs(k - l) <= 3) or A[k][l] == 0):
                        break
                if(count >= 2):
                    qq = ['.'] * len(A[0])
                    for z in q1:
                        qq[z[1]] = '('
                        qq[z[0]] = ')'
                    qq2 = ''
                    for z in qq:
                        qq2 = qq2 + z
                    allStructure.append(qq2)
                    q1.pop(0)
                    q2.pop()
                    while(len(q1) >= 2):
                        qqq1 = ['.'] * len(A[0])
                        qqq2 = ['.'] * len(A[0])
                        for z in q1:
                            qqq1[z[1]] = '('
                            qqq1[z[0]] = ')'
                        qq2 = ''
                        for z in qqq1:
                            qq2 = qq2 + z
                        allStructure.append(qq2)
                        for z in q2:
                            qqq2[z[1]] = '('
                            qqq2[z[0]] = ')'
                        qq2 = ''
                        for z in qqq2:
                            qq2 = qq2 + z
                        allStructure.append(qq2)
                        q1.pop(0)
                        q2.pop()
        c = c + 1
    allStructure = list(set(allStructure))
    Structures = []
    for i in allStructure:
        Structures.append(i)
    # 对茎区按照配对数量从多到少进行排序，并且配对数量相同时，按照茎区长度排序
    pairCount = []
    structureLength = []
    for i in Structures:
        count = 0
        length = 0
        lock = 0
        for j in range(0 , len(i)):
            if(i[j] == '('):
                count = count + 1
            if((j == 0 and (i[j] == '(')) or (i[j] == '(' and i[j - 1] == '.')):
                lock = 1
            if((j == len(i) - 1 and i[j] == ')') or (i[j] == ')' and i[j + 1] == '.')):
                length = length + 1
                lock = 0
            if(lock == 1):
                length = length + 1
        pairCount.append(count)
        structureLength.append(length)
    maxPair = 0
    signChange = -1
    for i in range(0 , len(pairCount)):
        maxPair = pairCount[i]
        for j in range(i , len(pairCount)):
            if(pairCount[j] > maxPair):
                maxPair = pairCount[j]
                signChange = j
        if(signChange != -1):
            t = pairCount[i]
            pairCount[i] = pairCount[signChange]
            pairCount[signChange] = t
            t = Structures[i]
            Structures[i] = Structures[signChange]
            Structures[signChange] = t
            t = structureLength[i]
            structureLength[i] = structureLength[signChange]
            structureLength[signChange] = t
        signChange = -1
    i = 0
    while(i < len(pairCount)):
        if(i < len(pairCount) - 1 and pairCount[i] == pairCount[i + 1]):
            c = 0
            for j in range(i + 1 , len(pairCount)):
                if(j == len(pairCount) - 1 and pairCount[j] == pairCount[i]):
                    c = len(pairCount) - 1
                if(pairCount[j] != pairCount[i]):
                    c = j - 1
                    break
            a = i + 1
            for j in range(i , c):
                maxL = structureLength[j]
                x = -1
                for z in range(a , c + 1):
                    if(structureLength[z] > maxL):
                        maxL = structureLength[z]
                        x = z
                if(x != -1):
                    t = Structures[x]
                    Structures[x] = Structures[j]
                    Structures[j] = t
                    t = structureLength[x]
                    structureLength[x] = structureLength[j]
                    structureLength[j] = t
                a = a + 1
            i = c
        i = i + 1
    leftStructure = []
    rightStructure = []
    leftStructures = []
    rightStructures = []
    leftStructuresLength = []
    rightStructuresLength = []
    leftStructures_K = []
    rightStructure_K = []
    longStructure = []
    StartAndEnd = []
    SortStructure = []
    for i in Structures:
        p = 0
        q = 0
        K = 0
        count = 0
        lock = 1
        for j in range(0 , len(i)):
            if(j != 0 and i[j] == '.' and i[j - 1] == '('):
                lock = 0
            if(i[j] == ')' and i[j - 1] == '.'):
                lock = 1
            if(lock == 0 and i[j] == '.'):
                count = count + 1
            if(i[j] == '('):
                K = K + 1
            if(j == 0 and i[j] == '('):
                p = 0
            if(i[j] == '.' and i[j + 1] == '('):
                p = j + 1
            if((j == len(i) - 1) and i[j] == ')'):
                q = len(i) - 1
                break
            if(i[j] == ')' and i[j + 1] == '.'):
                q = j
                break
        length = q - p + 1
        if(count >= 92):
            a = 0
            b = 0
            for j in range(0 , len(i)):
                if(i[j] == '.'):
                    a = a + 1
                elif(i[j] == '('):
                    break
            for j in range(len(i) - 1 , -1 , -1):
                if(i[j] == '.'):
                    b = b + 1
                elif(i[j] == ')'):
                    break
            if(a <= 5 and b <= 9):
                StartAndEnd.append([p , q])
                Zero_One = ''
                for j in range(0 , len(i)):
                    if(i[j] == '(' or i[j] == ')'):
                        Zero_One = Zero_One + '1'
                    if(i[j] == '.'):
                        Zero_One = Zero_One + '0'
                longStructure.append(i)
                SortStructure.append(Zero_One)
        if(p >= 11 and q <= 70 and (length >= 52 and length <= 55)):
            leftStructure.append(i)
        elif(p >= 11 and q <= 70):
            leftStructures.append(i)
            leftStructuresLength.append(length)
            leftStructures_K.append(K)
        if(p >= 64 and q <= 112 and (length >= 30 and length <= 45)):
            rightStructure.append(i)
        elif(p >= 64 and q <= 112):
            rightStructures.append(i)
            rightStructuresLength.append(length)
            rightStructure_K.append(K)
        K = 0
    rootStartAndEnd,rootZero_One = StartAndEnd[0],SortStructure[0]
    rootAllin = []
    rootAllin.append(rootStartAndEnd)
    rootNumber = []
    rootNumber.append(0)
    for j in range(1 , len(longStructure)):
        r = 0
        for a in range(0 , len(rootZero_One)):
            if(rootZero_One[a] == '1' and SortStructure[j][a] == '1'):
                r = 1
                break
        if(r == 1):
            continue
        r = 0
        for a in rootAllin:
            if(((StartAndEnd[j][0] < a[0]) and (StartAndEnd[j][1] > a[0] and StartAndEnd[j][1] < a[1])) or ((StartAndEnd[j][1] > a[1]) and (StartAndEnd[j][0] > a[0] and StartAndEnd[j][0] < a[1]))):
                r = 1
                break
        if(r == 1):
            continue
        rootStructures = ''
        for a in range(0 , len(rootZero_One)):
            if((rootZero_One[a] == '1' and SortStructure[j][a] == '0') or (rootZero_One[a] == '0' and SortStructure[j][a] == '1')):
                rootStructures = rootStructures + '1'
            if(rootZero_One[a] == '0' and SortStructure[j][a] == '0'):
                rootStructures = rootStructures + '0'
        rootZero_One = rootStructures
        rootAllin.append(StartAndEnd[j])
        rootNumber.append(j)
    rootStructure = longStructure[rootNumber[0]]
    for j in range(1 , len(rootNumber)):
        rootStructure2 = ''
        rootStructure1 = longStructure[rootNumber[j]]
        for l in range(0 , len(rootStructure)):
            if(rootStructure[l] == '.' and rootStructure1[l] == '.'):
                rootStructure2 = rootStructure2 + '.'
            if((rootStructure[l] == '(' and rootStructure1[l] == '.') or (rootStructure[l] == '.' and rootStructure1[l] == '(')):
                rootStructure2 = rootStructure2 + '('
            if((rootStructure[l] == ')' and rootStructure1[l] == '.') or (rootStructure[l] == '.' and rootStructure1[l] == ')')):
                rootStructure2 = rootStructure2 + ')'
        rootStructure = rootStructure2
    judgeCount = 0
    judge = 0
    for i in range(0 , len(rootStructure)):
        if(rootStructure[i] == '('):
            judgeCount = judgeCount + 1
    if(judge == 0 and judgeCount >= 6):
        c = 1
        for i in range(0 , len(leftStructures) - 1):
            a = leftStructuresLength[i]
            s = -1
            maxL = a
            for j in range(c , len(leftStructures)):
                b = leftStructuresLength[j]
                if(maxL < b):
                    s = j
                    maxL = b
            if(s != -1):
                t = leftStructures[i]
                leftStructures[i] = leftStructures[s]
                leftStructures[s] = t
                t = leftStructuresLength[i]
                leftStructuresLength[i] = leftStructuresLength[s]
                leftStructuresLength[s] = t
                t = leftStructures_K[i]
                leftStructures_K[i] = leftStructures_K[s]
                leftStructures_K[s] = t
            c = c + 1
        i = 0
        while(i < len(leftStructuresLength)):
            if(i < len(leftStructuresLength) - 1 and leftStructuresLength[i] == leftStructuresLength[i + 1]):
                c = 0
                for j in range(i + 1 , len(leftStructuresLength)):
                    if(j == len(leftStructuresLength) - 1 and leftStructuresLength[j] == leftStructuresLength[i]):
                        c = len(leftStructuresLength) - 1
                    if(leftStructuresLength[j] != leftStructuresLength[i]):
                        c = j - 1
                        break
                a = i + 1
                for j in range(i , c):
                    maxL = leftStructures_K[j]
                    x = -1
                    for z in range(a , c + 1):
                        if(leftStructures_K[z] > maxL):
                            maxL = leftStructures_K[z]
                            x = z
                    if(x != -1):
                        t = leftStructures[x]
                        leftStructures[x] = leftStructures[j]
                        leftStructures[j] = t
                        t = leftStructures_K[x]
                        leftStructures_K[x] = leftStructures_K[j]
                        leftStructures_K[j] = t
                    a = a + 1
                i = c
            i = i + 1
        c = 1
        for i in range(0 , len(rightStructures) - 1):
            a = rightStructuresLength[i]
            s = -1
            maxL = a
            for j in range(c , len(rightStructures)):
                b = rightStructuresLength[j]
                if(maxL < b):
                    s = j
                    maxL = b
            if(s != -1):
                t = rightStructures[i]
                rightStructures[i] = rightStructures[s]
                rightStructures[s] = t
                t = rightStructuresLength[i]
                rightStructuresLength[i] = rightStructuresLength[s]
                rightStructuresLength[s] = t
                t = rightStructure_K[i]
                rightStructure_K[i] = rightStructure_K[s]
                rightStructure_K[s] = t
            c = c + 1
        i = 0
        while(i < len(rightStructuresLength)):
            if(i < len(rightStructuresLength) - 1 and rightStructuresLength[i] == rightStructuresLength[i + 1]):
                c = 0
                for j in range(i + 1 , len(rightStructuresLength)):
                    if(j == len(rightStructuresLength) - 1 and rightStructuresLength[j] == rightStructuresLength[i]):
                        c = len(rightStructuresLength) - 1
                    if(rightStructuresLength[j] != rightStructuresLength[i]):
                        c = j - 1
                        break
                a = i + 1
                for j in range(i , c):
                    maxL = rightStructure_K[j]
                    x = -1
                    for z in range(a , c + 1):
                        if(rightStructure_K[z] > maxL):
                            maxL = rightStructure_K[z]
                            x = z
                    if(x != -1):
                        t = rightStructures[x]
                        rightStructures[x] = rightStructures[j]
                        rightStructures[j] = t
                        t = rightStructure_K[x]
                        rightStructure_K[x] = rightStructure_K[j]
                        rightStructure_K[j] = t
                    a = a + 1
                i = c
            i = i + 1
    else:
        judge = 1
    if(judge == 0):
        p = 0
        q = 0
        rootPair = []
        for i in range(0 , len(rootStructure)):
            if(rootStructure[i] == '(' and rootStructure[i + 1] == '.'):
                p = i
            if(rootStructure[i] == '.' and rootStructure[i + 1] == ')'):
                q = i + 1
                break
        rootPair.append([p , q])
        leftRootStructure = ''
        for i in range(len(leftStructure) - 1 , -1 , -1):
            if(leftStructure[i][rootPair[0][0] + 5] == '(' and leftStructure[i][rootPair[0][0] + 4] == '.'):
                leftRootStructure = leftStructure[i]
                break
        if(leftRootStructure == ''):
            for i in range(len(leftStructure) - 1 , -1 , -1):
                if(leftStructure[i][rootPair[0][0] + 4] == '(' and leftStructure[i][rootPair[0][0] + 3] == '.'):
                    leftRootStructure = leftStructure[i]
                    break
    else:
        judge = 1
    rightRootStructure = ''
    if(judge == 0 and leftRootStructure != ''):
        leftEnd = 0
        for i in range(0 , len(leftRootStructure)):
            if(leftRootStructure[i] == ')' and leftRootStructure[i + 1] == '.'):
                leftEnd = i
                break
        # rightRootStructure = ''
        for i in rightStructure:
            rightEnd = 0
            if(i[leftEnd + 1] == '.' and i[leftEnd + 2] == '('):
                for j in range(0 , len(i)):
                    if(i[j] == ')' and i[j + 1] == '.'):
                        rightEnd = j
                        break
            if(rightEnd >= (rootPair[0][1] - 3) and rightEnd <= (rootPair[0][1] - 1)):
                rightRootStructure = i
                break
        if(rightRootStructure == ''):
            for i in rightStructure:
                rightEnd = 0
                if(i[leftEnd + 2] == '.' and i[leftEnd + 3] == '('):
                    for j in range(0 , len(i)):
                        if(i[j] == ')' and i[j + 1] == '.'):
                            rightEnd = j
                            break
                if(rightEnd >= (rootPair[0][1] - 3) and rightEnd <= (rootPair[0][1] - 1)):
                    rightRootStructure = i
                    break
        if(rightRootStructure == ''):
            for i in range(len(leftStructure) - 1 , -1 , -1):
                if(leftStructure[i][rootPair[0][0] + 4] == '(' and leftStructure[i][rootPair[0][0] + 3] == '.'):
                    leftRootStructure = leftStructure[i]
                    break
            leftEnd = 0
            for i in range(0 , len(leftRootStructure)):
                if(leftRootStructure[i] == ')' and leftRootStructure[i + 1] == '.'):
                    leftEnd = i
                    break
            for i in rightStructure:
                rightEnd = 0
                if(i[leftEnd + 1] == '.' and i[leftEnd + 2] == '('):
                    for j in range(0 , len(i)):
                        if(i[j] == ')' and i[j + 1] == '.'):
                            rightEnd = j
                            break
                if(rightEnd >= (rootPair[0][1] - 3) and rightEnd <= (rootPair[0][1] - 1)):
                    rightRootStructure = i
                    break
    else:
        judge = 1
    if(judge == 0 and rightRootStructure != ''):
        p = 0
        q = 0
        leftBottom = []
        for i in range(0 , len(leftRootStructure)):
            if(leftRootStructure[i] == '(' and leftRootStructure[i + 1] == '.'):
                p = i
            if(leftRootStructure[i] == '.' and leftRootStructure[i + 1] == ')'):
                q = i + 1
                break
        leftBottom = [p , q]
        p = 0
        q = 0
        rightBottom = []
        for i in range(0 , len(rightRootStructure)):
            if(rightRootStructure[i] == '(' and rightRootStructure[i + 1] == '.'):
                p = i
            if(rightRootStructure[i] == '.' and rightRootStructure[i + 1] == ')'):
                q = i + 1
                break
        rightBottom = [p , q]
        rootStructure = list(rootStructure)
        for i in range(0 , len(rootStructure)):
            if(rootStructure[i] == '.' and (leftRootStructure[i] == '(' or rightRootStructure[i] == '(')):
                rootStructure[i] = '('
            if(rootStructure[i] == '.' and (leftRootStructure[i] == ')' or rightRootStructure[i] == ')')):
                rootStructure[i] = ')'
        rootStructures = ''
        for i in rootStructure:
            rootStructures = rootStructures + i
        leftOut = []
        leftIn = []
        p1 = 0
        q1 = 0
        p2 = 0
        q2 = 0
        for i in range(0 , len(leftStructures)):
            for j in range(0 , len(leftStructures[i])):
                if(leftStructures[i][j] == '.' and leftStructures[i][j + 1] == '('):
                    p1 = j + 1
                if(leftStructures[i][j] == '(' and leftStructures[i][j + 1] == '.'):
                    p2 = j
                if(leftStructures[i][j] == ')' and leftStructures[i][j + 1] == '.'):
                    q1 = j
                    break
                if(leftStructures[i][j] == '.' and leftStructures[i][j + 1] == ')'):
                    q2 = j + 1
            leftOut.append([p1 , q1])
            leftIn.append([p2 , q2])
        rightOut = []
        rightIn = []
        p1 = 0
        q1 = 0
        p2 = 0
        q2 = 0
        for i in range(0 , len(rightStructures)):
            for j in range(0 , len(rightStructures[i])):
                if(rightStructures[i][j] == '.' and rightStructures[i][j + 1] == '('):
                    p1 = j + 1
                if(rightStructures[i][j] == '(' and rightStructures[i][j + 1] == '.'):
                    p2 = j
                if(rightStructures[i][j] == ')' and rightStructures[i][j + 1] == '.'):
                    q1 = j
                    break
                if(rightStructures[i][j] == '.' and rightStructures[i][j + 1] == ')'):
                    q2 = j + 1
            rightOut.append([p1 , q1])
            rightIn.append([p2 , q2])
        leftAll = []
        for i in range(0 , len(leftOut)):
            if(leftOut[i][0] > leftBottom[0] and leftOut[i][1] < leftBottom[1] and abs((leftOut[i][0] - leftBottom[0]) - (leftBottom[1] - leftOut[i][1])) <= 2):
                leftBottom = leftIn[i]
                leftAll.append(i)
        rightAll = []
        for i in range(0 , len(rightOut)):
            if(rightOut[i][0] > rightBottom[0] and rightOut[i][1] < rightBottom[1] and abs((rightOut[i][0] - rightBottom[0]) - (rightBottom[1] - rightOut[i][1])) <= 2):
                rightBottom = rightIn[i]
                rightAll.append(i)
        rootStructure = list(rootStructure)
        for i in leftAll:
            for j in range(0 , len(rootStructure)):
                if(rootStructure[j] == '.' and leftStructures[i][j] == '('):
                    rootStructure[j] = '('
                if(rootStructure[j] == '.' and leftStructures[i][j] == ')'):
                    rootStructure[j] = ')'
        for i in rightAll:
            for j in range(0 , len(rootStructure)):
                if(rootStructure[j] == '.' and rightStructures[i][j] == '('):
                    rootStructure[j] = '('
                if(rootStructure[j] == '.' and rightStructures[i][j] == ')'):
                    rootStructure[j] = ')'
        rootStructures = ''
        for i in rootStructure:
            rootStructures = rootStructures + i
        return rootStructures
    else:
        judge = 1
    if(judge == 1):
        file = open(f, "r")
        content = file.readlines()
        Amm = []
        for i in content:
            Amm.append(i[:-1])
        B = []
        for i in Amm:
            lst = i.split(",")
            result = [float(item) for item in lst]
            B.append(result)
        s = data1
        A = B
        a = len(A)
        b = len(A[0])
        for i in range(0 , a):
            for j in range(0 , b):
                if(A[i][j] > 0.988500):
                    A[i][j] = 0
                elif(A[i][j] <= 0.988500):
                    if(((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or ((s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or ((s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                        if(abs(i - j) > 2):
                            A[i][j] = 1
                        else:
                            A[i][j] = 0
                    else:
                        A[i][j] = 0
        c = 1
        w = []
        for i in range(0 , a):
            for j in range(c , b):
                q = []
                count = 0
                if(A[i][j] == 1):
                    z = i
                    x = j
                    while z >= 0 and x < b and (A[z][x] == 1):
                        q.append([z , x])
                        count = count + 1
                        z = z - 1
                        x = x + 1
                if count >= 2:
                    w.append(q)
            c = c + 1
        Structure = []
        for i in w:
            s = ['.'] * a
            for j in i:
                s[j[0]] = '('
                s[j[1]] = ')'
            l = ''
            for k in s:
                l = l + k
            Structure.append(l)
        c = 1
        w = []
        for i in range(0 , a):
            for j in range(c , b):
                q = []
                count = 0
                if(A[j][i] == 1):
                    z = i
                    x = j
                    while x < b and z >= 0 and (A[x][z] == 1):
                        q.append([z , x])
                        count = count + 1
                        x = x + 1
                        z = z - 1
                if(count >= 2):
                    w.append(q)
            c = c + 1
        Structure1 = []
        for i in w:
            s = ['.'] * a
            for j in i:
                s[j[0]] = '('
                s[j[1]] = ')'
            l = ''
            for k in s:
                l = l + k
            Structure1.append(l)
        Structure = Structure1 + Structure
        Structures = list(set(Structure))
        pairCount = []
        structureLength = []
        for i in Structures:
            count = 0
            length = 0
            lock = 0
            for j in range(0 , len(i)):
                if(i[j] == '('):
                    count = count + 1
                if((j == 0 and (i[j] == '(')) or (i[j] == '(' and i[j - 1] == '.')):
                    lock = 1
                if((j == len(i) - 1 and i[j] == ')') or (i[j] == ')' and i[j + 1] == '.')):
                    length = length + 1
                    lock = 0
                if(lock == 1):
                    length = length + 1
            pairCount.append(count)
            structureLength.append(length)
        maxPair = 0
        signChange = -1
        for i in range(0 , len(pairCount)):
            maxPair = pairCount[i]
            for j in range(i , len(pairCount)):
                if(pairCount[j] > maxPair):
                    maxPair = pairCount[j]
                    signChange = j
            if(signChange != -1):
                t = pairCount[i]
                pairCount[i] = pairCount[signChange]
                pairCount[signChange] = t
                t = Structures[i]
                Structures[i] = Structures[signChange]
                Structures[signChange] = t
                t = structureLength[i]
                structureLength[i] = structureLength[signChange]
                structureLength[signChange] = t
            signChange = -1
        i = 0
        while(i < len(pairCount)):
            if(i < len(pairCount) - 1 and pairCount[i] == pairCount[i + 1]):
                c = 0
                for j in range(i + 1 , len(pairCount)):
                    if(j == len(pairCount) - 1 and pairCount[j] == pairCount[i]):
                        c = len(pairCount) - 1
                    if(pairCount[j] != pairCount[i]):
                        c = j - 1
                        break
                a = i + 1
                for j in range(i , c):
                    maxL = structureLength[j]
                    x = -1
                    for z in range(a , c + 1):
                        if(structureLength[z] > maxL):
                            maxL = structureLength[z]
                            x = z
                    if(x != -1):
                        t = Structures[x]
                        Structures[x] = Structures[j]
                        Structures[j] = t
                        t = structureLength[x]
                        structureLength[x] = structureLength[j]
                        structureLength[j] = t
                    a = a + 1
                i = c
            i = i + 1
        Structure = []
        for i in Structures:
            count = 0
            for j in range(0 , len(i)):
                if(i[j] == '('):
                    count = 0
                if(i[j] == '.'):
                    count = count + 1
                if(i[j] == ')' and count > 2):
                    Structure.append(i)
                    break
        Structures = []
        for i in Structure:
            Structures.append(i)
        allcome = []
        compare = []
        for i in Structures:
            s = ""
            for j in range(0 , len(i)):
                if(i[j] == '(' or i[j] == ')'):
                    s = s + '1'
                elif(i[j] == '.'):
                    s = s + '0'
            allcome.append(s)
            p = 0
            q = 0
            t = 0
            for j in range(0 , len(i)):
                if(j == 0 and i[j] == '('):
                    p = 0
                if(i[j] == '('):
                    t = t + 1
                if((j == len(i) - 1) and i[j] == ')'):
                    q = len(i) - 1
                    break
                if(i[j] == ')' and i[j + 1] == '.'):
                    q = j
                    break
                if(i[j] == '.' and i[j + 1] == '('):
                    p = j + 1
                if(i[j] == ')' and i[j + 1] == '.'):
                    q = j
            compare.append([p , q , t])
        allin = []
        allStructure = []
        number = []
        for i in range(0 , 20):
            s = allcome[i]
            allin.append(compare[i])
            number.append(i)
            for j in range(i + 1 , len(Structures)):
                r = 0
                for a in range(0 , len(Structures[0])):
                    if(allcome[i][a] == '1' and allcome[j][a] == '1'):
                        r = 1
                        break
                if(r == 1):
                    continue
                r = 0
                if(((compare[j][0] < compare[i][0]) and (compare[j][1] > compare[i][0] and compare[j][1] < compare[i][1])) or ((compare[j][1] > compare[i][1]) and (compare[j][0] > compare[i][0] and compare[j][0] < compare[i][1]))):
                    r = 1
                if(r == 1):
                    continue
                s1 = ""
                for a in range(0 , len(Structures[0])):
                    if((allcome[i][a] == '1' and allcome[j][a] == '0') or (allcome[i][a] == '0' and allcome[j][a] == '1')):
                        s1 = s1 + '1'
                    if(allcome[i][a] == '0' and allcome[j][a] == '0'):
                        s1 = s1 + '0'
                s = s1
                allin.append(compare[j])
                number.append(j)
                for k in range(j + 1 , len(Structures)):
                    r = 0
                    for a in range(0 , len(Structures[0])):
                        if(s[a] == '1' and allcome[k][a] == '1'):
                            r = 1
                            break
                    if(r == 1):
                        continue
                    r = 0
                    for a in allin:
                        if(((compare[k][0] < a[0]) and (compare[k][1] > a[0] and compare[k][1] < a[1])) or ((compare[k][1] > a[1]) and (compare[k][0] > a[0] and compare[k][0] < a[1]))):
                            r = 1
                            break
                    if(r == 1):
                        continue
                    s1 = ""
                    for a in range(0 , len(Structures[0])):
                        if((s[a] == '1' and allcome[k][a] == '0') or (s[a] == '0' and allcome[k][a] == '1')):
                            s1 = s1 + '1'
                        if(s[a] == '0' and allcome[k][a] == '0'):
                            s1 = s1 + '0'
                    s = s1
                    allin.append(compare[k])
                    number.append(k)
                s4 = Structures[number[0]]
                for k in range(1 , len(number)):
                    s5 = ""
                    s6 = Structures[number[k]]
                    for l in range(0 , len(s)):
                        if(s4[l] == '.' and s6[l] == '.'):
                            s5 = s5 + '.'
                        if((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                            s5 = s5 + '('
                        if((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                            s5 = s5 + ')'
                    s4 = s5
                allin = []
                allin.append(compare[i])
                number = []
                number.append(i)
                s = allcome[i]
                allStructure.append(s4)
            if(len(number) == 1):
                allStructure.append(Structures[number[0]])
            allin = []
            number = []
        bestStructure = ""
        powerful1 = 1000000
        for i in allStructure:
            power = lowerpower(data1 , i)
            if(power < powerful1):
                powerful1 = power
                bestStructure = i
        return bestStructure

# 长度在140以上的处理
def Processing_of_140(data , f):
    compair = 0
    if(len(data) <= 200):
        compair = 0.987564
    if(len(data) > 200 and len(data) <= 300):
        compair = 0.991129
    s = data
    file = open(f, "r")
    content = file.readlines()
    Amm = []
    for i in content:
        Amm.append(i[:-1])
    A = []
    for i in Amm:
        lst = i.split(",")
        result = [float(item) for item in lst]
        A.append(result)
    a = len(A)
    b = len(A[0])
    for i in range(0 , a):
        for j in range(0 , b):
            if(A[i][j] > compair):
                A[i][j] = 0
            elif(A[i][j] <= compair):
                if(((s[i] == 'A') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'A')) or ((s[i] == 'G') and (s[j] == 'C')) or ((s[i] == 'C') and (s[j] == 'G')) or ((s[i] == 'G') and (s[j] == 'U')) or ((s[i] == 'U') and (s[j] == 'G'))):
                    if(abs(i - j) > 3):
                        A[i][j] = 1
                    else:
                        A[i][j] = 0
                else:
                    A[i][j] = 0
    # 对配对矩阵进行茎区扩展
    # 针对上三角矩阵
    # 定义kk和ll保存茎区最外侧的配对碱基位置
    kk = 0
    ll = 0
    allStructure = []
    c = 1
    for i in range(0 , a):
        for j in range(c , b):
            q1 = []
            count = 0
            if(A[i][j] == 1):
                k = i - 1
                l = j + 1
                # 对茎区进行外部碱基扩展
                while(k >= 0 and l < b):
                    if((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                        A[k][l] = 1
                    else:
                        break
                    k = k - 1
                    l = l + 1
                kk = k
                ll = l
                k = i + 1
                l = j - 1
                # 对茎区进行内部碱基扩展
                while(True):
                    if((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                        if(((abs(kk - ll) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(kk - ll) + 1) % 2 == 0 and abs(k - l) <= 3)):
                            break
                        else:
                            A[k][l] = 1
                    else:
                        break
                    k = k + 1
                    l = l - 1
        c = c + 1
    # 针对下三角矩阵
    c = 1
    for i in range(0 , a):
        for j in range(c , b):
            count = 0
            q1 = []
            if(A[j][i] == 1):
                k = j + 1
                l = i - 1
                # 对茎区进行外部扩展
                while(k < b and l >= 0):
                    if((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                        A[k][l] = 1
                    else:
                        break
                    k = k + 1
                    l = l - 1
                kk = k
                ll = l
                k = j - 1
                l = i + 1
                # 对茎区进行内部扩展
                while(True):
                    if((s[k] == 'A' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'A') or (s[k] == 'C' and s[l] == 'G') or (s[k] == 'G' and s[l] == 'C') or (s[k] == 'G' and s[l] == 'U') or (s[k] == 'U' and s[l] == 'G')):
                        if(((abs(kk - ll) + 1) % 2 == 1 and abs(k - l) <= 2) or ((abs(kk - ll) + 1) % 2 == 0 and abs(k - l) <= 3)):
                            break
                        else:
                            A[k][l] = 1
                    else:
                        break
                    k = k - 1
                    l = l + 1
        c = c + 1
    # 生成茎区并添加进茎区池中
    # 针对上三角矩阵
    c = 1
    w = []
    for i in range(0 , a):
        for j in range(c , b):
            q = []
            count = 0
            if(A[i][j] == 1):
                z = i
                x = j
                while((z < b) and (x >= 0) and (A[z][x] == 1)):
                    q.append([z , x])
                    A[z][x] = 0
                    count = count + 1
                    z = z + 1
                    x = x - 1
            if(count >= 3):
                w.append(q)
        c = c + 1
    Structure = []
    for i in w:
        s = ['.'] * a
        for j in i:
            s[j[0]] = '('
            s[j[1]] = ')'
        l = ''
        for k in s:
            l = l + k
        Structure.append(l)
    c = 1
    w = []
    for i in range(0 , a):
        for j in range(c , b):
            q = []
            count = 0
            if(A[j][i] == 1):
                z = i
                x = j
                while z < b and x >= 0 and (A[x][z] == 1):
                    q.append([z , x])
                    A[x][z] = 0
                    count = count + 1
                    x = x - 1
                    z = z + 1
            if(count >= 3):
                w.append(q)
        c = c + 1
    Structure1 = []
    for i in w:
        s = ['.'] * a
        for j in i:
            s[j[0]] = '('
            s[j[1]] = ')'
        l = ''
        for k in s:
            l = l + k
        Structure1.append(l)
    Structure = Structure1 + Structure
    Structures = list(set(Structure))
    allcome = []
    compare = []
    for i in Structures:
        s = ""
        for j in range(0 , len(i)):
            if(i[j] == '(' or i[j] == ')'):
                s = s + '1'
            elif(i[j] == '.'):
                s = s + '0'
        allcome.append(s)
        p = 0
        q = 0
        t = 0
        for j in range(0 , len(i)):
            if(j == 0 and i[j] == '('):
                p = 0
            if(i[j] == '('):
                t = t + 1
            if((j == len(i) - 1) and i[j] == ')'):
                q = len(i) - 1
                break
            if(i[j] == ')' and i[j + 1] == '.'):
                q = j
                break
            if(i[j] == '.' and i[j + 1] == '('):
                p = j + 1
            if(i[j] == ')' and i[j + 1] == '.'):
                q = j
        compare.append([p , q , t])
    compare2 = []
    # 统计茎区内部配对
    for i in Structures:
        p = 0
        q = 0
        lock = 1
        point = 0
        for j in range(0 , len(i)):
            if(i[j] == '(' and i[j + 1] == '.'):
                p = j
                lock = 0
            if(i[j] == '.' and lock == 0):
                point = point + 1
            if(i[j] == '.' and i[j + 1] == ')'):
                q = j + 1
                break
        compare2.append([p , q , point])
    # 对茎区按照配对数量从多到少进行排序，并且配对数量相同时，按照茎区长度排序
    pairCount = []
    structureLength = []
    for i in Structures:
        count = 0
        length = 0
        lock = 0
        for j in range(0 , len(i)):
            if(i[j] == '('):
                count = count + 1
            if((j == 0 and (i[j] == '(')) or (i[j] == '(' and i[j - 1] == '.')):
                lock = 1
            if((j == len(i) - 1 and i[j] == ')') or (i[j] == ')' and i[j + 1] == '.')):
                length = length + 1
                lock = 0
            if(lock == 1):
                length = length + 1
        pairCount.append(count)
        structureLength.append(length)
    maxPair = 0
    signChange = -1
    for i in range(0 , len(pairCount)):
        maxPair = pairCount[i]
        for j in range(i , len(pairCount)):
            if(pairCount[j] > maxPair):
                maxPair = pairCount[j]
                signChange = j
        if(signChange != -1):
            t = pairCount[i]
            pairCount[i] = pairCount[signChange]
            pairCount[signChange] = t
            t = Structures[i]
            Structures[i] = Structures[signChange]
            Structures[signChange] = t
            t = structureLength[i]
            structureLength[i] = structureLength[signChange]
            structureLength[signChange] = t
        signChange = -1
    i = 0
    while(i < len(pairCount)):
        if(i < len(pairCount) - 1 and pairCount[i] == pairCount[i + 1]):
            c = 0
            for j in range(i + 1 , len(pairCount)):
                if(j == len(pairCount) - 1 and pairCount[j] == pairCount[i]):
                    c = len(pairCount) - 1
                if(pairCount[j] != pairCount[i]):
                    c = j - 1
                    break
            a = i + 1
            for j in range(i , c):
                maxL = structureLength[j]
                x = -1
                for z in range(a , c + 1):
                    if(structureLength[z] > maxL):
                        maxL = structureLength[z]
                        x = z
                if(x != -1):
                    t = Structures[x]
                    Structures[x] = Structures[j]
                    Structures[j] = t
                    t = structureLength[x]
                    structureLength[x] = structureLength[j]
                    structureLength[j] = t
                a = a + 1
            i = c
        i = i + 1
    allcome = []
    compare = []
    for i in Structures:
        s = ""
        for j in range(0 , len(i)):
            if(i[j] == '(' or i[j] == ')'):
                s = s + '1'
            elif(i[j] == '.'):
                s = s + '0'
        allcome.append(s)
        p = 0
        q = 0
        t = 0
        for j in range(0 , len(i)):
            if(j == 0 and i[j] == '('):
                p = 0
            if(i[j] == '('):
                t = t + 1
            if((j == len(i) - 1) and i[j] == ')'):
                q = len(i) - 1
                break
            if(i[j] == ')' and i[j + 1] == '.'):
                q = j
                break
            if(i[j] == '.' and i[j + 1] == '('):
                p = j + 1
            if(i[j] == ')' and i[j + 1] == '.'):
                q = j
        compare.append([p , q , t])
    compare2 = []
    # 统计茎区内部配对
    for i in Structures:
        p = 0
        q = 0
        lock = 1
        point = 0
        for j in range(0 , len(i)):
            if(i[j] == '(' and i[j + 1] == '.'):
                p = j
                lock = 0
            if(i[j] == '.' and lock == 0):
                point = point + 1
            if(i[j] == '.' and i[j + 1] == ')'):
                q = j + 1
                break
        compare2.append([p , q , point])
    variation = []
    for i in range(0 , len(Structures)):
        if(compare2[i][2] <= 8 or compare[i][2] <= 2):
            variation.append('NO')
        if(compare2[i][2] > 8 or compare[i][2] > 2):
            variation.append('YES')
    allstructure = []
    lowerP = []
    ii = 0
    while(ii < 40):
        Structures2 = []
        for i in Structures:
            Structures2.append(i)
        # 用于保存相容茎区的起始位置和结束位置以及配对数
        allin = []
        # 用于保存相容茎区的内部起始位置和内部结束位置
        allin2 = []
        # 保存茎区相容所有的结果
        allStructure = []
        # 保存相容的茎区号
        number = []
        # 保存替换删除的茎区
        delRoot = []
        # 保存相容后茎区的结构
        rootStructure = ""
        # 保存最小自由能对应的茎区
        lowerSStructure = []
        # 保存相容的茎区
        SStructure = []
        # 保存最小自由能对应的茎区号
        lowernumber = []
        # 用于保存最小自由能对应的茎区的起始位置和结束位置
        lowerallin = []
        # 用于保存最小自由能对应的茎区的内部起始位置和内部结束位置
        lowerallin2 = []
        # 保存当前迭代的二级结构
        rootStructure2 = ""
        # 保存最小自由能对应的茎区号
        lowernumber2 = []
        # 用于保存最小自由能对应的茎区的内部起始位置和内部结束位置
        T_lowernumber = []
        # 用于保存最小自由能对应的茎区的内部起始位置和内部结束位置
        T_lowerallin = []
        # 用于保存最小自由能对应的茎区的内部起始位置和内部结束位置
        T_lowerallin2 = []
        # 用于保存最小自由能对应的茎区
        T_lowerSStructure = []
        # 用于保存相容后的0，1序列
        s = ""
        s4 = ""
        s7 = ""
        i = 1
        str1 = data
        slist = []
        # 保存最小自由能对应的结构
        lowerStructure = ""
        lowerStructure2 = ""
        lower = 0
        lower2 = 0
        # 整体跑1000次
        while(i < 1000):
            # 当发现是第一次进行相容时
            if(i == 0):
                rootStructure = Structures2[0]
                # 将根茎区对应的0，1序列作为第一个茎区的序列
                s = allcome[0]
                # 将第一个茎区对应的起始和结束位置以及配对数保存下来
                inner = compare[0][0]
                out = compare[0][1]
                pair = compare[0][2]
                allin.append([inner , out , pair])
                # 将第一个茎区内部对应的起始和结束位置保存下来
                inner = compare2[0][0]
                out = compare2[0][1]
                allin2.append([inner , out])
                # 保存相容茎区的序号
                number.append(0)
                # 将茎区添加进茎区池中
                SStructure.append(Structures2[0])
            elif(number == []):
                # 当茎区全部被删除时，重新在2号茎区池中选择根茎区，来进行下一步的茎区相容操作
                for j in range(0 , len(Structures2)):
                    # 找到之前没有相容过的第一个茎区
                    if(Structures2[j] != '0'):
                        # 与第一次相容时的操作一样
                        rootStructure = Structures2[j]
                        s = allcome[j]
                        # 添加第一个不为0的茎区的起始和结束位置以及配对数
                        inner = compare[j][0]
                        out = compare[j][1]
                        pair = compare[j][2]
                        allin.append([inner , out , pair])
                        # 添加第一个不为0的茎区的编号
                        number.append(j)
                        # 添加第一个不为0的茎区的内部的起始和结束位置
                        inner = compare2[j][0]
                        out = compare2[j][1]
                        pair = compare2[j][2]
                        allin2.append([inner , out , pair])
                        # 添加第一个不为0的茎区
                        SStructure.append(Structures2[j])
                        break
            else:
                # 正常情况下正常处理
                # 将删除一些茎区后的二级结构变为0，1序列
                s = ""
                for j in range(0 , len(rootStructure)):
                    if(rootStructure[j] == '(' or rootStructure[j] == ')'):
                        s = s + '1'
                    if(rootStructure[j] == '.'):
                        s = s + '0'
            # 与其余的茎区进行相容操作
            for j in range(0 , len(Structures2)):
                if(Structures2[j] == '0'):
                    continue
                r = 0
                for a in range(0 , len(Structures[0])):
                    if(s[a] == '1' and allcome[j][a] == '1'):
                        r = 1
                        break
                if(r == 1):
                    continue
                r = 0
                for a in allin:
                    if(((compare[j][0] < a[0]) and (compare[j][1] > a[0] and compare[j][1] < a[1])) or ((compare[j][1] > a[1]) and (compare[j][0] > a[0] and compare[j][0] < a[1]))):
                        r = 1
                        break
                if(r == 1):
                    continue
                s1 = ""
                for a in range(0 , len(Structures[0])):
                    if((s[a] == '1' and allcome[j][a] == '0') or (s[a] == '0' and allcome[j][a] == '1')):
                        s1 = s1 + '1'
                    if(s[a] == '0' and allcome[j][a] == '0'):
                        s1 = s1 + '0'
                s = s1
                s4 = ""
                for l in range(0 , len(rootStructure)):
                    if(rootStructure[l] == '.' and Structures2[j][l] == '.'):
                        s4 = s4 + '.'
                    if((rootStructure[l] == '(' and Structures2[j][l] == '.') or (rootStructure[l] == '.' and Structures2[j][l] == '(')):
                        s4 = s4 + '('
                    if((rootStructure[l] == ')' and Structures2[j][l] == '.') or (rootStructure[l] == '.' and Structures2[j][l] == ')')):
                        s4 = s4 + ')'
                rootStructure = s4
                # 将相容得到的茎区的相关信息进行添加
                inner = compare[j][0]
                out = compare[j][1]
                pair = compare[j][2]
                allin.append([inner , out , pair])
                inner = compare2[j][0]
                out = compare2[j][1]
                pair = compare2[j][2]
                allin2.append([inner , out , pair])
                number.append(j)
                SStructure.append(Structures2[j])
            # 当前的二级结构的自由能是最小时
            if(lowerpower(str1 , rootStructure) < lower):
                # 将当前自由能，二级结构以及茎区相关信息进行保存
                lower = lowerpower(str1 , rootStructure)
                lowerStructure = rootStructure
                lowerallin = []
                for j in allin:
                    inner = j[0]
                    out = j[1]
                    pair = j[2]
                    lowerallin.append([inner , out , pair])
                lowernumber = []
                for j in number:
                    lowernumber.append(j)
                lowerallin2 = []
                for j in allin2:
                    inner = j[0]
                    out = j[1]
                    lowerallin2.append([inner , out])
                lowerSStructure = []
                for j in SStructure:
                    lowerSStructure.append(j)
                allStructure.append(rootStructure)
            # 当前的自由能比最小自由能大时
            elif(lowerpower(str1 , rootStructure) > lower):
                # 若当前的最小自由能与最小自由能之差在一定范围时，保存这个的二级结构，并进行迭代
                if((lowerpower(str1 , rootStructure) - lower) < (len(str1)/(10 * i))):
                    rootStructure2 = rootStructure
                    lowerStructure2 = rootStructure
                    lower2 = lowerpower(str1 , rootStructure)
                    # 保存迭代二级结构的相关信息
                    T_lowernumber = []
                    for j in number:
                        T_lowernumber.append(j)
                    T_lowerallin = []
                    for j in allin:
                        inner = j[0]
                        out = j[1]
                        pair = j[2]
                        T_lowerallin.append([inner , out , pair])
                    T_lowerallin2 = []
                    for j in allin2:
                        inner = j[0]
                        out = j[1]
                        T_lowerallin2.append([inner , out])
                    T_lowerSStructure = []
                    for j in SStructure:
                        T_lowerSStructure.append(j)
                    # 正式进行迭代
                    ll = 1
                    while(ll < 101):
                        # 若被删除的茎区池不为空，则将刚刚删除的茎区恢复到原来的位置
                        if(delRoot != []):
                            for j in range(0 , len(delRoot)):
                                Structures2[delRoot[j]] = Structures[delRoot[j]]
                        # 将已经相容的茎区对应到第二个茎区池的位置置为0
                        for j in range(0 , len(number)):
                            Structures2[number[j]] = '0'
                        # 生成随机数
                        random_numbers = [random.random() for _ in range(len(number))]
                        # 将删除的茎区编号保存下来，并将相应的列表中的元素置为-1
                        delRoot = []
                        numberlength = len(number)
                        for j in range(0 , numberlength):
                            if(random_numbers[j] > 0.5):
                                delRoot.append(number[j])
                                allin[j] = -1
                                number[j] = -1
                                allin2[j] = -1
                                SStructure[j] = -1
                        # 删除列表中值为-1的元素
                        new_list = [x for x in number if x != -1]
                        new_allin = [x for x in allin if x != -1]
                        new_allin2 = [x for x in allin2 if x != -1]
                        new_SStructure = [x for x in SStructure if x != -1]
                        # 重新设置number、allin、allin2、SStructure四个数组
                        number = []
                        for j in new_list:
                            number.append(j)
                        allin = []
                        for j in new_allin:
                            allin.append(j)
                        allin2 = []
                        for j in new_allin2:
                            allin2.append(j)
                        SStructure = []
                        for j in new_SStructure:
                            SStructure.append(j)
                        # 茎区相容
                        if(number != []):
                            s4 = SStructure[0]
                            for k in range(1 , len(number)):
                                s5 = ""
                                s6 = SStructure[k]
                                for l in range(0 , len(s)):
                                    if(s4[l] == '.' and s6[l] == '.'):
                                        s5 = s5 + '.'
                                    if((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                                        s5 = s5 + '('
                                    if((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                                        s5 = s5 + ')'
                                s4 = s5
                            rootStructure2 = s4
                            # 变异操作，若发生变异则进行以下操作
                            if(random.random() >= 0.98 and number != []):
                                # 判断配对碱基数大于2的茎区保存下来
                                number3 = []
                                for a in range(0 , len(allin)):
                                    if(allin[a][2] >= 3):
                                        number3.append(a)
                                # 生成大于3个配对碱基的茎区数量的随机值，并取最大的随机数对应的茎区进行后续的变异操作
                                if(number3 != []):
                                    count_numbers = [random.random() for _ in range(0 , len(number3))]
                                    max_number = max(count_numbers)
                                    maxcount = count_numbers.index(max_number)
                                    maxcount2 = number3[maxcount]
                                    j = maxcount2
                                    # 进行变异操作，若不能进行内部变异
                                    Srandom = random.random()
                                    if(variation[number[j]] == 'NO' or (variation[number[j]] == 'YES' and Srandom >= 0.5)):
                                        slist = list(s4)
                                        slist[allin[j][0]] = '.'
                                        slist[allin[j][1]] = '.'
                                        SStructure2 = SStructure[j]
                                        sstructure = list(SStructure2)
                                        sstructure[allin[j][0]] = '.'
                                        sstructure[allin[j][1]] = '.'
                                        Sstructure = ''
                                        for z in sstructure:
                                            Sstructure = Sstructure + z
                                        SStructure[j] = Sstructure
                                        allin[j][0] = allin[j][0] + 1
                                        allin[j][1] = allin[j][1] - 1
                                        allin[j][2] = allin[j][2] - 1
                                        s7 = ""
                                        for j in slist:
                                            s7 = s7 + j
                                        rootStructure2 = s7
                                    elif(variation[number[j]] == 'YES' and Srandom < 0.5):
                                        slist = list(s4)
                                        slist[allin2[j][0]] = '.'
                                        slist[allin2[j][1]] = '.'
                                        SStructure2 = SStructure[j]
                                        sstructure = list(SStructure2)
                                        sstructure[allin2[j][0]] = '.'
                                        sstructure[allin2[j][1]] = '.'
                                        Sstructure = ''
                                        for z in sstructure:
                                            Sstructure = Sstructure + z
                                        SStructure[j] = Sstructure
                                        allin2[j][0] = allin2[j][0] - 1
                                        allin2[j][1] = allin2[j][1] + 1
                                        allin[j][2] = allin[j][2] - 1
                                        s7 = ""
                                        for j in slist:
                                            s7 = s7 + j
                                        rootStructure2 = s7
                                elif(number3 == []):
                                    rootStructure2 = s4
                        if(number == []):
                            # 当茎区全部被删除时，重新在2号茎区池中选择根茎区，来进行下一步的茎区相容操作
                            for j in range(0 , len(Structures2)):
                                # 找到之前没有相容过的第一个茎区
                                if(Structures2[j] != '0'):
                                    # 与第一次相容时的操作一样
                                    rootStructure2 = Structures2[j]
                                    s = allcome[j]
                                    ap = compare[j]
                                    inner = compare[j][0]
                                    out = compare[j][1]
                                    pair = compare[j][2]
                                    allin.append([inner , out , pair])
                                    number.append(j)
                                    inner = compare2[j][0]
                                    out = compare2[j][1]
                                    pair = compare2[j][2]
                                    allin2.append([inner , out , pair])
                                    SStructure.append(Structures2[j])
                                    break
                        else:
                            # 正常情况下正常处理
                            # 将删除一些茎区后的二级结构变为0，1序列
                            s = ""
                            for j in range(0 , len(rootStructure2)):
                                if(rootStructure2[j] == '(' or rootStructure2[j] == ')'):
                                    s = s + '1'
                                if(rootStructure2[j] == '.'):
                                    s = s + '0'
                        # 与其余的茎区进行相容操作
                        for j in range(0 , len(Structures2)):
                            if(Structures2[j] == '0'):
                                continue
                            r = 0
                            for a in range(0 , len(Structures[0])):
                                if(s[a] == '1' and allcome[j][a] == '1'):
                                    r = 1
                                    break
                            if(r == 1):
                                continue
                            r = 0
                            for a in allin:
                                if(((compare[j][0] < a[0]) and (compare[j][1] > a[0] and compare[j][1] < a[1])) or ((compare[j][1] > a[1]) and (compare[j][0] > a[0] and compare[j][0] < a[1]))):
                                    r = 1
                                    break
                            if(r == 1):
                                continue
                            s1 = ""
                            for a in range(0 , len(Structures[0])):
                                if((s[a] == '1' and allcome[j][a] == '0') or (s[a] == '0' and allcome[j][a] == '1')):
                                    s1 = s1 + '1'
                                if(s[a] == '0' and allcome[j][a] == '0'):
                                    s1 = s1 + '0'
                            s = s1
                            s4 = ""
                            for l in range(0 , len(rootStructure2)):
                                if(rootStructure2[l] == '.' and Structures2[j][l] == '.'):
                                    s4 = s4 + '.'
                                if((rootStructure2[l] == '(' and Structures2[j][l] == '.') or (rootStructure2[l] == '.' and Structures2[j][l] == '(')):
                                    s4 = s4 + '('
                                if((rootStructure2[l] == ')' and Structures2[j][l] == '.') or (rootStructure2[l] == '.' and Structures2[j][l] == ')')):
                                    s4 = s4 + ')'
                            rootStructure2 = s4
                            inner = compare[j][0]
                            out = compare[j][1]
                            pair = compare[j][2]
                            allin.append([inner , out , pair])
                            inner = compare2[j][0]
                            out = compare2[j][1]
                            pair = compare2[j][2]
                            allin2.append([inner , out , pair])
                            number.append(j)
                            SStructure.append(Structures2[j])
                        # 在迭代过程中，若与最小自由能相差较小，则进行如下操作
                        if(lowerpower(str1 , rootStructure2) - lower2 < 10):
                            # 保存当前的二级结构以及最小自由能
                            lower2 = lowerpower(str1 , rootStructure2)
                            lowerStructure2 = rootStructure2
                            # 保存当前二级结构的相关信息
                            T_lowernumber = []
                            for j in number:
                                T_lowernumber.append(j)
                            T_lowerallin = []
                            for j in allin:
                                inner = j[0]
                                out = j[1]
                                pair = j[2]
                                T_lowerallin.append([inner , out , pair])
                            T_lowerallin2 = []
                            for j in allin2:
                                inner = j[0]
                                out = j[1]
                                T_lowerallin2.append([inner , out])
                            T_lowerSStructure = []
                            for j in SStructure:
                                T_lowerSStructure.append(j)
                        # 若相差超过一定范围则进行以下操作
                        elif(lowerpower(str1 , rootStructure2) - lower2 >= (len(str1)/(100 * l))):
                            # 将这次迭代过程中的最小自由能对应结构的信息
                            number = []
                            for j in T_lowernumber:
                                number.append(j)
                            allin = []
                            for j in T_lowerallin:
                                inner = j[0]
                                out = j[1]
                                pair = j[2]
                                allin.append([inner , out , pair])
                            allin2 = []
                            for j in T_lowerallin2:
                                inner = j[0]
                                out = j[1]
                                allin2.append([inner , out])
                            SStructure = []
                            for j in T_lowerSStructure:
                                SStructure.append(j)
                            rootStructure2 = lowerStructure2
                        ll = ll + 1
                    # 若迭代生成的最小自由能比迭代之前的最小自由能还小
                    if(lower2 < lower):
                        # 保存最小自由能对应的结构以及最小自由能
                        rootStructure = lowerStructure2
                        lowerStructure = lowerStructure2
                        lower = lower2
                        # 保存最小自由能对应的结构相关的信息
                        lowerallin = []
                        for j in allin:
                            inner = j[0]
                            out = j[1]
                            pair = j[2]
                            lowerallin.append([inner , out , pair])
                        lowerallin2 = []
                        for j in allin2:
                            inner = j[0]
                            out = j[1]
                            lowerallin2.append([inner , out])
                        lowernumber = []
                        for j in number:
                            lowernumber.append(j)
                        lowerSStructure = []
                        for j in SStructure:
                            lowerSStructure.append(j)
                    # 若迭代生成的最小自由能比迭代之前的最小自由能大
                    elif(lower2 >= lower):
                        # 保存之前最小自由能的相关信息
                        allin = []
                        for j in lowerallin:
                            inner = j[0]
                            out = j[1]
                            pair = j[2]
                            allin.append([inner , out , pair])
                        allin2 = []
                        for j in lowerallin2:
                            inner = j[0]
                            out = j[1]
                            allin2.append([inner , out])
                        number = []
                        for j in lowernumber:
                            number.append(j)
                        SStructure = []
                        for j in lowerSStructure:
                            SStructure.append(j)
                # 当前的二级结构的自由能大于最低的自由能
                else:
                    # 保存当前最小自由能对应的二级结构的信息
                    rootStructure = lowerStructure
                    allin = []
                    for j in lowerallin:
                        inner = j[0]
                        out = j[1]
                        pair = j[2]
                        allin.append([inner , out , pair])
                    allin2 = []
                    for j in lowerallin2:
                        inner = j[0]
                        out = j[1]
                        allin2.append([inner , out])
                    number = []
                    for j in lowernumber:
                        number.append(j)
                    SStructure = []
                    for j in lowerSStructure:
                        SStructure.append(j)
            # 若被删除的茎区池不为空，则将刚刚删除的茎区恢复到原来的位置
            if(delRoot != []):
                for j in range(0 , len(delRoot)):
                    Structures2[delRoot[j]] = Structures[delRoot[j]]
            # 将已经相容的茎区对应到第二个茎区池的位置置为0
            for j in range(0 , len(number)):
                Structures2[number[j]] = '0'
            # 生成随机数
            random_numbers = [random.random() for _ in range(len(number))]
            # 将删除的茎区编号保存下来，并将相应的列表中的元素置为-1
            delRoot = []
            numberlength = len(number)
            for j in range(0 , numberlength):
                if(random_numbers[j] > 0.5):
                    delRoot.append(number[j])
                    allin[j] = -1
                    number[j] = -1
                    allin2[j] = -1
                    SStructure[j] = -1
            # 删除列表中值为-1的元素
            new_list = [x for x in number if x != -1]
            new_allin = [x for x in allin if x != -1]
            new_allin2 = [x for x in allin2 if x != -1]
            new_SStructure = [x for x in SStructure if x != -1]
            # 重新设置number、allin、allin2、SStructure四个数组
            number = []
            for j in new_list:
                number.append(j)
            allin = []
            for j in new_allin:
                allin.append(j)
            allin2 = []
            for j in new_allin2:
                allin2.append(j)
            SStructure = []
            for j in new_SStructure:
                SStructure.append(j)
            # 茎区相容
            if(number != []):
                s4 = SStructure[0]
                for k in range(1 , len(number)):
                    s5 = ""
                    s6 = SStructure[k]
                    for l in range(0 , len(s)):
                        if(s4[l] == '.' and s6[l] == '.'):
                            s5 = s5 + '.'
                        if((s4[l] == '(' and s6[l] == '.') or (s4[l] == '.' and s6[l] == '(')):
                            s5 = s5 + '('
                        if((s4[l] == ')' and s6[l] == '.') or (s4[l] == '.' and s6[l] == ')')):
                            s5 = s5 + ')'
                    s4 = s5
                rootStructure = s4
                # 变异操作，若发生变异则进行以下操作
                if(random.random() >= 0.98 and number != []):
                    # 判断配对碱基数大于2的茎区保存下来
                    number3 = []
                    for a in range(0 , len(allin)):
                        if(allin[a][2] >= 3):
                            number3.append(a)
                    # 生成大于3个配对碱基的茎区数量的随机值，并取最大的随机数对应的茎区进行后续的变异操作
                    if(number3 != []):
                        count_numbers = [random.random() for _ in range(0 , len(number3))]
                        max_number = max(count_numbers)
                        maxcount = count_numbers.index(max_number)
                        maxcount2 = number3[maxcount]
                        j = maxcount2
                        # 进行变异操作，若不能进行内部变异
                        Srandom = random.random()
                        if(variation[number[j]] == 'NO' or (variation[number[j]] == 'YES' and Srandom >= 0.5)):
                            slist = list(s4)
                            slist[allin[j][0]] = '.'
                            slist[allin[j][1]] = '.'
                            SStructure2 = SStructure[j]
                            sstructure = list(SStructure2)
                            sstructure[allin[j][0]] = '.'
                            sstructure[allin[j][1]] = '.'
                            Sstructure = ''
                            for z in sstructure:
                                Sstructure = Sstructure + z
                            SStructure[j] = Sstructure
                            allin[j][0] = allin[j][0] + 1
                            allin[j][1] = allin[j][1] - 1
                            allin[j][2] = allin[j][2] - 1
                            s7 = ""
                            for j in slist:
                                s7 = s7 + j
                            rootStructure = s7
                        elif(variation[number[j]] == 'YES' and Srandom < 0.5):
                            slist = list(s4)
                            slist[allin2[j][0]] = '.'
                            slist[allin2[j][1]] = '.'
                            SStructure2 = SStructure[j]
                            sstructure = list(SStructure2)
                            sstructure[allin2[j][0]] = '.'
                            sstructure[allin2[j][1]] = '.'
                            Sstructure = ''
                            for z in sstructure:
                                Sstructure = Sstructure + z
                            SStructure[j] = Sstructure
                            allin2[j][0] = allin2[j][0] - 1
                            allin2[j][1] = allin2[j][1] + 1
                            allin[j][2] = allin[j][2] - 1
                            s7 = ""
                            for j in slist:
                                s7 = s7 + j
                            rootStructure = s7
                    elif(number3 == []):
                        rootStructure = s4
            i = i + 1
        ii = ii + 1
        allstructure.append(lowerStructure)
        lowerP.append(lower)
    return allstructure , lowerP

if __name__ == '__main__':
    print("输入需要预测的RNA序列")
    data = input()
    out(data)
    f = '配对概率矩阵2.txt'
    if(len(data) <= 110):
        print("wait about 10s.........")
        allStructures = peiduijuzhen(f, data)
        bestStructure = ""
        bestStructure2 = ""
        powerful1 = 1000000
        powerful2 = 1000000
        if (len(data) >= 65 and len(data) <= 90):
            for i in allStructures:
                power, lens = lowerpower(data, i)
                if (lens > 2 and power < powerful2):
                    powerful2 = power
                    bestStructure2 = i
                elif (lens <= 2 and power < powerful1):
                    powerful1 = power
                    bestStructure = i
            if ((powerful2 - powerful1) < 4):
                bestStructure = bestStructure2
            print("预测的结果为：")
            print(bestStructure)
        else:
            for i in allStructures:
                power = lowerpower(data, i)
                if (power < powerful1):
                    powerful1 = power
                    bestStructure = i
            print("预测的结果为：")
            print(bestStructure)
    if(len(data) >= 111 and len(data) < 140):
        print("wait about 30s...........")
        print(Processing_of_111(data,f))
    if(len(data) >= 140 and len(data) <= 300):
        print("wait about 3m...........")
        allstructure, lowerP = Processing_of_140(data, f)
        count = Counter(lowerP)
        most_common_number, most_common_count = count.most_common(1)[0]
        if (most_common_count <= 3):
            bestStructure = ""
            powerful1 = 1000000
            for i in allstructure:
                power = lowerpower(data, i)
                if (power < powerful1):
                    powerful1 = power
                    bestStructure = i
            print(bestStructure)
        else:
            for k in range(0, len(lowerP)):
                if (lowerP[k] == most_common_number):
                    print(allstructure[k])
                    break




