import S_Box
import invS_box
import log_table
import invlog_table
def init(text):# 将明文，密钥按列变为4×4矩阵形式，元素为字符串16进制数
    text_list = [] #转换为16进制数的列表
    word_list = text.split(' ')
    for i in word_list:
        word = int(i,16)
        hex_word = hex(word)
        text_list.append(hex_word) 
    text_matrix = [
        [],
        [],
        [],
        []
    ] #16进制矩阵
    for i in range(4):
        for j in range(4):
            text_matrix[j].append(text_list[i*4+j])
    return text_matrix
def hex_to_bcd(hex_str): #将字符串16进制数转换为以字符形式的BCD码
    hex_str = hex_str.lstrip("0x").zfill(2) # lstrip()去除前置字符0x,zfill()保留俩位，如，'0x7'变为'0x07'
    bcd_str = ""
    for char in hex_str:
        bcd_str += f"{int(char, 16):04b}"      
    return bcd_str
def bcd_to_hex(bcd_str):#将字符串BCD码转换为字符串16进制数
    hex_result = ""
    decimal_value = 0
    for i in range(0, 8, 4):
        bcd_digit = bcd_str[i:i+4]
        decimal_digit = int(bcd_digit, 2)
        decimal_value = decimal_value * 16 + decimal_digit
    return hex(decimal_value)
def xor_bcd(bcd1, bcd2): #BCD码异或操作
    result = ""
    for i in range(8):
        xor_bit = str(int(bcd1[i]) ^ int(bcd2[i]))
        result += xor_bit
    return result
def AddRoundKey(plaintext_matrix,keytext_matrix):# 与轮密钥进行异或
    temp_matrix = [
        [],
        [],
        [],
        []
    ] #明文与轮密钥异或后的矩阵
    xor_list = [] #异或后的元素列表
    for i in range(4):
        for j in range(4):
            plaintext_elem = plaintext_matrix[j][i]
            keytext_elem = keytext_matrix[j][i]
            plaintext_elem_bcd = hex_to_bcd(plaintext_elem)
            keytext_elem_bcd = hex_to_bcd(keytext_elem)
            xor_result = xor_bcd(plaintext_elem_bcd, keytext_elem_bcd)
            xor_list.append(bcd_to_hex(xor_result))
    for i in range(4):
        for j in range(4):
            temp_matrix[j].append(xor_list[i*4+j])
    return temp_matrix
def SubBytes(temp_matrix): # S盒变换
    SubBytes_matrix = [
        [],
        [],
        [],
        []
    ]
    elem_list = []
    new_elem_list = []
    for i in range(4):
        for j in range(4):
            elem_list.append(temp_matrix[i][j].lstrip("0x").zfill(2))
    for i in elem_list:
        new_elem_list.append(S_Box.subbytes(i[0],i[1]))
    for i in range(4):
        for j in range(4):
            SubBytes_matrix[i].append(new_elem_list[i*4+j])
    return SubBytes_matrix 
def invSubBytes(invShiftRows_matrix): #逆S盒变换
    invSubBytes_matrix = [
        [],
        [],
        [],
        []
    ]
    elem_list = []
    new_elem_list = []
    for i in range(4):
        for j in range(4):
            elem_list.append(invShiftRows_matrix[i][j].lstrip("0x").zfill(2))
    for i in elem_list:
        new_elem_list.append(invS_box.subbytes(i[0],i[1]))
    for i in range(4):
        for j in range(4):
            invSubBytes_matrix[i].append(new_elem_list[i*4+j])
    return invSubBytes_matrix
def ShiftRows(SubBytes_matrix):# 行左移
    ShiftRows_matrix = [
        SubBytes_matrix[0],  # 第一行不变
        SubBytes_matrix[1][1:] + SubBytes_matrix[1][:1],  # 第二行左移 1 个字节
        SubBytes_matrix[2][2:] + SubBytes_matrix[2][:2],  # 第三行左移 2 个字节
        SubBytes_matrix[3][3:] + SubBytes_matrix[3][:3]   # 第四行左移 3 个字节
    ]
    return ShiftRows_matrix
def invShiftRows(temp_matrix):#逆行左移
    invShiftRows_matrix = [
        temp_matrix[0],  # 第一行不变
        temp_matrix[1][-1:] + temp_matrix[1][:-1],  # 第二行右移 1 个字节
        temp_matrix[2][-2:] + temp_matrix[2][:-2],  # 第三行右移 2 个字节
        temp_matrix[3][-3:] + temp_matrix[3][:-3]   # 第四行右移 3 个字节
    ]
    return invShiftRows_matrix
def Multiply_matrix(i,j): #矩阵每一态相乘
    i = log_table.get(i[0],i[1])
    j = log_table.get(j[0],j[1])
    if j == -1:
        return hex(0).lstrip('0x').zfill(2)
    if int(i,16)+int(j,16) >255:
        p = hex(int(i,16)+int(j,16)-255).lstrip('0x').zfill(2)
    else:
        p = hex(int(i,16)+int(j,16)).lstrip('0x').zfill(2)
    q = invlog_table.get(p[0],p[1])
    return q
def xor_matrix(elem_list): #每一态相乘完总异或
    bcd0 = hex_to_bcd(elem_list[0])
    bcd1 = hex_to_bcd(elem_list[1])
    bcd2 = hex_to_bcd(elem_list[2])
    bcd3 = hex_to_bcd(elem_list[3])
    xor_result = xor_bcd(xor_bcd(xor_bcd(bcd0, bcd1), bcd2), bcd3)
    return bcd_to_hex(xor_result).lstrip("0x").zfill(2)
def MixColumns(ShiftRows_matrix):# 列混合变换
    K_matrix =[
        ['0x02','0x03','0x01','0x01'],
        ['0x01','0x02','0x03','0x01'],
        ['0x01','0x01','0x02','0x03'],
        ['0x03','0x01','0x01','0x02']
    ]
    MixColumns_matrix = [
        [],
        [],
        [],
        []
    ]
    # 逐列进行 MixColumns 操作
    for i in range(4):
        # 每次清空临时结果列表，用于存储每个元素乘积
        column_result = []
        for row in range(4):
            # 逐个相乘并异或得到新列的元素
            elem_list = [
                Multiply_matrix(K_matrix[row][0].lstrip("0x").zfill(2), ShiftRows_matrix[0][i].lstrip("0x").zfill(2)),
                Multiply_matrix(K_matrix[row][1].lstrip("0x").zfill(2), ShiftRows_matrix[1][i].lstrip("0x").zfill(2)),
                Multiply_matrix(K_matrix[row][2].lstrip("0x").zfill(2), ShiftRows_matrix[2][i].lstrip("0x").zfill(2)),
                Multiply_matrix(K_matrix[row][3].lstrip("0x").zfill(2), ShiftRows_matrix[3][i].lstrip("0x").zfill(2))
            ]
            # 将列的每个元素相乘后异或，得到每一列结果
            column_result.append(xor_matrix(elem_list))
        # 将新列添加到 MixColumns_matrix
        for row in range(4):
            MixColumns_matrix[row].append(column_result[row])
    return MixColumns_matrix     
def invMixColumns(AddRoundKey_matrix):# 逆列变换
    K_matrix =[
        ['0x0e','0x0b','0x0d','0x09'],
        ['0x09','0x0e','0x0b','0x0d'],
        ['0x0d','0x09','0x0e','0x0b'],
        ['0x0b','0x0d','0x09','0x0e']
    ]
    invMixColumns_matrix = [
        [],
        [],
        [],
        []
    ]
    # 逐列进行 MixColumns 操作
    for i in range(4):
        # 每次清空临时结果列表，用于存储每个元素乘积
        column_result = []
        for row in range(4):
            # 逐个相乘并异或得到新列的元素
            elem_list = [
                Multiply_matrix(K_matrix[row][0].lstrip("0x").zfill(2), AddRoundKey_matrix[0][i].lstrip("0x").zfill(2)),
                Multiply_matrix(K_matrix[row][1].lstrip("0x").zfill(2), AddRoundKey_matrix[1][i].lstrip("0x").zfill(2)),
                Multiply_matrix(K_matrix[row][2].lstrip("0x").zfill(2), AddRoundKey_matrix[2][i].lstrip("0x").zfill(2)),
                Multiply_matrix(K_matrix[row][3].lstrip("0x").zfill(2), AddRoundKey_matrix[3][i].lstrip("0x").zfill(2))
            ]
            # 将列的每个元素相乘后异或，得到每一列结果
            column_result.append(xor_matrix(elem_list))
        # 将新列添加到 MixColumns_matrix
        for row in range(4):
            invMixColumns_matrix[row].append(column_result[row])
    return invMixColumns_matrix
def xor_column(column1,column2): #对矩阵的俩个列进行异或
    column = []
    for i in range(4):
       column.append(bcd_to_hex(xor_bcd(hex_to_bcd(column1[i]),hex_to_bcd(column2[i]))).lstrip("0x").zfill(2))
    return column
def T(column,count): # 拓展密钥中的T函数
    Rcon = [
    ['0x01', '0x00', '0x00', '0x00'],
    ['0x02', '0x00', '0x00', '0x00'],
    ['0x04', '0x00', '0x00', '0x00'],
    ['0x08', '0x00', '0x00', '0x00'],
    ['0x10', '0x00', '0x00', '0x00'],
    ['0x20', '0x00', '0x00', '0x00'],
    ['0x40', '0x00', '0x00', '0x00'],
    ['0x80', '0x00', '0x00', '0x00'],
    ['0x1b', '0x00', '0x00', '0x00'],
    ['0x36', '0x00', '0x00', '0x00']
    ] #轮常量
    column1 = column[1:]+column[:1] # 循环左移一个字节
    column2 = []
    for i in column1:
        column2.append(S_Box.subbytes(i[0],i[1]).lstrip("0x").zfill(2))
    result = xor_column(Rcon[count-1],column2)
    return result
def KeyExpansion(keytext_matrix):# 密钥扩展
    w = []
    for i in range(4):
        elem_list = []
        for j in range(4):
            elem_list.append(keytext_matrix[j][i].lstrip("0x").zfill(2))
        w.append(elem_list)
    for i in range(4,44):
        if i % 4 == 0:
            count = i // 4
            w.append(xor_column(w[i - 4], T(w[i - 1], count)))
        else:
            w.append(xor_column(w[i - 4], w[i - 1]))

    big_matrix = []
    for i in range(0,44,4):
        sub_matrix = [[w[i + j][k] for j in range(4)] for k in range(4)]
        big_matrix.append(sub_matrix)
    return big_matrix
def Encryption(Text,Key):#加密函数
    plaintext_matrix = init(Text)
    keytext_matrix = init(Key)
    First_matrix = AddRoundKey(plaintext_matrix,keytext_matrix) #第一轮开始矩阵
    temp_matrix = First_matrix
    keytext_matrix = KeyExpansion(keytext_matrix)
    for i in range(1,11):
        if i == 10:
            SubBytes_matrix = SubBytes(temp_matrix)
            ShiftRows_matrix = ShiftRows(SubBytes_matrix)
            temp_matrix = AddRoundKey(ShiftRows_matrix,keytext_matrix[i])
            return temp_matrix                
        SubBytes_matrix = SubBytes(temp_matrix)
        ShiftRows_matrix = ShiftRows(SubBytes_matrix)
        MixColumns_matrix = MixColumns(ShiftRows_matrix)
        temp_matrix = AddRoundKey(MixColumns_matrix,keytext_matrix[i])
def Decryption(Text,Key):#解密函数
    plaintext_matrix = init(Text)
    keytext_matrix = init(Key)
    keytext_matrix = KeyExpansion(keytext_matrix)
    First_matrix = AddRoundKey(plaintext_matrix,keytext_matrix[10])
    temp_matrix = First_matrix
    for i in range(9,-1,-1):
        if i == 0:
            invShiftRows_matrix = invShiftRows(temp_matrix)
            invSubBytes_matrix = invSubBytes(invShiftRows_matrix)
            AddRoundKey_matrix = AddRoundKey(invSubBytes_matrix,keytext_matrix[i])
            return AddRoundKey_matrix
        invShiftRows_matrix = invShiftRows(temp_matrix)
        invSubBytes_matrix = invSubBytes(invShiftRows_matrix)
        AddRoundKey_matrix = AddRoundKey(invSubBytes_matrix,keytext_matrix[i])
        temp_matrix = invMixColumns(AddRoundKey_matrix)
def main():
    choice = int(input("请输入 1 进行加密, 2 进行解密: "))
    Text = input("密文(128位AES用16进制表示,空格分隔):") if choice == 2 else input("明文(128位AES用16进制表示,空格分隔):")
    Key = input("密钥：")

    switcher = {
        1: lambda: Encryption(Text, Key),
        2: lambda: Decryption(Text, Key)
    }

    result = switcher.get(choice, lambda: "无效选择")()
    
    if isinstance(result, str):
        print(result)
    elif choice == 1:  # 选择1进行加密时输出密文
        print("密文：", end="")
        for i in range(4):
            for j in range(4):
                print(result[j][i].lstrip("0x").zfill(2), end=" ")
        print()  
    elif choice == 2:  # 选择2进行解密时输出明文
        print("明文：", end="")
        for i in range(4):
            for j in range(4):
                print(result[j][i].lstrip("0x").zfill(2), end=" ")
        print()  
if __name__ == "__main__":
    #明文：32 43 f6 a8 88 5a 30 8d 31 31 98 a2 e0 37 07 34
    #密钥：2b 7e 15 16 28 ae d2 a6 ab f7 15 88 09 cf 4f 3c
    #密文：39 25 84 1d 02 dc 09 fb dc 11 85 97 19 6a 0b 32
    main()