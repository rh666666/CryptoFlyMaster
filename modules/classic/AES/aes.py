import config
from AES.config import I_MIXC, S_BOX, MIX_C


#默认128为位b
#编码默认UTF-8
#明文和密钥都是十六进制
class AES:
    def __init__(self,plaintext,key):
        # tem1 = list(plaintext.encode('utf-8'))
        # tem2 = len(tem1) % 16
        # tem1.extend([0]*(16-tem2))
        # tem2  =[[j[k:k+4]for k in range(0,16,4)] for j in [tem1[i:i+16] for i in range(0,len(tem1),16)]]
        # self.plaintext = tem2
        # tem1 = list(key.encode('utf-8'))
        # tem2 = len(tem1) % 16
        # tem1.extend([0]*(16-tem2))
        # tem1 = tem1[0:16]
        # tem2 = [tem1[i:i+4] for i in range(0,16,4)]
        # self.key= tem2
        tem1 = len(plaintext)%32
        plaintext+='0'*(32-tem1)
        tem1 = len(key)%32
        key += '0' * (32 - tem1)
        key = key[:32]
        self.cipher = []
        self.plaintext = [[[int(plaintext[i:i+32][j:j+8][k:k+2],16)for k in range(0,8,2)] for j in range(0,32,8) ]for i in range(0,len(plaintext),32)]
        self.key = [[int(key[i:i+8][k:k+2],16) for k in range(0,8,2)] for i in range(0,32,8)]
        self.round_key = self.key
        self.generate_round_key()
        self.ciphertext=''







    def generate_round_key(self):

       for i in range(4,44):
           if i%4:
               self.round_key.append([self.round_key[i-1][j]^self.round_key[i-4][j] for j in range(0,4)])
           else:
               temp = [self.round_key[i-1][(j+1)%4] for j in range(0,4)]
               temp1 = [ S_BOX[i>>4][i%16] for i in temp]
               temp2 = [ temp1[j]^self.round_key[i//4][j]^self.round_key[i-4][j] for j in range(0,4)]
               self.round_key.append(temp2)


    def encrypt(self):

        for i in self.plaintext:
            temp = i
            print(i)
            print("\n")
            self.add_round_key(temp,0)
            for j in range(1,10):
                print(temp)
                print("\n")
                self.sub_bytes(temp)
                print(temp)
                print("\n")
                self.shift_rows(temp)
                print(temp)
                print("\n")
                self.mix_columns(temp)
                print(temp)
                print("\n")
                self.add_round_key(temp,j)
            self.cipher.append(temp)
        for i in self.cipher:
            for j in i:
                for k in j:
                    self.ciphertext+=hex(k)[2:]
    def decrypt(self):
        pass

    def sub_bytes(self,temp):
        for i in range(0,4):
            for j in range(0,4):
                temp1 = temp[i][j]
                temp[i][j] = S_BOX[temp1//16][temp1%16]

    def shift_rows(self,temp):
        for i in range(0,4):
            temp[i]=temp[i][i:]+temp[i][:i]
    def mix_columns(self,temp):
        for i in range(0,4):
            for j in range(0,4):
                t = 0
                for k in range(0,4):
                    t=(t+temp[j][k]*MIX_C[i][k])%256
                temp[i][j]=t
    def add_round_key(self,temp,round):

        for i in range(0,4):
            for j in range(0,4):
                temp[i][j]^=self.round_key[round*4+i][j]

if __name__=='__main__':
    # # print('hello')
    # # print(I_MIXC)
    test = AES('123aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa','132acedfacdddd123')
    test.encrypt()
    print(test.ciphertext)

