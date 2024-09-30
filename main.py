import model
import argparse

import model.affine
import model.hill
import model.keyed_sub
import model.playfair
import model.vigenere

def nogui_mode():
    while True:
        print('''
            输入相应数字选择模式：
            1. 使用密钥的单表代替密码
            2. 仿射密码
            3. 维几尼亚密码
            4. Playfair密码
            5. 希尔密码
            q. 退出
            ''')
        mode = int(input("输入："))
        if mode == 1:
            model.keyed_sub.nogui()
        elif mode == 2:
            model.affine.nogui()
        elif mode == 3:
            model.vigenere.nogui()
        elif mode == 4:
            model.playfair.nogui()
        elif mode == 5:
            model.hill.nogui()
        elif mode == 'q':
            return
        else:
            print("Error: 请输入1-5.")

def ui_mode():
    print("不好意思哈，UI还没做……")

def main():
    parser = argparse.ArgumentParser(description='报错带师')
    parser.add_argument('-nogui', action='store_true', help='使用字符界面')
    args = parser.parse_args()

    if args.nogui:
        nogui_mode()
    else:
        ui_mode()

if __name__ == '__main__':
    main()