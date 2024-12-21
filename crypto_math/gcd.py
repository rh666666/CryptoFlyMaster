#求最大公约数
def gcd(a,b):
    while b!=0:
        a,b=b,a%b

    return a

if __name__=='__main__':
    a=int(input('输入数字a'))
    b=int(input('输入数字b'))
    print(gcd(365,25))