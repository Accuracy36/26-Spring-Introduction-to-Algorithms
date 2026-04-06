import random
import time

def run_simulation(n, data_type="sequential"):
    """
    模拟将 n 个元素放入 n 个桶中，对比单哈希与多重选择哈希的最大过载。
    """
    # 1. 构造不同的测试数据集合
    if data_type == "sequential":
        data = list(range(n))                     # 连续整数
    elif data_type == "random":
        data = [random.randint(0, 10**9) for _ in range(n)] # 离散随机数
    elif data_type == "even_numbers":
        data = [x * 2 for x in range(n)]          # 规律数列（全是偶数）
        
    # 2. 初始化哈希表（这里只记录每个桶里的元素个数 load）
    table_single = [0] * n
    table_two = [0] * n
    
    # 3. 准备两个独立的“盐值”，用来模拟两个不同的哈希函数
    seed1 = str(random.randint(1, 10**5))
    seed2 = str(random.randint(1, 10**5))
    
    for x in data:
        # 使用 Python 内置的 hash 结合盐值，保证两个哈希函数独立且随机
        str_x = str(x)
        h1 = hash(str_x + seed1) % n
        h2 = hash(str_x + seed2) % n
        
        # ================= 策略 A：简单单哈希 =================
        table_single[h1] += 1
        
        # ================= 策略 B：多重选择哈希 =================
        if table_two[h1] <= table_two[h2]:
            table_two[h1] += 1
        else:
            table_two[h2] += 1
            
    # 返回两种策略的最大过载（最大链表长度）
    return max(table_single), max(table_two)


def main():
    print("=" * 70)
    print(f"{'数据规模 (n)':<12} | {'数据分布特性':<15} | {'单哈希最大过载':<15} | {'多重选择最大过载'}")
    print("-" * 70)

    # 设计多组对照实验
    test_cases = [
        (10_000, "sequential"),
        (100_000, "sequential"),
        (1_000_000, "sequential"),
        (100_000, "random"),
        (100_000, "even_numbers")
    ]

    for n, dtype in test_cases:
        max_single, max_two = run_simulation(n, dtype)
        print(f"{n:<12} | {dtype:<18} | {max_single:<20} | {max_two}")
        
    print("=" * 70)

if __name__ == '__main__':
    main()