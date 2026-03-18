"""
给定两个字符串 a 和 b,寻找重复叠加字符串 a 的最小次数,使得字符串 b 成为叠加后的字符串 a 的子串,如果不存在则返回 -1。
注意:字符串 "abc" 重复叠加 0 次是 "",重复叠加 1 次是 "abc",重复叠加 2 次是 "abcabc"。

示例 1:
输入:a = "abcd", b = "cdabcdab"
输出:3
解释:a 重复叠加三遍后为 "abcdabcdabcd", 此时 b 是其子串。

示例 2:
输入:a = "a", b = "aa"
输出:2

示例 3:
输入:a = "a", b = "a"
输出:1

示例 4:
输入:a = "abc", b = "wxyz"
输出:-1
"""


def repeatedStringMatch(a: str, b: str) -> int:
    """
    思路：
    1. 如果 b 是 a 重复后的子串，则 b 最多跨越 a 的两个边界
    2. 因此重复次数范围是 [ceil(len(b)/len(a)), ceil(len(b)/len(a)) + 2]
    3. 如果 b 中存在任何不在 a 中的字符，直接返回 -1
    4. 使用向上取整计算最小重复次数

    时间复杂度: O(len(a) + len(b)) 最坏情况提前返回
    空间复杂度: O(len(a) + len(b)) 用于字符集
    """
    if not b:
        return 0

    # 快速排除：如果 b 中有字符不在 a 中，直接返回 -1
    if set(b) - set(a):
        return -1

    a_len, b_len = len(a), len(b)
    min_rep = (b_len + a_len - 1) // a_len  # 向上取整

    for rep in range(min_rep, min_rep + 3):
        if b in a * rep:
            return rep
    return -1


def repeatedStringMatch_kmp(a: str, b: str) -> int:
    """
    KMP 版本：使用 KMP 算法进行子串查找

    时间复杂度: O(len(a) * max_rep + len(b))
    空间复杂度: O(len(b)) 用于 KMP 的 next 数组
    """
    if not b:
        return 0

    # 快速排除
    if set(b) - set(a):
        return -1

    a_len, b_len = len(a), len(b)
    min_rep = (b_len + a_len - 1) // a_len

    # 构建 KMP 的 next 数组
    def build_next(pattern: str) -> list:
        n = len(pattern)
        next_arr = [0] * n
        j = 0
        for i in range(1, n):
            while j > 0 and pattern[i] != pattern[j]:
                j = next_arr[j - 1]
            if pattern[i] == pattern[j]:
                j += 1
                next_arr[i] = j
        return next_arr

    # KMP 匹配
    def kmp_search(text: str, pattern: str, next_arr: list) -> bool:
        j = 0
        for char in text:
            while j > 0 and char != pattern[j]:
                j = next_arr[j - 1]
            if char == pattern[j]:
                j += 1
                if j == len(pattern):
                    return True
        return False

    next_arr = build_next(b)

    for rep in range(min_rep, min_rep + 3):
        text = a * rep
        if kmp_search(text, b, next_arr):
            return rep
    return -1

# Rabin-Karp 算法
def repeatedStringMatch_rabin_karp(a: str, b: str) -> int:
    """
    滚动哈希（Rabin-Karp）版本：
    1. 使用滚动哈希在无限循环的 a 中查找 b 的起始位置
    2. 通过取模运算 i % n 模拟 a 的无限重复，避免实际构造长字符串
    3. 找到匹配位置后，根据 b 的起始位置和长度计算最小重复次数

    核心思想：
    - 不需要实际重复 a，而是在逻辑上处理循环
    - 哈希查找范围是 n + m - 1（b 可能从 a 的任意位置开始）
    - 重复次数 = (m + index - n - 1) // n + 2

    时间复杂度: O(len(a) + len(b))
    空间复杂度: O(1)
    """
    from random import randrange

    n, m = len(a), len(b)

    if m == 0:
        return 0

    # 快速排除：如果 b 中有字符不在 a 中，直接返回 -1
    if set(b) - set(a):
        return -1

    # 使用双哈希降低碰撞概率
    k1 = 10 ** 9 + 7
    k2 = 1337
    mod1 = randrange(k1) + k1  # 大质数作为模数
    mod2 = randrange(k2) + k2  # 基数

    # 计算 b 的哈希值
    hash_b = 0
    for c in b:
        hash_b = (hash_b * mod2 + ord(c)) % mod1

    # 计算 a 的前 m-1 个字符的哈希值（循环取）
    hash_a = 0
    for i in range(m - 1):
        hash_a = (hash_a * mod2 + ord(a[i % n])) % mod1

    # 用于移除最高位字符的系数：mod2^(m-1) % mod1
    extra = pow(mod2, m - 1, mod1)

    # 在 a 的循环扩展中滑动窗口查找 b
    # 查找范围：n + m - 1（b 可能从 a 的任意位置开始，最多延伸到第2个或第3个a）
    for i in range(m - 1, n + m - 1):
        # 加入新字符，窗口右移
        hash_a = (hash_a * mod2 + ord(a[i % n])) % mod1

        # 检查哈希是否匹配
        if hash_a == hash_b:
            # 找到匹配位置，计算重复次数
            index = i - m + 1  # b 在循环 a 中的起始位置

            # 如果 b 完全在第一个 a 内
            if n - index >= m:
                return 1

            # 计算重复次数：
            # 第1个a提供 n-index 个字符，还需 m-(n-index) 个字符
            # 需要额外的 ceil((m + index - n) / n) 个a
            # 总次数 = 1 + ceil((m + index - n) / n) = (m + index - n - 1) // n + 2
            return (m + index - n - 1) // n + 2

        # 移除窗口最左边的字符，准备下一次滑动
        # 减去最高位字符的贡献：extra * ord(a[(i - m + 1) % n])
        hash_a = (hash_a - extra * ord(a[(i - m + 1) % n])) % mod1
        hash_a = (hash_a + mod1) % mod1  # 确保非负

    return -1


if __name__ == "__main__":
    # 测试用例
    test_cases = [
        ("abcd", "cdabcdab", 3),
        ("a", "aa", 2),
        ("a", "a", 1),
        ("abc", "wxyz", -1),
        ("abc", "", 0),
        ("abc", "cabcabca", 4),
        ("abcd", "dabcdab", 3),
        ("abc", "abcabcabc", 3),
        ("abc", "ab", 1),
        ("abc", "bc", 1),
        ("abc", "ca", 2),
    ]

    print("\n" + "=" * 50)
    print("测试 repeatedStringMatch:")
    print("=" * 50)
    for a, b, expected in test_cases:
        result = repeatedStringMatch(a, b)
        status = "✓" if result == expected else "✗"
        print(f"  {status} a='{a}', b='{b}': {result} (期望 {expected})")

    print("\n" + "=" * 50)
    print("测试 repeatedStringMatch_kmp (KMP 版本):")
    print("=" * 50)
    for a, b, expected in test_cases:
        result = repeatedStringMatch_kmp(a, b)
        status = "✓" if result == expected else "✗"
        print(f"  {status} a='{a}', b='{b}': {result} (期望 {expected})")

    print("\n" + "=" * 50)
    print("测试 repeatedStringMatch_rabin_karp (滚动哈希版本):")
    print("=" * 50)
    for a, b, expected in test_cases:
        result = repeatedStringMatch_rabin_karp(a, b)
        status = "✓" if result == expected else "✗"
        print(f"  {status} a='{a}', b='{b}': {result} (期望 {expected})")
