import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data: return
        
    iterator = map(int, input_data)
    try:
        n = next(iterator)
    except StopIteration:
        return
    h = list(iterator)
    
    ls, rs = [-1] * n, [-1] * n
    st = [] 
    
    # 1. 单调栈构建笛卡尔树 O(N)
    for i in range(n):
        last_popped = -1
        while st and h[st[-1]] > h[i]:
            last_popped = st.pop()
        if last_popped != -1: ls[i] = last_popped
        if st: rs[st[-1]] = i
        st.append(i)
        
    if not st: return
    root = st[0]
    
    # 2. 迭代获取拓扑遍历序，防止深层递归导致爆栈
    post_order = [0] * n
    idx = 0
    q = [root]
    while q:
        u = q.pop()
        post_order[idx] = u; idx += 1
        if ls[u] != -1: q.append(ls[u])
        if rs[u] != -1: q.append(rs[u])
        
    # 3. 自底向上累加子树规模并计算极值
    size = [1] * n
    max_area = 0
    for i in range(n - 1, -1, -1):
        u = post_order[i]
        if ls[u] != -1: size[u] += size[ls[u]]
        if rs[u] != -1: size[u] += size[rs[u]]
            
        area = size[u] * h[u]
        if area > max_area: max_area = area
            
    print(max_area)

if __name__ == '__main__':
    solve()
