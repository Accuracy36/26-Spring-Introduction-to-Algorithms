import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
    data = list(map(int, input_data))
    
    n, m = data[0], data[1]
    edges = [(data[2+i*3+2], data[2+i*3], data[2+i*3+1], i+1) for i in range(m)]
    
    idx = 2 + m * 3
    k = data[idx]; idx += 1
    
    queries = [[] for _ in range(n + 1)]
    for i in range(k):
        u, v = data[idx+i*2], data[idx+i*2+1]
        queries[u].append((v, i)); queries[v].append((u, i))

    def find(i, parent_arr):
        root = i
        while root != parent_arr[root]: root = parent_arr[root]
        curr = i
        while curr != root:
            nxt = parent_arr[curr]; parent_arr[curr] = root; curr = nxt
        return root

    # 1. Kruskal
    edges.sort(key=lambda x: x[0])
    parent_k = list(range(n + 1))
    mst_weight, mst_edges, tree, edges_found = 0, [], [[] for _ in range(n + 1)], 0
    
    for w, u, v, orig_idx in edges:
        ru, rv = find(u, parent_k), find(v, parent_k)
        if ru != rv:
            parent_k[ru] = rv; mst_weight += w
            mst_edges.append(orig_idx)
            tree[u].append(v); tree[v].append(u)
            edges_found += 1
            if edges_found == n - 1: break
                
    # 2. Tarjan (显式栈)
    visited = [False] * (n + 1); ans = [-1] * k
    parent_t = list(range(n + 1)); ancestor = list(range(n + 1))
    stack = [[1, 0, 0]]; visited[1] = True
    
    while stack:
        u, p, child_idx = stack[-1]
        if child_idx < len(tree[u]):
            v = tree[u][child_idx]
            stack[-1][2] += 1
            if v != p:
                visited[v] = True; stack.append([v, u, 0])
        else:
            for v, q_idx in queries[u]:
                if visited[v]: ans[q_idx] = ancestor[find(v, parent_t)]
            stack.pop()
            if stack:
                parent_u = stack[-1][0]
                root_u, root_p = find(u, parent_t), find(parent_u, parent_t)
                if root_u != root_p:
                    parent_t[root_u] = root_p; ancestor[root_p] = parent_u

    print(mst_weight)
    print(" ".join(map(str, mst_edges)))
    print("\n".join(map(str, ans)))

if __name__ == '__main__':
    solve()
