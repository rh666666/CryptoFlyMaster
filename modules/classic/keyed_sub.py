# ################## 使用秘钥的单表代替密码 ########################
# ----------------------------------------------------------------

import os


def dict_get(key, mode):
    table = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    dic = {}
    new_table = []
    [new_table.append(i) for i in key if not i in new_table]
    [new_table.append(j) for j in table if not j in new_table]
    if mode == '1':
        for i,j in enumerate(table):
            dic[j] = new_table[i]
    elif mode == '2':
        for i,j in enumerate(new_table):
            dic[j] = table[i]
    return dic

def encrypt(text, key):
    dic = dict_get(key, mode='1')
    encrypted_text = ''
    for char in text:
        if char.isalpha():
            encrypted_text += dic[char] if char.islower() else dic[char.lower()]
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, key):
    dic = dict_get(key, mode='2')
    decrypted_text = ''
    traslate_table = str.maketrans(dic)
    decrypted_text = text.translate(traslate_table)
    return decrypted_text

def main():
    while(True):
        print('\n1. 加密 2. 解密 (q 退出): ')
        mode = input("\033[92m> \033[0m")
        if mode == '1':
            print('输入明文，可以是任意字母、数字或符号的组合，但只加密字母：')
            text = input("\033[92m> \033[0m")
            print('输入密钥，只能由英文小写字母组成：')
            key = input("\033[92m> \033[0m")
            encrypted_text = encrypt(text, key)
            
            print(f'\033[94m[+]\033[0m 明文：{text}')
            print(f'\033[94m[+]\033[0m 密钥：{key}')
            print('\033[92m[+] 加密成功！\033[0m')
            print(f'\033[92m[+] 密文：{encrypted_text}\033[0m')
            
        elif mode == '2':
            print('输入密文：')
            text = input("\033[92m> \033[0m")
            print('输入密钥，只能由英文小写字母组成：')
            key = input("\033[92m> \033[0m")
            decrypted_text = decrypt(text, key)
            
            print(f'\033[94m[+]\033[0m 密文：{text}')
            print(f'\033[94m[+]\033[0m 密钥：{key}')
            print('\033[92m[+] 解密成功！\033[0m')
            print(f'\033[92m[+] 明文：{decrypted_text}\033[0m')
            
        elif mode == 'q':
            break
        
        else:
            print('\033[91m[-] 输入有误，请重新输入。\033[0m')

if __name__ == '__main__':
    main()