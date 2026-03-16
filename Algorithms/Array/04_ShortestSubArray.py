"""
给定一个含有 n 个正整数的数组和一个正整数 s ，找出该数组中满足其和 ≥ s 的长度最小的连续子数组，并返回其长度。如果不存在符合条件的子数组，返回 0。
"""


def findSubArry(nums, s):
    length = len(nums)
    left, right = 0, 0
    cur_sum = 0
    min_len = length + 1

    while right < len(nums):
        cur_sum += nums[right]
        while cur_sum >= s:
            cur_sum -= nums[left]
            min_len = min(min_len, left - right + 1)
            left += 1

        right += 1

    return 0 if min_len == length + 1 else min_len
