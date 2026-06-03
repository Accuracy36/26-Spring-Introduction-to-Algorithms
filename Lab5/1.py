import sys

def solve():
    # 读取所有输入，去除首尾空白字符
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    s = input_data[0]
    
    # 1. 获取翻转字符串
    s_rev = s[::-1]
    
    # 2. 构造拼接字符串 (翻转串在前，原串在后)
    # 中间用 '#' 分隔，防止前后缀匹配时跨越原串和翻转串的边界
    combined = s_rev + '#' + s
    n = len(combined)
    
    # 3. 计算 KMP 的 pi 数组 (最长公共前后缀)
    pi = [0] * n
    for i in range(1, n):
        j = pi[i - 1]
        while j > 0 and combined[i] != combined[j]:
            j = pi[j - 1]
        if combined[i] == combined[j]:
            j += 1
        pi[i] = j
        
    # 4. 获取最长回文后缀的长度
    max_palindrome_suffix_len = pi[-1]
    
    # 5. 截取需要补充的字符并输出
    # 翻转串中，前 max_palindrome_suffix_len 个字符正好对应原串的最长回文后缀
    # 剩下的部分就是我们需要在原串末尾补齐的字符
    to_add = s_rev[max_palindrome_suffix_len:]
    
    sys.stdout.write(s + to_add + '\n')

if __name__ == '__main__':
    solve()
