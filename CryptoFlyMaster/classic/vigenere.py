# ################################ 维吉尼亚密码 ###################################################
# ------------------------------------------------------------------------------------------------
# 使用一个词组作为密钥，密钥中的每一个字母用来确定一个代替表。
# 每一个密钥字母被用来加密一个明文字母。等所有的密钥字母使用完后，密钥再循环使用.
# ------------------------------------------------------------------------------------------------
# 加密过程：给定一个密钥字母K和一个明文字母P，密文字母就是位于K所在行与P所在列的交叉点上的那个字母。
# 解密过程：由密钥字母决定行，在该行中找到密文字母，密文字母所在列的列首对应的明文字母就是相应的明文。
# ------------------------------------------------------------------------------------------------

# 字母转数字
def number(alpha):
    return ord(alpha) - ord('A')

# 数字转字母
def alpha(number):
    return chr(number + ord('A'))

def encrypt(message, key):
    message = list(message.upper())
    key = ''.join(filter(str.isalpha, key)).upper()
    for i in range(len(message)):
        if message[i].isalpha():
            message[i] = alpha((number(message[i]) + number(key[i % len(key)])) % 26)
    cipher_text = ''.join(message).lower()

    return cipher_text

def decrypt(cipher_text, key):
    cipher_text = list(cipher_text.upper())
    key = ''.join(filter(str.isalpha, key)).upper()
    for i in range(len(cipher_text)):
        if cipher_text[i].isalpha():
            cipher_text[i] = alpha((number(cipher_text[i]) - number(key[i % len(key)])) % 26)
    message = ''.join(cipher_text).lower()
    
    return message

def main():
    while True:
        mode = input("1. 加密 2. 解密 (q 退出): ")

        if mode == '1':
            message = input("输入明文：")
            key = input("输入密钥：")
            print(f"密文：{encrypt(message, key)}")
        elif mode == '2':
            cipher_text = input("输入密文：")
            key = input("输入密钥：")
            print(f"明文：{decrypt(cipher_text, key)}")
        elif mode == 'q':
            break
        else:
            print("输入有误，请重新输入。")

if __name__ == '__main__':
    main()