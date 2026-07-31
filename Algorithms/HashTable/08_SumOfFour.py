r"""
# 18. 四数之和（4Sum）

## 题目描述

给你一个整数数组 `nums` 和一个目标值 `target`，请你找出所有和为
`target` 且不重复的四元组 `[a, b, c, d]`，使得：

    a + b + c + d = target

注意：

1. 同一个数组元素只能使用一次；
2. 答案中不能包含重复的四元组；
3. 四元组内部通常按非递减顺序排列，答案的整体顺序不作要求。

示例：

    输入：nums = [1, 0, -1, 0, -2, 2], target = 0
    输出：[[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]

    输入：nums = [2, 2, 2, 2, 2], target = 8
    输出：[[2, 2, 2, 2]]

## 解法总览：排序 + 两层枚举 + 双指针

四数之和可以看成“在三数之和外面再固定一个数”：

1. 先排序，使数组有序，并让去重和剪枝成立；
2. 用 `a` 枚举第一个数；
3. 用 `b` 枚举第二个数；
4. 在 `[b + 1, n - 1]` 中，用 `left` 和 `right` 查找剩余两个数。

指针移动规则：

- 四数之和小于 `target`：右移 `left`，增大总和；
- 四数之和大于 `target`：左移 `right`，减小总和；
- 等于 `target`：记录答案，然后跳过左右两侧重复值。

### 搜索区间图解

    a        b        left              right
    |        |         |                  |
    v        v         v                  v
    [  ...  ...  ...   ?  ...  ...  ...    ?  ]
    \____固定____/     \____双指针搜索____/

在固定 `a` 和 `b` 后，每次只移动一个指针；由于数组有序，已经排除的
位置不可能重新产生更优的候选，因此双指针过程是线性的。

## 复杂度分析

设 `n = len(nums)`：

- 排序：`O(n log n)`；
- 两层枚举和双指针：`O(n³)`；
- 总时间复杂度：`O(n³)`；
- 额外空间复杂度：`O(1)`（不计排序实现细节和返回结果）。

结果列表本身的空间不计入额外空间复杂度。

## 正确性证明

固定任意一组 `a` 和 `b` 后，双指针维护区间 `[left, right]` 中尚未排除的
候选对。若当前四数之和小于 `target`，因为数组有序，增大 `left` 是唯一
可能使总和变大的方向；若总和大于 `target`，减小 `right` 是唯一可能使总和
变小的方向。因此每次移动都不会跳过满足条件的候选对。

外层循环枚举了所有可能的 `a` 和 `b`；双指针又枚举了对应的所有可行 `c`、`d`，
所以每个满足条件的四元组都会被找到。排序后，外层跳过重复的 `a`、`b`，
命中后跳过重复的 `c`、`d`，因此每个数值组合只输出一次。

## 易错点

- 去重条件必须是 `a > 0` 或 `b > a + 1`，否则会误跳过该层的第一个候选值。
- 找到答案后要先跳过重复的 `left`、`right`，再分别移动两个指针。
- 剪枝只能建立在数组有序的前提上；未排序时不能比较最小/最大可能和。
- 不要把“元素不能重复使用”误解为“数值不能重复使用”。例如四个 `2` 可以
  组成 `[2, 2, 2, 2]`，前提是数组中确实有四个 `2`。
- Python 整数不会溢出，但在其他语言中计算多个整数之和时要注意整数溢出。
"""


def sum_four(nums: list[int], target: int) -> list[list[int]]:
    """使用“排序 + 两层枚举 + 双指针”找出所有不重复的四元组。

    Args:
        nums: 待搜索的整数数组。函数会原地排序该数组。
        target: 四元组需要达到的目标和。

    Returns:
        所有和为 `target` 的不重复四元组；每个四元组按非递减顺序排列。

    剪枝说明：
        对固定的 `a`，若当前最小四数之和已经大于目标，后续更大的 `a`
        也不可能有解；若当前最大的四数之和仍小于目标，则只能尝试下一个
        `a`。固定 `a`、`b` 后也可以用同样的最小/最大和判断提前结束或跳过。
    """
    nums.sort()
    result: list[list[int]] = []
    n = len(nums)

    # 至少需要四个元素；这样也能避免访问不存在的下标。
    if n < 4:
        return result

    for a in range(n - 3):
        # a 层的最小可能和大于 target，后面的 a 只会更大。
        if nums[a] + nums[a + 1] + nums[a + 2] + nums[a + 3] > target:
            break
        # a 层的最大可能和仍小于 target，当前 a 不可能有解。
        if nums[a] + nums[n - 3] + nums[n - 2] + nums[n - 1] < target:
            continue

        # 只跳过同一层中重复的第一个数。
        if a > 0 and nums[a] == nums[a - 1]:
            continue

        for b in range(a + 1, n - 2):
            # 固定 a、b 后，剩余两个数取最小时已超过 target。
            if nums[a] + nums[b] + nums[b + 1] + nums[b + 2] > target:
                break
            # 剩余两个数取最大时仍不足 target，当前 b 不可能有解。
            if nums[a] + nums[b] + nums[n - 2] + nums[n - 1] < target:
                continue

            # 只跳过 b 层中重复的第二个数。
            if b > a + 1 and nums[b] == nums[b - 1]:
                continue

            left, right = b + 1, n - 1
            while left < right:
                total = nums[a] + nums[b] + nums[left] + nums[right]

                if total < target:
                    left += 1
                elif total > target:
                    right -= 1
                else:
                    result.append([nums[a], nums[b], nums[left], nums[right]])

                    # 找到一组后，跳过相同的第三、第四个数，避免重复答案。
                    while left < right and nums[left] == nums[left + 1]:
                        left += 1
                    while left < right and nums[right] == nums[right - 1]:
                        right -= 1
                    left += 1
                    right -= 1

    return result
