"""
给你一个整数数组 nums ，找出并返回所有该数组中不同的递增子序列，递增子序列中 至少有两个元素 。
你可以按 任意顺序 返回答案。数组中可能含有重复元素，如出现两个整数相等，也可以视作递增序列的一种特殊情况。

示例 1：
输入：nums = [4,6,7,7]
输出：[[4,6],[4,6,7],[4,6,7,7],[4,7],[4,7,7],[6,7],[6,7,7],[7,7]]

示例 2：
输入：nums = [4,4,3,2,1]
输出：[[4,4]]

提示：
- 1 <= nums.length <= 15
- -100 <= nums[i] <= 100
"""

from typing import List

# 解法一：回溯 + 哈希集合去重（标准解法）


def findSubsequences(nums: List[int]) -> List[List[int]]:
    """
    思路：
    每一层递归中，枚举从 start 开始到末尾的所有元素作为候选。
    对于每个候选元素 nums[i]：
      1. 非递减约束：只有 nums[i] >= path[-1] 时才能选（path 为空时任何元素都可选）
      2. 同层去重：在同一层递归中，已经用过的值不能再用（用 set 记录本层已选值）

    核心与"组合总和 II"的去重思路一致——在"同一层"去重：
      - 同层重复：在同一轮 for 循环中，相同值只取第一个（剪枝）
      - 不同层重复：path 中允许重复值（如 [7,7]），不在同层去重的考虑范围内

    时间复杂度：O(2^n × n) —— 每个元素选/不选共 2^n 种可能，每次复制路径 O(n)
    空间复杂度：O(n) —— 递归栈深度 O(n)，path 和 used_set 各 O(n)
    """
    res = []
    path = []
    n = len(nums)

    def backtrack(start: int) -> None:
        """从 nums[start] 开始搜索下一个元素"""
        # 当 path 长度 ≥ 2 时，记录当前子序列
        if len(path) >= 2:
            res.append(path[:])
        # 这里没有return，因为我们需要的是所有可能的子序列
        # 本层已使用过的值（用于同层去重）
        used = set()

        for i in range(start, n):
            # ===== 🟢 剪枝条件①：保持非递减 =====
            # 如果 path 不为空且当前元素 < path 最后一个元素，跳过
            if path and nums[i] < path[-1]:
                continue

            # ===== 🟢 剪枝条件②：同层去重 =====
            # 同一层递归中，相同数值只取第一个
            if nums[i] in used:
                continue

            # 标记本层已使用
            used.add(nums[i])

            # ① 做选择
            path.append(nums[i])

            # ② 递归：从 i+1 开始搜索下一个
            backtrack(i + 1)

            # ③ 撤销选择（回溯）
            path.pop()

    backtrack(0)
    return res


# 解法二：回溯 + 数组哈希去重（优化版）


def findSubsequences_array_hash(nums: List[int]) -> List[List[int]]:
    """
    思路：
    与解法一逻辑完全相同，但同层去重使用固定大小数组（201 个元素，映射 -100~100）
    代替哈希集合，利用数组 O(1) 访问更快。

    为什么用数组？因为 nums[i] 范围是 [-100, 100]，共 201 个可能取值，
    使用固定大小数组比哈希集合更高效。

    时间复杂度：O(2^n × n)
    空间复杂度：O(n)
    """
    res = []
    path = []
    n = len(nums)

    def backtrack(start: int) -> None:
        if len(path) >= 2:
            res.append(path[:])

        # 使用数组进行同层去重（偏移 +100 映射到 [0, 200]）
        used = [False] * 201  # 用于标记 -100 ~ 100 是否已被使用

        for i in range(start, n):
            # 剪枝①：非递减约束
            if path and nums[i] < path[-1]:
                continue

            # 剪枝②：同层去重
            idx = nums[i] + 100  # 映射到数组下标
            if used[idx]:
                continue

            used[idx] = True

            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


# 解法三：回溯 + 剪枝 + 条件判断去重（不依赖额外数据结构）


def findSubsequences_pruned(nums: List[int]) -> List[List[int]]:
    """
    思路：
    同层去重不依赖 set 或数组，而是利用"排序后的相邻性判断"思路的变体——
    在当前层遍历时，检查在 start ~ i-1 之间是否出现过与 nums[i] 相同的值。
    如果出现过，说明 nums[i] 在本层是重复值，跳过。

    注意：这里的前提是原数组不能排序（因为题目要求原序列顺序），
    所以不能先排序再用相邻比较法，只能用"往前查找"的方式。

    时间复杂度：O(2^n × n²) —— 每次检查重复需要 O(n)
    空间复杂度：O(n)
    """
    res = []
    path = []
    n = len(nums)

    def backtrack(start: int) -> None:
        if len(path) >= 2:
            res.append(path[:])

        for i in range(start, n):
            # 剪枝①：非递减约束
            if path and nums[i] < path[-1]:
                continue

            # 剪枝②：同层去重（检查 start ~ i-1 之间是否有相同值）
            is_duplicate = False
            for j in range(start, i):
                if nums[j] == nums[i]:
                    is_duplicate = True
                    break
            if is_duplicate:
                continue

            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return res


# 解法四：使用二进制枚举（位运算）—— 思路拓展


def findSubsequences_bit(nums: List[int]) -> List[List[int]]:
    """
    思路：
    用二进制掩码枚举所有子集（共 2^n 种），然后过滤出：
      1. 长度 ≥ 2
      2. 非递减
      3. 去重（用 set 去重）

    注意：这种方法效率较低，因为枚举了所有子集再过滤，
    但提供了一种不同的思考角度。

    时间复杂度：O(2^n × n)
    空间复杂度：O(2^n) —— 需要存储所有子集用于去重

    Args:
        nums: 输入数组

    Returns:
        所有不同的递增子序列
    """
    n = len(nums)
    seen = set()
    res = []

    for mask in range(1, 1 << n):  # 从 1 开始，排除空集
        subset = []
        # 构建当前掩码对应的子序列
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])

        # 过滤条件①：长度至少为 2
        if len(subset) < 2:
            continue

        # 过滤条件②：非递减
        is_increasing = True
        for k in range(1, len(subset)):
            if subset[k] < subset[k - 1]:
                is_increasing = False
                break
        if not is_increasing:
            continue

        # 过滤条件③：去重（用元组作为可哈希的标识）
        key = tuple(subset)
        if key not in seen:
            seen.add(key)
            res.append(subset)

    return res
