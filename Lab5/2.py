import sys
import random

def power(base, exp, mod):
    res = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            res = (res * base) % mod
        base = (base * base) % mod
        exp //= 2
    return res

def miller_rabin(n, k=5):
    """
    Miller-Rabin 算法：高效判断 n 是否为素数
    k 为测试轮数，轮数越多越准，对于 2^64 范围，取 5 轮或固定几个底数已经足够精确
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # 将 n - 1 写成 d * 2^s 的形式
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1

    # 进行 k 轮随机测试
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = power(a, d, n)
        if x == 1 or x == n - 1:
            continue
        
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def solve():
    # 快速读入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    
    # 从 n 开始往回找，找到第一个素数直接输出并结束
    curr = n
    while curr >= 2:
        if miller_rabin(curr):
            print(curr)
            return
        curr -= 1

if __name__ == '__main__':
    solve()