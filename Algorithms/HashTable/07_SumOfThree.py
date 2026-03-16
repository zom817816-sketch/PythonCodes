"""
给你一个包含 n 个整数的数组 nums,判断 nums 中是否存在三个元素 a,b,c ,使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。

注意： 答案中不可以包含重复的三元组。
"""

# 方法一: 排序 + 双指针
def sum_three_1(nums: list[int]) -> list[list[int]]:
    """
    给定一个整数数组 nums,判断 nums 中是否存在三个元素 a,b,c ,使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
    时间复杂度: O(n^2) 空间复杂度: O(1)
    """
    nums.sort()
    res = []
    for i in range(len(nums)):
        # 如果当前元素大于0, 则三数之和一定大于0, 直接返回结果
        if nums[i] > 0:
            return res
        # 跳过重复的元素
        if i > 0 and nums[i] == nums[i-1]:
            continue
        l, r = i+1, len(nums)-1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                # 跳过重复的元素
                while l < r and nums[l] == nums[l+1]:
                    l += 1
                while l < r and nums[r] == nums[r-1]:
                    r -= 1
                l += 1
                r -= 1
    return res 

# 排序 + 字典 
def sum_three_2(nums: list[int]) -> list[list[int]]:
    """
    给定一个整数数组 nums,判断 nums 中是否存在三个元素 a,b,c ,使得 a + b + c = 0 ？请你找出所有满足条件且不重复的三元组。
    时间复杂度: O(n^2) 空间复杂度: O(n)
    """
    nums.sort()
    res = []
    for i in range(len(nums)):
        # 如果当前元素大于0, 则三数之和一定大于0, 直接返回结果
        if nums[i] > 0:
            return res
        # 跳过重复的元素
        if i > 0 and nums[i] == nums[i-1]:
            continue
        d = {}
        for j in range(i+1, len(nums)):
            # 跳过重复的元素
            if j > i+1 and nums[j] == nums[j-1]:
                continue
            target = -nums[i] - nums[j]
            if target in d:
                res.append([nums[i], target, nums[j]])
                d.pop(target)
            else:
                d[nums[j]] = j 
    return res


if __name__ == "__main__":
    nums = [-1, 0, 1, 2, -1, -4]
    print(sum_three_1(nums))
    print(sum_three_2(nums))