"""
给你一个字符串 s，请你将 s 分割成一些 子串，使每个子串都是 回文串 。返回 s 所有可能的分割方案。
输入: "aab"

切割过程（树形结构）：
                 "aab"
             /           \
       切"a"             切"aa"
        /    \              |
    剩余"ab"   ❌"aab"   剩余"b"
     /      \               |
  切"a"    切"ab"          切"b"
   /         ❌              |
 剩余"b"                  ["aa","b"] ✅
   |
  切"b"
["a","a","b"] ✅

解题思路详解

1️⃣ 问题本质：
   - 将一个字符串切割成若干段，每段都是回文串
   - 回文串：正着读和反着读一样，如 "a", "aa", "aba"
   - 返回所有可能的切割方案

2️⃣ 为什么用回溯？
   - 我们需要在所有可能的切割点中做出选择
   - 如果当前切割出的子串是回文，就继续切割剩余部分
   - 如果所有字符都切割完，就找到一个有效方案
   - 这本质上是在一个决策树中进行深度优先搜索

3️⃣ 回溯核心逻辑（类似"全排列"的变体）：

   backtrack(start, path):
       │
       ├── 终止条件：start == n → 保存 path，返回
       │
       └── 遍历所有可能的切割点 end (start+1 到 n)：
               │
               ├── 取子串 sub = s[start:end]
               │
               ├── 判断 sub 是否回文
               │   ├── 是 → path.append(sub)
               │   │         backtrack(end, path)  # 递归处理剩余
               │   │         path.pop()             # 撤销选择（回溯）
               │   └── 否 → 跳过，尝试下一个切割点
               │
               └── 继续尝试更长的子串

4️⃣ 关键理解：
   - 这里的"切割点"就是递归中的 start
   - 每次从 start 开始，尝试切出不同长度的子串（end不断增大）
   - 切割点从 start 跳到 end，表示切掉 s[start:end] 这段
   - path 保存的是已经切出来的回文子串

5️⃣ 对比回溯经典问题：
   - 全排列：选择元素 → 递归剩余元素 → 撤销选择
   - 组合总和：选择候选 → 递归剩余候选 → 撤销选择
   - 分割回文串：选择回文子串 → 递归剩余字符串 → 撤销选择
   - 本质模式完全相同，只是"选择"的内容不同！
"""

from typing import List

# 方法一：基础回溯法（直接判断回文）


def partition(s: str) -> List[List[str]]:
    """
    回溯法实现：分割回文串（基础版）⭐⭐

    ⏱ 时间复杂度：O(N * 2^N)
        - 每个字符间可以选择切或不切，共 2^(N-1) 种分割方案
        - 每个方案复制需要 O(N) 时间
        - 每次判断回文 O(N)，总最坏 O(N² * 2^N)

    💾 空间复杂度：O(N)
        - 递归栈深度 O(N)
        - path 存储最多 N 个元素

    回溯三原则：
    1. 函数功能：从 start 位置开始搜索所有回文分割方案
    2. 终止条件：start == n 时，找到一个完整方案，保存 path
    3. 递归关系：s[start:end] 是回文 → 递归处理 end 到末尾

    Args:
        s: 输入字符串

    Returns:
        所有回文分割方案列表
    """
    n = len(s)
    result = []

    # 辅助函数：判断回文

    def is_palindrome(sub: str) -> bool:
        """
        判断子串是否为回文串
        双指针法，从两端向中心比较
        """
        left, right = 0, len(sub) - 1
        while left < right:
            if sub[left] != sub[right]:
                return False
            left += 1
            right -= 1
        return True

    # 核心：回溯函数

    path: List[str] = []  # 👈 将 path 提取到外层，所有递归层共享此列表

    def backtrack(start: int) -> None:
        """
        回溯搜索函数

        Args:
            start: 当前要处理的起始索引（在 s 中的位置）
        """
        # 🟢 终止条件：已处理完所有字符
        if start == n:
            # 保存当前方案的副本（必须拷贝，因为 path 后续会变化）
            result.append(path[:])
            return

        # 🔵 遍历所有可能的切割点
        # end 表示切割的结束位置（不含），即 s[start:end]
        for end in range(start + 1, n + 1):
            # 取出子串
            sub = s[start:end]

            # 🟡 约束条件：子串必须是回文
            if is_palindrome(sub):
                # ① 做选择：将回文子串加入路径
                path.append(sub)

                # ② 递归：从 end 位置继续处理剩余字符串
                backtrack(end)

                # ③ 撤销选择：回溯，尝试下一个切割点
                path.pop()

            # ❌ 如果不是回文，直接跳过，尝试下一个 end

    # 从索引 0 开始，空路径
    backtrack(0)
    return result


# 方法二：回溯 + 回文判断优化（双指针索引版）


def partition_optimized(s: str) -> List[List[str]]:
    """
    回溯优化版：直接用索引判断回文，避免反复切片取子串⭐⭐⭐

    优化点：
    - 不在每次调用 is_palindrome 时创建新的子串
    - 直接在原字符串上用双指针判断

    ⏱ 时间复杂度：O(N * 2^N)
    💾 空间复杂度：O(N)

    Args:
        s: 输入字符串

    Returns:
        所有回文分割方案列表
    """
    n = len(s)
    result = []

    def is_palindrome(left: int, right: int) -> bool:
        """
        判断 s[left:right+1] 是否为回文串
        直接通过索引在原字符串上判断，避免创建子串
        """
        i, j = left, right
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    path: List[str] = []

    def backtrack(start: int) -> None:
        # 终止条件
        if start == n:
            result.append(path[:])
            return

        # 尝试不同的切割结束位置
        for end in range(start, n):
            # 直接用索引判断回文 s[start:end+1]
            if is_palindrome(start, end):
                # 这里才真正切片取子串，只取一次
                path.append(s[start : end + 1])
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result


# 方法三：回溯 + DP 预处理回文信息（最优方案）


def partition_with_dp(s: str) -> List[List[str]]:
    """
    回溯法 + 动态规划预处理回文信息 🚀

    核心优化：提前计算所有子串是否为回文，回溯时 O(1) 判断

    DP 推导过程：
    ┌─────────────────────────────────────────────┐
    │ 状态定义：dp[i][j] = s[i:j+1] 是否为回文    │
    │                                             │
    │ 状态转移：                                  │
    │   dp[i][i] = True          (单个字符)       │
    │   dp[i][i+1] = s[i]==s[i+1] (两个字符)      │
    │   dp[i][j] = s[i]==s[j] ∧ dp[i+1][j-1]      │
    │            (首尾相同且中间是回文)            │
    │                                             │
    │ 计算顺序：按子串长度从小到大                  │
    └─────────────────────────────────────────────┘

    ⏱ 时间复杂度：O(N * 2^N)
        - DP 预处理 O(N²)
        - 回溯部分 O(N * 2^N)
    💾 空间复杂度：O(N²) DP 表 + O(N) 递归栈

    回溯三原则：
    1. 函数功能：从 start 开始搜索所有回文分割方案
    2. 终止条件：start == n 时保存方案
    3. 递归关系：如果 dp[start][end] 为 True，递归处理 end+1

    Args:
        s: 输入字符串

    Returns:
        所有回文分割方案列表
    """
    n = len(s)
    if n == 0:
        return []

    # ========== 步骤1：DP 预处理 ==========

    # dp[i][j] 表示 s[i:j+1] 是否是回文串
    dp = [[False] * n for _ in range(n)]

    # 按子串长度从小到大计算（从 1 到 n）
    for length in range(1, n + 1):
        # i 是子串的起始位置
        for i in range(n - length + 1):
            j = i + length - 1  # j 是子串的结束位置

            if length == 1:
                # 长度为 1：单个字符一定是回文
                dp[i][j] = True

            elif length == 2:
                # 长度为 2：两个字符相等才是回文
                dp[i][j] = s[i] == s[j]

            else:
                # 长度 >= 3：首尾相等 且 中间子串是回文
                dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]

    # ========== 步骤2：回溯搜索 ==========

    result = []

    path: List[str] = []

    def backtrack(start: int) -> None:
        """
        回溯搜索
        利用 dp 表 O(1) 判断回文，无需重复计算

        Args:
            start: 当前起始位置
        """
        # 终止条件
        if start == n:
            result.append(path[:])
            return

        # 尝试所有可能的结束位置
        for end in range(start, n):
            # O(1) 查询 s[start:end+1] 是否为回文
            if dp[start][end]:
                path.append(s[start : end + 1])
                backtrack(end + 1)
                path.pop()

    backtrack(0)
    return result


# 方法四：回溯 + 记忆化搜索


def partition_with_memo(s: str) -> List[List[str]]:
    """
    回溯法 + 记忆化搜索

    思想：缓存 s[i:] 的所有分割方案，避免重复计算
    适用于有大量重复子问题的场景（如 "aaaa..."）

    与 DP 版区别：
    - DP 版：缓存"子串是否为回文"的判断结果
    - 记忆化版：缓存"子串的所有分割方案"

    ⏱ 时间复杂度：O(N * 2^N)
    💾 空间复杂度：O(N * 2^N) 缓存所有子串的方案

    递归三原则：
    1. 函数功能：返回 s[start:] 的所有回文分割方案
    2. 终止条件：start == n 时，返回 [[]]（空方案）
    3. 递归关系：s[start:end+1] 是回文 → 与 s[end+1:] 的方案组合

    Args:
        s: 输入字符串

    Returns:
        所有回文分割方案列表
    """
    n = len(s)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def is_palindrome(left: int, right: int) -> bool:
        """判断 s[left:right+1] 是否为回文（带缓存）"""
        i, j = left, right
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    @lru_cache(maxsize=None)
    def dfs(start: int):
        """
        返回 s[start:] 的所有回文分割方案

        Args:
            start: 起始索引

        Returns:
            s[start:] 的所有分割方案列表
        """
        # 终止条件：空字符串，只有一种方案（不分割）
        if start == n:
            return [[]]

        result = []
        # 尝试不同长度的回文子串
        for end in range(start, n):
            if is_palindrome(start, end):
                # 取出回文子串
                sub = s[start : end + 1]

                # 递归获取剩余部分的所有方案
                rest_partitions = dfs(end + 1)

                # 将当前子串与每个剩余方案组合
                for rest in rest_partitions:
                    result.append([sub] + rest)

        return result

    return dfs(0)


# 方法五：迭代回溯法（使用栈）


def partition_iterative(s: str) -> List[List[str]]:
    """
    迭代回溯法：用栈模拟递归过程

    适用场景：
    - 当递归深度可能很大时（如超长字符串）
    - 避免递归调用栈溢出

    栈元素设计：(start, path)
    - start: 当前要处理的起始索引
    - path: 从根节点到当前位置的路径

    ⏱ 时间复杂度：O(N * 2^N)
    💾 空间复杂度：O(N * 2^N)

    Args:
        s: 输入字符串

    Returns:
        所有回文分割方案列表
    """
    n = len(s)

    # 预计算回文信息（用 DP 表）
    dp = [[False] * n for _ in range(n)]
    for length in range(1, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            if length == 1:
                dp[i][j] = True
            elif length == 2:
                dp[i][j] = s[i] == s[j]
            else:
                dp[i][j] = (s[i] == s[j]) and dp[i + 1][j - 1]

    result = []

    # 栈元素：(start, path, index_in_children)
    # index_in_children 表示当前处理到哪个子节点
    # -1 表示刚入栈，还未开始处理子节点
    stack = [(0, [], -1)]

    while stack:
        start, path, idx = stack.pop()

        if start == n:
            # 🟢 找到一个完整方案
            result.append(path[:])
            continue

        # 获取下一个需要处理的切割点
        next_idx = -1
        for end in range(start, n):
            if dp[start][end]:
                if idx == -1:
                    # 刚入栈，处理第一个有效切割点
                    idx = end
                    next_idx = end
                    break
                elif end > idx:
                    # 已经处理过 idx 了，下一个需要处理的是 end
                    next_idx = end
                    break

        if next_idx != -1:
            # 将当前节点重新入栈（带着更新后的 idx）
            stack.append((start, path, next_idx))

            # 做选择：将回文子串加入路径
            new_path = path + [s[start : next_idx + 1]]

            # 递归处理剩余部分（入栈）
            stack.append((next_idx + 1, new_path, -1))

    return result
