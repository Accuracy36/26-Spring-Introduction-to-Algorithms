import sys

def solve():
    # 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]
    
    MOD = 10**9 + 7
    
    # 1. 离散化 (Coordinate Compression)
    # 将输入数值映射到 1 到 K 的排名，使得树状数组的空间复杂度可控
    sorted_unique_a = sorted(list(set(a)))
    rank = {val: i + 1 for i, val in enumerate(sorted_unique_a)}
    max_rank = len(sorted_unique_a)
    
    # 2. 初始化树状数组 (Binary Indexed Tree)
    # tree_len 维护区间内的最大 LIS 长度
    # tree_cnt 维护区间内达到该最大长度的 LIS 数量和
    tree_len = [0] * (max_rank + 1)
    tree_cnt = [0] * (max_rank + 1)
    
    def query(idx):
        res_len = 0
        res_cnt = 0
        while idx > 0:
            if tree_len[idx] > res_len:
                res_len = tree_len[idx]
                res_cnt = tree_cnt[idx]
            elif tree_len[idx] == res_len and res_len > 0:
                res_cnt = (res_cnt + tree_cnt[idx]) % MOD
            idx -= idx & (-idx)
        return res_len, res_cnt
        
    def update(idx, l, c):
        while idx <= max_rank:
            if l > tree_len[idx]:
                tree_len[idx] = l
                tree_cnt[idx] = c
            elif l == tree_len[idx]:
                tree_cnt[idx] = (tree_cnt[idx] + c) % MOD
            idx += idx & (-idx)
            
    ans_f = []
    ans_g = []
    
    # 3. 核心 DP 转移
    for num in a:
        r = rank[num]
        
        # 查询前缀中，比当前数小 (即排名 <= r - 1) 的最大长度和方案数
        max_l, ways = query(r - 1)
        
        # 状态转移
        f_i = max_l + 1
        g_i = ways if max_l > 0 else 1
        
        ans_f.append(f_i)
        ans_g.append(g_i)
        
        # 将当前结果更新到树状数组
        update(r, f_i, g_i)
        
    # 按要求输出两行结果
    print(" ".join(map(str, ans_f)))
    print(" ".join(map(str, ans_g)))

if __name__ == '__main__':
    solve()