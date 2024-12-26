from modules.DES import DES
def pkcs7_pad(data: bytes, block_size: int = 8) -> bytes:
    """
    对数据进行 PKCS#7 填充。
    :param data: 输入的字节数据
    :param block_size: 块大小，默认为 8（DES 的块大小）
    :return: 填充后的字节数据
    """
    padding_len = block_size - len(data) % block_size
    padding = bytes([padding_len] * padding_len)
    return data + padding

def pkcs7_unpad(data: bytes) -> bytes:
    """
    去除 PKCS#7 填充。
    :param data: 填充后的字节数据
    :return: 去填充后的字节数据
    """
    padding_len = data[-1]  # 获取最后一个字节的值
    if padding_len > len(data):
        raise ValueError("Invalid padding.")
    return data[:-padding_len]
def main():
    while True:
        print('\n1. 加密 2. 解密 (q 退出): ')
        choice = input("\033[92m> \033[0m")
        if choice == 'q':
            return
        
        if choice not in ['1', '2']:
            print("\033[91m[-] 无效选择\033[0m")
            continue
        
        print("请输入文本:")
        Text = input("\033[92m> \033[0m")
        if choice == '1':
            Text_hex = ''.join(format(ord(char), '02x') for char in Text if char.isprintable())
            data_bytes = bytes.fromhex(Text_hex)
            Text_hex = pkcs7_pad(data_bytes).hex()
        else:
            Text_hex = Text

        print("请输入密钥:")
        Key = input("\033[92m> \033[0m")
        Key_hex = ''.join(format(ord(char), '02x') for char in Key if char.isprintable())
        if len(Key_hex) != 16:
            print("\033[91m[-] 密钥长度不为 64 位。\033[0m")
            continue
        
        result = ''

        for i in range(0, len(Text_hex),16):
            temp_str1 = Text_hex[i:i+16]
            result += DES.encryption(temp_str1, Key_hex) if choice == '1' else DES.decryption(temp_str1, Key_hex)

        if result:
            if choice == '1':
                print(f"\033[94m[+]\033[0m 明文：{Text}")
                print(f"\033[94m[+]\033[0m 密钥：{Key}")
                print(f'\033[92m[+] 加密成功！\033[0m')
                print(f'\033[92m[+] 密文：{result}\033[0m')
            else:
                data_bytes = bytes.fromhex(result)

                try:
                    result = pkcs7_unpad(data_bytes).hex()
                except ValueError:
                    print("\033[91m[-] 解密失败，填充错误。\033[0m")
                    continue

                byte_data = bytes.fromhex(result)
                result = ''.join(chr(b) for b in byte_data)
                
                print(f"\033[94m[+]\033[0m 密文：{Text}")
                print(f"\033[94m[+]\033[0m 密钥：{Key}")
                print(f'\033[92m[+] 解密成功！\033[0m')
                print(f'\033[92m[+] 明文：{result}\033[0m')
        else:
            print("处理失败，请检查输入。")

if __name__ == '__main__':
    main()