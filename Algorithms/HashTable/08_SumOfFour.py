"""
题意：给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。

注意：

答案中不可以包含重复的四元组。

示例： 给定数组 nums = [1, 0, -1, 0, -2, 2]，和 target = 0。 满足要求的四元组集合为： [ [-1, 0, 0, 1], [-2, -1, 1, 2], [-2, 0, 0, 2] ]
"""

def sum_four(nums: list[int], target: int) -> list[list[int]]: 
    """
    给定一个包含 n 个整数的数组 nums 和一个目标值 target，判断 nums 中是否存在四个元素 a，b，c 和 d ，使得 a + b + c + d 的值与 target 相等？找出所有满足条件且不重复的四元组。
    时间复杂度: O(n^3) 空间复杂度: O(1)
    """ 
    nums.sort() 
    n = len(nums) 
    res = []
    for a in range(n): 
        # 提前终止：当前元素乘以4大于target，后续元素更大，不可能找到解
        if nums[a] * 4 > target:
            break
        # 提前终止：当前元素加上最大的三个元素仍小于target，继续下一个a
        if nums[a] + nums[n-1] * 3 < target:
            continue
        # 跳过重复的元素
        if a > 0 and nums[a] == nums[a-1]: 
            continue 
        for b in range(a+1, n):
            # 提前终止：第一个元素加上第二个元素乘以3大于target
            if nums[a] + nums[b] * 3 > target:
                break
            # 提前终止：当前元素加上最大的三个元素仍小于target，继续下一个b
            if nums[a] + nums[b] + nums[n-1] * 2 < target:
                continue
            # 跳过重复的元素
            if b > a+1 and nums[b] == nums[b-1]:
                continue 
            c, d = b+1, n-1 
            while c < d: 
                total = nums[a] + nums[b] + nums[c] + nums[d] 
                if total < target: 
                    c += 1 
                elif total > target: 
                    d -= 1 
                else: 
                    res.append([nums[a], nums[b], nums[c], nums[d]])
                    # 跳过重复的元素
                    while c < d and nums[c] == nums[c+1]:
                        c += 1
                    while c < d and nums[d] == nums[d-1]:
                        d -= 1
                    c += 1
                    d -= 1 
    return res 

if __name__ == "__main__": 
    nums = [1,0,-1,0,-2,2]
    target = 0
    print(sum_four(nums, target))
