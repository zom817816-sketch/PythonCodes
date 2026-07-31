"""
# 383. 赎金信（Ransom Note）

## 题目描述

给定两个字符串 `ransomNote` 和 `magazine`，判断 `ransomNote` 是否可以由
`magazine` 中的字符拼出：

- `magazine` 中的每个字符最多只能使用一次；
- 字符的大小写和出现次数都要匹配；
- 如果可以拼出，返回 `True`，否则返回 `False`。

例如：

    ransomNote = "a", magazine = "ab"  -> True
    ransomNote = "aa", magazine = "ab" -> False

本文件保留三种等价实现，分别展示数组、`Counter` 和普通字典的用法：

- `can_construct_1`：适用于题目限定为 26 个小写英文字母的场景；
- `can_construct_2`：使用标准库 `collections.Counter`，代码最简洁；
- `can_construct_3`：使用普通字典，适合字符集不受限的场景。

## 解法总览

问题本质是比较两个字符串中每个字符的频次：

    ransomNote 中某字符的需求次数 <= magazine 中该字符的供应次数

只要有一个字符的需求超过供应，答案就是 `False`；如果所有字符都满足，答案就是
`True`。

### 解法一：固定大小数组

题目通常限定字符串只包含 26 个小写英文字母。可以将字符映射到下标：

    'a' -> 0, 'b' -> 1, ..., 'z' -> 25

先统计杂志中每个字符的数量，再逐个消耗赎金信所需字符。

图解：

    magazine = "aabbc"  -> [a:2, b:2, c:1, ...]
    ransomNote = "abc"

    读取 'a'：a 剩 1
    读取 'b'：b 剩 1
    读取 'c'：c 剩 0
    所有字符都能取出，因此返回 True

### 解法二：Counter 差集

`Counter(ransomNote) - Counter(magazine)` 会保留“需求仍未被满足”的字符及其数量。
如果差集为空，说明杂志足够；否则说明至少有一种字符不够。

### 解法三：普通字典

用字典动态记录杂志中出现的字符数量，并在扫描赎金信时逐个减少库存。
这种写法不依赖字符必须是小写英文字母。

## 正确性证明

以“库存”算法为例。扫描 `ransomNote` 前，库存记录了 `magazine` 中每个字符的
准确出现次数。

对赎金信中的任意字符 `ch`：

1. 如果库存中 `ch` 的数量为 0，说明杂志中没有未使用的 `ch`，当前字符无法构成，
   算法返回 `False`，且返回值正确。
2. 如果库存中 `ch` 的数量大于 0，算法消耗一个 `ch`。这与每个杂志字符只能使用
   一次的规则一致，并保持库存仍表示“剩余可用字符数”。

若整个赎金信扫描完仍未失败，则每个需求字符都成功消耗了一个库存字符，因此存在
一种合法拼法，算法返回 `True` 正确。

`can_construct_1`、`can_construct_2` 和 `can_construct_3` 都是在实现同一个频次判断，
所以三者的返回结果一致。

## 复杂度分析

令 `m = len(ransomNote)`，`n = len(magazine)`，`k` 为实际涉及的不同字符数：

- `can_construct_1`：时间 `O(m + n)`，空间 `O(1)`，因为数组固定为 26 个元素。
- `can_construct_2`：时间平均为 `O(m + n)`，空间 `O(k)`。
- `can_construct_3`：时间平均为 `O(m + n)`，空间 `O(k)`。

如果字符集固定为 26 个小写字母，`O(k)` 也可视为 `O(1)`；这里保留 `k` 是为了
准确描述通用字符集版本。

## 易错点

1. **重复字符必须重复计数**：`"aa"` 不能由只有一个 `a` 的杂志构成。
2. **不能只比较字符集合**：集合忽略出现次数，无法解决本题。
3. **字符只能使用一次**：检查到一个字符后必须减少库存。
4. **数组映射有前提**：`can_construct_1` 只适用于 `'a'` 到 `'z'`；如果输入可能
   包含大写字母、数字或其他 Unicode 字符，应使用 `can_construct_2` 或 `can_construct_3`。
5. **先统计谁都可以，但逻辑要一致**：本文件先统计 `magazine`，再消耗
   `ransomNote`，更直观地体现“供应与需求”的关系。
"""


def can_construct_1(ransomNote: str, magazine: str) -> bool:
    """使用长度为 26 的数组判断赎金信能否由杂志构成。

    适用前提：输入只包含小写英文字母 `a` 到 `z`。
    """
    magazine_counter = [0] * 26

    # 先建立杂志的字符库存。
    for char in magazine:
        magazine_counter[ord(char) - ord("a")] += 1

    # 逐个消耗库存；库存不足时可以立即确定失败。
    for char in ransomNote:
        index = ord(char) - ord("a")
        if magazine_counter[index] == 0:
            return False
        magazine_counter[index] -= 1

    return True


def can_construct_2(ransomNote: str, magazine: str) -> bool:
    """使用 `collections.Counter` 比较两个字符串的字符需求与供应。"""
    from collections import Counter

    required = Counter(ransomNote)
    available = Counter(magazine)

    # Counter 的减法会丢弃非正数，结果为空表示没有未满足的需求。
    return not (required - available)


def can_construct_3(ransomNote: str, magazine: str) -> bool:
    """使用普通字典判断赎金信能否由杂志构成，字符集不受限。"""
    magazine_counter = {}

    # 动态统计杂志中的字符，不要求字符属于固定范围。
    for char in magazine:
        magazine_counter[char] = magazine_counter.get(char, 0) + 1

    # 读取需求并减少库存。
    for char in ransomNote:
        if magazine_counter.get(char, 0) == 0:
            return False
        magazine_counter[char] -= 1

    return True
