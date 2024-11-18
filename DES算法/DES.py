import S_BOX
def init(text): #将明文，密钥转为64位二进制数
    if len(text)!=16:
            print('Invalid input: Text should be 16 characters long.')
            return 0
    text_str = ''
    for i in text:
        if i not in '0123456789ABCDEF':
            print('Invalid input: Text should only contain hexadecimal characters.')
            return 0
        else:
             i = f"{int(i, 16):04b}"
             text_str += i
    return text_str
def IP(text): #初始置换
    text_str = ''
    initial_permutation_table = [
        58, 50, 42, 34, 26, 18, 10, 2,
        60, 52, 44, 36, 28, 20, 12, 4,
        62, 54, 46, 38, 30, 22, 14, 6,
        64, 56, 48, 40, 32, 24, 16, 8,
        57, 49, 41, 33, 25, 17, 9,  1,
        59, 51, 43, 35, 27, 19, 11, 3,
        61, 53, 45, 37, 29, 21, 13, 5,
        63, 55, 47, 39, 31, 23, 15, 7
    ]
    for i in range(64):
        text_str += text[initial_permutation_table[i]-1]
    return text_str
def inv_IP(text): #初始逆置换
    text_str = ''
    inverse_initial_permutation_table = [
        40, 8, 48, 16, 56, 24, 64, 32,
        39, 7, 47, 15, 55, 23, 63, 31,
        38, 6, 46, 14, 54, 22, 62, 30,
        37, 5, 45, 13, 53, 21, 61, 29,
        36, 4, 44, 12, 52, 20, 60, 28,
        35, 3, 43, 11, 51, 19, 59, 27,
        34, 2, 42, 10, 50, 18, 58, 26,
        33, 1, 41, 9,  49, 17, 57, 25
    ]
    for i in range(64):
        text_str += text[inverse_initial_permutation_table[i]-1]
    return text_str
def E_expand(text): #扩展变换E
    text_str = ''
    expansion_table = [
        32, 1, 2, 3, 4, 5,
        4, 5, 6, 7, 8, 9,
        8, 9, 10, 11, 12, 13,
        12, 13, 14, 15, 16, 17,
        16, 17, 18, 19, 20, 21,
        20, 21, 22, 23, 24, 25,
        24, 25, 26, 27, 28, 29,
        28, 29, 30, 31, 32, 1
    ]    
    for i in range(48):
        text_str += text[expansion_table[i]-1]
    return text_str
def PC_1(text): #置换选择1
    text_C0 = ''
    text_D0 = ''
    PC1_C = [
        57, 49, 41, 33, 25, 17, 9,
        1, 58, 50, 42, 34, 26, 18,
        10, 2, 59, 51, 43, 35, 27,
        19, 11, 3, 60, 52, 44, 36
    ]
    PC1_D = [
        63, 55, 47, 39, 31, 23, 15,
        7, 62, 54, 46, 38, 30, 22,
        14, 6, 61, 53, 45, 37, 29,
        21, 13, 5, 28, 20, 12, 4
    ]   
    for i in range(28):
        text_C0 += text[PC1_C[i]-1]
        text_D0 += text[PC1_D[i]-1]
    return text_C0, text_D0
def PC_2(text): #置换选择2
    text_str = ''
    PC2_table = [
        14, 17, 11, 24, 1, 5,
        3, 28, 15, 6, 21, 10,
        23, 19, 12, 4, 26, 8,
        16, 7, 27, 20, 13, 2,
        41, 52, 31, 37, 47, 55,
        30, 40, 51, 45, 33, 48,
        44, 49, 39, 56, 34, 53,
        46, 42, 50, 36, 29, 32
    ]
    for i in range(48):
        text_str += text[PC2_table[i]-1]
    return text_str
def P_expand(text): #置换运算P
    text_str = ''
    P_table = [
        16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10,
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25
    ]
    for i in range(32):
        text_str += text[P_table[i]-1]
    return text_str
def Shift_left(text,i): #循环左移
    if i == 1:
        return text[1:] + text[0]
    elif i == 2:
        return text[2:] + text[:2]
def Key_expand(text): #子密钥生成
    C0,D0 = PC_1(text)
    Key_list = []
    for i in range(16):
        C_D = ''
        if i == 0 or i == 1 or i ==8 or i ==15:
            C0 = Shift_left(C0,1)
            D0 = Shift_left(D0,1)
        else:
            C0 = Shift_left(C0,2)
            D0 = Shift_left(D0,2)
        C_D = C0 + D0
        Key_list.append(PC_2(C_D))
    return Key_list 
def xor_bcd(bcd1, bcd2): #BCD码异或操作
    result = ""
    for i in range(len(bcd1)):
        xor_bit = str(int(bcd1[i]) ^ int(bcd2[i]))
        result += xor_bit
    return result
def F(text,key_text): # F函数
    E_text = E_expand(text)
    count = 0
    S_text = ''
    xor_text = xor_bcd(E_text,key_text)
    for i in range(0,48,6):
        temp = xor_text[i:i+6]
        S_text += S_BOX.get(temp,count)
        count +=1
    S_text = P_expand(S_text)
    return S_text
def bcd_to_hex(bcd_str):#将字符串BCD码转换为字符串16进制数
    hex_result = ""
    for i in range(0, len(bcd_str), 4):
        bcd_digit = bcd_str[i:i+4]
        hex_char = hex(int(bcd_digit, 2))[2:].upper()
        hex_result += hex_char
    return hex_result
def encryption(text,keytext):#加密函数 
    text = init(text)
    keytext = init(keytext)
    text_IP = IP(text)
    text_IP_L = text_IP[:32]
    text_IP_R = text_IP[32:]
    key_list = Key_expand(keytext)
    L_temp = text_IP_L
    R_temp = text_IP_R
    for i in range(16):
        if i == 15:
            L_temp = xor_bcd(L_temp,F(R_temp,key_list[i]))
            return bcd_to_hex(inv_IP(L_temp + R_temp))
        temp = L_temp
        L_temp = R_temp
        R_temp = xor_bcd(temp,F(R_temp,key_list[i]))
def decryption(text,keytext):#解密函数
    text = init(text)
    keytext = init(keytext)
    text_IP = IP(text)
    text_IP_L = text_IP[:32]
    text_IP_R = text_IP[32:]
    key_list = Key_expand(keytext)
    L_temp = text_IP_L
    R_temp = text_IP_R
    for i in range(16):
        if i == 15:
            L_temp = xor_bcd(L_temp,F(R_temp,key_list[15-i]))
            return bcd_to_hex(inv_IP(L_temp + R_temp))
        temp = L_temp
        L_temp = R_temp
        R_temp = xor_bcd(temp,F(R_temp,key_list[15-i]))
def main():
    try:
        choice = int(input("请输入 1 进行加密, 2 进行解密: "))
        if choice not in [1, 2]:
            print("无效选择")
            return
        
        Text = input("请输入文本 (16位十六进制): ")
        Key = input("请输入密钥 (16位十六进制): ")

        result = encryption(Text, Key) if choice == 1 else decryption(Text, Key)

        if result:
            if choice == 1:
                print("加密后的密文：", result)
            else:
                print("解密后的明文：", result)
        else:
            print("处理失败，请检查输入。")

    except ValueError:
        print("输入无效，请输入数字 1 或 2。") 
if __name__ == '__main__':
     main()
    # 明文：'123456ABCD132536'
    # 密钥：'AABB09182736CCDD'
    # 密文：'C0B7A8D05F3A829C'