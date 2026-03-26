import sys

# 设置 Python 处理超大字符串转整数的上限（防止报错）
sys.set_int_max_str_digits(2000) 

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 读入
a = int(sys.stdin.readline())
b = int(sys.stdin.readline())
print(gcd(a, b))