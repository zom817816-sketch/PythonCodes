"""
给定一个字符串 s 和一个整数 k,从字符串开头算起,每计数至 2k 个字符,就反转这 2k 字符中的前 k 个字符。
如果剩余字符少于 k 个,则将剩余字符全部反转。
如果剩余字符小于 2k 但大于或等于 k 个,则反转前 k 个字符,其余字符保持原样。
""" 

# 原地迭代+双指针
def reverse_str(s: str, k: int) -> str:
    """
    时间复杂度:O(n)
    空间复杂度:O(n)
    """ 
    def reverse_substr(substr: str) -> str:
        """
        反转子字符串
        """
        left, right = 0, len(substr) - 1
        while left < right:
            substr[left], substr[right] = substr[right], substr[left]
            left += 1
            right -= 1
        return substr 
    s_list = list(s) 
    for i in range(0, len(s_list), 2*k):
        s_list[i:i+k] = reverse_substr(s_list[i:i+k])
    return ''.join(s_list)

# 字符串切片 
def reverse_str_1(s: str, k: int) -> str: 
    """
    时间复杂度:O(n)
    空间复杂度:O(n)
    """ 
    res = ''
    for i in range(0, len(s), 2*k):
        res += s[i:i+k][::-1] + s[i+k:i+2*k]
    return res


# 递归+字符串切片
def reverse_str_2(s: str, k: int) -> str:
    """
    时间复杂度:O(n)
    空间复杂度:O(n)
    """ 
    if len(s) <= k: 
        return s[::-1] 
    elif len(s) < 2*k:
        return s[:k][::-1] + s[k:] 
    else:
        return s[:k][::-1] + s[k:2*k] + reverse_str_2(s[2*k:], k) 

if __name__ == '__main__':
    s = 'abcdefg'
    k = 2
    print(reverse_str(s, k))
    print(reverse_str_2(s, k)) 