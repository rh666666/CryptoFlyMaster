# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 21:40:07 2024

SHA-1   对输入的明文采用utf-8编码
        对输出的密文采用十六进制编码

@author: 晨
"""

#将明文字符串转换为二进制位串
def string_to_bitstring(s):
    """
    将字符串转换为二进制位串
    :param s: 输入字符串
    :return: 由每个字符转换成的 8 位二进制数拼接成的字符串
    """
    return ''.join(format(ord(char), '08b') for char in s)

#添加填充位。使数据位长度为 448 bit , 剩余的 64 bit用于表示原始明文字符串长度 eg abc，占三字节 24 bit，故末尾的 64 bit表示 24 
def add_padding_bits(bitstring):
    if len(bitstring) < 448: #若不够448位，则填充
        bitstring_padding=bitstring+'1' #先在明文二进制位串后面补上1
        while len(bitstring_padding)!=448:
            bitstring_padding+='0' #剩余的全补为0，直至数据长度为 448
        bitstring_hex_list=[bitstring_padding[i:i+4] for i in range(0,len(bitstring_padding),4)] #截取每四位二进制数，存入列表，以便转为16进制
    else: #若够448位，无需填充, 此时还有问题未解决，加密结果和正确的不一致
        print("明文字符串长度 >= 56, 尚未实现")
    bitstring_hex=''.join(hex(int(x,2))[2:] for x in bitstring_hex_list) #将二进制位串的数据转为十六进制串,因为只能是一位，所以不用zfill
    while len(bitstring_hex)!=128: #先将剩余的64bit全补为0
        bitstring_hex+='0'
    end_padding=hex(len(bitstring))[2:] #确定原始明文长度，十六进制，为了将原始明文长度添加到末尾,此处也不必zfill
    bitstring_hex=bitstring_hex[:-len(end_padding)]+end_padding #将原始明文长度添加到末尾
    return bitstring_hex

#循环左移
def circular_left_shift(x, n): #将整数x循环左移n位
    """
    对32位整数x进行n位的循环左移
    :param x: 输入的整数 (8位16进制数)
    :param n: 左移的位数
    :return: 循环左移后的结果
    """
    x_int=int(x,16) #将x转化为整数 eg. x从'0a'变成了 10
    result=((x_int << n) & 0xFFFFFFFF) | (x_int >> (32 - n)) #将x循环左移n位
    return f"{result:08x}" # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）

# 模 2**32 加法实现
def mod32_add(x, y, z, u, k):
    # 转换为整数并模 2**32，只保留低 32 位
    result = (int(x, 16) + int(y, 16) + int(z, 16) + int(u, 16) + int(k, 16)) & 0xFFFFFFFF
    # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
    return f"{result:08x}"

#压缩函数 f1
def f1(X, Y, Z):
    result = (int(X, 16) & int(Y, 16)) | ((~int(X, 16)) & int(Z, 16)) # ~ 取反操作是按位取反，但为了避免补码带来的负数影响，并确保始终在 32 位范围内，使用 ~X & 0xFFFFFFFF 来取反
    return f"{result:08x}" # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）

#压缩函数 f2
def f2(X, Y, Z):
    result = int(X,16) ^ int(Y,16) ^ int(Z,16)
    return f"{result:08x}" # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）

#压缩函数 f3
def f3(X, Y, Z):
    result = (int(X,16) & int(Y,16)) | (int(X,16) & int(Z,16)) | (int(Y,16) & int(Z,16))
    return f"{result:08x}" # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）

#压缩函数 f4
def f4(X, Y, Z):
    result = int(X,16) ^ int(Y,16) ^ int(Z,16)
    return f"{result:08x}" # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）

#sha-1加密
def sha_1_encode(bitstring_hex):
    #初始化五个寄存器
    A=['67452301']
    B=['EFCDAB89']
    C=['98BADCFE']
    D=['10325476']
    E=['C3D2E1F0']
    #生成字 W
    w=[bitstring_hex[i:i+8] for i in range(0,len(bitstring_hex),8)] #将每四个字节，构成一个字，存储到 w[]中，共 16个字
    #固定常数
    K=['5a827999','6ed9eba1','8f1bbcdc','ca62c1d6']
    #存储压缩函数
    function=[f1,f2,f3,f4]
    for i in range(16,80): #共 80个字
        w_tem=''.join([hex(int(a,16) ^ int(b,16) ^ int(c,16) ^ int(d,16))[2:] for a,b,c,d in zip(w[i-16],w[i-14],w[i-8],w[i-3])]) #异或操作，这里的''.join是为了让该列表变为字符串
        w_tem=circular_left_shift(w_tem, 1) #循环左移 1位
        w.append(w_tem) #将生成的字添加到 w列表中
    #经过四轮，每轮20步
    for i in range(4):
        for t in range(i*20,(i+1)*20):
            A_tem=mod32_add(E[len(E)-1],function[i](B[len(B)-1],C[len(C)-1],D[len(D)-1]),circular_left_shift(A[len(A)-1], 5), w[t], K[i])
            A.append(A_tem)
            B.append(A[len(A)-2])
            C.append(circular_left_shift(B[len(B)-2], 30))
            D.append(C[len(C)-2])
            E.append(D[len(D)-2])
    #输出变换
    A.append(mod32_add(A[len(A)-1], A[len(A)-81], '0', '0', '0'))
    B.append(mod32_add(B[len(B)-1], B[len(B)-81], '0', '0', '0'))
    C.append(mod32_add(C[len(C)-1], C[len(C)-81], '0', '0', '0'))
    D.append(mod32_add(D[len(D)-1], D[len(D)-81], '0', '0', '0'))
    E.append(mod32_add(E[len(E)-1], E[len(E)-81], '0', '0', '0'))
    ciphertext=A[len(A)-1]+B[len(B)-1]+C[len(C)-1]+D[len(D)-1]+E[len(E)-1]
    return ciphertext

#主程序
def main():
    while True:
        print('\n1. 加密 (q 退出): ')
        choice = input("\033[92m> \033[0m")
        if choice == 'q':
            return
        
        if choice != '1':
            print("\033[91m[-] 无效选择\033[0m")
            continue
        
        try:
            print("请输入明文:")
            plaintext = input("\033[92m> \033[0m")
            if not plaintext:
                raise ValueError("明文不能为空！")
            
            # 明文转化为二进制位字符串
            bitstring = string_to_bitstring(plaintext)
            # 填充为512位二进制，并转化为16进制，共128个字符
            bitstring_hex = add_padding_bits(bitstring)
            # sha-1加密
            ciphertext = sha_1_encode(bitstring_hex)
            
            print("\033[92m[+] 加密成功！\033[0m")
            print(f"\033[92m[+] 加密结果 (十六进制): {ciphertext}\033[0m")
        
        except ValueError as e:
            print(f"\033[91m[-] 输入错误: {e}\033[0m")
        except Exception as e:
            print(f"\033[91m[-] 发生错误: {e}\033[0m")

if __name__ == "__main__":
    main()
            
# 示例 密码书 P188
# =============================================================================
# #输入明文
# plaintext = "11111111111111111111111111111111111111111111111111111111"
# #明文转化为二进制位字符串
# bitstring = string_to_bitstring(plaintext)
# #填充为512位二进制，并转化为16进制，共128个字符
# bitstring_hex = add_padding_bits(bitstring)
# #sha-1加密
# ciphertext=sha_1_encode(bitstring_hex)
# print(f"输入字符串: {plaintext}")
# print(f"密文串: {ciphertext}")
# =============================================================================