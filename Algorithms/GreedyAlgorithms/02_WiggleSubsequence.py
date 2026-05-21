"""
摆动序列问题

题目描述：
如果连续数字之间的差严格地在正数和负数之间交替，则数字序列称为 摆动序列 。
第一个差（如果存在的话）可能是正数或负数。仅有一个元素或者含两个不等元素的序列也视作摆动序列。

例如：
- [1, 7, 4, 9, 2, 5] 是一个摆动序列，因为差值 (6, -3, 5, -7, 3) 是正负交替的
- [1, 4, 7, 2, 5] 不是摆动序列，因为前两个差值都是正数
- [1, 7, 4, 5, 5] 不是摆动序列，因为最后一个差值为零

子序列 可以通过从原始序列中删除一些（也可以不删除）元素来获得，剩下的元素保持其原始顺序。

给你一个整数数组 nums ，返回 nums 中作为 摆动序列 的 最长子序列的长度 。

本题异常情况的本质，就是要考虑平坡， 平坡分两种，一个是 上下中间有平坡，一个是单调有平坡

方法1：贪心算法（推荐）⭐
- 核心思想：找局部最优的峰谷
- 遍历数组，记录峰谷点
- 时间复杂度：O(n)
- 空间复杂度：O(1)

方法2：动态规划
- up[i] = 以nums[i]结尾且最后是上升的最长摆动序列长度
- down[i] = 以nums[i]结尾且最后是下降的最长摆动序列长度
- 时间复杂度：O(n)
- 空间复杂度：O(n)

方法3：更简洁的动态规划
- 状态机思想
- 时间复杂度：O(n)
- 空间复杂度：O(1)
"""

from typing import List


# 方法1：贪心算法
def wiggleMaxLength_greedy(nums: List[int]) -> int:
    """
    贪心算法解摆动序列

    核心思想：
    1. 摆动序列的关键是找到"峰"和"谷"
    2. 峰：比前后元素都大（或等于前一个，小于后一个的趋势）
    3. 谷：比前后元素都小（或等于前一个，大于后一个的趋势）
    4. 只要遇到差值符号变化，就找到了一个峰或谷

    算法步骤：
    - 初始化：prev_diff = 0（新差值）
    - 遍历数组，计算当前差值
    - 如果 curr_diff > 0 且 prev_diff <= 0，找到一个谷底（或上升起点）
    - 如果 curr_diff < 0 且 prev_diff >= 0，找到一个峰顶（或下降起点）
    - 更新 prev_diff = curr_diff

    为什么贪心正确？
    - 我们要最大化摆动序列长度
    - 每次遇到符号变化，就是一个新的摆动点
    - 保留所有符号变化的点，得到的序列一定是最长的
    - 因为任何更短的序列都会错过某些符号变化点
    """
    if len(nums) <= 1:
        return len(nums)

    res = 1
    prev_diff = 0

    for i in range(1, len(nums)):
        # 计算当前差值
        curr_diff = nums[i] - nums[i - 1]

        # 严格交替
        if (curr_diff > 0 and prev_diff <= 0) or (curr_diff < 0 and prev_diff >= 0):
            res += 1
            # 在严格交替的情况下才能更新，否则当出现单调坡度中间的平坡时prev_diff也会更新
            prev_diff = curr_diff

    return res


# 方法2：动态规划（状态机）
def wiggleMaxLength_dp(nums: List[List[int]]) -> int:
    """
    动态规划解摆动序列

    状态定义：
    - up[i] = 以nums[i]结尾，且最后是上升（nums[i-1] < nums[i]）的最长摆动序列长度
    - down[i] = 以nums[i]结尾，且最后是下降（nums[i-1] > nums[i]）的最长摆动序列长度

    状态转移：
    - 如果 nums[i] > nums[i-1]（上升）
      - up[i] = down[i-1] + 1（接在下降序列后面形成摆动）
      - down[i] = down[i-1]（保持下降序列）
    - 如果 nums[i] < nums[i-1]（下降）
      - down[i] = up[i-1] + 1（接在上升序列后面形成摆动）
      - up[i] = up[i-1]（保持上升序列）
    - 如果 nums[i] == nums[i-1]（相等）
      - up[i] = up[i-1]
      - down[i] = down[i-1]

    初始状态：
    - up[0] = down[0] = 1（单个元素）

    最终结果：
    - max(up[n-1], down[n-1])

    空间优化：只需要前一个状态，所以可以用 O(1) 空间
    """
    if len(nums) <= 1:
        return len(nums)

    n = len(nums)
    up = [1] * n
    down = [1] * n

    for i in range(1, n):
        if nums[i] > nums[i - 1]:
            up[i] = down[i - 1] + 1
            down[i] = down[i - 1]
        elif nums[i] < nums[i - 1]:
            down[i] = up[i - 1] + 1
            up[i] = up[i - 1]
        else:
            up[i] = up[i - 1]
            down[i] = down[i - 1]

    return max(up[n - 1], down[n - 1])


# 方法3：空间优化版动态规划
def wiggleMaxLength_dp_optimized(nums: List[int]) -> int:
    """
    空间优化版动态规划

    核心思想：
    - 只需要前一个状态的 up 和 down
    - 所以可以用两个变量代替整个数组
    - 空间从 O(n) 降到 O(1)

    状态转移（只需前一个状态）：
    - 如果 nums[i] > nums[i-1]：up = down_prev + 1
    - 如果 nums[i] < nums[i-1]：down = up_prev + 1
    - 如果 nums[i] == nums[i-1]：up, down 不变
    """
    if len(nums) <= 1:
        return len(nums)

    up = down = 1

    for i in range(1, len(nums)):
        if nums[i] > nums[i - 1]:
            up = down + 1
        elif nums[i] < nums[i - 1]:
            down = up + 1
        # 如果相等，什么都不做

    return max(up, down)


# 方法4：处理所有边界情况的标准贪心
def wiggleMaxLength_standard(nums: List[int]) -> int:
    """
    标准贪心算法（处理所有边界情况）

    这个版本更严谨，考虑了：
    1. 连续相同值的情况
    2. 初始差值为0的情况
    3. 正负号变化的判断

    算法步骤：
    1. 先去掉开头的连续相同元素
    2. 统计符号变化的次数
    """
    n = len(nums)
    if n < 2:
        return n

    # 找到第一个非零差值的位置
    start = 0
    while start < n - 1 and nums[start] == nums[start + 1]:
        start += 1

    # 如果全是相同元素，返回1
    if start == n - 1:
        return 1

    # 初始化结果
    res = 2  # 已经包含了两个不同元素

    # 记录上一个非零差值的方向
    prev_sign = 0  # 1表示正，-1表示负
    if nums[start + 1] > nums[start]:
        prev_sign = 1
    else:
        prev_sign = -1

    # 遍历剩余元素
    for i in range(start + 2, n):
        curr_sign = 0
        if nums[i] > nums[i - 1]:
            curr_sign = 1
        elif nums[i] < nums[i - 1]:
            curr_sign = -1
        else:
            continue  # 跳过相同值

        # 如果方向变化，增加计数
        if curr_sign != prev_sign:
            res += 1
            prev_sign = curr_sign

    return res
