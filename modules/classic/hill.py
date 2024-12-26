# ######################## 希尔密码 ###############################
# ----------------------------------------------------------------
# Hill密码要求将明文分成固定长度的分组（最后一个分组可能需要填充（注：填充双方都知道的字符），每个分组整体加密变换。其基本思想是：
# 将一个分组中的d个连续的明文字母通过线性变换转换为d个密文字母。
# 这种代替由d个线性方程决定，其中每个字母被分配一个数值（0，1，…，25）。解密只需要做一次逆变换就可以。
# ----------------------------------------------------------------
# ------------------------- 示例 ---------------------------------
# 明文：hi 
# 密钥矩阵：11 8
#           3 7
# 密文：XI
# ----------------------------------------------------------------

from numpy import array, linalg
from modules.math.mat import Matrix
from modules.math.exgcd import rp

# 字母转数字
def number(alpha):
    return ord(alpha) - ord('A')

# 数字转字母
def alpha(number):
    return chr(number + ord('A'))

# 分组
def make_groups(text, key):
    ls = [number(i) for i in text]
    groups = [ls[i:i + len(key)] for i in range(0, len(ls), len(key))]
    return array(groups)

def encrypt(message, key, fill_alpha):
    message = message.upper()
    key = array(key)
    if not rp(int(round(linalg.det(key))), 26):
        raise ValueError("Matrix is not invertible modulo 26")
    if len(message) % key.shape[1] != 0:
        message += fill_alpha[0].upper() * (key.shape[1] - len(message) % key.shape[1])
    groups = make_groups(message, key)
    encrypted_groups = []
    for group in groups:
        encrypted_group = (array(group) @ key) % 26
        encrypted_groups.append(''.join([alpha(num) for num in encrypted_group]))
    return ''.join(encrypted_groups)

def decrypt(cipher_text, key):
    cipher_text = cipher_text.upper()
    key = Matrix(array(key))
    if round(linalg.det(key.matrix)) == 0:
        print('密钥行列式为0，无法解密.')
        return
    key = key.inverse()
    groups = make_groups(cipher_text, key)
    decrypted_groups = []
    for group in groups:
        decrypted_group = (array(group) @ key) % 26
        decrypted_groups.append(''.join([alpha(num) for num in decrypted_group]))
    return ''.join(decrypted_groups)

def main():
    while True:
        print('\n1. 加密 2. 解密 (q 退出): ')
        mode = input("\033[92m> \033[0m")

        if mode == '1':
            print('输入明文：')
            message = input("\033[92m> \033[0m")
            
            print('输入密钥（用逗号分隔每行，用空格分隔每个元素）：')
            key = input("\033[92m> \033[0m")
            
            try:
                key = [[int(num) for num in row.split(' ')] for row in key.split(',')]
                
            except ValueError:
                print("\033[91m[-] 密钥错误，请重试。\033[0m")
                continue
            
            print('填充字母：')
            fill_alpha = input("\033[92m> \033[0m")
            
            print(f'\033[94m[+]\033[0m 明文：{message}')
            print(f'\033[94m[+]\033[0m 密钥矩阵：\n\033[93m{array(key)}\033[0m')
            print(f'\033[94m[+]\033[0m 填充字母：{fill_alpha}')
            
            try:
                cipher_text = encrypt(message, key, fill_alpha)
                
                print('\033[92m[+] 加密成功！\033[0m')
                print(f'\033[92m[+] 密文：{cipher_text}\033[0m')
                
            except ValueError:
                print("\033[91m[-] 密钥矩阵在模26下不可逆，请重试。\033[0m")
                continue

        elif mode == '2':
            print('输入密文：')
            cipher_text = input("\033[92m> \033[0m")
            
            print('输入密钥（用逗号分隔每行，用空格分隔每个元素）：')
            key = input("\033[92m> \033[0m")
            
            try:
                key = [[int(num) for num in row.split(' ')] for row in key.split(',')]
                
            except ValueError:
                print("\033[91m[-] 密钥错误，请重试。\033[0m")
                continue
            
            print(f'\033[94m[+]\033[0m 密文：{cipher_text}')
            print(f'\033[94m[+]\033[0m 密钥矩阵：\n\033[93m{array(key)}\033[0m')
            
            try:
                decrypted_text = decrypt(cipher_text, key)
                
                print('\033[92m[+] 解密成功！\033[0m')
                print(f'\033[92m[+] 明文：{decrypted_text}\033[0m')
                
            except ValueError:
                print("\033[91m[-] 密钥矩阵在模26下不可逆，请重试。\033[0m")
                continue

        elif mode == 'q':
            break

        else:
            print('\033[91m[-] 输入有误，请重新输入。\033[0m')

if __name__ == '__main__':
    main()