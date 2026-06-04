import sys
from lp_solver import solve_linear_program

def main():
    # 快速读取
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    d = int(input_data[1])
    
    points = []
    idx = 2
    for _ in range(n):
        pt = [float(x) for x in input_data[idx : idx + d]]
        points.append(pt)
        idx += d
        
    num_vars = 2 * n + 1
    
    # 1. 预先构造所有点通用的“上下界约束” (共 2n 条)
    # -t <= u_j - v_j <= t  ==>  u_j - v_j - t <= 0 且 -u_j + v_j - t <= 0
    base_constraints = []
    base_bounds = []
    for j in range(n):
        c1 = [0.0] * num_vars
        c1[2 * j]     =  1.0
        c1[2 * j + 1] = -1.0
        c1[-1]        = -1.0
        base_constraints.append(c1)
        base_bounds.append(0.0)
        
        c2 = [0.0] * num_vars
        c2[2 * j]     = -1.0
        c2[2 * j + 1] =  1.0
        c2[-1]        = -1.0
        base_constraints.append(c2)
        base_bounds.append(0.0)

    # 2. 预先构造坐标匹配约束的左半部分系数 (共 2d 条)
    coord_constraints_left = []
    for k in range(d):
        eq1 = [0.0] * num_vars
        eq2 = [0.0] * num_vars
        for j in range(n):
            val = points[j][k]
            eq1[2 * j]     =  val
            eq1[2 * j + 1] = -val
            eq2[2 * j]     = -val
            eq2[2 * j + 1] =  val
        coord_constraints_left.append((eq1, eq2))

    # 3. 目标函数固定：最大化 -t
    objective = [0.0] * num_vars
    objective[-1] = -1.0
    
    # 开始遍历每个点求解
    for i in range(n):
        # 动态拼接入当前点 A_i 的具体约束
        constraints = list(base_constraints)  # 浅拷贝基准约束
        bounds = list(base_bounds)
        
        for k in range(d):
            eq1, eq2 = coord_constraints_left[k]
            constraints.append(eq1)
            bounds.append(points[i][k])
            
            constraints.append(eq2)
            bounds.append(-points[i][k])
            
        # 直接调用矩阵接口，绕过类方法的封装开销
        ans = solve_linear_program(constraints, bounds, objective)
        
        importance = -ans
        print(f"{importance:.6f}")

if __name__ == '__main__':
    main()