from numpy import array, linalg
from ..math.exgcd import inverse as inv, rp

class Matrix():
    def __init__(self, matrix):
        self.matrix = array(matrix)

    # 求代数余子式
    def algebraic_cofactor(self, i, j):  
        n, m = len(self.matrix), len(self.matrix[0])  
        new_matrix = [[0 for _ in range(m-1)] for _ in range(n-1)]  
        
        # 遍历原矩阵，但跳过指定的行和列  
        for new_row in range(n-1):  
            for new_col in range(m-1):  
                # 根据是否跳过行和列来调整原矩阵的索引  
                if new_row < i:  
                    row = new_row  
                else:  
                    row = new_row + 1  
                if new_col < j:  
                    col = new_col  
                else:  
                    col = new_col + 1  
                new_matrix[new_row][new_col] = self.matrix[row][col]  
        
        # 计算代数余子式
        det = linalg.det(new_matrix)
        if (i + j) % 2 == 0:  
            return round(det)  
        else:  
            return round(-det)

    # 求伴随矩阵
    def c(self):
        # 初始化伴随矩阵
        conj_matrix = []
        for i in range(len(self.matrix)):
            conj_matrix.append([0] * len(self.matrix[i]))
            
        # 构造伴随矩阵
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                conj_matrix[i][j] = self.algebraic_cofactor(i, j)
        
        return array(conj_matrix)

    # 求模逆矩阵
    def inverse(self):  
        arr_adjoint = self.c()  
        arr_abs = int(round(linalg.det(self.matrix)))  # 确保行列式是整数  
        if rp(arr_abs, 26):  # 检查行列式与26是否互素  
            arr_inverse_element = inv(arr_abs, 26)  # 计算模逆元  
            arr_inverse = arr_inverse_element * arr_adjoint.T  # 计算逆矩阵（未取模）  
            arr_inverse = arr_inverse % 26  # 对结果取模26  
            return arr_inverse  
        else:  
            raise ValueError("Matrix is not invertible modulo 26")  # 如果不互素，则抛出异常