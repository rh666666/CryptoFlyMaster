def ksa(key: list) -> list:
    """
    RC4 密钥调度算法 (KSA)。
    :param key: 密钥（整数列表）
    :return: 初始化后的状态数组 S
    """
    S = list(range(256))  # 初始化状态数组
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]  # 交换 S[i] 和 S[j]
    return S

def prga(S: list, data_len: int) -> list:
    """
    RC4 伪随机数生成算法 (PRGA)。
    :param S: 状态数组
    :param data_len: 数据长度
    :return: 生成的密钥流
    """
    i = j = 0
    keystream = []
    for _ in range(data_len):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]  # 交换 S[i] 和 S[j]
        K = S[(S[i] + S[j]) % 256]
        keystream.append(K)
    return keystream


def rc4_encrypt_decrypt(key: str, text: str, is_encrypt: bool) -> str:
    """
    RC4 加密/解密函数。
    :param key: 密钥（字符串）
    :param text: 明文或密文（字符串）
    :param is_encrypt: 如果为 True，则加密；否则为解密
    :return: 加密后的密文（十六进制）或解密后的明文
    """
    # 转换密钥为整数列表
    key_bytes = [ord(char) for char in key]  # 每个字符转为整数

    if is_encrypt:
        # 加密时将字符串明文转为字节列表
        data_bytes = [ord(char) for char in text]
    else:
        # 解密时将十六进制字符串转为字节列表
        data_bytes = [int(text[i:i+2], 16) for i in range(0, len(text), 2)]

    # 调用 KSA 和 PRGA 生成密钥流
    S = ksa(key_bytes)
    keystream = prga(S, len(data_bytes))

    # 加密/解密：将数据字节与密钥流逐字节异或
    result_bytes = [data_byte ^ k for data_byte, k in zip(data_bytes, keystream)]

    if is_encrypt:
        # 加密返回十六进制字符串
        return ''.join(format(byte, '02x') for byte in result_bytes)
    else:
        # 解密返回明文字符串
        return ''.join(chr(byte) for byte in result_bytes)
    
def main():
    while True:
        choice = input("请输入 1 进行加密, 2 进行解密, q 退出: ")
        if choice == 'q':
                    return
        
        if choice not in ['1', '2']:
            print("无效选择")
            continue

        key = input("请输入密钥：")  # 用户输入密钥
        text = input("请输入文本：")  # 用户输入明文或密文

        if choice == '1':
            # 加密
            ciphertext = rc4_encrypt_decrypt(key, text, is_encrypt=True)
            print(f"加密后的密文：{ciphertext}")
        else:
            # 解密
            plaintext = rc4_encrypt_decrypt(key, text, is_encrypt=False)
            print(f"解密后的明文：{plaintext}")

if __name__ == '__main__':
    main()