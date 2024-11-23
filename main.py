import argparse,os , pyfiglet

from modules.classic import affine, hill, keyed_sub, playfair, vigenere
from modules.AES import ECB as AES
from modules.DES import ECB as DES
from modules.RC4 import RC4 as RC4
from modules.SM4 import ECB as SM4
from modules.math import eratosthenes

def nogui_mode():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear') 
        print(pyfiglet.figlet_format('CryptoFlyMaster'))
        print("输入相应数字选择模式：")
        print('''
            1.  使用密钥的单表代替密码
            2.  仿射密码
            3.  维吉尼亚密码
            4.  Playfair密码
            5.  希尔密码
            6.  输出200以内的所有素数
            7.  AES
            8.  DES
            9.  RC4
            10. SM4
            q. 退出
            ''')
        mode = input("输入：")
        if mode == '1':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('单表代替'))
            keyed_sub.main()
        elif mode == '2':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('仿射密码'))
            affine.main()
        elif mode == '3':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('Vigenere'))
            vigenere.main()
        elif mode == '4':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('Playfair'))
            playfair.main()
        elif mode == '5':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('Hill'))
            hill.main()
        elif mode == '6':
            os.system('cls' if os.name == 'nt' else 'clear') 
            eratosthenes.main()
        elif mode == '7':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('AES'))
            AES.main()
        elif mode == '8':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('DES'))
            DES.main()
        elif mode == '9':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('RC4'))
            RC4.main()
        elif mode == '10':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print(pyfiglet.figlet_format('SM4'))
            SM4.main()
        elif mode == 'q':
            os.system('cls' if os.name == 'nt' else 'clear') 
            return
        else:
            print("Error: 请输入1-8.")

def main():
    parser = argparse.ArgumentParser(description='CryptoFlyMaster 一个古典密码工具箱')
    parser.add_argument('--nogui', action='store_true', help='使用字符界面')
    args = parser.parse_args()

    nogui_mode()

if __name__ == '__main__':
    main()