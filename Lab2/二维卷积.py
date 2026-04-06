import sys
import math

# 设置快速输入
def input():
    return sys.stdin.readline()

def fft1d(a, invert):
    """
    :param invert: False表示正变换(FFT)，True表示逆变换(IFFT)
    """
    n = len(a)
    # 位反转置换 (Bit-reversal permutation)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]

    # 蝶形运算 (Danielson-Lanczos Lemma)
    ln = 2
    while ln <= n:
        angle = 2 * math.pi / ln * (-1 if invert else 1)
        wlen = complex(math.cos(angle), math.sin(angle))
        for i in range(0, n, ln):
            w = complex(1, 0)
            for j in range(ln // 2):
                u = a[i + j]
                v = a[i + j + ln // 2] * w
                a[i + j] = u + v
                a[i + j + ln // 2] = u - v
                w *= wlen
        ln *= 2
        
    # 如果是逆变换，所有元素都要除以长度 n
    if invert:
        for i in range(n):
            a[i] /= n

def fft2d(matrix, invert):
    """
    2维快速傅里叶变换
    先对每一行做 1D FFT，再对每一列做 1D FFT
    """
    R = len(matrix)
    C = len(matrix[0])
    
    # 1. 对每一行进行 1 维 FFT
    for i in range(R):
        fft1d(matrix[i], invert)

    # 2. 对每一列进行 1 维 FFT
    matrix_t = [[matrix[i][j] for i in range(R)] for j in range(C)]
    for i in range(C):
        fft1d(matrix_t[i], invert)

    for i in range(R):
        for j in range(C):
            matrix[i][j] = matrix_t[j][i]

def solve():
    # 读取输入
    raw_input = sys.stdin.read().split()
    if not raw_input:
        return
        
    ptr = 0
    n = int(raw_input[ptr])
    m = int(raw_input[ptr+1])
    ptr = 2
    
    A = []
    for _ in range(n):
        A.append([int(raw_input[ptr + j]) for j in range(m)])
        ptr += m
        
    p = int(raw_input[ptr])
    q = int(raw_input[ptr+1])
    ptr += 2
    
    K = []
    for _ in range(p):
        K.append([int(raw_input[ptr + j]) for j in range(q)])
        ptr += q

    # 找到足以容纳卷积结果的、且是 2的指数次幂 的长和宽
    R = 1
    while R < n + p: 
        R *= 2
    C = 1
    while C < m + q: 
        C *= 2

    # 填充矩阵 A，其余补 0
    A_pad = [[complex(0, 0)] * C for _ in range(R)]
    for i in range(n):
        for j in range(m):
            A_pad[i][j] = complex(A[i][j], 0)

    # 翻转卷积核 K (180度翻转)，并放入同等大小的矩阵中，其余补 0
    K_pad = [[complex(0, 0)] * C for _ in range(R)]
    for i in range(p):
        for j in range(q):
            K_pad[i][j] = complex(K[p - 1 - i][q - 1 - j], 0)

    # 步骤 1：分别进行 2D FFT 转换到频率域
    fft2d(A_pad, False)
    fft2d(K_pad, False)

    # 步骤 2：频率域下，矩阵元素逐个对应相乘
    for i in range(R):
        for j in range(C):
            A_pad[i][j] *= K_pad[i][j]

    # 步骤 3：进行 2D IFFT (逆变换) 转换回空间域
    fft2d(A_pad, True)

    # 计算输出矩阵的偏移量
    cx = p // 2
    cy = q // 2
    
    # 输出结果并四舍五入获取实数部分
    for i in range(n):
        row_out = []
        for j in range(m):
            # 推导出的目标坐标映射
            x = i + p - 1 - cx
            y = j + q - 1 - cy
            # 提取实部，并四舍五入解决浮点数精度误差
            val = round(A_pad[x][y].real)
            row_out.append(str(val))
        print(" ".join(row_out))

if __name__ == '__main__':
    solve()