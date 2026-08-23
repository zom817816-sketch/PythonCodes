"""
无重复字符的最长子串（Longest Substring Without Repeating Characters）

题目描述：
给定一个字符串 s，请你找出其中不含有重复字符的最长子串的长度。
子串 是字符串中连续的字符序列。

输入描述：
一个字符串 s

输出描述：
不含重复字符的最长子串的长度

输入示例：
s = "abcabcbb"
输出示例：
3
解释：因为无重复字符的最长子串是 "abc"，所以其长度为 3。
注意 "bca" 和 "cab" 也是正确答案。

════════════════════════════════════════════════════════════════════════
核心概念：滑动窗口 + 哈希表去重
════════════════════════════════════════════════════════════════════════

核心思路：
    本题的本质是在字符串上维护一个"窗口"（左右指针之间），
    保证窗口内没有重复字符，记录窗口最大长度。

    暴力法的浪费：
    暴力法枚举所有起点 i，每个起点都用内层循环 j 从头扫到重复。
    问题在于：当 s[j] 重复时，暴力法直接 break，下一个 i 从 i+1 重新开始，
    但实际上新窗口的左边界只需跳到「重复字符上一次出现位置的下一个」即可，
    中间那些不可能成为最优解的起点不需要再枚举。

    滑动窗口优化原理：
    ┌───────────────────────────────────────────────────────────────┐
    │  暴力法: 对每个起点 i，向右扩展直到重复 → O(n²)              │
    │  滑动窗口: 左右指针只前进不回退 → 每个字符最多访问 2 次 → O(n)│
    │                                                               │
    │  关键洞察:                                                    │
    │  当 s[right] 在窗口内重复时，left 可以直接跳到                │
    │  「重复字符上次出现位置 + 1」，跳过无用的起点。               │
    └───────────────────────────────────────────────────────────────┘

    滑动窗口示意图：
    s = "a b c a b c b b"
         ↑           ↑
         left       right（发现 a 重复）

    left 直接跳到第一个 a 之后：
    s = "a b c a b c b b"
              ↑     ↑
             left  right
    窗口 = "a b c"，长度 3

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
暴力法（双层循环 + Set）        O(n²)           O(min(m,n))     ⭐⭐⭐
滑动窗口（Set + 逐个左移）     O(2n)           O(min(m,n))     ⭐⭐⭐
滑动窗口（HashMap 直接跳转）    O(n)            O(min(m,n))     ⭐⭐⭐⭐ 推荐
滑动窗口（数组优化 ASCII）      O(n)            O(128)          ⭐⭐⭐⭐
────────────────────────────────────────────────────────────────────────

其中 n 为字符串长度，m 为字符集大小。
对于 ASCII 字符集，m = 128；对于 Unicode，m 可能很大。

核心思想（滑动窗口 + HashMap）：
────────────────────────────────────────────────────────────────────────
维护窗口 [left, right]，用 HashMap 记录每个字符最近一次出现的下标。
当 s[right] 已在窗口内时，left 直接跳到「上次出现位置 + 1」，
无需像 Set 解法那样逐个左移。

状态定义：
    left  — 窗口左边界（含）
    right — 窗口右边界（含），即当前考察的字符
    char_index — HashMap，记录字符 → 最近出现的下标

初始条件：
    left = 0, result = 0, char_index = {}

最终答案：
    result = 窗口最大长度
"""


# ══════════════════════════════════════════════════════════
# 解法一：暴力法（双层循环 + Set）
# ══════════════════════════════════════════════════════════


def lengthOfLongestSubstring_brute(s: str) -> int:
    """
    暴力法 ⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    枚举每个起点 i，用 Set 记录已出现的字符，
    向右扩展直到遇到重复字符或到达末尾。

    算法步骤：
    1. 遍历每个起点 i
    2. 用 Set 从 i 向右扩展，遇到重复字符就 break
    3. 每次内层循环结束后，用当前长度更新 result

    时间复杂度：O(n²) — 两层循环
    空间复杂度：O(min(m,n)) — Set 最多存 min(m,n) 个字符

    图解示例：
    ────────────────────────────────────────────────────────
    s = "abcabcbb"

    i=0: [a] → [a,b] → [a,b,c] → 遇到 a 重复，break，length=3
    i=1: [b] → [b,c] → [b,c,a] → 遇到 b 重复，break，length=3
    i=2: [c] → [c,a] → [c,a,b] → 遇到 c 重复，break，length=3
    i=3: [a] → [a,b] → [a,b,c] → [a,b,c,b] 遇到 b 重复，length=3
    i=4: [b] → [b,c] → [b,c,b] 遇到 b 重复，break，length=2
    i=5: [c] → [c,b] → [c,b,b] 遇到 b 重复，length=2
    i=6: [b] → [b,b] 遇到 b 重复，length=1
    i=7: [b]，length=1

    result = max(3,3,3,3,2,2,1,1) = 3

    结果：3 ✓
    """
    n = len(s)
    result = 0                           # ✅ 初始化为 0，正确处理空串

    for i in range(n):
        length = 0                       # 当前子串长度
        seen = set()                     # 记录已出现的字符
        for j in range(i, n):
            if s[j] in seen:             # 遇到重复字符
                break
            seen.add(s[j])               # 添加到已见集合
            length += 1
        result = max(result, length)     # ✅ 移到循环外，无论是否 break 都更新

    return result


# ══════════════════════════════════════════════════════════
# 解法二：滑动窗口（Set + 逐个左移）
# ══════════════════════════════════════════════════════════


def lengthOfLongestSubstring_set(s: str) -> int:
    """
    滑动窗口（Set + 逐个左移）⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    用左右指针维护窗口，Set 记录窗口内的字符。
    right 向右扩展，遇到重复时 left 逐个右移直到窗口无重复。
    left 和 right 都只前进不回退，每个字符最多访问 2 次。

    与暴力法的区别：
    暴力法每次重复后从 i+1 重新开始扫描；
    滑动窗口法 left 只需右移到去掉重复字符即可，不从头扫描。

    算法步骤：
    1. left = 0, right = 0, Set = {}, result = 0
    2. right 向右扩展，如果 s[right] 不在 Set 中，加入并更新 result
    3. 如果 s[right] 在 Set 中，left 右移并从 Set 中移除 s[left]
    4. 重复 2-3 直到 right 到达末尾

    时间复杂度：O(2n) = O(n) — left 和 right 各最多遍历 n 次
    空间复杂度：O(min(m,n)) — Set 最多存 min(m,n) 个字符

    图解示例：
    ────────────────────────────────────────────────────────
    s = "abcabcbb"

    [a]bcabcbb    left=0, right=0  seen={a}      result=1
    [a b]cabcbb   left=0, right=1  seen={a,b}    result=2
    [a b c]abcbb  left=0, right=2  seen={a,b,c}   result=3
     a[b c a]bcbb  → a 重复！left 右移去掉旧 a
         left=1, right=3  seen={b,c,a}   result=3
         b[c a b]cbb  → b 重复！left 右移去掉旧 b
             left=2, right=4  seen={c,a,b}  result=3
         ...继续到末尾

    result = 3

    结果：3 ✓
    """
    result = 0
    seen = set()                         # 窗口内字符集合
    left = 0                             # 窗口左边界

    for right in range(len(s)):
        # 如果 s[right] 已在窗口内，左边界逐个右移直到无重复
        while s[right] in seen:
            seen.remove(s[left])         # 从窗口移除最左字符
            left += 1                    # 左边界右移
        seen.add(s[right])               # 将当前字符加入窗口
        result = max(result, right - left + 1)  # 更新最大长度

    return result


# ══════════════════════════════════════════════════════════
# 解法三：滑动窗口（HashMap 直接跳转）推荐
# ══════════════════════════════════════════════════════════


def lengthOfLongestSubstring(s: str) -> int:
    """
    滑动窗口（HashMap 直接跳转）⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    用 HashMap 记录每个字符最近一次出现的下标。
    当 s[right] 重复时，left 直接跳到「上次出现位置 + 1」，
    无需像 Set 解法那样逐个左移。

    与 Set 解法的区别：
    Set 解法遇到重复时，left 逐个右移（while 循环），O(2n)；
    HashMap 解法遇到重复时，left 直接跳转，O(n)，常数更优。

    关键洞察：
    - 只有当 s[right] 上次出现的位置 ≥ left 时，才算"窗口内重复"
    - 否则 s[right] 上次出现的位置在 left 之前，已在窗口外，不影响

    算法步骤：
    1. left = 0, char_index = {}, result = 0
    2. right 遍历字符串
    3. 如果 s[right] 在 char_index 中且其位置 ≥ left，left 跳到该位置+1
    4. 更新 char_index[s[right]] = right，更新 result

    时间复杂度：O(n) — right 只遍历一次，left 最多跳跃 n 次
    空间复杂度：O(min(m,n)) — HashMap 最多存 min(m,n) 个字符

    图解示例：
    ────────────────────────────────────────────────────────
    s = "abcabcbb"

    right=0, s[0]='a'  未见过  left=0  window="a"      result=1
    right=1, s[1]='b'  未见过  left=0  window="ab"     result=2
    right=2, s[2]='c'  未见过  left=0  window="abc"    result=3
    right=3, s[3]='a'  上次在0≥left → left=0+1=1  window="bca"  result=3
    right=4, s[4]='b'  上次在1≥left → left=1+1=2  window="cab"  result=3
    right=5, s[5]='c'  上次在2≥left → left=2+1=3  window="abc"  result=3
    right=6, s[6]='b'  上次在4≥left → left=4+1=5  window="cb"   result=3
    right=7, s[7]='b'  上次在6≥left → left=6+1=7  window="b"    result=3

    result = 3

    结果：3 ✓

    图解示例2（窗口外重复不影响）：
    ────────────────────────────────────────────────────────
    s = "tmmzuxt"

    right=0, s[0]='t'  未见过  left=0  window="t"       result=1
    right=1, s[1]='m'  未见过  left=0  window="tm"      result=2
    right=2, s[2]='m'  上次在1≥left → left=2  window="m"  result=2
    right=3, s[3]='z'  未见过  left=2  window="mz"       result=2
    right=4, s[4]='u'  未见过  left=2  window="mzu"      result=3
    right=5, s[5]='x'  未见过  left=2  window="mzux"     result=4
    right=6, s[6]='t'  上次在0，但 0 < left(2) → 不在窗口内
                         left 不变=2  window="mzuxt"    result=5

    result = 5 ✓
    （关键：t 的上次出现位置 0 在 left=2 之前，不影响当前窗口）
    """
    result = 0
    left = 0                                       # 窗口左边界
    char_index = {}                                # 字符 → 最近出现的下标

    for right, ch in enumerate(s):
        # 如果 ch 之前出现过，且上次出现位置在当前窗口内
        if ch in char_index and char_index[ch] >= left:
            left = char_index[ch] + 1              # left 直接跳到上次出现位置 + 1
        char_index[ch] = right                     # 更新 ch 的最新位置
        result = max(result, right - left + 1)    # 更新最大窗口长度

    return result


# ══════════════════════════════════════════════════════════
# 解法四：滑动窗口（数组优化 ASCII）
# ══════════════════════════════════════════════════════════


def lengthOfLongestSubstring_ascii(s: str) -> int:
    """
    滑动窗口（数组优化 ASCII）⭐⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    与 HashMap 解法逻辑完全相同，但用数组代替 HashMap。
    因为 ASCII 字符共 128 个，可以用长度 128 的数组存储每个字符最近出现的下标。
    数组查询比 HashMap 更快（O(1) 常数更小）。

    适用场景：
    - 字符集为 ASCII（0-127）
    - 如果字符是 Unicode，不适用（数组太大）

    算法步骤：
    1. 初始化长度 128 的数组，全部填 -1（表示未出现过）
    2. left = 0, right 遍历字符串
    3. 如果 s[right] 上次位置 ≥ left，left 跳转到该位置 + 1
    4. 更新数组中 s[right] 的位置为 right，更新 result

    时间复杂度：O(n) — 单次遍历
    空间复杂度：O(128) = O(1) — 固定大小数组

    图解示例：
    ────────────────────────────────────────────────────────
    s = "pwwkew"

    right=0, s[0]='p'(112) 上次=-1    left=0  window="p"     result=1
    right=1, s[1]='w'(119) 上次=-1    left=0  window="pw"    result=2
    right=2, s[2]='w'(119) 上次=1≥left → left=2  window="w"  result=2
    right=3, s[3]='k'(107) 上次=-1    left=2  window="wk"    result=2
    right=4, s[4]='e'(101) 上次=-1    left=2  window="wke"   result=3
    right=5, s[5]='w'(119) 上次=2≥left → left=3  window="kew"  result=3

    result = 3

    结果：3 ✓
    """
    result = 0
    left = 0
    # 初始化为 -1，表示每个字符尚未出现过
    char_index = [-1] * 128             # ASCII 字符集大小为 128

    for right, ch in enumerate(s):
        idx = ord(ch)                   # 字符 → ASCII 码（0-127）
        # 如果该字符上次出现位置在当前窗口内
        if char_index[idx] >= left:
            left = char_index[idx] + 1  # left 跳转到上次出现位置 + 1
        char_index[idx] = right         # 更新该字符的最新位置
        result = max(result, right - left + 1)

    return result


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 算法正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：滑动窗口（HashMap）法能正确找到无重复字符的最长子串长度。
#
# 证明：
# （1）窗口无重复性：每次 right 右移后，若 s[right] 在窗口内重复，
#     left 立即跳到「上次出现位置 + 1」，保证窗口内无重复字符。
# （2）窗口完备性：left 只前进不回退，right 遍历到每个字符，
#     所以每个可能的合法窗口都被考察过。
# （3）最优性：result 在每步取 max，记录了所有合法窗口的最大长度。
#
# 关键约束 char_index[ch] >= left 的正确性：
#   当 ch 上次出现位置 < left 时，说明它在窗口外（已被 left 跳过），
#   不影响当前窗口的无重复性，因此不需要移动 left。
#   只有 ch 上次出现位置 >= left（即在窗口内）时，才需要跳转。
#
#
# 四种解法对比：
# ────────────────────────────────────────────────────────
#
# 维度          暴力法          Set滑窗          HashMap滑窗      数组滑窗
# ────────────────────────────────────────────────────────────────
# 时间复杂度     O(n²)           O(2n)            O(n)             O(n)
# 空间复杂度     O(min(m,n))     O(min(m,n))      O(min(m,n))     O(128)=O(1)
# 左指针移动     重新扫描        逐个右移          直接跳转          直接跳转
# 字符集限制     无              无                无               ASCII
# 常数性能       差              一般              好               最好
# 推荐程度       ⭐⭐⭐          ⭐⭐⭐            ⭐⭐⭐⭐         ⭐⭐⭐⭐
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. ❌ result 初始化为 1
#    → ✅ result 应初始化为 0
#    当 s = "" 时，应为 0 而非 1；当 s = "abcd" 无重复时，
#    若 result=1 且 max 更新逻辑有误，可能返回错误结果。
#
# 2. ❌ result = max(result, length) 只放在 break 分支内
#    → ✅ 应放在内层循环外，无论是否 break 都执行
#    原因：如果子串一直无重复直到末尾（自然结束循环，没有 break），
#    length 不会被用来更新 result，导致遗漏。
#    例如 s = "abcd"，内层循环自然结束，length=4 但 result 仍为初始值。
#
# 3. ❌ HashMap 解法中不加 char_index[ch] >= left 条件
#    → ✅ 必须判断上次出现位置是否在当前窗口内
#    例如 s = "tmmzuxt"，最后的 't' 上次出现在位置 0，
#    但 left=2，位置 0 在窗口外，不影响当前窗口无重复性。
#    如果不加此条件，left 会被错误地跳回 1，导致窗口缩小。
# ══════════════════════════════════════════════════════════
