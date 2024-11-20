import argparse,os , pyfiglet

import crypto_modules.keyed_sub, crypto_modules.affine, crypto_modules.vigenere, crypto_modules.playfair, crypto_modules.hill, crypto_modules.eratosthenes
from crypto_modules.exgcd import rp as rp
from crypto_modules.errors import MessageError, KeyError, AlphaError

def nogui_mode():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') 
        print(pyfiglet.figlet_format('CryptoFlyMaster'))
        print("输入相应数字选择模式：")
        print('''
            1. 使用密钥的单表代替密码
            2. 仿射密码
            3. 维吉尼亚密码
            4. Playfair密码
            5. 希尔密码
            6. 输出200以内的所有素数
            q. 退出
            ''')
        mode = input("输入：")
        if mode == '1':
            os.system('cls' if os.name == 'nt' else 'clear') 
            crypto_modules.keyed_sub.nogui()
        elif mode == '2':
            os.system('cls' if os.name == 'nt' else 'clear') 
            crypto_modules.affine.nogui()
        elif mode == '3':
            os.system('cls' if os.name == 'nt' else 'clear') 
            crypto_modules.vigenere.nogui()
        elif mode == '4':
            os.system('cls' if os.name == 'nt' else 'clear') 
            crypto_modules.playfair.nogui()
        elif mode == '5':
            os.system('cls' if os.name == 'nt' else 'clear') 
            crypto_modules.hill.nogui()
        elif mode == '6':
            os.system('cls' if os.name == 'nt' else 'clear') 
            crypto_modules.eratosthenes.nogui()
        elif mode == 'q':
            os.system('cls' if os.name == 'nt' else 'clear') 
            return
        else:
            print("Error: 请输入1-5.")

def main():
    parser = argparse.ArgumentParser(description='CryptoFlyMaster 一个古典密码工具箱')
    parser.add_argument('--nogui', action='store_true', help='使用字符界面')
    args = parser.parse_args()

    nogui_mode()

if __name__ == '__main__':
    main()