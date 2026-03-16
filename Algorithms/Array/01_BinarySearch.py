"""
给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target  ，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。
"""


# 左闭右闭
def binary_search_1(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:  # 找到目标，返回下标
            return mid
        elif nums[mid] > target:  # 目标在左区间，更新右边界
            right = mid - 1
        else:  # 目标在右区间，更新左边界
            left = mid + 1
    return -1


# 左闭右开
def binary_search_2(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] == target:  # 找到目标，返回下标
            return mid
        elif nums[mid] > target:  # 目标在左区间，更新右边界
            right = mid
        else:  # 目标在右区间，更新左边界
            left = mid - 1
    return -1
