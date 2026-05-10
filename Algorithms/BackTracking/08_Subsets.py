"""
给你一个整数数组 nums ，数组中的元素 互不相同 。返回该数组所有可能的子集（幂集）。
解集 不能 包含重复的子集。你可以按 任意顺序 返回解集。

示例 1：
输入：nums = [1,2,3]
输出：[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

示例 2：
输入：nums = [0]
输出：[[],[0]]

提示：
- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- nums 中的所有元素 互不相同
"""

from typing import List

# 解法一：回溯法（选与不选 二叉树思想）


def subsets_backtrack(nums: List[int]) -> List[List[int]]:
    """
    思路：
    将每个元素看作二叉树的一个节点，每个节点有两种选择：
        1. 选择当前元素（左子树）
        2. 不选当前元素（右子树）
    遍历所有元素，递归地进行选/不选决策，当遍历到数组末尾时，
    将当前路径（已选元素）加入结果集。

    时间复杂度：O(n × 2^n) —— 每个元素选/不选共 2^n 种组合，每次复制路径 O(n)
    空间复杂度：O(n) —— 递归栈深度为 n，path 列表长度也为 n
    """
    n = len(nums)
    res = []
    path = []

    def dfs(i: int) -> None:
        """深度优先遍历到第 i 个元素（0-indexed）"""
        if i == n:
            # 已遍历完所有元素，记录当前子集
            res.append(path[:])  # 拷贝一份，避免后续修改影响
            return

        # 1. 不选当前元素，直接去下一个
        dfs(i + 1)

        # 2. 选当前元素
        path.append(nums[i])
        dfs(i + 1)

        # 回溯：撤销选择，恢复状态
        path.pop()

    dfs(0)
    return res


# 解法二：回溯法（组合枚举 多叉树思想）


def subsets_combine(nums: List[int]) -> List[List[int]]:
    """
    思路：
    在每一层递归中，依次枚举「从当前位置开始到末尾」的元素作为下一个加入子集的元素。
    与解法一的区别：解法一在树的每一层"硬性"决定选/不选当前元素；
                     本解法在树的每一层"尝试"将某个后面的元素加入子集。

    时间复杂度：O(n × 2^n)
    空间复杂度：O(n)
    """
    res = []
    path = []

    def backtrack(start: int) -> None:
        """
        start：本次递归可以从 nums[start] 开始选取元素
        每次进入递归时，当前 path 已经是一个合法子集，直接加入结果
        """
        # 每到一个节点，path 都是一个新的合法子集
        res.append(path[:])

        for i in range(start, len(nums)):
            # 选择 nums[i]
            path.append(nums[i])
            # 继续递归，下一轮从 i+1 开始（避免重复使用同一个元素）
            backtrack(i + 1)
            # 回溯：撤销选择
            path.pop()

    backtrack(0)
    return res


# 解法三：迭代法（增量构造）


def subsets_iterative(nums: List[int]) -> List[List[int]]:
    """
    思路：
    从空集开始，每遇到一个新元素，就将其追加到当前已有的所有子集中，
    从而生成新的子集，不断迭代即可得到完整幂集。

    举例 nums = [1, 2, 3]：
        res = [[]]
        处理 1：res = [[], [1]]
        处理 2：res = [[], [1], [2], [1, 2]]
        处理 3：res = [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3]]

    时间复杂度：O(n × 2^n)
    空间复杂度：O(1)（不计输出空间）
    """
    res = [[]]  # 初始包含空集
    for num in nums:
        # 对当前结果中的每个子集，追加当前元素生成新子集
        res += [cur + [num] for cur in res]
    return res


# 解法四：位运算（二进制掩码）


def subsets_bit(nums: List[int]) -> List[List[int]]:
    """
    思路：
    对于长度为 n 的数组，共有 2^n 个子集。
    用 0 ~ 2^n - 1 的二进制数来代表每一个子集：
        - 二进制位为 1 表示选取对应位置的元素
        - 二进制位为 0 表示不选

    例如 nums = [1, 2, 3]：
        000 -> []
        001 -> [3]      （从右往左，最低位对应末尾元素）
        010 -> [2]
        011 -> [2, 3]
        100 -> [1]
        101 -> [1, 3]
        110 -> [1, 2]
        111 -> [1, 2, 3]

    时间复杂度：O(n × 2^n)
    空间复杂度：O(1)（不计输出空间）
    """
    n = len(nums)
    res = []
    # 共有 2^n 个子集
    for mask in range(1 << n):
        subset = []
        # 检查 mask 的每一位
        for i in range(n):
            if mask & (1 << i):
                subset.append(nums[i])
        res.append(subset)
    return res


# 解法五：Python 标准库 itertools.combinations
from itertools import combinations


def subsets_itertools(nums: List[int]) -> List[List[int]]:
    """
    思路：
    利用 Python 标准库 itertools.combinations，
    分别取长度为 0, 1, 2, ..., n 的组合，汇总即得所有子集。

    时间复杂度：O(n × 2^n)
    空间复杂度：O(n)（combinations 内部开销）
    """
    res = []
    n = len(nums)
    for k in range(n + 1):
        for combo in combinations(nums, k):
            res.append(list(combo))
    return res
