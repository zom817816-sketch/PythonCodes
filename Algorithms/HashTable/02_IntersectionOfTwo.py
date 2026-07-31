"""
# 题目：两个数组的交集（Intersection of Two Arrays）

根据不同题意，计算两个整数数组的交集。这里同时整理两种常见定义：

- **不考虑重复次数的交集**：每个元素在结果中最多出现一次（LeetCode 349）。
- **考虑重复次数的交集**：一个元素在结果中出现的次数，等于它在两个数组中出现
  次数的较小值（LeetCode 350）。

## 示例

```text
输入：nums1 = [1, 2, 2, 1], nums2 = [2, 2]

按重复次数取交集： [2, 2]
去重后取交集：     [2]
```

结果中的元素顺序不作要求，因此使用集合实现时，返回列表的顺序可能不同。

## 核心概念

1. **集合交集**：只关心元素是否存在时，用 `set1 & set2` 去重并取交集。
2. **频次表**：关心重复次数时，用哈希表记录每个元素出现次数。
3. **保留较小频次**：重复交集中元素的次数是两个频次的最小值。
4. **空间换时间**：哈希表平均能提供 O(1) 的查找，避免排序带来的 O(n log n)。

## 复杂度总览

| 函数 | 交集定义 | 时间复杂度 | 额外空间复杂度 |
| --- | --- | --- | --- |
| `get_intersection_1` | 考虑重复次数 | O(n + m) | O(u + r) |
| `get_intersection_2` | 不考虑重复次数 | O(n + m) | O(u + v) |
| `get_intersection_3` | 不考虑重复次数 | O(n + m) | O(u + r) |

其中 `n`、`m` 是两个数组长度，`u`、`v` 是两个数组中的不同元素数量，`r` 是
结果中的不同元素数量。若把输出列表占用的空间也计入，空间复杂度还应加上结果大小。
"""

from collections import Counter


def get_intersection_1(nums1: list[int], nums2: list[int]) -> list[int]:
    """计算两个数组的多重集交集，并保留重复元素。

    步骤：
        1. 用 `Counter` 分别统计两个数组中每个数字的出现次数。
        2. 对两个频次表做 `&` 操作：每个数字保留两个计数中的较小值。
        3. 将频次结果展开为列表。

    图解：

    ```text
    nums1 = [1, 2, 2, 1]  -> {1: 2, 2: 2}
    nums2 = [2, 2]        -> {2: 2}
    Counter 交集 (&)      -> {2: 2}
    展开                   -> [2, 2]
    ```

    Args:
        nums1: 第一个整数数组。
        nums2: 第二个整数数组。

    Returns:
        多重集交集。每个数字出现的次数是它在两个数组中出现次数的较小值。
        返回顺序不作要求。

    Complexity:
        时间复杂度 O(n + m)，空间复杂度 O(u + r)，其中 `r` 为结果中的不同元素数。
    """
    counts1 = Counter(nums1)
    counts2 = Counter(nums2)

    # Counter 的 & 会对相同键取 min(counts1[x], counts2[x])。
    common_counts = counts1 & counts2
    return list(common_counts.elements())


def get_intersection_2(nums1: list[int], nums2: list[int]) -> list[int]:
    """使用集合运算计算去重后的数组交集。

    步骤：
        1. 将两个数组转换成集合，自动去除重复元素。
        2. 使用集合交集 `&` 找出同时存在于两个集合中的数字。
        3. 将集合转换为列表返回。

    图解：

    ```text
    set(nums1) = {1, 2}
    set(nums2) = {2}
    {1, 2} & {2} = {2}  -> 结果 [2]
    ```

    Args:
        nums1: 第一个整数数组。
        nums2: 第二个整数数组。

    Returns:
        去重后的交集列表，每个数字最多出现一次，顺序不作要求。

    Complexity:
        时间复杂度 O(n + m)，额外空间复杂度 O(u + v)。
    """
    set1 = set(nums1)
    set2 = set(nums2)

    # 集合交集天然去重，正好对应“不考虑出现次数”的题意。
    return list(set1 & set2)


def get_intersection_3(nums1: list[int], nums2: list[int]) -> list[int]:
    """使用一个集合和结果集合，逐个扫描得到去重后的数组交集。

    步骤：
        1. 将 `nums1` 放入集合，作为 O(1) 平均时间的查找表。
        2. 遍历 `nums2`，若当前数字在查找表中，就加入结果集合。
        3. 结果集合会自动去重，最后转换为列表。

    图解：

    ```text
    set1 = {1, 2}
    扫描 nums2 = [2, 2]：
      2 在 set1 -> res 加入 2
      2 在 set1 -> res 已有 2，不重复加入
    res = {2} -> [2]
    ```

    Args:
        nums1: 第一个整数数组。
        nums2: 第二个整数数组。

    Returns:
        去重后的交集列表，每个数字最多出现一次，顺序不作要求。

    Complexity:
        时间复杂度 O(n + m)，额外空间复杂度 O(u + r)。
    """
    values = set(nums1)
    common = set()

    for number in nums2:
        # 先判断是否属于 nums1，再加入集合以避免 nums2 中重复输出。
        if number in values:
            common.add(number)

    return list(common)


# 原文件 __main__ 示例曾调用过拼写错误的函数名，保留别名避免旧代码报错。
get_intsersection_1 = get_intersection_1


# 本文件只提供可复用的解法，不放置测试代码或运行时输出。

# 正确性证明
# ----------
# 对 get_intersection_1：Counter(nums1)[x] 和 Counter(nums2)[x] 分别是 x 在两个
# 数组中的出现次数。Counter 的交集为 min(count1, count2)，这正是 x 能在两个数组
# 中配对出现的最大次数；elements() 按该次数展开，因此结果恰好是多重集交集。
#
# 对 get_intersection_2：转换为集合后，每个数字只保留一次；集合交集恰好保留同时
# 出现在两个数组中的数字，因此结果正是去重交集。
#
# 对 get_intersection_3：每个被加入 common 的数字都先验证存在于 nums1 中，因此
# 结果不会包含无效数字；common 是集合，所以不会重复；nums2 中所有同时出现在
# nums1 的数字都会被扫描到并加入，因此结果既不多也不少。

# 易错点
# ------
# 1. 先确认题目是否要求保留重复次数：349 返回 [2]，350 返回 [2, 2]。
# 2. `set` 会丢失频次，不能用它直接解决“考虑重复次数”的交集。
# 3. 集合无序，不能依赖结果列表的排列顺序；若题目要求有序，需要额外排序。
# 4. `Counter.elements()` 返回迭代器，必须转成 `list` 才能得到题目要求的列表结果。
# 5. 哈希集合查找是平均 O(1)，理论最坏情况可能退化，但通常按平均复杂度分析。
