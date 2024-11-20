# ################## 使用秘钥的单表代替密码 ########################
# ----------------------------------------------------------------

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
        mode = input('1. 加密 2. 解密 (q 退出): ')
        if mode == '1':
            text = input('输入明文：')
            key = input('输入密钥key：')
            encrypted_text = encrypt(text, key)
            print('密文：', encrypted_text)
        elif mode == '2':
            text = input('输入密文：')
            key = input('输入密钥key：')
            decrypted_text = decrypt(text, key)
            print('明文：', decrypted_text)
        elif mode == 'q':
            break
        else:
            print('输入有误，请重新输入。')

if __name__ == '__main__':
    main()