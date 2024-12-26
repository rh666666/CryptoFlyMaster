import argparse,os , pyfiglet

from modules.classic import affine, hill, keyed_sub, playfair, vigenere
from modules.AES import ECB as AES
from modules.DES import ECB as DES
from modules.RC4 import RC4 as RC4
from modules.SM4 import ECB as SM4
from modules.ZUC import ZUC as ZUC
from modules.SM3 import SM3
from modules.SHA1 import SHA1
from modules.math import eratosthenes

def nogui_mode():
    error = False
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(pyfiglet.figlet_format('CryptoFlyMaster'))
        print("="*50)
        print("CryptoFlyMaster - A Classical Cryptography Toolbox")
        print("="*50)
        print("请选择一个模式：")
        print('''
        \033[94m 1\033[0m  使用密钥的单表代替密码
        \033[94m 2\033[0m  仿射密码
        \033[94m 3\033[0m  维吉尼亚密码
        \033[94m 4\033[0m  Playfair密码
        \033[94m 5\033[0m  希尔密码
        \033[0m 6\033[0m  输出200以内的所有素数
        \033[94m 7\033[0m  AES
        \033[94m 8\033[0m  DES
        \033[94m 9\033[0m  RC4
        \033[94m10\033[0m  SM4
        \033[94m11\033[0m  ZUC（未完成）
        \033[94m12\033[0m  SM3
        \033[94m13\033[0m  SHA-1
          
        \033[94m q\033[0m  退出
        ''')
        print("\n" * (os.get_terminal_size().lines - 32))
        if error:
            print('\033[91m输入有误，请重新输入！\033[0m')
            error = False

        mode = input("\033[92m> \033[0m")

        if mode == '1':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("单表代替密码：一种简单的替换密码，每个字母被替换为密钥字母表中的对应字母")
            print("="*50)
            keyed_sub.main()
            
        elif mode == '2':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("仿射密码：一种基于线性代数的替换密码")
            print("="*50)
            print(pyfiglet.figlet_format('Affine'))
            affine.main()

        elif mode == '3':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("维吉尼亚密码：一种基于多表替换的密码")
            print("="*50)
            print(pyfiglet.figlet_format('Vigenere'))
            vigenere.main()

        elif mode == '4':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("Playfair密码：一种基于矩阵的替换密码")
            print("="*50)
            print(pyfiglet.figlet_format('Playfair'))
            playfair.main()

        elif mode == '5':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("希尔密码：一种基于线性代数的多表替换密码")
            print("="*50)
            print(pyfiglet.figlet_format('Hill'))
            hill.main()

        elif mode == '6':
            os.system('cls' if os.name == 'nt' else 'clear') 
            eratosthenes.main()

        elif mode == '7':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("AES：高级加密标准，一种对称加密算法")
            print("="*50)
            print(pyfiglet.figlet_format('AES'))
            AES.main()

        elif mode == '8':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("DES：数据加密标准，一种对称加密算法")
            print("="*50)
            print(pyfiglet.figlet_format('DES'))
            DES.main()

        elif mode == '9':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("RC4：一种流密码算法")
            print("="*50)
            print(pyfiglet.figlet_format('RC4'))
            RC4.main()

        elif mode == '10':
            os.system('cls' if os.name == 'nt' else 'clear') 
            print("="*50)
            print("SM4：一种中国国家标准的分组密码算法")
            print("="*50)
            print(pyfiglet.figlet_format('SM4'))
            SM4.main()
            
        elif mode == '11':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*50)
            print("ZUC：一种流密码算法，尚未完成")
            print("="*50)
            print(pyfiglet.figlet_format('ZUC'))
            ZUC.main()
            
        elif mode == '12':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*50)
            print("SM3：一种中国国家标准的哈希算法")
            print("="*50)
            print(pyfiglet.figlet_format('SM3'))
            SM3.main()

        elif mode == '13':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("="*50)
            print("SHA-1：一种广泛使用的哈希算法")
            print("="*50)
            print(pyfiglet.figlet_format('SHA-1'))
            SHA1.main()

        elif mode == 'q':
            os.system('cls' if os.name == 'nt' else 'clear') 
            return
        
        else:
            error = True

def main():
    parser = argparse.ArgumentParser(description='CryptoFlyMaster 一个古典密码工具箱')
    parser.add_argument('--nogui', action='store_true', help='使用字符界面')
    args = parser.parse_args()

    nogui_mode()

if __name__ == '__main__':
    main()