# 欧几里得和扩展欧几里得算法
def exgcd(a, b):
    if b == 0:
        return (a, 1, 0)
    else:
        g, x, y = exgcd(b, a % b)
        return (g, y, x - (a // b) * y)
    
# 判断两数是否互素
def rp(a, b):
    g, _, _ = exgcd(a, b)
    return g == 1

# 输出a mod b的逆元
def inverse(a, b):
    g, x, _ = exgcd(a, b)
    if g != 1:
        raise ValueError(f"{a}和{b}不互素，因此{a}没有模{b}的逆元。")
    return (x % b + b) % b

if __name__ == '__main__':
    a, b = map(int, input().split())
    g, x, y = exgcd(a, b)
    
    print(f'GCD of {a} and {b} is {g}')
    print(f'X = {x}, Y = {y}')