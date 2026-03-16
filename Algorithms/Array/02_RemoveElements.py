"""
给你一个数组 nums 和一个值 val，你需要 原地 移除所有数值等于 val 的元素，并返回移除后数组的新长度。不要使用额外的数组空间，你必须仅使用 O(1) 额外空间
"""


# 单向指针
def removeSingleDir(nums, val):
    # 快慢指针
    fast, slow = 0, 0
    while fast < len(nums):
        # 慢指针用于保存非目标值
        if nums[fast] != val:
            slow += 1
            nums[slow] = nums[fast]
        fast += 1
    return slow


# 双向指针
def removeDoubleDir(nums, val):
    # 双向指针
    left, right = 0, len(nums) - 1
    # 左右指针未相遇时持续遍历
    while left <= right:
        # 左指针右移：跳过所有「不需要删除」的元素，直到找到待删元素或指针越界
        while left <= right and nums[left] != val:
            left += 1
        # 右指针左移：跳过所有「需要删除」的元素，直到找到保留元素或指针越界
        while left <= right and nums[right] == val:
            right -= 1
        # 若左右指针未相遇，用右指针的保留元素覆盖左指针的待删元素
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
    return left  # 左指针最终位置 = 新数组有效长度
