import sys

def solve():
    # 使用 sys.stdin.read 快速读取全部输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    d = int(input_data[1])
    
    # 构建图 (邻接表)
    adj = [[] for _ in range(n + 1)]
    idx = 2
    for _ in range(n - 1):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        w = int(input_data[idx+2])
        adj[u].append((v, w))
        adj[v].append((u, w))
        idx += 3
        
    # BFS 寻找父节点并确定拓扑序 (自底向上的顺序)
    order = []
    parent = [0] * (n + 1)
    weight_to_parent = [0] * (n + 1)
    visited = [False] * (n + 1)
    
    queue = [1]
    visited[1] = True
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        order.append(u)
        for v, w in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                weight_to_parent[v] = w
                queue.append(v)
                
    # 翻转 BFS 顺序得到标准的自底向上的处理顺序 (Post-order)
    order.reverse()
    
    INF = 10**16
    f = [0] * (n + 1)
    g = [INF] * (n + 1)
    S = []
    
    # 树形 DP 自底向上转移
    for u in order:
        f_u = 0          # 默认 u 自身距离为 0 (待覆盖)
        g_u = INF
        
        # 汇总所有子节点的信息
        for v, w in adj[u]:
            if v != parent[u]:
                if f[v] + w > f_u:
                    f_u = f[v] + w
                if g[v] + w < g_u:
                    g_u = g[v] + w
                    
        if f_u + g_u <= d:
            f_u = -INF   # 已经覆盖掉了，不再具有未覆盖的距离威胁
            
        if u != 1:  # 如果不是根节点
            w_p = weight_to_parent[u]
            if f_u + w_p > d:
                # 无法推迟到父节点，必须在当前节点建立覆盖点
                S.append(u)
                g_u = 0
                f_u = -INF
        else:       # 如果是根节点
            if f_u >= 0:
                # 仍然有未能覆盖的节点，必须在根建立覆盖点
                S.append(u)
                g_u = 0
                f_u = -INF
                
        # 记录当前节点状态，供其父节点使用
        f[u] = f_u
        g[u] = g_u
        
    # 输出结果
    print(len(S))
    print(" ".join(map(str, S)))

if __name__ == '__main__':
    solve()