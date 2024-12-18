#求a,b,乘法逆元
#a*x+b*y=gcd(a,b)
#xn=yn+1
#yn=xn+1 - ( ( an / bn ) * yn+1 )
#
#终点(a,0)=a
def gcd_ext(a,b,c):
    if(b==0):
        return (1,0,a)
    else:
        a1,b1,c1=gcd_ext(b,a%b,c)

        return (b1,a1-(a//b)*b1,c1)




if __name__=='__main__':
    a=int(input('输入数字a'))
    b=int(input('输入数字b'))
    print(gcd_ext(550,1723,0))