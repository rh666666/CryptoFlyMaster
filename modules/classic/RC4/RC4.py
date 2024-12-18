import base64
class RC4:


    def __init__(self,plaintext,key):
        self.cipher = []
        self.plaintext=plaintext.encode()   #接受明文
        self.key=key.encode()           #接受密钥
        self.keylen=len(key)            #密钥长度
        self.s = list(range(256))       #初始化S盒子
        j = 0
        for i in range(256):            #置换s盒子
            j = (j+self.s[i]+self.key[i%self.keylen])%256
            self.s[i],self.s[j]=self.s[j],self.s[i]

    def encrypt(self):
        self.cipher=[]
        i = 0
        j = 0
        for l in range(len(self.plaintext)):
            i = (i+1)%256
            j = (j+self.s[i])%256
            self.s[i],self.s[j]=self.s[j],self.s[i]
            k = self.s[(self.s[i]+self.s[j])%256]
            self.cipher.append(k^l)

            return base64.b64encode(bytes(self.cipher))
    def decrypt(self):
        pass


if __name__ == '__main__':
    plaintext = input("输入明文")
    key = input("输入密钥")
    test = RC4(plaintext,key)
    print(test.encrypt())


            