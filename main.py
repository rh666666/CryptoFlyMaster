import argparse,os , sys, pyfiglet
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QIcon

import UI.Ui_tool, UI.Ui_main
import model.keyed_sub, model.affine, model.vigenere, model.playfair, model.hill
from model.exgcd import rp as rp

class ui_keyed_sub(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UI.Ui_tool.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_fill.setVisible(False)
        self.ui.lineEdit_fill.setVisible(False)
        self.ui.label_key2.setVisible(False)
        self.ui.lineEdit_key2.setVisible(False)
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.setWindowTitle("使用密钥的单表代替密码")
        

    def encrypt(self):
        message = self.ui.lineEdit_text.text()
        key = self.ui.lineEdit_key1.text()
        self.ui.textBrowser.setPlainText(f"密文：{model.keyed_sub.encrypt(message, key)}")

    def decrypt(self):
        cipher_text = self.ui.lineEdit_text.text()
        key = self.ui.lineEdit_key1.text()
        self.ui.textBrowser.setPlainText(f"明文：{model.keyed_sub.decrypt(cipher_text, key)}")
    
class ui_affine(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UI.Ui_tool.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_key1.setText('key1')
        self.ui.label_fill.setVisible(False)
        self.ui.lineEdit_fill.setVisible(False)
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.setWindowTitle("仿射密码")
        

    def encrypt(self):
        message = self.ui.lineEdit_text.text()
        key1 = int(self.ui.lineEdit_key1.text())
        key2 = int(self.ui.lineEdit_key2.text())
        self.ui.textBrowser.setPlainText(f"密文：{model.affine.encrypt(message, key1, key2)}")

    def decrypt(self):
        cipher_text = self.ui.lineEdit_text.text()
        key1 = int(self.ui.lineEdit_key1.text())
        if not rp(key1,26):
            self.ui.textBrowser.setPlainText("由于key1与26不互素，该密文不可逆！")
            return
        key2 = int(self.ui.lineEdit_key2.text())
        self.ui.textBrowser.setPlainText(f"明文：{model.affine.decrypt(cipher_text, key1, key2)}")

class ui_vegenere(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UI.Ui_tool.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_fill.setVisible(False)
        self.ui.lineEdit_fill.setVisible(False)
        self.ui.label_key2.setVisible(False)
        self.ui.lineEdit_key2.setVisible(False)
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.setWindowTitle("维吉尼亚密码")
        

    def encrypt(self):
        message = self.ui.lineEdit_text.text()
        key = self.ui.lineEdit_key1.text()
        self.ui.textBrowser.setPlainText(f"密文：{model.vigenere.encrypt(message, key)}")

    def decrypt(self):
        cipher_text = self.ui.lineEdit_text.text()
        key = self.ui.lineEdit_key1.text()
        self.ui.textBrowser.setPlainText(f"明文：{model.vigenere.decrypt(cipher_text, key)}")

class ui_playfair(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UI.Ui_tool.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_key2.setVisible(False)
        self.ui.lineEdit_key2.setVisible(False)
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.setWindowTitle("Playfair密码")
        

    def encrypt(self):
        message = self.ui.lineEdit_text.text()
        key = self.ui.lineEdit_key1.text()
        fill_char = self.ui.lineEdit_fill.text()
        self.ui.textBrowser.setPlainText(f"密文：{model.playfair.encrypt(message, key, fill_char)}")

    def decrypt(self):
        cipher_text = self.ui.lineEdit.text()
        key = self.ui.lineEdit_key1.text()
        fill_char = self.ui.lineEdit_fill.text()
        self.ui.textBrowser.setPlainText(f"明文：{model.playfair.encrypt(cipher_text, key, fill_char)}")

class ui_hill(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = UI.Ui_tool.Ui_Form()
        self.ui.setupUi(self)
        self.ui.label_key2.setVisible(False)
        self.ui.lineEdit_key2.setVisible(False)
        self.ui.pushButton.clicked.connect(self.encrypt)
        self.ui.pushButton_2.clicked.connect(self.decrypt)
        self.setWindowIcon(QIcon("image/icon.png"))
        self.setWindowTitle("希尔密码")
        

    def encrypt(self):
        message = self.ui.lineEdit_text.text()
        key = self.ui.lineEdit_key1.text()
        try:
            key = [[int(num) for num in row.split(' ')] for row in key.split(',')]
        except ValueError:
            self.ui.textBrowser.setPlainText('密钥错误，请重试。')
        fill_char = self.ui.lineEdit_fill.text()
        try:
            self.ui.textBrowser.setPlainText(f"密文：{model.hill.encrypt(message, key, fill_char)}")
        except ValueError:
            self.ui.textBrowser.setPlainText('密钥矩阵在模26下不可逆，请重试。')

    def decrypt(self):
        cipher_text = self.ui.lineEdit.text()
        key = self.ui.lineEdit_key1.text()
        try:
            key = [[int(num) for num in row.split(' ')] for row in key.split(',')]
        except ValueError:
            self.ui.textBrowser.setPlainText('密钥错误，请重试。')
        fill_char = self.ui.lineEdit_fill.text()
        self.ui.textBrowser.setPlainText(f"明文：{model.hill.encrypt(cipher_text, key, fill_char)}")

def ui_mode():
    print("不好意思哈，UI还没做好……")
    print("这边建议 python main.py --nogui 无UI启动程序呢~")
    app = QApplication(sys.argv)
    window = QMainWindow()

    main_ui = UI.Ui_main.Ui_MainWindow()
    main_ui.setupUi(window)
    
    window.keyed_sub = ui_keyed_sub()
    window.affine = ui_affine()
    window.vegenere = ui_vegenere()
    window.playfair = ui_playfair()
    window.hill = ui_hill()

    main_ui.pushButton.clicked.connect(window.keyed_sub.show)
    main_ui.pushButton_2.clicked.connect(window.affine.show)
    main_ui.pushButton_3.clicked.connect(window.vegenere.show)
    main_ui.pushButton_4.clicked.connect(window.playfair.show)
    main_ui.pushButton_5.clicked.connect(window.hill.show)

    window.setWindowTitle('CryptoFlyMaster')
    window.setWindowIcon(QIcon('image/icon.png'))
    window.show()
    sys.exit(app.exec_())

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
            q. 退出
            ''')
        mode = input("输入：")
        if mode == '1':
            os.system('cls' if os.name == 'nt' else 'clear') 
            model.keyed_sub.nogui()
        elif mode == '2':
            os.system('cls' if os.name == 'nt' else 'clear') 
            model.affine.nogui()
        elif mode == '3':
            os.system('cls' if os.name == 'nt' else 'clear') 
            model.vigenere.nogui()
        elif mode == '4':
            os.system('cls' if os.name == 'nt' else 'clear') 
            model.playfair.nogui()
        elif mode == '5':
            os.system('cls' if os.name == 'nt' else 'clear') 
            model.hill.nogui()
        elif mode == 'q':
            os.system('cls' if os.name == 'nt' else 'clear') 
            return
        else:
            print("Error: 请输入1-5.")

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