"""
给你一个按 非递减顺序 排序的整数数组 nums，返回 每个数字的平方 组成的新数组，要求也按 非递减顺序 排序。
暴力解法：O(nlogn)
"""


# 数组平方的最大值一定在数组的两端
def solution(nums):
    length = len(nums)
    left, right = 0, length - 1
    result = [0] * length
    k = length - 1
    while left <= right:
        if nums[left] ** 2 >= nums[right] ** 2:
            result[k] = nums[left] ** 2
            left += 1
        else:
            result[k] = nums[right] ** 2
            right -= 1
        k -= 1
    return result
