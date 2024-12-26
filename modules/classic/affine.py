from modules.math.exgcd import rp, inverse as inv

def encrypt(message, key1, key2):
    table = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    cipher_text = ''
    for char in message:
        if char.isalpha():
            x = table.index(char) if char.islower() else table.index(char.lower())
            y = (x * key1 + key2) % len(table)
            cipher_text += table[y]
        else:
            cipher_text += char
    return cipher_text

def decrypt(cipher_text, key1, key2):
    table = [chr(i) for i in range(ord('a'), ord('z') + 1)]
    decrypted_text = ''
    for char in cipher_text:
        if char.isalpha():
            y = table.index(char) if char.islower() else table.index(char.lower())
            x = (inv(key1, len(table)) * (y - key2) % len(table))
            decrypted_text += table[x]
        else:
            decrypted_text += char
    return decrypted_text

def main():
    while True:
        print('\n1. 加密 2. 解密 (q 退出): ')
        mode = input("\033[92m> \033[0m")

        if mode == '1':
            print('输入明文：')
            message = input("\033[92m> \033[0m")
            try:
                print('输入 key1, key2, 用空格分隔：')
                key1, key2 = map(int, input('\033[92m> \033[0m').split(' '))
            except ValueError:
                print("\033[91m[-] 密钥格式错误，请重新输入。\033[0m")
                continue

            print(f'\033[94m[+]\033[0m 明文：{message}')
            print(f'\033[94m[+]\033[0m 密钥1: {key1}')
            print(f'\033[94m[+]\033[0m 密钥2: {key2}')
            
            cipher_text = encrypt(message, key1, key2)
            
            print('\033[92m[+] 加密成功！\033[0m')
            print(f'\033[92m[+] 密文：{cipher_text}\033[0m')

        elif mode == '2':
            print('输入密文：')
            cipher_text = input("\033[92m> \033[0m")
            try:
                print('输入 key1, key2, 用空格分隔：')
                key1, key2 = map(int, input('\033[92m> \033[0m').split(' '))
            except ValueError:
                print("\033[91m[-] 密钥格式错误，请重新输入。\033[0m")
                continue

            print(f'\033[94m[+]\033[0m 密文：{cipher_text}')
            print(f'\033[94m[+]\033[0m 密钥1: {key1}')
            print(f'\033[94m[+]\033[0m 密钥2: {key2}')
            
            if not rp(key1, 26):
                print('\033[91m[-] 由于key1与26不互素, 该密文不可逆! \033[0m')
                continue

            decrypted_text = decrypt(cipher_text, key1, key2)
            
            print('\033[92m[+] 解密成功！\033[0m')
            print(f'\033[92m[+] 明文：{decrypted_text}\033[0m')

        elif mode == 'q':
            break

        else:
            print('\033[91m[-] 输入有误，请重新输入。\033[0m')

if __name__ == '__main__':
    main()