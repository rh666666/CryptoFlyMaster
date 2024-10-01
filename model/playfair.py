# ################### palyfair密码 ###############################
# ----------------------------------------------------------------
# 多表代替密码，基于一个5×5字母矩阵，该矩阵使用一个关键词（密钥）来构造。
# ----------------------------------------------------------------
# 构造方法：从左至右，从上至下依次填入关键词的字母（去除重复的字母），然后再以字母表顺序依次填入其他的字母。字母I和J被算作一个字母。
# ----------------------------------------------------------------
# P1、P2同行：对应的C1和C2分别是紧靠P1、P2右端的字母。其中第一列被看作是最后一列的右方。（解密时反向）
# P1、P2同列：对应的C1和C2分别是紧靠P1、P2下方的字母。其中第一行看作是最后一行的下方。（解密时反向）
# P1、P2不同行、不同列：C1和C2是由P1和P2确定的矩形的其它两角的字母，并且C1和P1、C2和P2同行。（解密时处理方法相同）
# P1＝P2：则插入一个字母于重复字母之间，并用前述方法处理。
# 若明文字母数为奇数时：则在明文的末端添加某个事先约定的字母作为填充。
# ----------------------------------------------------------------
# 例：
# 密钥是：PLAYFAIR　IS　A　DIGRAM　CIPHER
# 如果明文是：P＝playfair cipher
# 明文两个一组： pl    ay    fa    ir    ci       ph    er
# 对应密文为: 　  LA    YF    PY   RS   MR    AM    CD
# ----------------------------------------------------------------

# 格式化文本
def text_format(text):
    # 仅保留字母，并转化为大写，将'J'转化成'I'
    text = list(''.join(filter(str.isalpha, text)).upper().replace('J','I'))
    return text

# 获取value在二维列表中的位置
def getTwoDimensionListIndex(list, value):
    for i in range(len(list)):
        for j in range(len(list[i])):
            if list[i][j] == value:
                return i, j

#构造字母矩阵     
def setTwoDimensionList(key):
    alpha_table = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    alpha_table.remove('j')

    table = []
    key = text_format(key)
    
    #将key去重加入列表
    for i in key:
        if not i in table:
            table.append(i)
    
    # 将剩余字母加入列表
    for i in alpha_table:
        if not i in table:
            table.append(i)
    
    # 若明文字母数为奇数，在明文的末端添加预先约定好的字母
    if len(table) % 2 == 1:  
        table.append(alpha_table[0])    # 若明文字母数为奇数，在明文的末端添加预先约定好的字母
    
    # 若明文字母数为偶数，在明文的末端添加一个字母，该字母在明文中不可能与任何字母重合
    if len(table) % 2 == 0:  
        table.append(alpha_table[1])    # 若明文字母数为偶数，在明文的末端添加一个字母，该字母在明文中不可能与任何字母重

    # 全员大写
    table = [i.upper() if i.islower() else i for i in table]
    
    # 构造5×5字母矩阵
    table = [table[0:5], table[5:10], table[10:15], table[15:20], table[20:25]]
    return table

# 加密算法
def encrypt(message, key, alpha):
    # 构造矩阵
    table = setTwoDimensionList(key)
    
    # 明文中转化为大写，并把J替换为I
    message = text_format(message)
    alpha = text_format(alpha)

    # 检查每组是否会出现p1=p2情况，如果有，则填充预先约定好的字母
    i = 0
    while True:
        if message[i] == message[i+1]: message.insert(i+1, alpha[0])
        i += 2
        if i >= len(message) - 1: break

    if len(message) % 2 == 1:  
        message.append(alpha[0])    # 若明文字母数为奇数，在明文的末端添加预先约定好的字母
    
    # 明文分组
    groups = [message[i:i+2] for i in range(0, len(message), 2)]
    
    # 明文两两对照
    cipher_text = ''
    for group in groups:
        p1 = group[0]
        p2 = group[1]
        print(f'p1 = {p1}')
        print(f'p2 = {p2}')

        # 寻找p1和p2在表中的位置
        i1, j1 = getTwoDimensionListIndex(table, p1)
        i2, j2 = getTwoDimensionListIndex(table, p2)

        # 同行
        if i1 == i2:  
            c1 = table[i1][(j1 + 1) % 5]  # 循环回到第一列  
            c2 = table[i2][(j2 + 1) % 5]
        # 同列
        elif j1 == j2:  
            c1 = table[(i1 + 1) % 5][j1]  # 循环回到第一行  
            c2 = table[(i2 + 1) % 5][j2]
        # 不同行不同列
        else:
            c1 = table[i1][j2]
            c2 = table[i2][j1]

        cipher_text += c1 + c2

    return cipher_text

def decrypt(cipher_text, key):
    # 构造矩阵
    table = setTwoDimensionList(key)

    # 密文如果是小写，则转化为大写
    cipher_text = text_format(cipher_text)

    # 密文分组
    groups = [cipher_text[i:i+2] for i in range(0, len(cipher_text), 2)]

    # 密文两两对照
    message = ''
    for group in groups:
        c1 = group[0]
        c2 = group[1]

        # 寻找c1和c2在表中的位置
        i1, j1 = getTwoDimensionListIndex(table, c1)
        i2, j2 = getTwoDimensionListIndex(table, c2)

        #同行
        if i1 == i2:  
            p1 = table[i1][(j1 - 1) % 5]  # 循环回到最后一列  
            p2 = table[i2][(j2 - 1) % 5]
        # 同列
        elif j1 == j2:  
            p1 = table[(i1 - 1) % 5][j1]  # 循环回到最后一行  
            p2 = table[(i2 - 1) % 5][j2]
        # 不同行不同列
        else:
            p1 = table[i1][j2]
            p2 = table[i2][j1]

        message += p1 + p2
    return message
    

def nogui():
    while True:
        mode = input("选择1加密2解密(输入q退出)：")
        if mode == "1":
            message = input("明文：")
            key = input("密钥：")
            alpha = input("填充字母：")
            print("密文：", encrypt(message, key, alpha))
        elif mode == "2":
            cipher_text = input("密文：")
            key = input("密钥：")
            print("明文：", decrypt(cipher_text, key))
        elif mode == "q":
            break
        else:
            print("输入有误，请重新输入。")

def main():
    pass

if __name__ == "__main__":
    main()