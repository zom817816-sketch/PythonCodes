""" 
给定一个非空的字符串 s ，检查是否可以通过由它的一个子串重复多次构成。
示例 1:
输入: s = "abab"
输出: true
解释: 可由子串 "ab" 重复两次构成。
示例 2:
输入: s = "aba"
输出: false
示例 3:
输入: s = "abcabcabcabc"
输出: true
解释: 可由子串 "abc" 重复四次构成。 (或子串 "abcabc" 重复两次构成。)
""" 

def repeatedSubstring(s: str) -> bool: 
    """
    遍历可能的子字符串，并进行字符串乘法与原字符串对比
    """
    n = len(s) 
    for i in range(1, n // 2 + 1): 
        if n % i != 0: 
            continue 
        sub_string = s[:i] 
        if sub_string * (n // i) == s: 
            return True 
    return False 

def repeatedSubstring_1(s: str) -> bool: 
    """
    利用重复字符串的周期性特征
    如果字符串 s 由重复子串组成，那么将 s 与自身拼接后，去掉首尾字符，原字符串 s 必然出现在这个新字符串中。
    时间复杂度 平均O(n) 最坏O(n^2)
    """
    return s in (s + s)[1:-1] 

if __name__ == "__main__": 
    s1 = "abab"
    s2 = "aba" 
    print(f'repeatedSubstring: s1:{repeatedSubstring(s1)}, s2:{repeatedSubstring(s2)}')
    print(f'repeatedSubstring_1: s1:{repeatedSubstring_1(s1)}, s2:{repeatedSubstring_1(s2)}') 

