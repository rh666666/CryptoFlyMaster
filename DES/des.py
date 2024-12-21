from itertools import permutations

from config import *
class DES():

    def __init__(self,plaintext,key):
        self.plaintext = [[int(l) for l in k] for k in[bin(int(j,16))[2:].rjust(64,'0') for j in[plaintext[i:i+16].ljust(16,'0') for i in range(0,len(plaintext),16)]]]
        self.key = [  int(j) for j in bin(int(key[0:16].ljust(16,'0'),16))[2:].rjust(64,'0') ]
        self.subkey = []
        self.generate_sun_key()#产生子密钥
        self.cipher = []

    def encrypt(self):
        for i in self.plaintext:
            temp1 = [ i[IP_table[j]-1] for j in range(64)]#初始置换
            l = temp1[:32]
            r = temp1[32:]
            for j in range(MaxTime):#16轮函数
                temp2 = self.f(j,r)
                for k in range(32):
                    temp2[k]^=l[k]
                l,r = r,temp2
            #交换位置
            l,r = r,l
            temp3 = l+r
            #逆置换
            temp4 = [temp3[Inv_IP_table[j]-1] for j in range(64)]
            self.cipher.append(temp4)
        tem5 = []
        for j in self.cipher:
            t = []
            for k in j:
                t.append(str(k))
            tem5.append(t)
        return "".join([hex(int(''.join(j),2))[2:].rjust(16,'0') for j in tem5])


    def decrypt(self):
        pass

    def generate_sun_key(self):     #密钥产生算法
        temp = []                   #密钥置换选择1，64位密钥转换56位
        for i in key_table1:
            temp.append(self.key[i-1])
        C = temp[0:28]
        D = temp[28:]

        for i in range(16):
            C = C[loop_position[i]:] + C[:loop_position[i]]
            D = D[loop_position[i]:] + D[:loop_position[i]]
            temp2 = []
            temp3 = C+D

            for j in key_table2:
                temp2.append(temp3[j-1])#置换选择2

            self.subkey.append(temp2)


    def f(self,round,r):
        #拓展变换
        temp = [r[i - 1] for i in extend_table]
        #密钥异或
        for i in range(len(temp)):
            temp[i]^=self.subkey[round][i]
        #s盒子替代
        tem3 = []
        for i in range(0,8):
            match i:
                case 0:
                    temp2 = temp[i*6:i*6+6]
                    row = temp2[0]*2+temp2[-1]
                    column = temp2[1]*8+temp2[2]*4+temp2[3]*2+temp2[4]
                    tem3.append([int(j)for j in bin(S1[row][column])[2:].rjust(4,'0')])

                case 1:
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in bin(S2[row][column])[2:].rjust(4,'0')])

                case 2:
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in str(bin(S3[row][column]))[2:].rjust(4,'0')])

                case 3:
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in bin(S4[row][column])[2:].rjust(4,'0')])

                case 4:
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in bin(S5[row][column])[2:].rjust(4,'0')])

                case 5 :
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in bin(S6[row][column])[2:].rjust(4,'0')])

                case 6 :
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in bin(S7[row][column])[2:].rjust(4,'0')])

                case 7:
                    temp2 = temp[i * 6:i * 6 + 6]
                    row = temp2[0] * 2 + temp2[-1]
                    column = temp2[1] * 8 + temp2[2] * 4 + temp2[3] * 2 + temp2[4]
                    tem3.append([int(j) for j in bin(S8[row][column])[2:].rjust(4,'0')])

        #置换运算
        tem3 = sum(tem3,[])
        tem4 = [tem3[j-1] for j in P_table]

        return tem4





if __name__ =='__main__':
    # print(S1)
    test_plaintext =  input("输入16进制明文")
    test_key = input("输入16进制密钥")
    test = DES(test_plaintext,test_key)
    # print(test.plaintext)
    # print(test.key)
    # for i in test.subkey:
    #     print(i)
    #     print('\n')
    print(test.encrypt())