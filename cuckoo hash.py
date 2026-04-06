import sys
import random
import math

class CuckooHashTable:
    def __init__(self, q, n):
        self.q = q
        self.max_kicks = int(10 * math.log2(n)) if n > 1 else 20
        self.table1 = [None] * q
        self.table2 = [None] * q
        self._gen_coeffs()

    def _gen_coeffs(self, k=10):
        self.c1 = [random.randint(0, self.q - 1) for _ in range(k + 1)]
        self.c2 = [random.randint(0, self.q - 1) for _ in range(k + 1)]

    def _hash(self, x, coeffs):
        q = self.q
        val = x % q
        res = 0
        for a in reversed(coeffs):
            res = (res * val + a) % q
        return res

    def insert(self, x):
        curr = x
        for _ in range(self.max_kicks):
            idx1 = self._hash(curr, self.c1)
            if self.table1[idx1] is None:
                self.table1[idx1] = curr
                return
            curr, self.table1[idx1] = self.table1[idx1], curr
            
            idx2 = self._hash(curr, self.c2)
            if self.table2[idx2] is None:
                self.table2[idx2] = curr
                return
            curr, self.table2[idx2] = self.table2[idx2], curr
        
        # 3. 达到踢出上限，触发 Rehash
        self._rehash_all(curr)

    def _rehash_all(self, extra_x):
        # 收集表内所有元素
        elements = [x for x in self.table1 if x is not None]
        elements.extend([x for x in self.table2 if x is not None])
        elements.append(extra_x)
        while True:
            self._gen_coeffs()
            self.table1 = [None] * self.q
            self.table2 = [None] * self.q
            try:
                for x in elements:
                    self._safe_insert(x)
                break
            except RuntimeError: 
                continue

    def _safe_insert(self, x):
        curr = x
        for _ in range(self.max_kicks):
            idx1 = self._hash(curr, self.c1)
            if self.table1[idx1] is None:
                self.table1[idx1] = curr
                return
            curr, self.table1[idx1] = self.table1[idx1], curr
            idx2 = self._hash(curr, self.c2)
            if self.table2[idx2] is None:
                self.table2[idx2] = curr
                return
            curr, self.table2[idx2] = self.table2[idx2], curr
        raise RuntimeError("Rehash loop")

    def remove(self, x):
        idx1 = self._hash(x, self.c1)
        if self.table1[idx1] == x:
            self.table1[idx1] = None
            return
        idx2 = self._hash(x, self.c2)
        if self.table2[idx2] == x:
            self.table2[idx2] = None

    def query(self, x):
        return self.table1[self._hash(x, self.c1)] == x or \
               self.table2[self._hash(x, self.c2)] == x

def solve():
    input_iter = map(int, sys.stdin.read().split())
    try:
        n = next(input_iter)
    except StopIteration: return

    PRIME_Q = 2000003 
    ht = CuckooHashTable(PRIME_Q, n)
    
    results = []
    fast_append = results.append
    
    for _ in range(n):
        op = next(input_iter)
        x = next(input_iter)
        if op == 1:
            ht.insert(x)
        elif op == 2:
            ht.remove(x)
        else:
            fast_append("Yes" if ht.query(x) else "No")
    
    sys.stdout.write("\n".join(results) + "\n")

if __name__ == '__main__':
    solve()