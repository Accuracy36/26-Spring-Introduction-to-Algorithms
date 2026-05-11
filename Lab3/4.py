import sys
from collections import deque

def solve():
    # 快速读取所有输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    
    # c 数组为 1-indexed
    c = [0] * (n + 1)
    for i in range(1, n + 1):
        c[i] = int(input_data[i])
        
    # 构建无向图邻接表
    adj = [[] for _ in range(n + 1)]
    idx = n + 1
    for _ in range(n - 1):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        adj[v].append(u)
        idx += 2
        
    # BFS 建立父子关系及拓扑序
    parent = [0] * (n + 1)
    children = [[] for _ in range(n + 1)]
    order = []
    
    q = deque([1])
    visited = [False] * (n + 1)
    visited[1] = True
    
    while q:
        curr = q.popleft()
        order.append(curr)
        for nxt in adj[curr]:
            if not visited[nxt]:
                visited[nxt] = True
                parent[nxt] = curr
                children[curr].append(nxt)
                q.append(nxt)
                
    # Phase 1: 自底向上计算 f[u]
    f = c.copy()
    for u in reversed(order):
        if len(children[u]) >= 2:
            min1 = float('inf')
            min2 = float('inf')
            # 找到 f 值最小的两个子节点
            for child in children[u]:
                val = f[child]
                if val < min1:
                    min2 = min1
                    min1 = val
                elif val < min2:
                    min2 = val
            # 状态转移
            if min1 + min2 < f[u]:
                f[u] = min1 + min2
                
    # Phase 2 & Phase 3: 自顶向下计算 ans[u]
    ans = [0] * (n + 1)
    for u in order:
        if len(children[u]) >= 2:
            min1_val = float('inf')
            min2_val = float('inf')
            min1_node = -1
            
            # 找到 f 值最小和次小的子节点
            for child in children[u]:
                val = f[child]
                if val < min1_val:
                    min2_val = min1_val
                    min1_val = val
                    min1_node = child
                elif val < min2_val:
                    min2_val = val
                    
            # 遍历并赋值子节点的 ans 状态
            for child in children[u]:
                if child == min1_node:
                    g = min2_val
                else:
                    g = min1_val
                # ans[子节点] = ans[父节点] + 兄弟合并的最小开销
                ans[child] = ans[u] + g
                
    # 统一格式化输出，输出询问 [1, n] 的答案
    print(" ".join(map(str, ans[1:])))

if __name__ == '__main__':
    solve()
