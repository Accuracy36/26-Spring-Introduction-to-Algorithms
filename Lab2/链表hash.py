import sys
import random

random.seed(42)

class ChainedHashTable:
    def __init__(self, q, k=10):
        self.q = q
        # 随机生成多项式系数 a_0, a_1, ..., a_k
        self.coeffs = [random.randint(0, q - 1) for _ in range(k + 1)]
        # 初始化哈希表，每个桶是一个列表（链表）
        self.table = [[] for _ in range(q)]

    def _hash(self, x):
        val = x % self.q
        res = 0
        # 从高次项向低次项迭代: res = (...((a_k * x + a_{k-1}) * x + a_{k-2}) ...)
        for i in range(len(self.coeffs) - 1, -1, -1):
            res = (res * val + self.coeffs[i]) % self.q
        return res

    def insert(self, x):
        idx = self._hash(x)
        self.table[idx].append(x)

    def remove(self, x):
        idx = self._hash(x)
        # 题目保证待删除元素一定存在
        self.table[idx].remove(x)

    def query(self, x):
        idx = self._hash(x)
        # 返回布尔值
        return x in self.table[idx]

def solve():
    # 使用快速 I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # 选取一个大于 n 的质数作为哈希表大小
    # 对于 10^6 的规模，选取 1000003 或更大的质数
    PRIME_Q = 1000003
    ht = ChainedHashTable(PRIME_Q)
    
    results = []
    ptr = 1
    for _ in range(n):
        op = int(input_data[ptr])
        x = int(input_data[ptr + 1])
        ptr += 2
        
        if op == 1:
            ht.insert(x)
        elif op == 2:
            ht.remove(x)
        elif op == 3:
            if ht.query(x):
                results.append("Yes")
            else:
                results.append("No")
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()