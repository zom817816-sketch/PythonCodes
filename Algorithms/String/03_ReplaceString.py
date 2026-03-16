"""
给定一个字符串 s,它包含小写字母和数字字符,请编写一个函数,将字符串中的字母字符保持不变,而将每个数字字符替换为number。

例如,对于输入字符串'a1b2c3',函数应该将其转换为 'anumberbnumbercnumber'。

对于输入字符串 'a5b',函数应该将其转换为 'anumberb'
""" 

def replace_str(s: str) -> str:
    """
    时间复杂度:O(n)
    空间复杂度:O(n)
    """
    res = ''
    for char in s:
        if char.isdigit():
            res += 'number'
        else:
            res += char
    return res