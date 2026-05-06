"""
有效 IP 地址 正好由四个整数（每个整数位于 0 到 255 之间组成，且不能含有前导 0），整数之间用 '.' 分隔。
例如："0.1.2.201" 和 "192.168.1.1" 是 有效 IP 地址，但是 "0.011.255.245"、"192.168.1.312" 和 "192.168@1.1" 是 无效 IP 地址。
给定一个只包含数字的字符串 s ，用以表示一个 IP 地址，返回所有可能的有效 IP 地址，这些地址可以通过在 s 中插入 '.' 来形成。
你 不能 重新排序或删除 s 中的任何数字。你可以按 任何 顺序返回答案。
🧠 解题思路详解：
1️⃣ 问题本质：
   - 将数字字符串分割成 4 段，每段都是一个合法的 IP 地址段
   - 本质是"切割问题"，与"分割回文串"是同类问题
   - 不同点：固定切 4 段，且每段有合法性约束

2️⃣ 合法 IP 段的三个条件：
   (1) 长度在 1~3 之间（因为最大 255 是三位数）
   (2) 不能有前导零（如 "01"、"012" 非法，"0" 合法）
   (3) 数值在 0~255 之间

3️⃣ 回溯分析：
   - 做选择：从 start 切出子串 s[start:end]
   - 约束条件：子串是合法 IP 段
   - 目标条件：切出 4 段 且 用完所有字符
   - 剪枝提前终止：
     a) 剩余字符 > 剩余段数 * 3（每段最多 3 位）
     b) 剩余字符 < 剩余段数 * 1（每段至少 1 位）
     c) 已选段数 > 4

4️⃣ 与"分割回文串"的对比：
   ┌──────────────────────┬─────────────────────────┐
   │    分割回文串        │      恢复 IP 地址        │
   ├──────────────────────┼─────────────────────────┤
   │ 不固定段数           │ 固定 4 段               │
   │ 约束：子串是回文     │ 约束：数字在 0~255     │
   │ 终止：start == n     │ 终止：段数==4 且字符用完  │
   │ 剪枝：无固定规则     │ 剪枝：长度范围限制      │
   └──────────────────────┴─────────────────────────┘

5️⃣ 回溯树结构（"25525511135"）：
```
                     "25525511135" (start=0, segments=0)
                   /        |         \
              切"2"      切"25"      切"255"
               /            |            \
          剩余...        剩余...       剩余...
          segments=1     segments=1    segments=1
```

6️⃣ 重要优化：在 for 循环中限制 end 的范围
   - 每段最多 3 位数字：end <= start + 3
   - 每段至少 1 位数字：end >= start + 1
   - 避免无意义的遍历
"""

from typing import List

# 方法一：基础回溯法（清晰易懂版）


def restoreIpAddresses(s: str) -> List[str]:
    """
    回溯法实现：恢复 IP 地址⭐⭐⭐

    ⏱ 时间复杂度：O(3^4) = O(81) ≈ O(1)
        - 每层最多 3 种选择（1位、2位、3位）
        - 固定 4 层，所以是常数时间
        - 但字符串越长，无效分支越多，实际约为 O(3^4 * n)

    💾 空间复杂度：O(1)
        - 递归深度固定为 4
        - path 固定存储 4 个段

    回溯三原则：
    1. 函数功能：从 start 位置开始，选择 IP 地址的第 len(path)+1 段
    2. 终止条件：已选 4 段且用完所有字符，或剩余字符无法构成合法 IP
    3. 递归关系：选择合法子串 → 递归选择下一段 → 撤销选择

    Args:
        s: 只包含数字的字符串

    Returns:
        所有可能的有效 IP 地址列表
    """
    res = []
    path = []  # 👈 存储当前已选的 IP 段，如 ["192", "168", "1", "1"]
    n = len(s)

    # ---------- 辅助函数：判断 IP 段是否合法 ----------

    def is_valid_segment(sub: str) -> bool:
        """
        判断子串是否为合法的 IP 地址段

        IP 段合法条件：
        1. 长度在 1~3 之间
        2. 没有前导零（长度为 1 时可以是 "0"）
        3. 数值在 0~255 之间

        Args:
            sub: 待判断的子串

        Returns:
            是否合法
        """
        # 条件①：长度范围（理论上不会超过 3，因为循环限制了）
        if len(sub) > 3:
            return False

        # 条件②：前导零检测
        # "0" 合法，"00"、"01"、"012" 不合法
        if len(sub) > 1 and sub[0] == "0":
            return False

        # 条件③：数值范围
        return 0 <= int(sub) <= 255

    # ---------- 核心：回溯函数 ----------

    def backtrack(start: int) -> None:
        """
        回溯搜索函数

        Args:
            start: 当前要处理的起始索引
        """
        # ========== 🟢 剪枝①：剩余字符不够或太多 ==========
        remaining = n - start  # 剩余未处理的字符数
        segments_left = 4 - len(path)  # 还需要选几个段

        # 如果剩余字符 < 需要的最少字符数（每段至少 1 位）
        if remaining < segments_left:
            return
        # 如果剩余字符 > 需要的最大字符数（每段最多 3 位）
        if remaining > segments_left * 3:
            return

        # ========== 🟢 终止条件 ==========
        # 选了 4 段且刚好用完所有字符
        if len(path) == 4:
            if start == n:
                res.append(".".join(path))
            return

        # ========== 🔵 遍历选择 ==========
        # 每段最多 3 位，所以 end 最多到 start + 3
        # 同时 end 不能超过字符串长度
        for end in range(start + 1, min(start + 4, n + 1)):
            sub = s[start:end]

            # 🟡 约束条件：子串必须是合法 IP 段
            if is_valid_segment(sub):
                # ① 做选择
                path.append(sub)

                # ② 递归：选择下一段
                backtrack(end)

                # ③ 撤销选择（回溯）
                path.pop()

            # ❌ 非法则跳过，尝试更长的子串

    backtrack(0)
    return res


# 方法二：剪枝优化版（提前终止 + 段数限制）


def restoreIpAddresses_pruned(s: str) -> List[str]:
    """
    回溯法 + 强剪枝优化版⭐⭐

    相比基础版的改进：
    1. 在进入递归前就检查剩余字符长度范围，提前剪枝
    2. 显式控制每段长度在 1~3 位
    3. 提前终止：一旦选了 4 段但还没处理完，立即返回

    ⏱ 时间复杂度：O(3^4) = O(1)
    💾 空间复杂度：O(1)

    Args:
        s: 只包含数字的字符串

    Returns:
        所有可能的有效 IP 地址列表
    """
    n = len(s)
    # 总长度必须在 4~12 之间（4 段，每段 1~3 位）
    if n < 4 or n > 12:
        return []

    res = []
    path = []

    def is_valid(sub: str) -> bool:
        """判断是否为合法 IP 段"""
        if len(sub) > 1 and sub[0] == "0":
            return False
        return 0 <= int(sub) <= 255

    def backtrack(start: int) -> None:
        # ===== 🟢 剪枝：剩余字符必须满足长度要求 =====
        remaining = n - start
        segments_left = 4 - len(path)

        # 剩余字符不够每段至少 1 位，或太多每段最多 3 位
        if remaining < segments_left or remaining > segments_left * 3:
            return

        # ===== 🟢 终止条件 =====
        if start == n and len(path) == 4:
            res.append(".".join(path))
            return

        # ===== 🔵 最多尝试 3 位（start+1, start+2, start+3） =====
        for end in range(start + 1, min(start + 4, n + 1)):
            sub = s[start:end]

            if is_valid(sub):
                path.append(sub)
                backtrack(end)
                path.pop()

    backtrack(0)
    return res


# 方法三：显式迭代版（4 层循环，无递归）


def restoreIpAddresses_iterative(s: str) -> List[str]:
    """
    显式迭代法：4 层循环枚举所有可能的 IP 段拆分⭐⭐

    思想：
    - IP 地址固定 4 段，用 3 个点分割
    - 枚举 3 个切割点的位置（即每段的长度）
    - 用 3 层循环确定 4 段的起止位置
    - 检查每段是否合法

    ⏱ 时间复杂度：O(3³) = O(1)
        - 每段长度 1~3，共 3 种可能
        - 4 段共 3³ = 27 种拆分方式（最后一个由前面的决定）

    💾 空间复杂度：O(1)

    优点：不需要递归，实现直观，容易理解
    缺点：扩展性差（只对固定 4 段有效）

    Args:
        s: 只包含数字的字符串

    Returns:
        所有可能的有效 IP 地址列表
    """
    n = len(s)
    # 总长度必须在 4~12 之间
    if n < 4 or n > 12:
        return []

    res = []

    def is_valid(sub: str) -> bool:
        """判断是否为合法 IP 段"""
        if len(sub) > 1 and sub[0] == "0":
            return False
        return 0 <= int(sub) <= 255

    # 枚举第 1 段的长度（1~3 位）
    for len1 in range(1, 4):
        end1 = len1
        if end1 >= n:
            break
        seg1 = s[:end1]
        if not is_valid(seg1):
            continue

        # 枚举第 2 段的长度（1~3 位）
        for len2 in range(1, 4):
            end2 = end1 + len2
            if end2 >= n:
                break
            seg2 = s[end1:end2]
            if not is_valid(seg2):
                continue

            # 枚举第 3 段的长度（1~3 位）
            for len3 in range(1, 4):
                end3 = end2 + len3
                if end3 >= n:
                    break
                seg3 = s[end2:end3]
                if not is_valid(seg3):
                    continue

                # 第 4 段：剩余所有字符
                seg4 = s[end3:]
                if not is_valid(seg4):
                    continue

                # 所有段都合法，构建 IP 地址
                ip = f"{seg1}.{seg2}.{seg3}.{seg4}"
                res.append(ip)

    return res


# 方法四：带字符串构建的"原地"回溯（不存 path，直接构建字符串）


def restoreIpAddresses_inplace(s: str) -> List[str]:
    """
    原地回溯法：直接在原字符串上加点，不额外存储 path⭐

    思想：
    - 使用当前构建的 IP 字符串而不是 path 列表
    - 每选一个合法段，直接追加到字符串末尾
    - 递归返回后，删除追加的部分（回溯）

    优缺点：
    + 内存占用更少（不需要 path 列表）
    - 字符串拼接操作 O(n)，不如列表 join 高效

    ⏱ 时间复杂度：O(3⁴ * n) ≈ O(n)
    💾 空间复杂度：O(1)

    回溯三原则：
    1. 函数功能：在 IP 字符串后追加下一个合法段
    2. 终止条件：4 段且字符用完
    3. 递归关系：追加合法段 → 递归 → 删除追加的段

    Args:
        s: 只包含数字的字符串

    Returns:
        所有可能的有效 IP 地址列表
    """
    n = len(s)
    if n < 4 or n > 12:
        return []

    res = []

    def is_valid(sub: str) -> bool:
        if len(sub) > 1 and sub[0] == "0":
            return False
        return 0 <= int(sub) <= 255

    def backtrack(start: int, segments: int, ip_so_far: str) -> None:
        """
        Args:
            start: 当前起始索引
            segments: 已选段数
            ip_so_far: 当前已构建的 IP 字符串
        """
        # 剪枝：剩余字符长度范围检查
        remaining = n - start
        segments_left = 4 - segments
        if remaining < segments_left or remaining > segments_left * 3:
            return

        # 终止条件
        if segments == 4:
            if start == n:
                # 去掉末尾的 "."
                res.append(ip_so_far[:-1])
            return

        for end in range(start + 1, min(start + 4, n + 1)):
            sub = s[start:end]

            if is_valid(sub):
                # 做选择：追加到 IP 字符串
                backtrack(end, segments + 1, ip_so_far + sub + ".")

    backtrack(0, 0, "")
    return res


# 方法五：优化版 - 提前生成所有可能的段组合


def restoreIpAddresses_fast(s: str) -> List[str]:
    """
    高效版：利用 Python 特性 + 精确剪枝⭐⭐⭐

    优化点：
    1. 遍历范围精确控制：每段长度由剩余字符数动态决定
    2. 使用列表推导式提高可读性
    3. 三重循环+过滤的模式，适合 IP 地址这种固定结构

    ⏱ 时间复杂度：O(1)
    💾 空间复杂度：O(1)

    Args:
        s: 只包含数字的字符串

    Returns:
        所有可能的有效 IP 地址列表
    """
    n = len(s)
    if n < 4 or n > 12:
        return []

    def is_valid(sub: str) -> bool:
        """判断 IP 段是否合法"""
        # 前导零检测 + 数值范围
        if len(sub) > 1 and sub[0] == "0":
            return False
        num = int(sub)
        return 0 <= num <= 255

    res = []

    # 第 1 段：起始位置 0，长度 1~3
    # 但必须保证后面 3 段有足够的字符空间
    # 后面 3 段最少 3 个字符（每段 1 位），最多 9 个字符（每段 3 位）
    for i in range(1, 4):
        if n - i < 3:  # 剩余字符不够 3 段各 1 位
            break
        if n - i > 9:  # 剩余字符太多，当前段太短
            continue
        seg1 = s[:i]
        if not is_valid(seg1):
            continue

        # 第 2 段：起始位置 i，长度 1~3
        for j in range(i + 1, min(i + 4, n)):
            if n - j < 2:  # 剩余字符不够 2 段各 1 位
                break
            if n - j > 6:  # 剩余字符太多
                continue
            seg2 = s[i:j]
            if not is_valid(seg2):
                continue

            # 第 3 段：起始位置 j，长度 1~3
            for k in range(j + 1, min(j + 4, n)):
                if n - k < 1:  # 剩余字符不够 1 段
                    break
                if n - k > 3:  # 第 4 段最多 3 位
                    continue
                seg3 = s[j:k]
                if not is_valid(seg3):
                    continue

                # 第 4 段：起始位置 k 到末尾
                seg4 = s[k:]
                if not is_valid(seg4):
                    continue

                res.append(f"{seg1}.{seg2}.{seg3}.{seg4}")

    return res
