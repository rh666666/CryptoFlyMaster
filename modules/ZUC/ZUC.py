from concurrent.futures import ThreadPoolExecutor
from modules.ZUC.config import *
#输入输出为16进制
#

m32 = pow(2,32)
m31 = pow(2,31)
class ZUC:
    def __init__(self,plaintext,key,IV):
        print("\033[94m[+]\033[0m 初始化 ZUC 实例...")
        self.precomputed_sbox = self.precompute_sbox()  # 确保 S 盒预计算在其他初始化之前完成
        self.plaintext =[int(plaintext[i:i+2].ljust(2,'0'),16) for i in range(0,len(plaintext),2)]
        print(self.plaintext)
        if len(key)%32:
            key+='0'*(32-len(key))
        self.key = [int(key[i:i+2],16) for i in range(0,32,2)]
        if len(IV)%32:
            IV+='0'*(32-len(IV))
        self.IV =[int(IV[i:i+2],16) for i in range(0,32,2)]
        self.lfsr_s = [(self.key[i]<<23)|(D[i])<<8|self.IV[i] for i in range(0,16)]
        print(f"\033[94m[+]\033[0m 明文: {plaintext}, 密钥: {key}, IV: {IV}")
        print(f"\033[94m[+]\033[0m LFSR 初始状态: {self.lfsr_s}")

        self.R1=0
        self.R2=0
        self.LFSP_init()
        self.encrypt_stream = []

    def precompute_sbox(self):
        """预计算 S0 和 S1 的查表结果"""
        print("\033[94m[+]\033[0m 预计算 S 盒查表...")
        precomputed = {}
        for i in range(256):
            precomputed[i] = (S0[i // 16][i % 16], S1[i // 16][i % 16])
        print("\033[92m[+] S 盒查表预计算完成！\033[0m")
        return precomputed

    def encrypt(self):
        """生成密钥流"""
        print("\033[94m[+]\033[0m 开始生成密钥流...")
        with ThreadPoolExecutor() as executor:
            futures = []
            for i in range(len(self.plaintext)):
                v = self.bit_reorganization()
                future = executor.submit(self.F, v)
                futures.append(future)
                self.LFSPwithworkmode()
            self.encrypt_stream = [future.result() for future in futures]
        
        print(f"\033[94m[+]\033[0m 密钥流: {self.encrypt_stream}")
        print("\033[92m[+] 密钥流生成完成！\033[0m")

    def LFSP_init(self):
        print("\033[94m[+]\033[0m 初始化 LFSR...")
        for i in range(0, 32):
            print(f"\033[94m[+]\033[0m 初始化进度: {i+1}/32")
            v = self.bit_reorganization()
            u = self.F(v) ^ (v >> 64 & 0xffffffff)
            self.LFSPwithworkmode_n(u >> 1)
        print(f"\033[94m[+]\033[0m LFSR 初始化完成，最终状态: {self.lfsr_s}")
        print("\033[92m[+] LFSR 初始化完成！\033[0m")

    def bit_reorganization(self):
        """优化后的位重组函数，减少冗余计算"""
        x0 = ((self.lfsr_s[15] & 0xFFFF0000) | (self.lfsr_s[14] & 0xFFFF)) & 0xFFFFFFFF  # 限制为 32 位
        x1 = ((self.lfsr_s[11] & 0xFFFF) | ((self.lfsr_s[9] >> 16) & 0xFFFF) << 16) & 0xFFFFFFFF  # 限制为 32 位
        x2 = ((self.lfsr_s[7] & 0xFFFF) | ((self.lfsr_s[5] >> 16) & 0xFFFF) << 16) & 0xFFFFFFFF  # 限制为 32 位
        x3 = ((self.lfsr_s[2] & 0xFFFF) | ((self.lfsr_s[0] >> 16) & 0xFFFF) << 16) & 0xFFFFFFFF  # 限制为 32 位
        print(f"\033[94m[+]\033[0m 位重组结果: x0={x0}, x1={x1}, x2={x2}, x3={x3}")
        return (x0 << 96) | (x1 << 64) | (x2 << 32) | x3

    def F(self, v):
        """修复 F 函数，确保返回正确的密钥流片段"""
        x = (v >> 96) & 0xff
        x1 = (v >> 64) & 0xff
        x2 = (v >> 32) & 0xff
        w = (((x ^ self.R1) + self.R2) & 0xFFFFFFFF)  # 限制为 32 位
        w1 = (self.R1 + x1) & 0xFFFFFFFF  # 限制为 32 位
        w2 = self.R2 ^ x2
        self.R1 = self.SL1(w1, w2)
        self.R2 = self.SL2(w1, w2)
        print(f"\033[94m[+]\033[0m F 函数输入: v={v}, 输出: w={w}, R1={self.R1}, R2={self.R2}")
        return w

    def loop(self,n,p):
        temp  =bin(n)[2:].rjust(32, '0')

        return int(temp[p:]+temp[:p],2)
    def SL1(self,w1,w2):
        """优化后的 S 盒查表逻辑"""
        temp = (((w1 >> 16) << 16) + (w2 >> 16)) & 0xFFFFFFFF  # 限制为 32 位
        temp ^= self.loop(temp, 2) ^ self.loop(temp, 10) ^ self.loop(temp, 18) ^ self.loop(temp, 24)
        result = 0
        for i in range(4):
            byte = (temp >> (24 - i * 8)) & 0xFF
            result = (result << 8) + self.precomputed_sbox[byte][i % 2]
        print(f"\033[94m[+]\033[0m SL1 输入: w1={w1}, w2={w2}, 输出: result={result}")
        return result & 0xFFFFFFFF  # 限制为 32 位

    def SL2(self,w1,w2):
        """优化后的 S 盒查表逻辑"""
        temp = (((w2 >> 16) << 16) + (w1 >> 16)) & 0xFFFFFFFF  # 限制为 32 位
        temp ^= self.loop(temp, 8) ^ self.loop(temp, 14) ^ self.loop(temp, 22) ^ self.loop(temp, 30)
        result = 0
        for i in range(4):
            byte = (temp >> (24 - i * 8)) & 0xFF
            result = (result << 8) + self.precomputed_sbox[byte][i % 2]
        print(f"\033[94m[+]\033[0m SL2 输入: w1={w1}, w2={w2}, 输出: result={result}")
        return result & 0xFFFFFFFF  # 限制为 32 位

    def LFSPwithworkmode_n(self,n):
        """优化后的 LFSR 工作模式函数"""
        v = ((self.lfsr_s[15] << 15) + (self.lfsr_s[13] << 17) + (self.lfsr_s[4] << 20) + (1 + (2 ** 8) * self.lfsr_s[0])) & 0x7FFFFFFF  # 限制为 31 位
        if v == 0:
            v = m31 - 1

        s16 = (v + n) & 0x7FFFFFFF  # 限制为 31 位
        if s16 == 0:
            s16 = m31 - 1

        self.lfsr_s = self.lfsr_s[1:] + [s16]
        print(f"\033[94m[+]\033[0m LFSPwithworkmode_n 输入: n={n}, 更新后 LFSR: {self.lfsr_s}")

    def LFSPwithworkmode(self):
        """修复 LFSR 工作模式，确保正确更新"""
        s16 = ((self.lfsr_s[15] << 15) + (self.lfsr_s[13] << 17) + (self.lfsr_s[4] << 20) + (1 + (2 ** 8) * self.lfsr_s[0])) & 0x7FFFFFFF  # 限制为 31 位
        if s16 == 0:
            s16 = m31 - 1

        self.lfsr_s = self.lfsr_s[1:] + [s16]
        print(f"\033[94m[+]\033[0m LFSPwithworkmode 更新后 LFSR: {self.lfsr_s}")

def test():
    test = ZUC('133333ACCBACBACBABCABCABCBACBABCABCABCBACBABBABCBACBABCABCB', '1111', 'acd')
    test.encrypt()
    print(test.encrypt_stream)

def main():
    while True:
        print('\n1. 生成密钥流 (q 退出): ')
        choice = input("\033[92m> \033[0m")
        if choice == 'q':
            return
        
        if choice != '1':
            print("\033[91m[-] 无效选择\033[0m")
            continue
        
        try:
            print("\033[94m[+]\033[0m 请输入明文字符: ")
            message = input("\033[92m> \033[0m")
            if not message:
                print("\033[91m[-] 明文不能为空！\033[0m")
                continue
            
            print("\033[94m[+]\033[0m 请输入密钥，数字: ")
            key = input("\033[92m> \033[0m")
            if not key:
                print("\033[91m[-] 密钥不能为空！\033[0m")
                continue
            
            print("\033[94m[+]\033[0m 请输入IV: ")
            iv = input("\033[92m> \033[0m")
            if not iv:
                print("\033[91m[-] IV不能为空！\033[0m")
                continue
            
            plaintext_hex = ''.join([hex(ord(c))[2:].zfill(2) for c in message])
            zuc = ZUC(plaintext_hex, key, iv)
            zuc.encrypt()
            
            print("\033[94m[+]\033[0m 密钥流:")
            print(f"\033[92m{zuc.encrypt_stream}\033[0m")
        
        except ValueError as e:
            print(f"\033[91m[-] 输入错误: {e}\033[0m")
        except Exception as e:
            print(f"\033[91m[-] 发生错误: {e}\033[0m")

if __name__ == '__main__':
    test()