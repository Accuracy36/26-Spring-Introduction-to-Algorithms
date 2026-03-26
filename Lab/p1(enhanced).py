# 比较两个大数列表（忽略前导0）
def is_greater_equal(a_list, b_list):
    if len(a_list) != len(b_list):
        return len(a_list) > len(b_list)
    return a_list >= b_list # Python 列表按位比较逻辑与数字一致

# 大数减法：a_list - b_list (假设 a >= b)
def big_sub(a_list, b_list):
    res = []
    # 补齐长度
    b_padded = [0] * (len(a_list) - len(b_list)) + b_list
    borrow = 0
    for i in range(len(a_list) - 1, -1, -1):
        diff = a_list[i] - b_padded[i] - borrow
        if diff < 0:
            diff += 10
            borrow = 1
        else:
            borrow = 0
        res.append(diff)
    # 反转并去除前导 0
    while len(res) > 1 and res[-1] == 0:
        res.pop()
    return res[::-1]
def big_mod(a_list, b_list):
    if not is_greater_equal(a_list, b_list):
        return a_list
    
    rem = [] # 存放当前的“余数”
    for digit in a_list:
        # 1. 落下下一位
        if rem == [0]: rem = [digit]
        else: rem.append(digit)
        
        # 2. 去掉落下后产生的前导0 (例如 05 变成 5)
        while len(rem) > 1 and rem[0] == 0:
            rem.pop(0)
            
        # 3. 试商：因为是逐位落下，rem 最多比 b_list 多一位
        # 这里的 while 循环最多跑 9 次，相当于求商
        while is_greater_equal(rem, b_list):
            rem = big_sub(rem, b_list)
            
    return rem
import sys

def solve():
    # 读取输入并转为数字列表
    s1 = sys.stdin.readline().strip()
    s2 = sys.stdin.readline().strip()
    if not s1 or not s2: return
    
    a = [int(d) for d in s1]
    b = [int(d) for d in s2]

    # 辗转相除法
    while b != [0]:
        a, b = b, big_mod(a, b)
    
    # 输出结果
    print("".join(map(str, a)))

if __name__ == "__main__":
    solve()
