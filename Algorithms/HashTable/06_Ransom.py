"""
383. 赎金信（Ransom Note）

题目描述：
给你两个字符串 ransomNote 和 magazine，判断 ransomNote 能不能由 magazine
里面的字符构成。magazine 中的每个字符只能在 ransomNote 中使用一次。

输入描述：
两个字符串 ransomNote 和 magazine。
1 <= ransomNote.length, magazine.length <= 10^5，
ransomNote 和 magazine 由小写英文字母组成。

输出描述：
如果可以构成返回 True，否则返回 False。

输入示例 1：
ransomNote = "a", magazine = "b"
输出示例 1：
False

输入示例 2：
ransomNote = "aa", magazine = "ab"
输出示例 2：
False

输入示例 3：
ransomNote = "aa", magazine = "aab"
输出示例 3：
True

════════════════════════════════════════════════════════════════════════
核心概念：频次比较 — 供应与需求
════════════════════════════════════════════════════════════════════════

赎金信问题本质：magazine 的字符频次表能否"覆盖" ransomNote 的频次表。
    对每个字符 ch：magazine 中 ch 的数量 >= ransomNote 中 ch 的数量

    magazine = "aabbc" → {a:2, b:2, c:1}
    ransomNote = "abc"  → {a:1, b:1, c:1}
    每个字符供应 >= 需求 → True

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
26 位数组                      O(m+n)          O(1)            ⭐⭐⭐⭐⭐ 推荐
Counter 差集                  O(m+n)          O(k)            ⭐⭐⭐⭐ 代码简洁
字典频次法                    O(m+n)          O(k)            ⭐⭐⭐ 通用字符集
────────────────────────────────────────────────────────────────────────

核心思想（数组法）：
────────────────────────────────────────────────────────────────────────
先统计 magazine 的字符库存（数组计数），再遍历 ransomNote 逐个消耗库存。
库存不足时立即返回 False。
"""


from collections import Counter


# ══════════════════════════════════════════════════════════
# 解法一：26 位数组 ⭐⭐⭐⭐⭐ 推荐
# ══════════════════════════════════════════════════════════


def canConstruct(ransomNote: str, magazine: str) -> bool:
    """26 位数组 ⭐⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    用长度 26 的数组统计 magazine 的字符库存。
    遍历 ransomNote 逐个消耗库存，库存不足返回 False。

    算法步骤：
    1. counts[26] 统计 magazine 中每个字符的出现次数。
    2. 遍历 ransomNote 的每个字符：
       a. 对应计数为 0 → 库存不足，返回 False。
       b. 否则计数减一。
    3. 全部消耗完返回 True。

    时间复杂度：O(m+n) — 遍历两个字符串。
    空间复杂度：O(1) — 固定 26 个元素。

    图解示例：
    ────────────────────────────────────────────────────────
    magazine = "aabbc" → counts = [a:2, b:2, c:1, ...]
    ransomNote = "abc"

    读 'a': counts[a]=2>0 → counts[a]=1
    读 'b': counts[b]=2>0 → counts[b]=1
    读 'c': counts[c]=1>0 → counts[c]=0
    全部成功 → True ✓

    ransomNote = "aa", magazine = "ab"
    读 'a': counts[a]=1>0 → counts[a]=0
    读 'a': counts[a]=0 → 库存不足 → False ✓
    """
    counts = [0] * 26

    # 统计 magazine 的字符库存
    for ch in magazine:
        counts[ord(ch) - ord("a")] += 1

    # 遍历 ransomNote 逐个消耗库存
    for ch in ransomNote:
        idx = ord(ch) - ord("a")
        if counts[idx] == 0:
            return False  # 库存不足
        counts[idx] -= 1

    return True


# ══════════════════════════════════════════════════════════
# 解法二：Counter 差集 ⭐⭐⭐⭐
# ══════════════════════════════════════════════════════════


def canConstruct_counter(ransomNote: str, magazine: str) -> bool:
    """Counter 差集 ⭐⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    Counter(ransomNote) - Counter(magazine) 保留"需求仍未满足"的字符。
    差集为空说明 magazine 能覆盖 ransomNote 的所有需求。

    算法步骤：
    1. required = Counter(ransomNote)。
    2. available = Counter(magazine)。
    3. 返回 not (required - available)。

    时间复杂度：O(m+n) — 构建两个 Counter。
    空间复杂度：O(k) — k 为不同字符数。

    图解示例：
    ────────────────────────────────────────────────────────
    ransomNote = "aa" → required = {a: 2}
    magazine = "aab"  → available = {a: 2, b: 1}
    required - available = {} (a: 2-2=0, 被丢弃)
    not {} → True ✓

    ransomNote = "aa" → required = {a: 2}
    magazine = "ab"   → available = {a: 1, b: 1}
    required - available = {a: 1} (a: 2-1=1, 保留)
    not {a: 1} → False ✓
    """
    required = Counter(ransomNote)
    available = Counter(magazine)
    # Counter 减法丢弃非正数，差集为空说明所有需求都被满足
    return not (required - available)


# ══════════════════════════════════════════════════════════
# 解法三：字典频次法 ⭐⭐⭐
# ══════════════════════════════════════════════════════════


def canConstruct_dict(ransomNote: str, magazine: str) -> bool:
    """字典频次法 ⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    用普通字典统计 magazine 的字符库存，不依赖字符集范围。
    适用于任意可哈希字符（Unicode、大写字母、数字等）。

    算法步骤：
    1. 用字典 counts 统计 magazine 的字符频次。
    2. 遍历 ransomNote，逐个消耗库存。

    时间复杂度：O(m+n)。
    空间复杂度：O(k) — k 为不同字符数。
    """
    counts: dict[str, int] = {}
    for ch in magazine:
        counts[ch] = counts.get(ch, 0) + 1

    for ch in ransomNote:
        if counts.get(ch, 0) == 0:
            return False
        counts[ch] -= 1

    return True


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 一、数组法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：数组法返回 True 当且仅当 magazine 能构成 ransomNote。
#
# 证明：
# （1）counts 初始记录了 magazine 中每个字符的准确出现次数。
# （2）遍历 ransomNote 时，每次消耗一个库存字符。
#     - 库存 > 0：消耗一个，库存仍表示"剩余可用字符数"。
#     - 库存 = 0：该字符不够用，返回 False 正确。
# （3）全部遍历完未失败，说明每个需求字符都有对应的库存字符，
#     返回 True 正确。
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. 用集合比较：
#    set(ransomNote) <= set(magazine) 只检查字符是否存在，
#    不检查次数。如 "aa" 和 "ab" 集合都是 {'a','b'} 的子集，但实际不够。
#
# 2. 忘记减一：
#    只检查 counts[idx] > 0 但不减一，会导致同一字符被重复使用。
#
# 3. 数组法用于非小写字母：
#    ord(ch) - ord('a') 对大写字母或 Unicode 字符会越界。
#    应使用字典法或 Counter 法。
#
# 4. Counter 减法的语义：
#    Counter 的减法会丢弃结果 <= 0 的键。
#    required - available 为空 = 所有需求被满足。
#    但 available - required 为空 ≠ magazine 能构成 ransomNote
#    （这只说明 magazine 没有多余字符）。
# ══════════════════════════════════════════════════════════
