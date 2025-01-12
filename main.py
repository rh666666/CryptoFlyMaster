import argparse,os

from modules.classic import affine, hill, keyed_sub, playfair, vigenere
from modules.AES import ECB as AES
from modules.DES import ECB as DES
from modules.RC4 import RC4 as RC4
from modules.SM4 import ECB as SM4
from modules.ZUC import ZUC as ZUC
from modules.SM3 import SM3
from modules.SHA1 import SHA1
from modules.math import eratosthenes

def console_mode():
    import pyfiglet
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
    parser.add_argument('--console', action='store_true', help='控制台界面')
    parser.add_argument('--version', action='version', version='CryptoFlyMaster 1.0')
    
    # 参数选择模式，用法举例：python main.py playfair --encrypt abcd --key haks --fill x
    subparsers = parser.add_subparsers(title='模式', dest='mode')
    
    # 单表代替
    keyed_sub_parser = subparsers.add_parser('keyed_sub', help='单表代替密码')
    keyed_sub_parser.add_argument('-e', '--encrypt', help='加密')
    keyed_sub_parser.add_argument('-d', '--decrypt', help='解密')
    keyed_sub_parser.add_argument('-k', '--key', help='密钥')
    
    # 仿射
    affine_parser = subparsers.add_parser('affine', help='仿射密码')
    affine_parser.add_argument('-e', '--encrypt', help='加密')
    affine_parser.add_argument('-d', '--decrypt', help='解密')
    affine_parser.add_argument('-a', help='密钥a')
    affine_parser.add_argument('-b', help='密钥b')
    
    # playfair
    playfair_parser = subparsers.add_parser('playfair', help='Playfair密码')
    playfair_parser.add_argument('-e', '--encrypt', help='加密')
    playfair_parser.add_argument('-d', '--decrypt', help='解密')
    playfair_parser.add_argument('-k', '--key', help='密钥')
    playfair_parser.add_argument('--fill', help='填充字符')
    
    # 维吉尼亚
    vigenere_parser = subparsers.add_parser('vigenere', help='维吉尼亚密码')
    vigenere_parser.add_argument('-e', '--encrypt', help='加密')
    vigenere_parser.add_argument('-d', '--decrypt', help='解密')
    vigenere_parser.add_argument('-k', '--key', help='密钥')
    
    # 希尔
    hill_parser = subparsers.add_parser('hill', help='希尔密码')
    hill_parser.add_argument('-e', '--encrypt', help='加密')
    hill_parser.add_argument('-d', '--decrypt', help='解密')
    hill_parser.add_argument('-k', '--key', help='密钥')
    hill_parser.add_argument('--fill', help='填充字符')
    
    # DES
    des_parser = subparsers.add_parser('des', help='DES')
    des_parser.add_argument('-e', '--encrypt', help='加密')
    des_parser.add_argument('-d', '--decrypt', help='解密')
    des_parser.add_argument('-k', '--key', help='密钥')
    
    # AES
    aes_parser = subparsers.add_parser('aes', help='AES')
    aes_parser.add_argument('-e', '--encrypt', help='加密')
    aes_parser.add_argument('-d', '--decrypt', help='解密')
    aes_parser.add_argument('-k', '--key', help='密钥')
    
    # RC4
    rc4_parser = subparsers.add_parser('rc4', help='RC4')
    rc4_parser.add_argument('-e', '--encrypt', help='加密')
    rc4_parser.add_argument('-d', '--decrypt', help='解密')
    rc4_parser.add_argument('-k', '--key', help='密钥')
    
    # SM4
    sm4_parser = subparsers.add_parser('sm4', help='SM4')
    sm4_parser.add_argument('-e', '--encrypt', help='加密')
    sm4_parser.add_argument('-d', '--decrypt', help='解密')
    sm4_parser.add_argument('-k', '--key', help='密钥')
    
    # ZUC
    zuc_parser = subparsers.add_parser('zuc', help='ZUC')
    zuc_parser.add_argument('-e', '--encrypt', help='加密')
    zuc_parser.add_argument('-d', '--decrypt', help='解密')
    zuc_parser.add_argument('-k', '--key', help='密钥')
    
    # SM3
    sm3_parser = subparsers.add_parser('sm3', help='SM3')
    sm3_parser.add_argument('-e', '--encrypt', help='加密')
    sm3_parser.add_argument('-d', '--decrypt', help='解密')
    sm3_parser.add_argument('-k', '--key', help='密钥')
    
    # SHA-1
    sha1_parser = subparsers.add_parser('sha1', help='SHA-1')
    sha1_parser.add_argument('-e', '--encrypt', help='加密')
    sha1_parser.add_argument('-d', '--decrypt', help='解密')
    sha1_parser.add_argument('-k', '--key', help='密钥')
    
    args = parser.parse_args()

    if args.console:
        console_mode()
        
    elif args.mode == 'keyed_sub':
        if args.encrypt:
            print(keyed_sub.encrypt(args.encrypt, args.key))
        elif args.decrypt:
            print(keyed_sub.decrypt(args.decrypt, args.key))
            
    elif args.mode == 'affine':
        if args.encrypt:
            print(affine.encrypt(args.encrypt, args.a, args.b))
        elif args.decrypt:
            print(affine.decrypt(args.decrypt, args.a, args.b))
        
    elif args.mode == 'playfair':
        if args.encrypt:
            if args.fill:
                print(playfair.encrypt(args.encrypt, args.key, args.fill))
            else:
                print(playfair.encrypt(args.encrypt, args.key))
        elif args.decrypt:
            print(playfair.decrypt(args.decrypt, args.key))
            
    elif args.mode == 'vigenere':
        if args.encrypt:
            print(vigenere.encrypt(args.encrypt, args.key))
        elif args.decrypt:
            print(vigenere.decrypt(args.decrypt, args.key))
            
    elif args.mode == 'hill':
        try:
            key = [[int(num) for num in row.split(' ')] for row in args.key.split(',')]
            
        except ValueError:
            print("\033[91m[-] 密钥错误，请重试。\033[0m")
            exit()
        if args.encrypt:
            if args.fill:
                print(hill.encrypt(args.encrypt, key, args.fill))
            else:
                print(hill.encrypt(args.encrypt, key))
        elif args.decrypt:
            print(hill.decrypt(args.decrypt, key))
            
    else:
        parser.print_help()

if __name__ == '__main__':
    main()