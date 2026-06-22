"""
零钱兑换 II（Coin Change II）

题目描述：
给你一个整数数组 coins 表示不同面额的硬币，另给一个整数 amount 表示总金额。
请你计算并返回可以凑成总金额的硬币组合数。如果任何硬币组合都无法凑出总金额，返回 0 。
假设每一种面额的硬币有无限个。
题目数据保证最终结果符合 32 位带符号整数。

示例 1：
    输入：amount = 5, coins = [1, 2, 5]
    输出：4
    解释：有四种方式可以凑成总金额：
    5=5
    5=2+2+1
    5=2+1+1+1
    5=1+1+1+1+1

示例 2：
    输入：amount = 3, coins = [2]
    输出：0
    解释：只用面额 2 的硬币不能凑成总金额 3 。

示例 3：
    输入：amount = 10, coins = [10]
    输出：1

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
回溯算法                       O(S^amount)     O(amount)       超时，仅用于理解
记忆化搜索（Top-Down DP）       O(n×amount)     O(n×amount)     ⭐⭐
动态规划（Bottom-Up DP）        O(n×amount)     O(amount)       ⭐⭐⭐⭐  推荐
────────────────────────────────────────────────────────────────────────
（n = len(coins)）

核心思想（动态规划）：
────────────────────────────────────────────────────────────────────────
关键洞察（转化为完全背包问题）：
1. 每种硬币可以无限使用 → 完全背包问题
2. 目标是求组合数（而非排列数）
3. 递推公式：dp[i] += dp[i - coin]

⚠️ 易错点提醒（Combinations vs Permutations）：
────────────────────────────────────────────────────────────────────────
1. 记忆化搜索中缺少 index 参数
   - 错误：dfs(remaining) 遍历所有硬币
   - 后果：把 1+2 和 2+1 算成两种方案，计算的是排列数
   - 正确：dfs(remaining, index)，只从 index 往后选硬币

2. 记忆化搜索中 base case 写成 remaining in coins
   - 错误：if remaining in coins: return 1
   - 后果：跳过了其他组合，例如 amount=5, coins=[1,2,5] 返回 1 而非 4
   - 正确：if remaining == 0: return 1

3. 动态规划中循环顺序写反
   - 错误：外层遍历金额，内层遍历硬币
   - 后果：计算的是排列数，例如 coins=[1,2], amount=3 返回 3 而非 2
   - 正确：外层遍历硬币，内层遍历金额（保证组合的有序性）

状态定义（一维 DP）：
    dp[i] = 凑成金额 i 的硬币组合数

状态转移：
    对于每种硬币 coin：
    dp[i] += dp[i - coin]  （当 i >= coin）

初始条件：
    dp[0] = 1（凑成金额 0 有 1 种方案：不选任何硬币）

最终答案：
    dp[amount]
"""


# ══════════════════════════════════════════════════════════
# 解法一：回溯算法（Brute Force）
# ══════════════════════════════════════════════════════════


def change_brute(amount: int, coins: list[int]) -> int:
    """
    回溯算法（Brute Force）

    核心思路：
    ────────────────────────────────────────────────────────
    枚举所有可能的硬币组合，检查哪些组合能凑成目标金额。

    算法步骤：
    1. 使用回溯遍历所有可能的组合
    2. 通过 index 参数保证只从当前硬币往后选（避免重复组合）
    3. 维护当前组合的金额总和
    4. 当金额总和等于目标时，计数加一

    时间复杂度：O(S^amount) — S 为硬币种类数，最坏情况每层递归 S 个分支
    空间复杂度：O(amount)   — 递归调用栈深度（最多 amount 层）

    ⚠️ 易错点：
    ────────────────────────────────────────────────────────
    必须使用 index 参数限制遍历范围！
    - for i in range(index, n) 而非 for coin in coins
    - 否则会把 1+2 和 2+1 算成两种方案（排列而非组合）
    """
    result = 0
    n = len(coins)

    def backtrack(index: int, current_sum: int) -> None:
        nonlocal result
        if current_sum > amount:
            return
        if current_sum == amount:
            result += 1
            return

        # ⚠️ 必须从 index 开始，而非从 0 开始
        for i in range(index, n):
            current_sum += coins[i]
            backtrack(i, current_sum)  # 传 i 而非 i+1，因为硬币可以重复使用
            current_sum -= coins[i]

    backtrack(0, 0)
    return result


# ══════════════════════════════════════════════════════════
# 解法二：记忆化搜索（Top-Down DP）
# ══════════════════════════════════════════════════════════


def change_memo(amount: int, coins: list[int]) -> int:
    """
    记忆化搜索解法（Top-Down DP）⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    将问题转化为完全背包问题：
    - 每种硬币可以无限使用
    - 通过 index 参数保证组合的有序性（避免重复计数）

    算法步骤：
    1. 创建缓存 memo[(remaining, index)]
    2. 使用递归 + 缓存求解
    3. 每次递归只从 index 往后选硬币

    时间复杂度：O(n×amount) — 每个状态只计算一次
    空间复杂度：O(n×amount) — 缓存 + 递归调用栈

    ⚠️ 易错点：
    ────────────────────────────────────────────────────────
    1. 缺少 index 参数 → 计算排列数而非组合数
       错误写法：dfs(remaining)，遍历所有硬币
       正确写法：dfs(remaining, index)，只从 index 往后选

    2. base case 写成 remaining in coins
       错误：if remaining in coins: return 1
       后果：跳过其他组合，amount=5, coins=[1,2,5] 返回 1 而非 4
       正确：if remaining == 0: return 1

    状态定义：
    - memo[(remaining, index)] = 从第 index 种硬币开始，凑成 remaining 金额的组合数

    状态转移：
    - 选硬币 i：dfs(remaining - coins[i], i) + dfs(remaining, i+1)
    - 不选硬币 i：dfs(remaining, i+1)

    初始条件：
    - remaining == 0 时返回 1（找到一种有效组合）
    """
    n = len(coins)
    memo = {}

    def dfs(remaining: int, index: int) -> int:
        # ✅ 正确的 base case
        if remaining == 0:
            return 1
        if (remaining, index) in memo:
            return memo[(remaining, index)]
        total = 0
        # ⚠️ 必须从 index 开始，而非从 0 开始
        for i in range(index, n):
            if coins[i] <= remaining:
                total += dfs(remaining - coins[i], i)
        memo[(remaining, index)] = total
        return total

    return dfs(amount, 0)


# ══════════════════════════════════════════════════════════
# 解法三：动态规划（Bottom-Up DP）
# ══════════════════════════════════════════════════════════


def change_dp(amount: int, coins: list[int]) -> int:
    """
    动态规划解法（Bottom-Up DP）⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    完全背包问题的一维 DP 解法。
    通过控制循环顺序来保证计算的是组合数而非排列数。

    算法步骤：
    1. 创建一维 DP 数组 dp[amount+1]，初始化 dp[0] = 1
    2. 外层循环遍历硬币，内层循环遍历金额
    3. 对于每种硬币 coin，更新 dp[i] += dp[i - coin]

    时间复杂度：O(n×amount) — 双重循环
    空间复杂度：O(amount)   — 一维 DP 数组

    ⚠️ 易错点：循环顺序！
    ────────────────────────────────────────────────────────
    外层必须遍历硬币，内层遍历金额！

    错误写法（计算排列数）：
        for i in range(1, amount + 1):      # 外层遍历金额
            for coin in coins:               # 内层遍历硬币
                if coin <= i:
                    dp[i] += dp[i - coin]

    正确写法（计算组合数）：
        for coin in coins:                   # 外层遍历硬币
            for i in range(coin, amount + 1):  # 内层遍历金额
                dp[i] += dp[i - coin]

    为什么顺序很重要？
    ────────────────────────────────────────────────────────
    - 外层遍历硬币：保证每种硬币只会按顺序被考虑
      例如 coins=[1,2]，先处理 coin=1，再处理 coin=2
      这样 dp[3] 只会计算 {1,1,1} 和 {1,2}，不会重复计算 {2,1}

    - 外层遍历金额：对于每个金额，所有硬币都会被考虑
      例如 amount=3 时，coin=1 和 coin=2 都会被尝试
      这样会把 1+2 和 2+1 算成两种方案

    图示示例：
    ────────────────────────────────────────────────────────
    coins = [1, 2], amount = 3

    正确写法（外层遍历硬币）：
    dp = [1, 0, 0, 0]

    处理 coin=1：
    dp[1] += dp[0] = 1  → dp = [1, 1, 0, 0]
    dp[2] += dp[1] = 1  → dp = [1, 1, 1, 0]
    dp[3] += dp[2] = 1  → dp = [1, 1, 1, 1]

    处理 coin=2：
    dp[2] += dp[0] = 2  → dp = [1, 1, 2, 1]
    dp[3] += dp[1] = 2  → dp = [1, 1, 2, 2]

    结果：dp[3] = 2 ✓（组合：{1,1,1} 和 {1,2}）

    错误写法（外层遍历金额）：
    dp = [1, 0, 0, 0]

    i=1: coin=1 → dp[1] += dp[0] = 1  → dp = [1, 1, 0, 0]
    i=2: coin=1 → dp[2] += dp[1] = 1
         coin=2 → dp[2] += dp[0] = 2  → dp = [1, 1, 2, 0]
    i=3: coin=1 → dp[3] += dp[2] = 2
         coin=2 → dp[3] += dp[1] = 3  → dp = [1, 1, 2, 3]

    结果：dp[3] = 3 ✗（错误！把 {1,2} 和 {2,1} 算成两种）

    状态定义：
    - dp[i] = 凑成金额 i 的硬币组合数

    状态转移：
    - dp[i] += dp[i - coin]

    初始条件：
    - dp[0] = 1（凑成金额 0 有 1 种方案：不选任何硬币）

    最终答案：
    - dp[amount]
    """
    dp = [0] * (amount + 1)
    dp[0] = 1

    # ⚠️ 外层遍历硬币，内层遍历金额（顺序不能反！）
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
