#输入输出皆为16进制
from DES.config import loop_position
from config import *
class SM4:
    def __init__(self,plaintext,key):
        if len(plaintext)%32:
            plaintext+='0'*(32-len(plaintext)%32)
        self.plaintext = [[int(plaintext[i:i+32][j:j+8],16) for j in range(0,32,8)]for i in range(0,len(plaintext),32)]
        if len(key)%32:
            key+='0'*(32-len(key)%32)
        self.key = [int(key[i:i+8])for i in range(0,32,8)]
        self.round_key = []
        self.expand_key()
        self.cipher=[]

    def encrypt(self):
        for i in self.plaintext:
            a0 = i[0]
            a1 = i[1]
            a2 = i[2]
            a3 = i[3]
            for j in range(0,32):
                temp = a0
                a0 = a1
                a1 = a2
                a2 = a3
                a3 = temp^(self.T(a0^a1^a2^self.round_key[j]))
            self.cipher.append([a3,a2,a1,a0])#反序变换



    def T(self,temp):
        #先S盒子变换，再次L变换
        a0 = (temp >> 24) & 0xff
        a1 = (temp >> 16) & 0xff
        a2 = (temp >> 8) & 0xff
        a3 = (temp >> 0) & 0xff
        B = S_BOX[a0 // 16][a0 % 16] ^ S_BOX[a1 // 16][a1 % 16] ^ S_BOX[a2 // 16][a2 % 16] ^ S_BOX[a3 // 16][a3 % 16]
        return B^self.loop_position(B,2)^self.loop_position(B,10)^self.loop_position(B,18)^self.loop_position(B,24)

    def R(self):
        pass
    def loop_position(self,i,j):
        temp = bin(i)[2:].rjust(32,'0')
        temp = temp[j:]+temp[:j]
        return int(temp,2)
    def T_for_key(self,temp):
        a0=(temp>>24)&0xff
        a1=(temp>>16)&0xff
        a2=(temp>>8)&0xff
        a3=(temp>>0)&0xff
        B = S_BOX[a0//16][a0%16]^S_BOX[a1//16][a1%16]^S_BOX[a2//16][a2%16]^S_BOX[a3//16][a3%16]

        return B^self.loop_position(B,13)^self.loop_position(B,23)

    def expand_key(self):
        temp=[]
        for i in range(4):
            temp.append(self.key[i]^FK[i])
        for i in range(0,32):
            t = temp[i]^self.T_for_key(temp[i+1]^temp[i+2]^temp[i+3]^CK[i])
            temp.append(i)
            self.round_key.append(t)


    def decrypt(self):
        pass

if __name__ =="__main__":
    test= SM4('13131313aacdefacdefacdefacdefacedfacedfacdefacde','1231313131')
    test.encrypt()
    print(test.cipher)
