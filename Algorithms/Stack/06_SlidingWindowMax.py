"""
给定一个数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。
你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。
返回滑动窗口中的最大值。

进阶：你能在线性时间复杂度内解决此题吗？

当前解法思路：
- 维护当前窗口中的最大值及其索引
- 滑动窗口时，索引减1表示最大值相对位置左移
- 如果新进入的数字大于等于上一个最大值，则它一定是新窗口的最大值
- 如果原最大值仍在窗口内（max_idx >= 0），继续复用它
- 如果原最大值已滑出窗口，重新遍历查找新最大值

时间复杂度：O(n × k) - 最坏情况下每次都要重新查找最大值
空间复杂度：O(k) - 维护窗口列表
"""

from collections import deque


def slidingWindowMax(nums: list, k: int) -> list:
    """
    滑动窗口最大值 - 原始解法
    时间复杂度：O(n × k) 最坏情况
    空间复杂度：O(k) - 维护窗口列表
    """
    length = len(nums)
    if length == 0 or k == 0:
        return []
    if length <= k:
        return [max(nums)]

    # 初始化窗口和剩余元素
    window = nums[:k]
    remain = nums[k:]

    # 找到初始窗口的最大值及其索引
    max_idx, max_val = max(enumerate(window), key=lambda x: x[1])
    res = [max_val]

    while remain:
        # 窗口滑动：移除最左边元素
        window.pop(0)
        # 最大值索引左移（相对位置）
        max_idx -= 1

        # 新元素进入窗口
        new_num = remain.pop(0)
        window.append(new_num)

        # 情况1：新元素大于等于上一个最大值，则它一定是新窗口最大值
        if new_num >= res[-1]:
            res.append(new_num)
            max_idx = k - 1  # 新元素在窗口最右端
            max_val = new_num
        else:
            # 情况2：新元素小于上一个最大值
            if max_idx >= 0:
                # 原最大值仍在窗口内，继续复用
                res.append(max_val)
            else:
                # 原最大值已滑出窗口，重新查找最大值
                max_idx, max_val = max(enumerate(window), key=lambda x: x[1])
                res.append(max_val)

    return res


def slidingWindowMaxOptimized(nums: list, k: int) -> list:
    """
    滑动窗口最大值 - 单调队列优化解法（线性时间复杂度）

    思路：
    - 使用双端队列维护可能成为最大值的元素索引
    - 队列中的索引对应的值单调递减
    - 队首始终是当前窗口的最大值
    - 滑动窗口时，移除不在窗口内的元素，保持队列单调性

    时间复杂度：O(n) - 每个元素最多入队出队一次
    空间复杂度：O(k) - 队列最多存储 k 个索引
    """
    if not nums or k == 0:
        return []

    # 双端队列存储索引，对应值单调递减
    dq = deque()
    res = []

    for i, num in enumerate(nums):
        # 1. 移除不在当前窗口内的元素（队首元素超出窗口左边界）
        if dq and dq[0] <= i - k:
            dq.popleft()

        # 2. 保持队列单调递减：移除队尾所有小于当前值的元素
        # 这些元素不可能成为后续窗口的最大值
        while dq and nums[dq[-1]] < num:
            dq.pop()

        # 3. 当前元素入队
        dq.append(i)

        # 4. 窗口形成后开始记录结果（队首即为当前窗口最大值）
        if i >= k - 1:
            res.append(nums[dq[0]])

    return res
