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
        mode = input('1. 加密 2. 解密 (q 退出): ')

        if mode == '1':
            message = input('输入明文：')
            try:
                key1, key2 = map(int,input('输入 key1, key2：').split(' '))
            except ValueError:
                print("密钥格式错误，请重新输入。")
                continue

            cipher_text = encrypt(message, key1, key2)
            print('Encrypted text:', cipher_text)

        elif mode == '2':
            cipher_text = input('输入密文：')
            try:
                key1, key2 = map(int,input('输入 key1, key2：').split(' '))
            except ValueError:
                print("密钥格式错误，请重新输入。")
                continue

            if not rp(key1,26):
                print('由于key1与26不互素，该密文不可逆！')
                continue

            decrypted_text = decrypt(cipher_text, key1, key2)
            print('Decrypted text:', decrypted_text)

        elif mode == 'q':
            break

        else:
            print('输入有误，请重新输入。')

if __name__ == '__main__':
    main()