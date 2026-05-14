import sys
import heapq

def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
        
    n, m, K, s, t = map(int, input_data[:5])
    
    adj = [[] for _ in range(n + 1)]
    idx = 5
    for _ in range(m):
        u, v, w, c = map(int, input_data[idx:idx+4])
        adj[u].append((v, w, c))
        adj[v].append((u, w, c))
        idx += 4
        
    # dist[u][k] 表示到达点 u 且用掉 k 次升级机会的极小用时
    dist = [[float('inf')] * (K + 1) for _ in range(n + 1)]
    dist[s][0] = 0
    
    # 优先队列：存入 (当前总用时 d, 所在节点 u, 已用升级次数 k)
    pq = [(0, s, 0)]
    
    while pq:
        d, u, k = heapq.heappop(pq)
        
        # 懒惰删除：过滤旧状态
        if d > dist[u][k]: continue
            
        # 第一次遇见终点必定是最优解
        if u == t:
            print(d)
            return
            
        for v, w, c in adj[u]:
            # 情况 1：不升级，同层转移
            if d + w < dist[v][k]:
                dist[v][k] = d + w
                heapq.heappush(pq, (d + w, v, k))
                
            # 情况 2：使用升级，向 k+1 层跃迁
            if k < K and d + c < dist[v][k + 1]:
                dist[v][k + 1] = d + c
                heapq.heappush(pq, (d + c, v, k + 1))

    print(min(dist[t]))

if __name__ == '__main__':
    solve()
