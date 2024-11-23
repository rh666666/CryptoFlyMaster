from modules.SM4 import S_box
CK_matrix = [ 
 '00000000000001110000111000010101',
 '00011100001000110010101000110001',
 '00111000001111110100011001001101',
 '01010100010110110110001001101001',
 '01110000011101110111111010000101',
 '10001100100100111001101010100001',
 '10101000101011111011011010111101',
 '11000100110010111101001011011001',
 '11100000111001111110111011110101',
 '11111100000000110000101000010001',
 '00011000000111110010011000101101',
 '00110100001110110100001001001001',
 '01010000010101110101111001100101',
 '01101100011100110111101010000001',
 '10001000100011111001011010011101',
 '10100100101010111011001010111001',
 '11000000110001111100111011010101',
 '11011100111000111110101011110001',
 '11111000111111110000011000001101',
 '00010100000110110010001000101001',
 '00110000001101110011111001000101',
 '01001100010100110101101001100001',
 '01101000011011110111011001111101',
 '10000100100010111001001010011001',
 '10100000101001111010111010110101',
 '10111100110000111100101011010001',
 '11011000110111111110011011101101',
 '11110100111110110000001000001001',
 '00010000000101110001111000100101',
 '00101100001100110011101001000001',
 '01001000010011110101011001011101',
 '01100100011010110111001001111001'
]
def init(text):
    text_str = ''
    for i in text:
        i = f"{int(i, 16):04b}"
        text_str += i

    text_matrix = [text_str[i:i+32] for i in range(0, len(text_str), 32)]
    return text_matrix
def bcd_to_hex(bcd_str):#将字符串BCD码转换为字符串16进制数
    hex_result = ""
    for i in range(0, len(bcd_str), 4):
        bcd_digit = bcd_str[i:i+4]
        hex_char = hex(int(bcd_digit, 2))[2:].upper()
        hex_result += hex_char
    return hex_result
def xor_bcd(bcd1, bcd2): #BCD码异或操作
    result = ""
    for i in range(len(bcd1)):
        xor_bit = str(int(bcd1[i]) ^ int(bcd2[i]))
        result += xor_bit
    return result
def T(text):
    text_str = ''
    for i in range(0,len(text),8):
        text_str += S_box.get(text[i:i+8])
    text_str2 = text_str[2:]+text_str[:2]
    text_str10 = text_str[10:]+text_str[:10]
    text_str18 = text_str[18:]+text_str[:18]
    text_str24 = text_str[24:]+text_str[:24]
    return xor_bcd(text_str,xor_bcd(xor_bcd(xor_bcd(text_str18,text_str24),text_str10),text_str2))
def T_new(text):
    text_str = ''
    for i in range(0,len(text),8):
        text_str += S_box.get(text[i:i+8])
    text_str_13 = text_str[13:]+text_str[:13]
    text_str_23 = text_str[23:]+text_str[:23]
    return xor_bcd(text_str,xor_bcd(text_str_13,text_str_23))
def Key_expand(key_matrix):
    key_list = []
    FK_matrix = init('A3B1BAC656AA3350677D9197B27022DC')
    K_list = []
    for i in range(4):
        K_list.append(xor_bcd(key_matrix[i],FK_matrix[i]))
    for i in range(32):
        temp = (xor_bcd(xor_bcd(xor_bcd(K_list[i+1], K_list[i+2]),K_list[i+3]),CK_matrix[i]))
        K_list.append(xor_bcd(K_list[i],T_new(temp)))
        key_list.append(xor_bcd(K_list[i],T_new(temp)))
    return key_list
def encryption(text,key):
    key_matrix = init(key)
    text_matrix = init(text)
    key_list = Key_expand(key_matrix)
    text_list = []
    for i in range(32):
        temp = xor_bcd(text_matrix[i],T(xor_bcd(key_list[i],xor_bcd(xor_bcd(text_matrix[i+1],text_matrix[i+2]),text_matrix[i+3]))))
        text_matrix.append(temp)
    
    result = ''
    result += ''.join(text_matrix[-1:-5:-1]) 
    return bcd_to_hex(result)
def decryption(text,key):
    key_matrix = init(key)
    text_matrix = init(text)
    key_list = Key_expand(key_matrix)
    text_list = []
    for i in range(32):
        temp = xor_bcd(text_matrix[i],T(xor_bcd(key_list[31-i],xor_bcd(xor_bcd(text_matrix[i+1],text_matrix[i+2]),text_matrix[i+3]))))
        text_matrix.append(temp)
    
    result = ''
    result += ''.join(text_matrix[-1:-5:-1]) 
    return bcd_to_hex(result)

if __name__ == '__main__':
    pass
#明文：0123456789abcdeffedcba9876543210
#密钥：0123456789abcdeffedcba9876543210
#密文：681edf34d206965e86b3e94f536e4246