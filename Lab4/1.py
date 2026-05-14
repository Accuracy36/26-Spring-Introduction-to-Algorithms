import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
    
    n, m, s, t = map(int, input_data[:4])
    adj = [[] for _ in range(n + 1)]
    rev_adj = [[] for _ in range(n + 1)]
    
    idx = 4
    for _ in range(m):
        u, v, w = map(int, input_data[idx:idx+3])
        adj[u].append((v, w))
        rev_adj[v].append(u)
        idx += 3
        
    # 可达性预处理
    reach_s = [False] * (n + 1)
    q_s = deque([s]); reach_s[s] = True
    while q_s:
        u = q_s.popleft()
        for v, w in adj[u]:
            if not reach_s[v]: reach_s[v] = True; q_s.append(v)
                
    reach_t = [False] * (n + 1)
    q_t = deque([t]); reach_t[t] = True
    while q_t:
        u = q_t.popleft()
        for v in rev_adj[u]:
            if not reach_t[v]: reach_t[v] = True; q_t.append(v)
                
    valid = [i for i in range(1, n + 1) if reach_s[i] and reach_t[i]]
    is_valid = [False] * (n + 1)
    for i in valid: is_valid[i] = True
    valid_count = len(valid)

    # SPFA
    dist = [float('inf')] * (n + 1)
    parent = [-1] * (n + 1)
    cnt = [0] * (n + 1)
    in_q = [False] * (n + 1)
    dist[s] = 0; q = deque([s]); in_q[s] = True
    
    cycle_node = -1
    while q:
        u = q.popleft(); in_q[u] = False
        for v, w in adj[u]:
            if not is_valid[v]: continue
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                cnt[v] = cnt[u] + 1
                if cnt[v] >= valid_count:
                    cycle_node = v; break
                if not in_q[v]:
                    in_q[v] = True
                    if q and dist[v] < dist[q[0]]: q.appendleft(v)
                    else: q.append(v)
        if cycle_node != -1: break
            
    if cycle_node != -1:
        # 提取负环
        curr = cycle_node
        for _ in range(valid_count): curr = parent[curr]
        start = curr; cycle = [start]; curr = parent[start]
        while curr != start:
            cycle.append(curr); curr = parent[curr]
        cycle.reverse()
        print("-1\n{}\n{}".format(len(cycle), " ".join(map(str, cycle))))
    else:
        # 输出最短路
        path = []; curr = t
        while curr != -1:
            path.append(curr); curr = parent[curr]
        path.reverse()
        print("{}\n{}\n{}".format(dist[t], len(path), " ".join(map(str, path))))

if __name__ == '__main__':
    solve()
