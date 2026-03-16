"""
实现 strStr() 函数。
给定一个 haystack 字符串和一个 needle 字符串，在 haystack 字符串中找出 needle 字符串出现的第一个位置 (从0开始)。如果不存在，则返回  -1。
示例 1: 输入: haystack = "hello", needle = "ll" 输出: 2
示例 2: 输入: haystack = "aaaaa", needle = "bba" 输出: -1
说明: 当 needle 是空字符串时，我们应当返回什么值呢？这是一个在面试中很好的问题。 对于本题而言，当 needle 是空字符串时我们应当返回 0 。这与C语言的 strstr() 以及 Java的 indexOf() 定义相符。
""" 

def strStr(haystack: str, needle: str) -> int: 
    """
    暴力匹配
    """
    if not needle: 
        return 0 
    first = needle[0] 
    needle_len = len(needle)
    haystack_len = len(haystack)
    for i in range(haystack_len - needle_len + 1): 
        if needle == haystack[i:i+needle_len]: 
            return i 
    return -1 

def strStr_find(haystack: str, needle: str) -> int: 
    """
    使用内置的find方法,经过高度优化的C语言实现
    """
    return haystack.find(needle)

# KMP算法的核心思想: 当匹配失败时,不是简单的将模式串向后移动一位重新开始，而是利用已经匹配的部分信息，跳过一些不会匹配的位置
# 当在模式串中的第j个字符不匹配时,前面已经匹配的j-1个字符是已知的,我们可以根据这个信息来决定模式串应该向右移动多少位 
# 时间复杂度:O(m+n) 在匹配过程中， i 指针（文本串）只会向前移动，不会回退。 j 指针（模式串）可能会回退，但每次回退都意味着之前有字符匹配成功。 空间复杂度:O(m) 部分匹配表
def strStr_KMP(haystack: str, needle: str) -> int: 
    if not needle: 
        return 0 
    
    # 创建部分匹配表 
    def build_prefix_table(pattern): 
        n = len(pattern) 
        prefix = [0] * n # 部分匹配表
        length = 0 # 当前最长前缀后缀的长度
        i = 1 # 从第二个字符开始

        while i < n: 
            if pattern[i] == pattern[length]: 
                # 字符匹配,长度加1
                length += 1 
                prefix[i] = length 
                i += 1 
            else: 
                if length != 0: 
                    # 不匹配,但之前有匹配的部分
                    # 回退到前一个位置的部分匹配值
                    length = prefix[length-1] 
                else: 
                    # 完全不匹配
                    prefix[i] = 0 
                    i += 1 
        return prefix 

    prefix_table = build_prefix_table(needle) 
    i = 0 # haystack的索引 
    j = 0 # needle的索引 
    n, m = len(haystack), len(needle) 

    while i < n: 
        if haystack[i] == needle[j]: 
            # 字符匹配,两个指针都向前移动
            i += 1 
            j += 1

            if j == m:
                # 找到完整匹配 
                return i - j 
        else: 
            if j != 0: 
                # 不匹配,但之前有匹配的部分
                # 利用部分匹配表跳过一些位置
                j = prefix_table[j-1] 
            else: 
                # 完全不匹配,haystack指针向前移动
                i += 1

    return -1 


if __name__ == "__main__": 
    haystack = "sadbutsad" 
    needle = "sad" 
    print(strStr(haystack, needle))
    print(strStr_KMP(haystack, needle))
