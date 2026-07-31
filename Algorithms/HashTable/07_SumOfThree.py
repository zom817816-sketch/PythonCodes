"""
# 15. 三数之和（3Sum）

## 题目描述

给你一个整数数组 `nums`，请你找出所有和为 `0` 且不重复的三元组
`[a, b, c]`，使得：

    a + b + c = 0

注意：

1. 同一个数组元素只能使用一次；
2. 答案中不能包含重复的三元组；
3. 三元组内部通常按非递减顺序排列，答案的整体顺序不作要求。

示例：

    输入：nums = [-1, 0, 1, 2, -1, -4]
    输出：[[-1, -1, 2], [-1, 0, 1]]

    输入：nums = [0, 0, 0, 0]
    输出：[[0, 0, 0]]

## 解法总览

### 方法一：排序 + 双指针（`sum_three_1`）

先排序，固定第一个数 `nums[i]`，再在右侧区间使用左右指针寻找：

    nums[i] + nums[left] + nums[right] = 0

因为数组已经有序：

- 和小于 `0`：增大 `left`，让总和变大；
- 和大于 `0`：减小 `right`，让总和变小；
- 和等于 `0`：记录答案，并同时跳过两端重复值。

这是本题最常用、最推荐的写法。

### 方法二：排序 + 哈希表（`sum_three_2`）

固定前两个数中的第一个数 `nums[i]`，遍历第二个数 `nums[j]`，
用哈希表记录已经见过的值，检查目标值
`-nums[i] - nums[j]` 是否出现过。

两种方法的时间复杂度都是 `O(n²)`；方法一额外空间更小，方法二更直观地
展示了“查找两数之和”的哈希表思想。

## 复杂度总览

设 `n = len(nums)`：

| 函数 | 时间复杂度 | 额外空间复杂度 | 是否原地排序 |
| --- | --- | --- | --- |
| `sum_three_1` | `O(n²)` | `O(1)`（不计结果） | 是 |
| `sum_three_2` | `O(n²)` | `O(n)`（不计结果） | 是 |

排序在 Python 中为 `O(n log n)`，被后续的 `O(n²)` 搜索过程覆盖。
返回结果本身占用的空间不计入额外空间复杂度。
"""


def sum_three_1(nums: list[int]) -> list[list[int]]:
    """使用“排序 + 双指针”找出所有不重复的三元组。

    Args:
        nums: 待搜索的整数数组。函数会原地排序该数组。

    Returns:
        所有和为 0 的不重复三元组；每个三元组按非递减顺序排列。

    正确性证明（循环不变式）：
        对于固定的 `i`，`left` 与 `right` 始终位于尚未排除的候选区间内。
        若当前和小于 0，由于数组有序，只有右移 `left` 才可能增大总和；
        若当前和大于 0，只有左移 `right` 才可能减小总和。因此每次移动都不会
        遗漏解。找到解后跳过相同值，只会删除值相同的重复表示，不会删除新的
        数值组合。外层同样跳过重复的 `nums[i]`，故最终结果恰好是不重复解集。

    易错点：
        - 不能只跳过外层重复值；找到答案后，`left` 和 `right` 也要去重。
        - `nums[i] > 0` 时可以提前结束，而不是 `nums[i] >= 0`；三个 0 可能是答案。
        - 移动指针后必须继续检查边界，不能在 `left == right` 时取值。
    """
    nums.sort()
    result: list[list[int]] = []
    n = len(nums)

    for i in range(n - 2):
        # 排序后，当前最小数都大于 0，后面不可能再得到 0。
        if nums[i] > 0:
            break

        # 固定位置不能使用相同的值，否则会生成重复三元组。
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]

            if total < 0:
                # nums[left] 太小；右移后总和只会增大或不变。
                left += 1
            elif total > 0:
                # nums[right] 太大；左移后总和只会减小或不变。
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])

                # 图解：找到 [i, left, right] 后，跳过相同端点。
                #   i      left                 right
                #   |        |                    |
                #   v        v                    v
                # [ ...  x  x  ...  y  y  ...  ]
                #      跳过左侧 x          跳过右侧 y
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1

                # 排除当前这组已处理的端点，继续寻找下一组。
                left += 1
                right -= 1

    return result


def sum_three_2(nums: list[int]) -> list[list[int]]:
    """使用“排序 + 哈希表”找出所有不重复的三元组。

    Args:
        nums: 待搜索的整数数组。函数会原地排序该数组。

    Returns:
        所有和为 0 的不重复三元组；每个三元组按非递减顺序排列。

    正确性证明：
        对每个固定的 `i`，遍历 `j` 时，哈希表保存了当前 `j` 之前已经看过的
        候选值。若目标值 `-nums[i] - nums[j]` 在表中，则它与当前两个数构成
        和为 0 的三元组；若不在表中，当前数会被加入表中，供后续位置使用。
        因而每个可行组合都会被发现。外层和内层分别跳过相同值，并在命中后
        删除已配对的目标值，保证相同数值组合不会重复输出。

    易错点：
        - 哈希表必须表示“当前 `j` 之前”的元素，不能先加入当前值再查找。
        - 命中后删除目标值，是为了避免同一固定 `i` 下重复输出相同组合。
        - 排序后才可以安全地使用外层去重和 `nums[i] > 0` 提前结束。
    """
    nums.sort()
    result: list[list[int]] = []
    n = len(nums)

    for i in range(n - 2):
        if nums[i] > 0:
            break
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        seen: set[int] = set()
        for j in range(i + 1, n):
            # 同一个固定的 i 下，重复的第二个数不产生新的三元组。
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue

            target = -nums[i] - nums[j]
            if target in seen:
                result.append([nums[i], target, nums[j]])
                # 当前目标值已经配对；删除可避免重复使用同一表示。
                seen.remove(target)
            else:
                seen.add(nums[j])

    return result
