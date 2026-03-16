"""
给定两个字符串 s 和 t ，编写一个函数来判断 t 是否是 s 的字母异位词。

示例 1: 输入: s = "anagram", t = "nagaram" 输出: true

示例 2: 输入: s = "rat", t = "car" 输出: false

说明: 你可以假设字符串只包含小写字母。
""" 

def if_anagram_1(s: str, t: str) -> bool:
    """
    判断 t 是否是 s 的字母异位词
    时间复杂度: O(n) 空间复杂度: O(1)
    """ 
    if len(s) != len(t): 
        return False 
    counter = [0] * 26 
    for i in range(len(s)): 
        counter[ord(s[i]) - ord('a')] += 1 
        counter[ord(t[i]) - ord('a')] -= 1 
    return all(x == 0 for x in counter) 

def is_anagram_2(s: str, t: str) -> bool:
    """
    判断 t 是否是 s 的字母异位词
    时间复杂度: O(n) 空间复杂度: O(1)
    """
    from collections import Counter 
    return Counter(s) == Counter(t)



if __name__ == '__main__': 
    s = "anagram"
    t = "nagaram"
    print(if_anagram_1(s, t))
    print(is_anagram_2(s, t))
