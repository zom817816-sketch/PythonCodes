"""
给定一个赎金信 (ransom) 字符串和一个杂志(magazine)字符串，判断第一个字符串 ransom 能不能由第二个字符串 magazines 里面的字符构成。如果可以构成，返回 true ；否则返回 false。

(题目说明：为了不暴露赎金信字迹，要从杂志上搜索各个需要的字母，组成单词来表达意思。杂志字符串中的每个字符只能在赎金信字符串中使用一次。)
"""

def can_construct_1(ransomNote: str, magazine: str) -> bool:
    """
    判断赎金信是否可以由杂志中的字符构成。
    
    时间复杂度: O(n) 空间复杂度: O(1)
    """
    # 使用数组存储杂志中每个字符的出现次数
    magazine_counter = [0] * 26
    for d in magazine:
        magazine_counter[ord(d)-ord('a')] += 1
    # 检查赎金信中的每个字符是否在杂志中出现足够次数
    for d in ransomNote:
        if magazine_counter[ord(d)-ord('a')] <= 0:
            return False
        magazine_counter[ord(d)-ord('a')] -= 1
    return True 

# 使用Counter 
def can_construct_2(ransomNote: str, magazine: str) -> bool:
    """
    判断赎金信是否可以由杂志中的字符构成。
    
    时间复杂度: O(n) 空间复杂度: O(1)
    """
    from collections import Counter
    return not (Counter(ransomNote) - Counter(magazine)) 

# 使用字典 
def can_construct_3(ransomNote: str, magazine: str) -> bool:
    """
    判断赎金信是否可以由杂志中的字符构成。
    
    时间复杂度: O(n) 空间复杂度: O(1)
    """
    # 使用字典存储杂志中每个字符的出现次数
    magazine_counter = {}
    for d in magazine:
        magazine_counter[d] = magazine_counter.get(d, 0) + 1
    # 检查赎金信中的每个字符是否在杂志中出现足够次数
    for d in ransomNote:
        if magazine_counter.get(d, 0) <= 0:
            return False
        magazine_counter[d] -= 1
    return True 

if __name__ == "__main__":
    ransomNote = "a"
    magazine = "ab"
    print(can_construct_1(ransomNote, magazine))
    print(can_construct_2(ransomNote, magazine))
    print(can_construct_3(ransomNote, magazine))