"""
给你一个整数数组 nums ，其中可能包含重复元素，请你返回该数组所有可能的 子集（幂集）。

解集 不能 包含重复的子集。返回的解集中，子集可以按 任意顺序 排列。
 示例 1：

 输入：nums = [1,2,2]
 输出：[[],[1],[1,2],[1,2,2],[2],[2,2]]
 示例 2：

 输入：nums = [0]
 输出：[[],[0]]
"""


from typing import List
from collections import Counter

def subsetsWithDup(nums: List[int]) -> list[List[int]]:
    """
    回溯法 + 排序去重
    思路：先排序，让相同元素相邻。在回溯时，如果当前元素和前一个元素相同，且前一个元素在当前轮次没有被使用（i > start），则跳过，避免生成重复子集。
    时间复杂度: O(n * 2^n) - 共有 2^n 个子集，每个子集需要 O(n) 时间复制
    空间复杂度: O(n) - 递归栈深度 + 当前路径
    """
    res = []
    path = []
    n = len(nums)

    nums.sort() # 先排序，重复元素相邻方便后续去重

    def backtrack(start: int):
        # 每次进入递归，当前路径就是一个有效子集，直接加入结果集
        res.append(path[:])

        # 从start开始遍历，避免回头取元素（保证子集内元素按原数组顺序）
        for i in range(start, n):
            # 去重关键：如果当前元素和前一个相同，且前一个元素在当前轮次没被使用
            # i > start 表示不是当前层的第一个元素，且nums[i] == nums[i-1]
            # 说明这个元素已经被用过了，跳过避免重复
            if i > start and nums[i] == nums[i-1]:
                continue

            # 做选择：将nums[i]加入路径
            path.append(nums[i])
            # 递归进入下一层，从 i+1 开始（每个元素只能用一次）
            backtrack(i+1)
            # 撤销选择：回溯，移除最后一个元素
            path.pop()

    backtrack(0)
    return res


def subsetsWithDup_iter(nums: List[int]) -> List[List[int]]:
    """
    迭代法：逐元素构建子集
    思路：逐个处理元素。如果当前元素与上一个不同，从所有已有子集扩展；如果相同，只从上一步新增加的子集扩展
    时间复杂度：O(n * 2 ^ n)
    空间复杂度：O(2 ^ n) - 存储所有子集
    """

    nums.sort() # 先排序
    res = [[]] # 初始包含空集
    n = len(nums)
    i = 0

    while i < n:
        # 统计当前重复元素的个数
        count = 1
        while i + count < n and nums[i+count] == nums[i]:
            count += 1

        # 当前已有子集数量
        prev_size = len(res)

        # 对于每一个已有子集，考虑加入1个、2个...count个nums[i]
        for j in range(prev_size):
            # 从已有子集出发，逐步加入当前元素
            cur = res[j].copy()
            for _ in range(count):
                cur.append(nums[i])
                res.append(cur.copy())

        i += count # 跳过重复元素

    return res


def subsetsWithDup_bitmask(nums: List[int]) -> List[List[int]]:
    """
    位运算枚举 + 哈希去重
    思路：思路：用二进制位表示每个元素是否选取，然后用 set 去重。虽然不够优雅，但直观易懂。
    时间复杂度：O(n * 2^n)
    空间复杂度：O(2^n) - 哈希集合存储去重
    """
    nums.sort()
    n = len(nums)
    res_set = set()

    # 枚举所有2^n种状态
    for mask in range(1 << n): # 1 << n 等于 2^n
        subset = []
        for i in range(n):
            # 检查第i位是否为1
            if mask & (1 << i):
                subset.append(nums[i])
        # 用元组存入集合去重（列表不可哈希）
        res_set.add(tuple(subset))

    # 转回列表
    return [list(t) for t in res_set]


def subsetsWithDup_counter(nums: List[int]) -> List[List[int]]:
    """
    回溯法 + 计数器（不依赖排序）
    时间复杂度：O(n * 2^n)
    空间复杂度：O(n)
    """
    # 统计每个元素出现的次数
    count = Counter(nums)
    # 获取所有唯一元素
    unique_nums = list(count.keys())
    res = []
    path = []

    def backtrack(i: int):
        # 所有元素处理完毕，加入结果
        if i == len(unique_nums):
            res.append(path[:])
            return

        num = unique_nums[i]
        max_count = count[num]

        # 对于当前元素，可以选择取0,1,2，...，max_count个
        for times in range(max_count + 1):
            # 添加times个num
            for _ in range(times):
                path.append(num)
            # 递归处理下一个元素
            backtrack(i + 1)
            # 回溯：移除刚才添加的
            for _ in range(times):
                path.pop()

    backtrack(0)
    return res
