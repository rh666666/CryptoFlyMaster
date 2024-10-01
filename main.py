import argparse, subprocess, sys, pyfiglet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QIcon

import model.keyed_sub
import model.affine
import model.hill
import model.playfair
import model.vigenere

import UI.Ui_main

def nogui_mode():
    while True:
        subprocess.call("cls", shell=True)
        print(pyfiglet.figlet_format('CryptoFlyMaster'))
        print("输入相应数字选择模式：")
        print('''
            1. 使用密钥的单表代替密码
            2. 仿射密码
            3. 维几尼亚密码
            4. Playfair密码
            5. 希尔密码
            q. 退出
            ''')
        mode = input("输入：")
        if mode == '1':
            subprocess.call("cls", shell=True)
            model.keyed_sub.nogui()
        elif mode == '2':
            subprocess.call("cls", shell=True)
            model.affine.nogui()
        elif mode == '3':
            subprocess.call("cls", shell=True)
            model.vigenere.nogui()
        elif mode == '4':
            subprocess.call("cls", shell=True)
            model.playfair.nogui()
        elif mode == '5':
            subprocess.call("cls", shell=True)
            model.hill.nogui()
        elif mode == 'q':
            subprocess.call("cls", shell=True)
            return
        else:
            print("Error: 请输入1-5.")

def ui_mode():
    print("不好意思哈，UI还没做好……")
    print("这边建议 python main.py --nogui 无UI启动程序呢~")
    app = QApplication(sys.argv)
    win = QMainWindow()
    ui = UI.Ui_main.Ui_MainWindow()
    ui.setupUi(win)
    win.setWindowTitle('CryptoFlyMaster')
    win.setWindowIcon(QIcon('image/icon.png'))
    win.show()
    sys.exit(app.exec_())

def main():
    parser = argparse.ArgumentParser(description='CryptoFlyMaster 一个古典密码工具箱')
    parser.add_argument('--nogui', action='store_true', help='使用字符界面')
    args = parser.parse_args()

    if args.nogui:
        nogui_mode()
    else:
        ui_mode()

if __name__ == '__main__':
    main()