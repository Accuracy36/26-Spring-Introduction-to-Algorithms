import sys

def solve():
    # 使用 sys.stdin.read 快速读取所有的输入
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    m = int(input_data[1])
    
    # 构建反向图
    rev_adj = [[] for _ in range(n + 1)]
    
    idx = 2
    for _ in range(m):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        # 原图是 u -> v，反向图是 v -> u
        rev_adj[v].append(u)
        idx += 2
        
    min_reach = [0] * (n + 1)
    max_reach = [0] * (n + 1)
    
    # 1. 求每个节点能到达的最小标号节点
    visited_min = [False] * (n + 1)
    # 从 1 到 n 枚举起点，保证第一次访问时就是最小可能到达的节点
    for i in range(1, n + 1):
        if not visited_min[i]:
            stack = [i]
            visited_min[i] = True
            min_reach[i] = i
            while stack:
                curr = stack.pop()
                for neighbor in rev_adj[curr]:
                    if not visited_min[neighbor]:
                        visited_min[neighbor] = True
                        min_reach[neighbor] = i
                        stack.append(neighbor)
                        
    # 2. 求每个节点能到达的最大标号节点
    visited_max = [False] * (n + 1)
    # 从 n 到 1 枚举起点，保证第一次访问时就是最大可能到达的节点
    for i in range(n, 0, -1):
        if not visited_max[i]:
            stack = [i]
            visited_max[i] = True
            max_reach[i] = i
            while stack:
                curr = stack.pop()
                for neighbor in rev_adj[curr]:
                    if not visited_max[neighbor]:
                        visited_max[neighbor] = True
                        max_reach[neighbor] = i
                        stack.append(neighbor)
                        
    # 统一输出结果
    out = []
    for i in range(1, n + 1):
        out.append(f"{min_reach[i]} {max_reach[i]}")
        
    # 一次性快速输出
    sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()