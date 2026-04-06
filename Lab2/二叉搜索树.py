import sys

class TreeNode:
    __slots__ = ['val', 'left', 'right']
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def solve():
    # 快速读入所有数据
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    root = None
    
    def insert(val):
        nonlocal root
        if not root:
            root = TreeNode(val)
            return
        curr = root
        while True:
            if val < curr.val:
                if not curr.left:
                    curr.left = TreeNode(val)
                    break
                curr = curr.left
            elif val > curr.val:
                if not curr.right:
                    curr.right = TreeNode(val)
                    break
                curr = curr.right
            else:
                break
                
    def delete(val):
        nonlocal root
        parent = None
        curr = root
        
        while curr and curr.val != val:
            parent = curr
            if val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
                
        if not curr:
            return
            
        if curr.left and curr.right:
            successor_parent = curr
            successor = curr.right
            while successor.left:
                successor_parent = successor
                successor = successor.left
            
            # 替换当前节点的值
            curr.val = successor.val
            # 接下来转为删除该后继节点
            curr = successor
            parent = successor_parent

        # 此时 curr 最多只有一个子节点
        child = curr.left if curr.left else curr.right
        
        if not parent:
            root = child
        elif parent.left is curr:
            parent.left = child
        else:
            parent.right = child

    def search(val):
        curr = root
        while curr:
            if curr.val == val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    idx = 1
    out = []
    
    for _ in range(n):
        op = int(input_data[idx])
        if op == 1:
            x = int(input_data[idx+1])
            insert(x)
            idx += 2
        elif op == 2:
            x = int(input_data[idx+1])
            delete(x)
            idx += 2
        elif op == 3:
            x = int(input_data[idx+1])
            if search(x):
                out.append("Yes")
            else:
                out.append("No")
            idx += 2
        elif op == 4:
            x = int(input_data[idx+1])
            y = int(input_data[idx+2])
            # 修改操作等效于删除原节点后，插入新节点
            delete(x)
            insert(y)
            idx += 3
    if out:
        sys.stdout.write('\n'.join(out) + '\n')

if __name__ == '__main__':
    solve()