"""
编写一个算法来判断一个数 n 是不是快乐数。

「快乐数」定义为：对于一个正整数，每一次将该数替换为它每个位置上的数字的平方和，然后重复这个过程直到这个数变为 1，也可能是 无限循环 但始终变不到 1。如果 可以变为  1，那么这个数就是快乐数。

如果 n 是快乐数就返回 True ；不是，则返回 False 。
""" 

def if_happy_num_1(n: int) -> bool:
    """
    判断 n 是否是快乐数
    时间复杂度: O(logn) 空间复杂度: O(logn)
    """
    def next(num): 
        return sum(int(digit) ** 2 for digit in str(num)) 
    seen = set() 
    while n not in seen and n != 1: 
        seen.add(n) 
        n = next(n) 
        if n == 1: 
            return True 
    return False 

def if_happy_num_2(n: int) -> bool:
    """
    判断 n 是否是快乐数
    时间复杂度: O(logn) 空间复杂度: O(1)
    """ 
    def next(num): 
        return sum(int(digit) ** 2 for digit in str(num)) 
    fast, slow = next(n), n 
    while fast != 1 and fast != slow: 
        slow = next(slow) 
        fast = next(next(fast)) 
        if slow == fast: 
            return False 
    return fast == 1

if __name__ == "__main__": 
    n = 19
    print(if_happy_num_1(n))
    print(if_happy_num_2(n)) 