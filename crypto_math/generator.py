#求生成元
#必有生成元的条件
#2、4
#素数的K次幂
#2的k次幂 k>=3
#模n的阶是欧拉函数(n)
import math
from gcd import gcd
#求生成元
def generator(n):
    generatorlist=[]
    further=[]
    for i in range(2,n):#找到所有互素的数字
        if(gcd(i,n)==1):
            further.append(i)
    length=len(further)#欧拉函数结果
    for i in further:#对所有数字进行测试
        all_result = []
        for j in range(length):
            all_result.append(pow(i,j,n))
        all_result=set(all_result)
        if(len(all_result)==length):
            generatorlist.append(i)

    return generatorlist

if __name__=='__main__':

    n = int( input( '输入数字模N' ) )

    print( generator( n ) )