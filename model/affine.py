from model.exgcd import rp, inverse as inv

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

def nogui():
    message = input('Enter the message to encrypt: ')
    key1, key2 = map(int,input('Enter key1, key2: ').split(' '))
    cipher_text = encrypt(message, key1, key2)
    print('Encrypted text:', cipher_text)
    if not rp(key1,26):
        print('由于key1与26不互素，该密文不可逆！')
        exit()
    decrypted_text = decrypt(cipher_text, key1, key2)
    print('Decrypted text:', decrypted_text)

def main():
    pass

if __name__ == '__main__':
    main()