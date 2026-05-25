"""
跳跃游戏 IV（Jump Game IV）

题目描述：
给你一个整数数组 arr，你一开始在数组的第一个元素处（下标为 0）。
每一步，你可以从下标 i 跳到下标 i + 1、i - 1 或者 j：
    - i + 1 需满足：i + 1 < arr.length
    - i - 1 需满足：i - 1 >= 0
    - j 需满足：arr[i] == arr[j] 且 i != j
请你返回到达数组最后一个元素的下标处所需的 最少操作次数。
注意：任何时候你都不能跳到数组外面。

示例 1：
    输入：arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
    输出：3
    解释：需要跳跃 3 次，下标依次为 0 --> 4 --> 3 --> 9。
          下标 9 为数组的最后一个元素的下标。

示例 2：
    输入：arr = [7]
    输出：0
    解释：一开始就在最后一个元素处，不需要跳跃。

示例 3：
    输入：arr = [7, 6, 9, 6, 9, 6, 9, 7]
    输出：1
    解释：可以直接从下标 0 跳到下标 7（arr[0] == arr[7] == 7）。

解题思路总览：
───────────────────────────────────────────────────────────────────────
解法                      时间复杂度    空间复杂度    说明
───────────────────────────────────────────────────────────────────────
BFS + 同值分组（队列）       O(n)          O(n)       ⭐ 最优解
BFS + 同值分组（逐层处理）   O(n)          O(n)       显式分层，更易理解
双向 BFS                    O(n)          O(n)       两端交替搜索，实际更快
───────────────────────────────────────────────────────────────────────

问题分析：
    三种跳法可以把数组建模为一个无向图，每个节点 i 的邻居：
        - 左邻居：i - 1（如果 >= 0）
        - 右邻居：i + 1（如果 < n）
        - 同值邻居：所有满足 arr[j] == arr[i] 且 j != i 的下标 j
    求从节点 0 到节点 n-1 的最短路径 → BFS。

    关键优化（同值分组剪枝）：
        最直接的思路是提前建好每个节点的邻接表，但同值邻居可能非常多
        （如全相同数组），建图就是 O(n²)。
        正确做法：不提前建图，而是用哈希表记录"值 → 下标列表"。
        当 BFS 第一次遇到某个值时，一次性将所有同值下标入队，
        然后立即从哈希表中删除该键，避免后续重复处理（每个同值组
        只会被处理一次）。

与跳跃游戏 I / II / III 的区别：
    ─────────────────────────────────────────────────────────────────
    题目      跳法                                                    返回值
    ─────────────────────────────────────────────────────────────────
    Jump I    仅向右，[0, nums[i]] 步                                 能否到终点
    Jump II   仅向右，[0, nums[i]] 步                                 最少步数
    Jump III  左右均可，固定 arr[i] 步                                能否到 0
    Jump IV   左右均可 ±1 步，或跳转到任意同值下标                    最少步数
    ─────────────────────────────────────────────────────────────────
"""

from typing import List
from collections import deque, defaultdict


# ══════════════════════════════════════════════════════════
# 解法一：BFS + 同值分组（标准队列）
# ══════════════════════════════════════════════════════════

def minJumps_group_bfs(arr: List[int]) -> int:
    """
    BFS + 同值分组 ⭐⭐⭐

    核心思路：
    ────────────────────────────────────────────────────────
    标准的 BFS 求最短路径，每次从队列头部取出一个下标 i：
        1. 检查是否到达终点（n - 1），是则返回步数
        2. 将左邻居（i - 1）和右邻居（i + 1）加入队列（有效且未访问）
        3. 将所有同值邻居一次性加入队列，然后删除该值对应的
           所有下标（同值组只处理一次）

    为什么删除同值组能保证 O(n)？
    ────────────────────────────────────────────────────────
    如果不删除，每次遇到同值节点就要重新遍历整个同值组。
    例如 arr = [1, 1, 1, 1, ..., 1]（长度 10⁵），
    每个节点都有 O(n) 个同值邻居，总复杂度会退化为 O(n²)。

    删除后，每个同值组只被处理一次，每条边（左、右、同值）
    最多被访问两次，总复杂度 O(n)。

    图解示例：arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
    ─────────────────────────────────────────────────────────────────────
    下标:  0     1     2     3     4     5     6     7     8     9
    值:  [100, -23, -23, 404, 100, 23,  23,  23,   3,   404]
                                                          ↑
                                                        终点

    同值映射：
        100 → [0, 4]
        -23 → [1, 2]
        404 → [3, 9]
        23  → [5, 6, 7]
        3   → [8]

    BFS 过程：
    ─────────────────────────────────────────────────────────────────────
    初始：queue = [0], visited = {0}, steps = 0

    第 0 步（层 0，起始层）：
        弹出 i = 0, arr[0] = 100 ≠ 404（arr[9]）

        入队左右邻居：
            i+1 = 1  ✅ 未访问 → 入队 [1]

        同值组处理：值 100 → [0, 4]
            已访问 0，入队 4 ✅ → 队列 [1, 4]
            删除 100 的映射（以后不再处理值 100）

    第 1 步（层 1）：
        弹出 i = 1, arr[1] = -23 ≠ 404

        左右：
            i-1 = 0  ❌ 已访问
            i+1 = 2  ✅ → 入队 [4, 2]

        同值组 -23 → [1, 2]
            已访问 1，入队 2 ✅
            删除 -23 映射

        弹出 i = 4, arr[4] = 100
            值 100 已被删除 → 同值已处理过，跳过

        左右：
            i-1 = 3  ✅ → 入队 [2, 3]
            i+1 = 5  ✅ → 入队 [2, 3, 5]

    第 2 步（层 2）：
        弹出 i = 2, arr[2] = -23（同值组已删除，跳过）
            左右邻居都已访问

        弹出 i = 3, arr[3] = 404

        左右：
            i-1 = 2  ❌ 已访问
            i+1 = 4  ❌ 已访问

        同值组 404 → [3, 9]
            已访问 3，入队 9 ✅
            队列 → [5, 9]

        弹出 i = 5, arr[5] = 23

        左右：
            i-1 = 4  ❌ 已访问
            i+1 = 6  ✅ → 入队 [9, 6]

        同值组 23 → [5, 6, 7]
            已访问 5，入队 6 ✅，入队 7 ✅
            队列 → [9, 6, 7]

    第 3 步（层 3）：
        弹出 i = 9, arr[9] == 终点 ✅ → 返回 3！

    ⚠️ 易错点：
        必须将同值组入队后立即删除映射，否则之后再次遇到
        同值节点时会重复遍历整个组，退化到 O(n²)。

    时间复杂度：O(n) — 每个下标入队一次，每个同值组处理一次
    空间复杂度：O(n) — 队列 + visited 数组 + 值映射表
    """
    n = len(arr)

    # 边界情况：长度为 1，起点就是终点
    if n == 1:
        return 0

    # 值 → 下标列表（同值分组）
    val_to_indices: dict[int, list[int]] = defaultdict(list)
    for idx, val in enumerate(arr):
        val_to_indices[val].append(idx)

    visited = [False] * n
    queue = deque([0])
    visited[0] = True
    steps = 0

    while queue:
        # 逐层处理，方便统计步数
        level_size = len(queue)
        for _ in range(level_size):
            i = queue.popleft()

            # 到达终点
            if i == n - 1:
                return steps

            # 1) 右邻居
            if i + 1 < n and not visited[i + 1]:
                visited[i + 1] = True
                queue.append(i + 1)
            # 2) 左邻居
            if i - 1 >= 0 and not visited[i - 1]:
                visited[i - 1] = True
                queue.append(i - 1)

            # 3) 同值邻居：一次性处理整个同值组
            val = arr[i]
            if val in val_to_indices:
                for j in val_to_indices[val]:
                    if not visited[j]:
                        visited[j] = True
                        queue.append(j)
                # ⭐ 关键：处理完后立即删除，保证每个同值组只处理一次
                del val_to_indices[val]

        # 当前层遍历完毕，步数 + 1
        steps += 1

    # 题目保证有解，这里不会执行到
    return -1


# ══════════════════════════════════════════════════════════
# 解法二：BFS + 同值分组（逐层处理，步骤更清晰）
# ══════════════════════════════════════════════════════════

def minJumps_level_bfs(arr: List[int]) -> int:
    """
    BFS + 同值分组（逐层处理版本）⭐⭐

    核心思路：
    ────────────────────────────────────────────────────────
    与解法一本质上相同，但使用"当前层"和"下一层"两个队列
    显式区分 BFS 的层边界，代码意图更清晰，适合初学者理解
    BFS 分层处理的思想。

    算法步骤：
    1. 建同值映射表 val → indices
    2. current_level = {0}（起始层）
    3. steps = 0
    4. 当 current_level 非空时循环：
        a. next_level = set()（下一层节点集合）
        b. 遍历 current_level 中的每个节点 i：
            - 如果 i == n-1，返回 steps
            - 将 i-1, i+1 加入 next_level（有效且未访问）
            - 将所有同值节点加入 next_level，然后删除映射
        c. 标记 next_level 中所有节点为已访问
        d. current_level = next_level
        e. steps += 1

    使用 set 代替 deque 的好处：
    ────────────────────────────────────────────────────────
    - 自动去重：左右邻居可能和同值邻居重复，set 避免重复入队
    - 分层逻辑更为显式，不必在单队列中记录层大小

    图解示例：arr = [7, 6, 9, 6, 9, 6, 9, 7]
    ────────────────────────────────────────────────────────
    下标:  0    1    2    3    4    5    6    7
    值:   [7,   6,   9,   6,   9,   6,   9,   7]
                                               ↑
                                             终点

    同值映射：
        7 → [0, 7]
        6 → [1, 3, 5]
        9 → [2, 4, 6]

    BFS 分层过程：
    ────────────────────────────────────────────────────────
    steps = 0: current = {0}
               弹出 0，arr[0]=7
               - 左右邻居：1
               - 同值组 7 → [0, 7]，入队 7 ✅
               - 删除 7 映射
               next = {1, 7}

    steps = 1: current = {1, 7}
               弹出 1，arr[1]=6
               - 左右邻居：0(已访), 2
               - 同值组 6 → [1, 3, 5]，入队 3, 5
               - 删除 6 映射

               弹出 7，arr[7]=7（同值已删，跳过）
               - 左右邻居：6
               - 同值已处理（7 已被删）

               next = {2, 3, 5, 6}
               其中 6 是终点 ✅，steps=1 时返回！

    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    n = len(arr)

    if n == 1:
        return 0

    # 同值分组
    val_to_indices: dict[int, list[int]] = defaultdict(list)
    for idx, val in enumerate(arr):
        val_to_indices[val].append(idx)

    visited = [False] * n
    visited[0] = True
    current_level = {0}
    steps = 0

    while current_level:
        next_level = set()

        for i in current_level:
            if i == n - 1:
                return steps

            # 左邻居
            if i - 1 >= 0 and not visited[i - 1]:
                visited[i - 1] = True
                next_level.add(i - 1)
            # 右邻居
            if i + 1 < n and not visited[i + 1]:
                visited[i + 1] = True
                next_level.add(i + 1)

            # 同值邻居
            val = arr[i]
            if val in val_to_indices:
                for j in val_to_indices[val]:
                    if not visited[j]:
                        visited[j] = True
                        next_level.add(j)
                # ⭐ 处理完立即删除
                del val_to_indices[val]

        current_level = next_level
        steps += 1

    return -1


# ══════════════════════════════════════════════════════════
# 解法三：双向 BFS
# ══════════════════════════════════════════════════════════

def minJumps_bidirectional_bfs(arr: List[int]) -> int:
    """
    双向 BFS（两端交替搜索）⭐⭐⭐

    核心思路：
    ────────────────────────────────────────────────────────
    标准 BFS 从起点单向扩展，每层扩散的节点数呈指数增长。
    双向 BFS 同时从起点和终点开始搜索，每次选择节点数较少
    的一端进行扩展，当两端的搜索区域"相遇"时即找到最短路径。

    为什么双向 BFS 更快？
    ────────────────────────────────────────────────────────
    假设图的分支因子为 b，最短路径长度为 d：
        - 单向 BFS：需要探索 O(b^d) 个节点
        - 双向 BFS：两端各探索 O(b^(d/2))，合计 O(2 * b^(d/2))
    在跳棋 IV 问题中，同值跳转可能带来大量分支，双向 BFS
    往往能提前相遇，减少探索节点数。

    算法步骤：
    1. 建同值映射表 val → indices
    2. 起点集合 head = {0}，终点集合 tail = {n-1}
    3. visited_from_start / visited_from_end 分别记录两端访问情况
    4. steps = 0
    5. 当 head 和 tail 都非空时循环：
        a. 选择较小的一侧扩展（优化关键）
        b. 对选中侧的每个节点，将未访问的邻居加入下一层
        c. 扩展前检查是否有节点已被对方访问过 → 相遇则返回 steps
        d. steps += 1

    图解示例：arr = [100, -23, -23, 404, 100, 23, 23, 23, 3, 404]
    ────────────────────────────────────────────────────────────────
    同值映射：
        100 → [0, 4]
        -23 → [1, 2]
        404 → [3, 9]
        23  → [5, 6, 7]
        3   → [8]

    head = {0}, tail = {9}, steps = 0

    第 0 步：
        选择扩展 head（size=1，小于 tail 的 size=1，选 head）
        展开 0 → 得到 {1, 4}
        head = {1, 4}
        检查交集：{1, 4} ∩ {9} = ∅
        steps = 1

    第 1 步：
        head size=2, tail size=1 → 选择扩展 tail
        展开 9 → 得到 {3, 8}
        tail = {3, 8}
        检查交集：{1, 4} ∩ {3, 8} = ∅
        steps = 2

    第 2 步：
        head size=2, tail size=2 → 选 head（size 相同）
        展开 1 → 得到 {0(已访), 2}
        展开 4 → 得到 {3, 5}
        head = {2, 3, 5}
        检查交集：{2, 3, 5} ∩ {3, 8} = {3} ✅ → 相遇！
        返回 steps + 1 = 3

    ⚠️ 注意：
        为什么返回 steps + 1 而不是 steps？
        因为 steps 记录的是"已经扩展过的轮数"，
        当发现交集时，当前步骤还没有被计入 steps，
        而找到交集意味着"再从当前层迈一步就到对方"，
        所以需要 steps + 1。

    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    n = len(arr)

    if n == 1:
        return 0
    if arr[0] == arr[n - 1]:
        return 1

    # 同值分组
    val_to_indices: dict[int, list[int]] = defaultdict(list)
    for idx, val in enumerate(arr):
        val_to_indices[val].append(idx)

    # 两端访问标记
    visited_from_start = [False] * n
    visited_from_end = [False] * n

    head = {0}
    tail = {n - 1}
    visited_from_start[0] = True
    visited_from_end[n - 1] = True

    steps = 0

    while head and tail:
        # ⭐ 优化关键：总是扩展节点数较少的一侧
        if len(head) > len(tail):
            head, tail = tail, head
            # 交换 head/tail 时，必须同时交换 visited 数组
            # 保证 visited_from_start 始终对应 head，visited_from_end 始终对应 tail
            visited_from_start, visited_from_end = visited_from_end, visited_from_start

        next_level = set()

        for i in head:
            # ----- 左右邻居 -----
            # 左
            if i - 1 >= 0:
                if not visited_from_start[i - 1]:
                    # 检查是否被对方访问过（相遇）
                    if visited_from_end[i - 1]:
                        return steps + 1
                    visited_from_start[i - 1] = True
                    next_level.add(i - 1)
            # 右
            if i + 1 < n:
                if not visited_from_start[i + 1]:
                    if visited_from_end[i + 1]:
                        return steps + 1
                    visited_from_start[i + 1] = True
                    next_level.add(i + 1)

            # ----- 同值邻居 -----
            val = arr[i]
            if val in val_to_indices:
                for j in val_to_indices[val]:
                    if not visited_from_start[j]:
                        if visited_from_end[j]:
                            return steps + 1
                        visited_from_start[j] = True
                        next_level.add(j)
                # ⭐ 同值组只处理一次
                del val_to_indices[val]

        head = next_level
        steps += 1

    return -1
