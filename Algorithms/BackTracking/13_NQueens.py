"""
按照国际象棋的规则，皇后可以攻击与之处在同一行或同一列或同一斜线上的棋子。
n 皇后问题 研究的是如何将 n 个皇后放置在 n×n 的棋盘上，并且使皇后彼此之间不能相互攻击。
给你一个整数 n ，返回所有不同的 n 皇后问题 的解决方案。
每一种解法包含一个不同的 n 皇后问题 的棋子放置方案，该方案中 'Q' 和 '.' 分别代表了皇后和空位。
"""

# 解法一：回溯法（集合记录冲突）
# 时间复杂度 O(N!)  空间复杂度 O(N)
def solveNQueens(n: int):
    """
    :param n: 棋盘大小 n x n
    :return: List[List[str]] 所有合法的摆放方案
    """
    res = []  # 存储所有合法解

    def backtrack(row: int, cols: set, diagonals: set, antiDiagonals: set, board: list):
        """
        :param row: 当前正在处理的行号（0-based）
        :param cols: 已占用的列号集合
        :param diagonals: 已占用的主对角线集合（row - col 为常数）
        :param antiDiagonals: 已占用的副对角线集合（row + col 为常数）
        :param board: 当前棋盘状态（二维字符列表）
        """
        # 所有行都成功放置了皇后，找到一个合法解
        if row == n:
            # board[:] 是浅拷贝，但 board 中的每一行是列表，需要深拷贝
            # 实际上这里用 board[:] 是不够的，需要用深拷贝
            res.append([''.join(r) for r in board])  # 将每行列表转为字符串
            return

        # 尝试将皇后放在当前行的每一列
        for col in range(n):
            # 如果当前列或两条对角线已被占用，跳过
            if col in cols or (row - col) in diagonals or (row + col) in antiDiagonals:
                continue

            # --- 做选择 ---
            cols.add(col)                     # 标记列被占用
            diagonals.add(row - col)           # 标记主对角线被占用
            antiDiagonals.add(row + col)       # 标记副对角线被占用
            board[row][col] = 'Q'              # 放置皇后

            # 递归处理下一行
            backtrack(row + 1, cols, diagonals, antiDiagonals, board)

            # --- 撤销选择（回溯）---
            board[row][col] = '.'
            cols.remove(col)
            diagonals.remove(row - col)
            antiDiagonals.remove(row + col)

    # 初始化棋盘：全部为 '.'
    initial_board = [['.' for _ in range(n)] for _ in range(n)]
    backtrack(0, set(), set(), set(), initial_board)
    return res


# 解法二：回溯法（布尔数组记录冲突，性能更优）
# 时间复杂度 O(N!)  空间复杂度 O(N)
def solveNQueens_boolean(n: int):
    """
    用布尔数组代替集合，省去哈希计算，速度更快
    """
    res = []
    # 列占用标志
    cols = [False] * n
    # 主对角线占用标志：共有 2n-1 条，索引范围 0 ~ 2n-2
    # 对于位置 (row, col)，主对角线索引为 row - col + n - 1
    diagonals = [False] * (2 * n - 1)
    # 副对角线占用标志：索引范围 0 ~ 2n-2
    # 对于位置 (row, col)，副对角线索引为 row + col
    anti_diagonals = [False] * (2 * n - 1)

    board = [['.' for _ in range(n)] for _ in range(n)]

    def backtrack(row: int):
        if row == n:
            res.append([''.join(r) for r in board])
            return

        for col in range(n):
            # 计算对角线索引
            diag_idx = row - col + n - 1   # 主对角线
            anti_idx = row + col           # 副对角线

            if cols[col] or diagonals[diag_idx] or anti_diagonals[anti_idx]:
                continue

            # 做选择
            cols[col] = True
            diagonals[diag_idx] = True
            anti_diagonals[anti_idx] = True
            board[row][col] = 'Q'

            backtrack(row + 1)

            # 撤销选择
            board[row][col] = '.'
            cols[col] = False
            diagonals[diag_idx] = False
            anti_diagonals[anti_idx] = False

    backtrack(0)
    return res


# 解法三：位运算回溯法（最快，适合 C++/Java，Python 也适用）
# 时间复杂度 O(N!)  空间复杂度 O(N)
def solveNQueens_bit(n: int):
    """
    用整数的位来表示哪些列/对角线被占用，是最高效的解法。
    三位运算：col_bit, diag1_bit, diag2_bit 的每一位表示对应位置是否被占用。
    """
    res = []
    # 用列表记录每行皇后放在哪一列
    queens = [-1] * n

    def backtrack(row: int, cols_bit: int, diag1_bit: int, diag2_bit: int):
        """
        :param row: 当前行
        :param cols_bit: 列占用位图（1 表示占用）
        :param diag1_bit: 主对角线占用位图
        :param diag2_bit: 副对角线占用位图
        """
        if row == n:
            # 将 queens 列表转换为棋盘字符串
            board = []
            for col in queens:
                line = ['.'] * n
                line[col] = 'Q'
                board.append(''.join(line))
            res.append(board)
            return

        # 获取当前行所有可用的列位置
        # 1. (cols_bit | diag1_bit | diag2_bit) 得到所有被占用的位
        # 2. 取反后，1 表示可用位置（但只取低 n 位）
        # 3. & ((1 << n) - 1) 只保留低 n 位
        available = (~(cols_bit | diag1_bit | diag2_bit)) & ((1 << n) - 1)

        # 尝试每个可用位置
        while available:
            # 取出最低位的 1（即最右边可用的列）
            pick = available & -available
            # 得到该位对应的列号
            col = (pick.bit_length() - 1)

            queens[row] = col

            # 递归：下一行的列位图要加上当前列
            # diag1 左移：下一行时主对角线的影响左移一位
            # diag2 右移：下一行时副对角线的影响右移一位
            backtrack(row + 1,
                      cols_bit | pick,
                      (diag1_bit | pick) << 1,
                      (diag2_bit | pick) >> 1)

            # 清除最低位的 1，继续尝试下一个可用位置
            available &= available - 1

    backtrack(0, 0, 0, 0)
    return res


# 解法四：DFS + 排列剪枝（效率较低，但思路直观）
# 时间复杂度 O(N!)  空间复杂度 O(N)
def solveNQueens_permutation(n: int):
    """
    思路：N个皇后放在N行，每行一个，所以本质上是求1~N的一个排列，
    然后检查排列是否满足对角线约束（即任意两个皇后不在同一对角线上）。

    相当于先生成全排列（N!种），再筛选，所以效率不如回溯法。
    这里只做演示，n 较大时不宜使用。
    """
    res = []
    used = [False] * n
    cols = []  # 用于记录当前排列（每行皇后的列号）

    def is_valid(cols):
        """检查当前排列是否满足对角线约束"""
        for i in range(len(cols)):
            for j in range(i + 1, len(cols)):
                # 行差 == 列差，说明在同一条对角线上
                if j - i == abs(cols[j] - cols[i]):
                    return False
        return True

    def backtrack(row: int):
        if row == n:
            if is_valid(cols):
                board = []
                for col in cols:
                    line = ['.'] * n
                    line[col] = 'Q'
                    board.append(''.join(line))
                res.append(board)
            return

        for col in range(n):
            if not used[col]:
                used[col] = True
                cols.append(col)

                backtrack(row + 1)

                cols.pop()
                used[col] = False

    backtrack(0)
    return res


# 解法五：迭代回溯（非递归）
# 时间复杂度 O(N!)  空间复杂度 O(N)
def solveNQueens_iterative(n: int):
    """
    用栈模拟递归过程，避免递归调用栈开销。
    每个栈帧: (row, col, state)
      state=0: 刚进入，需要找可放置的位置
      state=1: 从该行的下一列继续尝试
      state=2: 回溯，撤销该行的皇后
    """
    res = []
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)
    diag2 = [False] * (2 * n - 1)
    queens = [-1] * n

    # (row, state) 当前处理的行和状态
    # 用 next_col 记录该行下一个要尝试的列
    next_col = [0] * (n + 1)  # 多一个给 n 行（记录解）
    row = 0

    while row >= 0:
        if row == n:
            # 找到一个解，记录
            board = []
            for q in queens:
                line = ['.'] * n
                line[q] = 'Q'
                board.append(''.join(line))
            res.append(board)
            # 回溯到上一行，继续尝试
            row -= 1
            continue

        # 尝试从 next_col[row] 开始找可放置的位置
        placed = False
        for c in range(next_col[row], n):
            d1 = row - c + n - 1
            d2 = row + c
            if not cols[c] and not diag1[d1] and not diag2[d2]:
                # 找到可放置位置
                if queens[row] != -1:
                    # 先撤销之前的皇后（因为之前在该行放过）
                    old = queens[row]
                    queens[row] = -1
                    cols[old] = False
                    diag1[row - old + n - 1] = False
                    diag2[row + old] = False

                # 放置新皇后
                queens[row] = c
                cols[c] = True
                diag1[d1] = True
                diag2[d2] = True

                # 记录下次从下一列开始尝试
                next_col[row] = c + 1
                # 进入下一行
                row += 1
                next_col[row] = 0  # 下一行从第0列开始
                placed = True
                break

        if not placed:
            # 当前行没有可用位置
            # 撤销当前行的皇后（如果有的话）
            if queens[row] != -1:
                old = queens[row]
                queens[row] = -1
                cols[old] = False
                diag1[row - old + n - 1] = False
                diag2[row + old] = False
            # 重置 next_col，回溯到上一行
            next_col[row] = 0
            row -= 1

    return res


# 解法六：对称性优化（减少一半搜索空间）
# 时间复杂度 O(N!/2)  空间复杂度 O(N)
def solveNQueens_symmetric(n: int):
    """
    利用棋盘的对称性：如果第一行皇后的位置只在左半部分搜索，
    然后通过镜像对称可以得到另一半的解（以及主对角线对称的解）。

    注意：当 n 为奇数时，中间列需要特殊处理（避免重复计数）。
    这里只做简单实现，体现优化思路。
    """
    res = []
    cols = [False] * n
    diag1 = [False] * (2 * n - 1)
    diag2 = [False] * (2 * n - 1)
    board = [['.' for _ in range(n)] for _ in range(n)]

    def backtrack(row: int):
        if row == n:
            res.append([''.join(r) for r in board])
            return

        # 第一行只搜索左半部分（包括中间列）
        col_range = range(n // 2) if row == 0 else range(n)

        for col in col_range:
            d1 = row - col + n - 1
            d2 = row + col
            if cols[col] or diag1[d1] or diag2[d2]:
                continue

            cols[col] = True
            diag1[d1] = True
            diag2[d2] = True
            board[row][col] = 'Q'

            backtrack(row + 1)

            board[row][col] = '.'
            cols[col] = False
            diag1[d1] = False
            diag2[d2] = False

    backtrack(0)

    # 对称性扩展：将第一行在左半部分的解镜像到右半部分
    # 注意：这里简化处理，仅做概念演示，n=1 需要特判
    if n == 1:
        return [["Q"]]

    # 完整的对称优化需要妥善处理解的重复问题，此处略去完整实现
    return res
