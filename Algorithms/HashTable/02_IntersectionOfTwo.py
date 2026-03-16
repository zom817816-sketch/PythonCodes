"""
题意：给定两个数组，编写一个函数来计算它们的交集。
"""

def get_intersection_1(nums1: list[int], nums2: list[int]) -> list[int]:
    """
    时间复杂度: O(n) 空间复杂度: O(n)
    """
    from collections import Counter
    counter1 = Counter(nums1)
    counter2 = Counter(nums2)
    return list(set((counter1 & counter2).elements())) 

def get_intersection_2(nums1: list[int], nums2: list[int]) -> list[int]: 
    """
    时间复杂度: O(n) 空间复杂度: O(n)
    """ 
    set1 = set(nums1) 
    set2 = set(nums2) 
    return list(set1 & set2) 

def get_intersection_3(nums1: list[int], nums2: list[int]) -> list[int]: 
    """
    时间复杂度: O(n) 空间复杂度: O(n)
    """ 
    set1 = set(nums1) 
    res = set()
    for num in nums2: 
        if num in set1: 
            res.add(num) 
    return list(res) 

if __name__ == "__main__": 
    nums1 = [1, 2, 2, 1]
    nums2 = [2, 2]
    print(get_intsersection_1(nums1, nums2))
    print(get_intersection_2(nums1, nums2))
    print(get_intersection_3(nums1, nums2))