from modules.ZUC.config import *
#输入输出为16进制
#

m32 = pow(2,32)
m31 = pow(2,31)
class ZUC:
    def __init__(self,plaintext,key,IV):
        self.plaintext =[int(plaintext[i:i+2].ljust(2,'0'),16) for i in range(0,len(plaintext),2)]
        print(self.plaintext)
        if len(key)%32:
            key+='0'*(32-len(key))
        self.key = [int(key[i:i+2],16) for i in range(0,32,2)]
        if len(IV)%32:
            IV+='0'*(32-len(IV))
        self.IV =[int(IV[i:i+2],16) for i in range(0,32,2)]
        self.lfsr_s = [(self.key[i]<<23)|(D[i])<<8|self.IV[i] for i in range(0,16)]

        self.R1=0
        self.R2=0
        self.LFSP_init()
        self.encrypt_stream = []

    def encrypt(self):
        print("\033[94m[+]\033[0m 开始加密...")
        v = self.bit_reorganization()
        self.F(v)
        self.LFSPwithworkmode()
        count = 0
        while count < len(self.plaintext):
            v = self.bit_reorganization()
            self.encrypt_stream.append(self.F(v))
            self.LFSPwithworkmode()
            count += 16
        print("\033[92m[+] 加密完成！\033[0m")

    def LFSP_init(self):
        print("\033[94m[+]\033[0m 初始化 LFSR...")
        for i in range(0, 32):
            if i % 8 == 0:
                print(f"\033[94m[+]\033[0m 初始化进度: {i}/32")
            v = self.bit_reorganization()
            u = self.F(v) ^ (v >> 64 & 0xffffffff)
            self.LFSPwithworkmode_n(u >> 1)
        print("\033[92m[+] LFSR 初始化完成！\033[0m")

    def bit_reorganization(self):
        x1 = (self.lfsr_s[11] % (2 ** 16)) + ((self.lfsr_s[9] >> 16) << 16)
        x2 = (self.lfsr_s[7] % (2 ** 16)) + ((self.lfsr_s[5] >> 16) << 16)
        x3 = (self.lfsr_s[2] % (2 ** 16)) + ((self.lfsr_s[0] >> 16) << 16)
        x0 = (((self.lfsr_s[15]) >> 16) << 16) + (self.lfsr_s[14] % (2 ** 16))
        return (x0 << 96) + (x1 << 64) + (x2 << 32) + x3

    def F(self, v):
        x = (v >> 96) & 0xff
        x1 = (v >> 64) & 0xff
        x2 = (v >> 32) & 0xff
        w = ((x ^ self.R1) + self.R2) % m32
        w1 = (self.R1 + x1) % m32
        w2 = self.R2 ^ x2
        self.R1 = self.SL1(w1, w2)
        self.R2 = self.SL2(w1, w2)
        return w

    def loop(self,n,p):
        temp  =bin(n)[2:].rjust(32, '0')

        return int(temp[p:]+temp[:p],2)
    def SL1(self,w1,w2):
        temp = ((w1>>16)<<16)+(w2>>16)
        temp = (temp^self.loop(temp,2)^self.loop(temp,10)^self.loop(temp,18)^self.loop(temp,24))
        x0 = temp >> 24
        x1 = temp >> 16 & 0xff
        x2 = temp >> 8 & 0xff
        x3 = temp & 0xff
        result = 0
        for i in range(0, 4):
            result = result << 8
            if (i % 2 == 0):
                result += S0[x0 // 16][x0 % 16]

            else:
                result += S1[x0 // 16][x0 % 16]
        return result
    def SL2(self,w1,w2):
        temp = ((w2 >> 16) << 16) + (w1 >> 16)
        temp = (temp ^ self.loop(temp, 8) ^ self.loop(temp, 14) ^ self.loop(temp, 22) ^ self.loop(temp, 30))
        x0=temp>>24
        x1=temp>>16&0xff
        x2=temp>>8&0xff
        x3=temp&0xff
        result = 0
        for i in range(0,4):
            result=result<<8
            if(i%2==0):
                result+=S0[x0//16][x0%16]

            else:
                result += S1[x0 // 16][x0 % 16]
        return result
    def LFSPwithworkmode_n(self,n):

        v = (self.lfsr_s[15]<<15+self.lfsr_s[13]<<17+self.lfsr_s[4]<<20+(1+(2^8)*self.lfsr_s[0]))%(m31-1)
        if v==0:
            v = m31-1

        s16 = (v+n)%(m31-1)
        if s16==0:
            s16=m31-1
        s16=[s16]
        for i in range(15):
            self.lfsr_s[i]=self.lfsr_s[i+1]
        self.lfsr_s[15]=s16[0]



    def LFSPwithworkmode(self):
        s16 = self.bit_reorganization()
        if s16==0:
            s16 = m31-1

        for i in range(15):
            self.lfsr_s[i] = self.lfsr_s[i + 1]
        self.lfsr_s.append(s16)



def test():
    test = ZUC('133333ACCBACBACBABCABCABCBACBABCABCABCBACBABBABCBACBABCABCB', '1111', 'acd')

    test.encrypt()
    print(test.encrypt_stream)

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
            print("\033[94m[+]\033[0m 请输入明文字符:")
            message = input("\033[92m> \033[0m")
            if not message:
                print("\033[91m[-] 明文不能为空！\033[0m")
                continue
            
            print("\033[94m[+]\033[0m 请输入密钥，数字:")
            key = input("\033[92m> \033[0m")
            if not key:
                print("\033[91m[-] 密钥不能为空！\033[0m")
                continue
            
            print("\033[94m[+]\033[0m 请输入IV:")
            iv = input("\033[92m> \033[0m")
            if not iv:
                print("\033[91m[-] IV不能为空！\033[0m")
                continue
            
            plaintext_hex = ''.join([hex(ord(c))[2:].zfill(2) for c in message])
            zuc = ZUC(plaintext_hex, key, iv)
            zuc.encrypt()
            
            print("\033[94m[+]\033[0m 加密结果:")
            print(f"\033[92m{zuc.encrypt_stream}\033[0m")
        
        except ValueError as e:
            print(f"\033[91m[-] 输入错误: {e}\033[0m")
        except Exception as e:
            print(f"\033[91m[-] 发生错误: {e}\033[0m")

if __name__ == '__main__':
    test()