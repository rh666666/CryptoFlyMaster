import argparse,os , sys, pyfiglet
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import UI.Ui_main
import model.keyed_sub, model.affine, model.vigenere, model.playfair, model.hill, model.eratosthenes
from model.exgcd import rp as rp
from model.errors import MessageError, KeyError, AlphaError


def ui_keyed_sub(ui):
    ui.title.setVisible(True)
    ui.label_text.setVisible(True)
    ui.lineEdit_text.setVisible(True)
    ui.lineEdit_text.setText('')
    ui.label_key1.setVisible(True)
    ui.lineEdit_key1.setVisible(True)
    ui.lineEdit_key1.setText('')
    ui.label_key2.setVisible(False)
    ui.lineEdit_key2.setVisible(False)
    ui.label_fill.setVisible(False)
    ui.lineEdit_fill.setVisible(False)
    ui.pushButton.setVisible(True)
    ui.pushButton_2.setVisible(True)
    ui.textBrowser.setVisible(True)

    ui.pushButton.clicked.connect(lambda: encrypt())
    ui.pushButton_2.clicked.connect(lambda: decrypt())
    ui.title.setText('密钥单表')
    ui.title.setAlignment(Qt.AlignCenter)
    
    def encrypt():
        message = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        ui.textBrowser.setPlainText(f"密文：{model.keyed_sub.encrypt(message, key)}")

    def decrypt():
        cipher_text = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        ui.textBrowser.setPlainText(f"明文：{model.keyed_sub.decrypt(cipher_text, key)}")
    
def ui_affine(ui):
    ui.title.setVisible(True)
    ui.label_text.setVisible(True)
    ui.lineEdit_text.setVisible(True)
    ui.lineEdit_text.setText('')
    ui.label_key1.setVisible(True)
    ui.label_key1.setText('key1')
    ui.lineEdit_key1.setVisible(True)
    ui.lineEdit_key1.setText('')
    ui.label_key2.setVisible(True)
    ui.label_key2.setText('key2')
    ui.lineEdit_key2.setVisible(True)
    ui.lineEdit_key2.setText('')
    ui.label_fill.setVisible(False)
    ui.lineEdit_fill.setVisible(False)
    ui.pushButton.setVisible(True)
    ui.pushButton_2.setVisible(True)
    ui.textBrowser.setVisible(True)

    ui.pushButton.clicked.connect(lambda: encrypt())
    ui.pushButton_2.clicked.connect(lambda: decrypt())
    ui.title.setText('仿射密码')
    ui.title.setAlignment(Qt.AlignCenter)
        

    def encrypt():
        message = ui.lineEdit_text.text()
        key1 = int(ui.lineEdit_key1.text())
        key2 = int(ui.lineEdit_key2.text())
        ui.textBrowser.setPlainText(f"密文：{model.affine.encrypt(message, key1, key2)}")

    def decrypt():
        cipher_text = ui.lineEdit_text.text()
        key1 = int(ui.lineEdit_key1.text())
        if not rp(key1,26):
            ui.textBrowser.setPlainText("由于key1与26不互素，该密文不可逆！")
            return
        key2 = int(ui.lineEdit_key2.text())
        ui.textBrowser.setPlainText(f"明文：{model.affine.decrypt(cipher_text, key1, key2)}")

def ui_vegenere(ui):
    ui.title.setVisible(True)
    ui.label_text.setVisible(True)
    ui.lineEdit_text.setVisible(True)
    ui.lineEdit_text.setText('')
    ui.label_key1.setVisible(True)
    ui.lineEdit_key1.setVisible(True)
    ui.lineEdit_key1.setText('')
    ui.label_key2.setVisible(False)
    ui.lineEdit_key2.setVisible(False)
    ui.label_fill.setVisible(False)
    ui.lineEdit_fill.setVisible(False)
    ui.pushButton.setVisible(True)
    ui.pushButton_2.setVisible(True)
    ui.textBrowser.setVisible(True)

    ui.pushButton.clicked.connect(lambda: encrypt())
    ui.pushButton_2.clicked.connect(lambda: decrypt())
    ui.title.setText('维吉尼亚密码')
    ui.title.setAlignment(Qt.AlignCenter)
        

    def encrypt():
        message = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        ui.textBrowser.setPlainText(f"密文：{model.vigenere.encrypt(message, key)}")

    def decrypt():
        cipher_text = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        ui.textBrowser.setPlainText(f"明文：{model.vigenere.decrypt(cipher_text, key)}")

def ui_playfair(ui):
    ui.title.setVisible(True)
    ui.label_text.setVisible(True)
    ui.lineEdit_text.setVisible(True)
    ui.lineEdit_text.setText('')
    ui.label_key1.setVisible(True)
    ui.lineEdit_key1.setVisible(True)
    ui.lineEdit_key1.setText('')
    ui.label_key2.setVisible(False)
    ui.lineEdit_key2.setVisible(False)
    ui.label_fill.setVisible(True)
    ui.lineEdit_fill.setVisible(True)
    ui.lineEdit_fill.setText('')
    ui.pushButton.setVisible(True)
    ui.pushButton_2.setVisible(True)
    ui.textBrowser.setVisible(True)

    ui.pushButton.clicked.connect(lambda: encrypt())
    ui.pushButton_2.clicked.connect(lambda:decrypt())
    ui.title.setText(' Playfair 密码')
    ui.title.setAlignment(Qt.AlignCenter)
        
    def encrypt():
        message = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        fill_char = ui.lineEdit_fill.text()
        try:
            ui.textBrowser.setPlainText(f"密文：{model.playfair.encrypt(message, key, fill_char)}")
        except MessageError:
            ui.textBrowser.setPlainText('明文不能为空！')
        except AlphaError:
            ui.textBrowser.setPlainText('加密填充字符不能为空！')

    def decrypt():
        cipher_text = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        fill_char = ui.lineEdit_fill.text()
        ui.textBrowser.setPlainText(f"明文：{model.playfair.decrypt(cipher_text, key)}")

def ui_hill(ui):
    ui.title.setVisible(True)
    ui.label_text.setVisible(True)
    ui.lineEdit_text.setVisible(True)
    ui.lineEdit_text.setText('')
    ui.label_key1.setVisible(True)
    ui.lineEdit_key1.setVisible(True)
    ui.lineEdit_key1.setText('')
    ui.label_key2.setVisible(False)
    ui.lineEdit_key2.setVisible(False)
    ui.label_fill.setVisible(True)
    ui.lineEdit_fill.setVisible(True)
    ui.lineEdit_fill.setText('')
    ui.pushButton.setVisible(True)
    ui.pushButton_2.setVisible(True)
    ui.textBrowser.setVisible(True)

    ui.pushButton.clicked.connect(lambda: encrypt())
    ui.pushButton_2.clicked.connect(lambda: decrypt())
    ui.title.setText('希尔密码')
    ui.title.setAlignment(Qt.AlignCenter)

    def encrypt():
        message = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        try:
            key = [[int(num) for num in row.split(' ')] for row in key.split(',')]
        except ValueError:
            ui.textBrowser.setPlainText('密钥错误，请重试。')
        fill_char = ui.lineEdit_fill.text()
        try:
            ui.textBrowser.setPlainText(f"密文：{model.hill.encrypt(message, key, fill_char)}")
        except ValueError:
            ui.textBrowser.setPlainText('密钥矩阵在模26下不可逆，请重试。')

    def decrypt():
        cipher_text = ui.lineEdit_text.text()
        key = ui.lineEdit_key1.text()
        try:
            key = [[int(num) for num in row.split(' ')] for row in key.split(',')]
        except ValueError:
            ui.textBrowser.setPlainText('密钥错误，请重试。')
        ui.textBrowser.setPlainText(f"明文：{model.hill.decrypt(cipher_text, key)}")

def ui_mode():
    app = QApplication(sys.argv)
    win = QMainWindow()

    main_ui = UI.Ui_main.Ui_MainWindow()
    main_ui.setupUi(win)
    main_ui.title.setText('CryptoFlyMaster')
    main_ui.title.setAlignment(Qt.AlignCenter)

    main_ui.title.setVisible(True)
    main_ui.label_text.setVisible(False)
    main_ui.lineEdit_text.setVisible(False)
    main_ui.label_key1.setVisible(False)
    main_ui.lineEdit_key1.setVisible(False)
    main_ui.label_key2.setVisible(False)
    main_ui.lineEdit_key2.setVisible(False)
    main_ui.label_fill.setVisible(False)
    main_ui.lineEdit_fill.setVisible(False)
    main_ui.pushButton.setVisible(False)
    main_ui.pushButton_2.setVisible(False)
    main_ui.textBrowser.setVisible(False)
    
    main_ui.actionKeyedsub.triggered.connect(lambda: ui_keyed_sub(main_ui))
    main_ui.actionAffine.triggered.connect(lambda: ui_affine(main_ui))
    main_ui.actionVegenere.triggered.connect(lambda: ui_vegenere(main_ui))
    main_ui.actionPlayfair.triggered.connect(lambda: ui_playfair(main_ui))
    main_ui.actionHill.triggered.connect(lambda: ui_hill(main_ui))

    win.setWindowTitle('CryptoFlyMaster')
    win.setWindowIcon(QIcon('image/icon.png'))
    win.show()
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
            6. 输出200以内的所有素数
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
        elif mode == '6':
            os.system('cls' if os.name == 'nt' else 'clear') 
            model.eratosthenes.nogui()
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