import sys
import random

class MultiChoiceHashTable:
    def __init__(self, q, k=10):
        self.q = q
        # 生成两组不同的多项式系数，对应两个独立的哈希函数 h1 和 h2
        self.coeffs1 = [random.randint(0, q - 1) for _ in range(k + 1)]
        self.coeffs2 = [random.randint(0, q - 1) for _ in range(k + 1)]
        self.table = [[] for _ in range(q)]

    def _get_hashes(self, x):
        q = self.q
        val = x % q
        
        # 计算第一个哈希值 h1
        res1 = 0
        for a in reversed(self.coeffs1):
            res1 = (res1 * val + a) % q
            
        # 计算第二个哈希值 h2
        res2 = 0
        for a in reversed(self.coeffs2):
            res2 = (res2 * val + a) % q
            
        return res1, res2

    def insert(self, x):
        idx1, idx2 = self._get_hashes(x)
        # 核心逻辑：哪边链表短，就插入哪边
        if len(self.table[idx1]) <= len(self.table[idx2]):
            self.table[idx1].append(x)
        else:
            self.table[idx2].append(x)

    def remove(self, x):
        idx1, idx2 = self._get_hashes(x)
        if x in self.table[idx1]:
            self.table[idx1].remove(x)
        else:
            self.table[idx2].remove(x)

    def query(self, x):
        idx1, idx2 = self._get_hashes(x)
        return x in self.table[idx1] or x in self.table[idx2]



def solve():
    input_iter = map(int, sys.stdin.read().split())
    
    try:
        n = next(input_iter)
    except StopIteration:
        return
    PRIME_Q = 1500007
    ht = MultiChoiceHashTable(PRIME_Q)
    
    results = []
    append_res = results.append
    for _ in range(n):
        op = next(input_iter)
        x = next(input_iter)
        
        if op == 1:
            ht.insert(x)
        elif op == 2:
            ht.remove(x)
        else:
            if ht.query(x):
                append_res("Yes")
            else:
                append_res("No")
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == '__main__':
    solve()