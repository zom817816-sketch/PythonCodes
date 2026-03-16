""" 
反转字符串
"""

def reverse_string_1(chars):
    """
    方法1:双指针原地反转
    时间复杂度:O(n)
    空间复杂度:O(1)
    """
    chars = chars[:]
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return chars


def reverse_string_2(chars):
    """
    方法2:使用切片
    时间复杂度:O(n)
    空间复杂度:O(n)    
    """
    chars = chars[:]
    return chars[::-1]


def reverse_string_3(chars):
    """
    方法3:使用内置 reversed
    时间复杂度:O(n)
    空间复杂度:O(n)    
    """
    chars = chars[:]
    return list(reversed(chars))


def reverse_string_4(chars):
    """
    方法4:递归反转
    时间复杂度:O(n)
    空间复杂度:O(n)    
    """
    chars = chars[:]
    if len(chars) <= 1:
        return chars
    return [chars[-1]] + reverse_string_4(chars[:-1])

if __name__ == '__main__':
    chars = ['h', 'e', 'l', 'l', 'o']
    print(reverse_string_1(chars))
    print(reverse_string_2(chars))
    print(reverse_string_3(chars))
    print(reverse_string_4(chars))
