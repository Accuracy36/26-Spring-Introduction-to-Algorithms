from typing import Any


import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    if n < 2:
        return
        
    pts = []
    it = iter(input_data[1:])
    for x, y in zip(it, it):
        pts.append((float(x), float(y)))
        
    Px = sorted(pts, key=lambda p: p[0])
    Py = sorted(pts, key=lambda p: p[1])

    def closest_pair(Px, Py):
        n_pts = len(Px)
        if n_pts <= 3:
            min_d2 = float('inf')
            for i in range(n_pts):
                for j in range(i + 1, n_pts):
                    dx = Px[i][0] - Px[j][0]
                    dy = Px[i][1] - Px[j][1]
                    d2 = dx*dx + dy*dy
                    if d2 < min_d2:
                        min_d2 = d2
            return min_d2

        mid = n_pts // 2
        mid_x = Px[mid][0]

        Px_left = Px[:mid]
        Px_right = Px[mid:]

        left_set = set(Px_left)
        Py_left = []
        Py_right = []
        for p in Py:
            if p in left_set:
                Py_left.append(p)
            else:
                Py_right.append(p)
        d1 = closest_pair(Px_left, Py_left)
        d2 = closest_pair(Px_right, Py_right)
        min_d2 = d1 if d1 < d2 else d2

        strip = []
        for p in Py:
            if (p[0] - mid_x)**2 < min_d2:
                strip.append(p)

        strip_len = len(strip)
        for i in range(strip_len):
            for j in range(i + 1, strip_len):
                dy = strip[j][1] - strip[i][1]
                if dy * dy >= min_d2:
                    break 
                dx = strip[i][0] - strip[j][0]
                d2 = dx*dx + dy*dy
                if d2 < min_d2:
                    min_d2 = d2

        return min_d2

    ans_d2 = closest_pair(Px, Py)
    sys.stdout.write(f"{ans_d2**0.5:.6f}\n")

if __name__ == '__main__':
    sys.setrecursionlimit(2000000)
    solve()