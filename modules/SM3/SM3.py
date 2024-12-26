# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 21:40:07 2024

SM3   对输入的明文采用utf-8编码
        对输出的密文采用十六进制编码

@author: 晨
"""
#常量T
def T(j):
    if j>=0 and j<=15:
        return 0x79cc4519
    elif j>=16 and j<=63:
        return 0x7a879d8a
#布尔函数FF
def FF(X, Y, Z, j):
    if j>=0 and j<=15:
        result=X^Y^Z
        return result # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
    else:
        result=(X & Y) | (X & Z) | (Y & Z)
        return result # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
#布尔函数GG
def GG(X, Y, Z, j):
    if j>=0 and j<=15:
        result=X^Y^Z
        return result # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
    else:
        result=(X & Y) | (~X & Z)
        return result # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
#循环左移
def circular_left_shift(x_int, n): #将整数x循环左移n位
    """
    对32位整数x进行n位的循环左移
    :param x: 输入的整数 (8位16进制数)
    :param n: 左移的位数
    :return: 循环左移后的结果
    """
    #因为n可能会大于32，此时相当于循环左移n%32位，所以提前对n进行处理
    n=n%32
#   x_int=int(x,16) #将x转化为整数 eg. x从'0a'变成了 10
    result=((x_int << n) & 0xFFFFFFFF) | (x_int >> (32 - n)) #将x循环左移n位
#    return f"{result:08x}" # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
    return result
#置换函数P
def P0(X):
    result=X^circular_left_shift(X,9)^circular_left_shift(X,17)
    return result 
def P1(X):
    result=X^circular_left_shift(X,15)^circular_left_shift(X,23)
    return result
#将明文字符串转换为二进制位串
def string_to_bitstring(s):
    """
    将字符串转换为二进制位串
    :param s: 输入字符串
    :return: 由每个字符转换成的 8 位二进制数拼接成的字符串
    """
    result=''.join(format(ord(char), '08b') for char in s)
    return result
#添加填充位。使数据位长度为 448 bit , 剩余的 64 bit用于表示原始明文字符串长度 eg abc，占三字节 24 bit，故末尾的 64 bit表示 24 
def add_padding_bits(bitstring):
    bitstring_padding=bitstring+'1' #先在明文二进制位串后面补上1
    if len(bitstring_padding)>448: #若数据长度大于等于448，继续填充
        rule=(len(bitstring_padding)//512+1)*512+448 #填充后的长度
        while len(bitstring_padding)!=rule: #若数据长度不足mod512后不为418，则补0，直至数据长度满足mod512后为448
            bitstring_padding+='0' 
    else: #若数据长度小于448,则补0，使数据长度为448
        while len(bitstring_padding)!=448:
            bitstring_padding+='0'
    bitstring_hex_list=[bitstring_padding[i:i+4] for i in range(0,len(bitstring_padding),4)] #截取每四位二进制数，存入列表，以便转为16进制
    bitstring_hex=''.join(hex(int(x,2))[2:] for x in bitstring_hex_list) #将二进制位串的数据转为十六进制串,因为只能是一位，所以不用zfill
    while len(bitstring_hex)%128!=0: #先将剩余的64bit全补为0,直至长度为512的整数倍
        bitstring_hex+='0'
    end_padding=hex(len(bitstring))[2:] #确定原始明文长度，十六进制，为了将原始明文长度添加到末尾,此处也不必zfill
    bitstring_hex=bitstring_hex[:-len(end_padding)]+end_padding #将原始明文长度添加到末尾
    return bitstring_hex
# 模 2**32 加法实现
def mod32_add(x, y, z, u):
    # 转换为整数并模 2**32，只保留低 32 位
    result = (x + y + z + u) & 0xFFFFFFFF
    # 转换为十六进制字符串，去掉前缀 '0x'，并保持长度为 8 位（补零）
#    return f"{result:08x}"
    return result
#SM3杂凑函数
def sm3_encode(bitstring_hex):
    #将消息分组，每组128个十六进制，即512bit
    bitstring_hex_group=[bitstring_hex[i:i+128] for i in range(0,len(bitstring_hex),128)] #将128位一组分割
    #初始向量IV
    IV = [0x7380166f, 0x4914b2b9, 0x172442d7, 0xda8a0600, 0xa96f30bc, 0x163138aa, 0xe38dee4d, 0xb0fb0e4e]
    #生成字 W,对每个分组都进行
    for bitstring_hex_i in bitstring_hex_group:
        w=[bitstring_hex_i[i:i+8] for i in range(0,len(bitstring_hex_i),8)] #将每四个字节，构成一个字，存储到 w[]中，共 16个字
        for j in range(16,68):
            w_tem=P1(int(w[j-16],16)^int(w[j-9],16)^circular_left_shift(int(w[j-3],16),15))^circular_left_shift(int(w[j-13],16),7)^int(w[j-6],16)
            w.append(format(w_tem, '08x')) #将w_tem转化为16进制字符串，并保持长度为 8 位（补零）
        for j in range(0,64): #从w列表的第68位开始，存储w0'，w1',...,w63'
            w_tem=int(w[j],16)^int(w[j+4],16)
            w.append(format(w_tem, '08x'))
        #迭代压缩
        A=[IV[len(IV)-8]]
        B=[IV[len(IV)-7]]
        C=[IV[len(IV)-6]]
        D=[IV[len(IV)-5]]
        E=[IV[len(IV)-4]]
        F=[IV[len(IV)-3]]
        G=[IV[len(IV)-2]]
        H=[IV[len(IV)-1]]
        for j in range(0,64):
            if j!=0:
                A=[int(i,16) for i in A]
                B=[int(i,16) for i in B]
                C=[int(i,16) for i in C]
                D=[int(i,16) for i in D]
                E=[int(i,16) for i in E]
                F=[int(i,16) for i in F]
                G=[int(i,16) for i in G]
                H=[int(i,16) for i in H]
            SS1=circular_left_shift(mod32_add(circular_left_shift(A[len(A)-1],12),E[len(E)-1],circular_left_shift(T(j),j),0),7)
            SS2=SS1^circular_left_shift(A[len(A)-1],12)
            TT1=mod32_add(FF(A[len(A)-1],B[len(B)-1],C[len(C)-1],j),D[len(D)-1],SS2,int(w[j+68],16))
            TT2=mod32_add(GG(E[len(E)-1],F[len(F)-1],G[len(G)-1],j),H[len(H)-1],SS1,int(w[j],16))
            D.append(C[len(C)-1])
            C.append(circular_left_shift(B[len(B)-1],9))
            B.append(A[len(A)-1])
            A.append(TT1)
            H.append(G[len(G)-1])
            G.append(circular_left_shift(F[len(F)-1],19))
            F.append(E[len(E)-1])
            E.append(P0(TT2))
            A=[format(i, '08x') for i in A]
            B=[format(i, '08x') for i in B]
            C=[format(i, '08x') for i in C]
            D=[format(i, '08x') for i in D]
            E=[format(i, '08x') for i in E]
            F=[format(i, '08x') for i in F]
            G=[format(i, '08x') for i in G]
            H=[format(i, '08x') for i in H]
        
        #更新IV
        A=[int(i,16) for i in A]
        B=[int(i,16) for i in B]
        C=[int(i,16) for i in C]
        D=[int(i,16) for i in D]
        E=[int(i,16) for i in E]
        F=[int(i,16) for i in F]
        G=[int(i,16) for i in G]
        H=[int(i,16) for i in H]
        IV.append(A[len(A)-1]^IV[len(IV)-8])
        IV.append(B[len(B)-1]^IV[len(IV)-8])
        IV.append(C[len(C)-1]^IV[len(IV)-8])
        IV.append(D[len(D)-1]^IV[len(IV)-8])
        IV.append(E[len(E)-1]^IV[len(IV)-8])
        IV.append(F[len(F)-1]^IV[len(IV)-8])
        IV.append(G[len(G)-1]^IV[len(IV)-8])
        IV.append(H[len(H)-1]^IV[len(IV)-8])
    #将IV转化为16进制字符串，并保持长度为 8 位（补零）
    IV=[format(i, '08x') for i in IV]
    #将IV_hex拼接成16进制字符串
    result=IV[len(IV)-8]+IV[len(IV)-7]+IV[len(IV)-6]+IV[len(IV)-5]+IV[len(IV)-4]+IV[len(IV)-3]+IV[len(IV)-2]+IV[len(IV)-1]
    return result
#主程序
def main():
    while True:
        print("==================== SM3 加密======================")
        print("[1] 加密")
        print("[0] 退出")
        print("====================================================")
        try:
            choice = int(input("请输入操作选项 (0 或 1 ): "))
            if choice == 0:
                print("\n\n程序已退出。感谢使用 SM3 加密工具！")
                break
            elif choice == 1:
                # 加密流程
                plaintext = input("请输入明文 (UTF-8 编码，任意长度): ")
                #明文转化为二进制位字符串
                bitstring = string_to_bitstring(plaintext)
                #填充为512位二进制，并转化为16进制，共128个字符
                bitstring_hex = add_padding_bits(bitstring)
                if not plaintext:
                    raise ValueError("明文不能为空！")
                #sha-1加密
                ciphertext=sm3_encode(bitstring_hex)
                print("\n加密结果 (十六进制):")
                print(ciphertext)
            else:
                raise ValueError("无效选项")
    
        except ValueError as e:
            print(f"输入错误: {e}")
        except Exception as e:
            print(f"发生错误: {e}")
# =============================================================================
# # 示例 密码书 P318
# #输入明文
# plaintext = "abc"
# #明文转化为二进制位字符串
# bitstring = string_to_bitstring(plaintext)
# #填充为512位二进制，并转化为16进制，共128个字符
# bitstring_hex = add_padding_bits(bitstring)
# #SM3加密
# ciphertext=sm3_encode(bitstring_hex)
# print(f"输入字符串: {plaintext}")
# print(f"密文串: {ciphertext}")
# =============================================================================
if __name__=="__main__":
    main()
