"""
编写一个程序，通过填充空格来解决数独问题。

数独的解法需 遵循如下规则：

数字 1-9 在每一行只能出现一次。
数字 1-9 在每一列只能出现一次。
数字 1-9 在每一个以粗实线分隔的 3x3 宫内只能出现一次。（请参考示例图）
数独部分空格内已填入了数字，空白格用 '.' 表示。


解题思路：回溯法（Backtracking）

┌─────────────────────────────────────────────────────────────┐
│                      数独解题思路                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  核心思想：                                                  │
│  1. 找到一个空白格（'.'）                                     │
│  2. 尝试填入 1-9 中的数字                                     │
│  3. 检查是否合法（行、列、3x3宫格都不冲突）                     │
│  4. 如果合法，填入并递归解决剩余部分                            │
│  5. 如果递归成功，返回True                                     │
│  6. 如果递归失败，回溯（恢复为'.'），尝试下一个数字              │
│  7. 如果1-9都失败，返回False（需要上层回溯）                   │
│                                                             │
│  决策树示例：                                                 │
│                                                             │
│                    找到空格(0,2)                              │
│                         │                                   │
│         ┌───────┬───────┼───────┬───────┐                   │
│         │       │       │       │       │                   │
│        试1     试2     试3     ...    试9                    │
│         ✗       ✓                                    │
│       冲突    合法                                          │
│                │                                            │
│           填入board[0][2]='2'                                │
│                │                                            │
│           递归找下一个空格                                     │
│                │                                            │
│           递归成功 → 返回True                                 │
│           递归失败 → 恢复为'.'，继续试4                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘


时间复杂度：O(9^(n*n))，其中n=9，最坏情况下需要尝试所有可能
空间复杂度：O(n*n)，递归栈深度
"""

from typing import List, Set


def solveSudoku(board: List[List[str]]) -> None:
    """
    解数独主函数
    直接修改输入的board，不返回新board
    """
    backtrack(board)


def backtrack(board: List[List[str]]) -> bool:
    """
    回溯函数⭐⭐
    返回：是否成功解决数独
    
    思路：
    1. 遍历board找到第一个空格'.'
    2. 尝试填入1-9
    3. 检查合法性
    4. 合法则递归，成功返回True
    5. 失败则回溯，恢复'.'
    6. 都失败返回False
    """
    # 找到第一个空格的位置
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                # 尝试填入1-9
                for num in range(1, 10):
                    num_str = str(num)
                    # 检查是否合法
                    if isValid(board, i, j, num_str):
                        # 做选择：填入数字
                        board[i][j] = num_str
                        
                        # 递归：如果成功解决，返回True
                        if backtrack(board):
                            return True
                        
                        # 撤销选择：回溯，恢复为空格
                        board[i][j] = '.'
                
                # 1-9都试过了都不行，返回False（需要上层回溯）
                return False
    
    # 没有找到空格，说明所有格子都填满了，数独解决成功！
    return True


def isValid(board: List[List[str]], row: int, col: int, num: str) -> bool:
    """
    检查在board[row][col]位置填入num是否合法
    
    检查三个条件：
    1. 同一行没有重复数字
    2. 同一列没有重复数字
    3. 同一个3x3宫格没有重复数字
    """
    # 1. 检查行：同一行其他列是否有num
    for j in range(9):
        if j != col and board[row][j] == num:
            return False
    
    # 2. 检查列：同一列其他行是否有num
    for i in range(9):
        if i != row and board[i][col] == num:
            return False
    
    # 3. 检查3x3宫格
    # 计算宫格的起始位置
    # 行起始：0, 3, 6  （row // 3 * 3）
    # 列起始：0, 3, 6  （col // 3 * 3）
    box_row_start = (row // 3) * 3
    box_col_start = (col // 3) * 3
    
    for i in range(box_row_start, box_row_start + 3):
        for j in range(box_col_start, box_col_start + 3):
            # if (i != row or j != col)条件冗余，因为board[i][j]位置是"."
            if (i != row or j != col) and board[i][j] == num:
                return False
    
    # 三个检查都通过，合法
    return True


#优化版：使用哈希集合预存储

"""
优化思路：使用哈希集合预存储每行、每列、每宫格已使用的数字

┌─────────────────────────────────────────────────────────────┐
│                      优化版思路                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  核心优化：用三个集合数组记录已用数字                          │
│                                                             │
│  rows[i]  = 第i行已使用的数字集合                             │
│  cols[j]  = 第j列已使用的数字集合                             │
│  boxes[k] = 第k个宫格已使用的数字集合                          │
│            (k = (i//3)*3 + j//3)                             │
│                                                             │
│  宫格编号：                                                   │
│  ┌───┬───┬───┐                                               │
│  │ 0 │ 1 │ 2 │  行0-2                                         │
│  ├───┼───┼───┤                                               │
│  │ 3 │ 4 │ 5 │  行3-5                                         │
│  ├───┼───┼───┤                                               │
│  │ 6 │ 7 │ 8 │  行6-8                                         │
│  └───┴───┴───┘                                               │
│                                                             │
│  验证复杂度对比：                                              │
│  ┌─────────────┬──────────────┬──────────────┐              │
│  │   检查项目   │  基础版复杂度 │  优化版复杂度  │              │
│  ├─────────────┼──────────────┼──────────────┤              │
│  │    行检查    │    O(9)      │    O(1)      │              │
│  │    列检查    │    O(9)      │    O(1)      │              │
│  │   宫格检查   │    O(9)      │    O(1)      │              │
│  │    总计     │    O(27)     │    O(1)      │              │
│  └─────────────┴──────────────┴──────────────┘              │
│                                                             │
│  优化点：                                                     │
│  1. 初始化时一次性统计所有已填入的数字                          │
│  2. 填入数字时同步更新三个集合                                  │
│  3. 验证时只需3次集合查找                                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
"""


def solveSudoku_optimized(board: List[List[str]]) -> None:
    """
    解数独优化版主函数
    使用哈希集合预存储，验证复杂度O(1)
    """
    # 初始化三个集合数组
    rows: List[Set[str]] = [set() for _ in range(9)]   # 每行已用数字
    cols: List[Set[str]] = [set() for _ in range(9)]   # 每列已用数字
    boxes: List[Set[str]] = [set() for _ in range(9)]  # 每宫格已用数字
    
    # 初始化：遍历board，将已有数字加入对应集合
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = board[i][j]
                rows[i].add(num)
                cols[j].add(num)
                # 计算宫格编号：行块*3 + 列块
                box_idx = (i // 3) * 3 + (j // 3)
                boxes[box_idx].add(num)
    
    backtrack_optimized(board, rows, cols, boxes)


def backtrack_optimized(
    board: List[List[str]],
    rows: List[Set[str]],
    cols: List[Set[str]],
    boxes: List[Set[str]]
) -> bool:
    """
    优化版回溯函数⭐⭐
    
    参数：
    - board: 数独棋盘
    - rows: 每行已用数字集合
    - cols: 每列已用数字集合
    - boxes: 每宫格已用数字集合
    """
    # 找到第一个空格
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                box_idx = (i // 3) * 3 + (j // 3)
                
                # 尝试填入1-9
                for num in range(1, 10):
                    num_str = str(num)
                    
                    # O(1)验证：检查三个集合
                    if (num_str in rows[i] or      # 行冲突
                        num_str in cols[j] or      # 列冲突
                        num_str in boxes[box_idx]): # 宫格冲突
                        continue
                    
                    # 做选择：填入数字并更新集合
                    board[i][j] = num_str
                    rows[i].add(num_str)
                    cols[j].add(num_str)
                    boxes[box_idx].add(num_str)
                    
                    # 递归
                    if backtrack_optimized(board, rows, cols, boxes):
                        return True
                    
                    # 撤销选择：回溯，恢复并更新集合
                    board[i][j] = '.'
                    rows[i].remove(num_str)
                    cols[j].remove(num_str)
                    boxes[box_idx].remove(num_str)
                
                # 1-9都失败
                return False
    
    # 没有空格，成功
    return True


"""
进一步优化策略：

1. 位运算优化：用二进制位代替集合，空间更小，速度更快
2. 最少选择优先：优先填可填数字最少的格子，减少分支
3. Dancing Links：最高效的数据结构（Donald Knuth提出）
"""


# 优化版本2：位运算 + 最少选择优先
"""
位运算优化说明：

用9位二进制数表示每行/列/宫格已使用的数字
第k位为1表示数字k+1已使用

示例：
  二进制 000000101 = 十进制 5
  表示数字1和3已使用（第0位和第2位为1）

位运算操作：
  - 检查数字num是否已用：rows[row] & (1 << (num-1))
  - 标记数字num已用：rows[row] |= (1 << (num-1))
  - 取消标记：rows[row] ^= (1 << (num-1))
  - 获取可用数字：~rows[row] & 0x1FF（低9位）
"""


def solveSudoku_bitmask(board: List[List[str]]) -> None:
    """
    位运算优化版⭐⭐
    用整数二进制位代替集合，验证O(1)，空间更小
    """
    # rows[i], cols[j], boxes[k] 用9位二进制表示已用数字
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    
    # 初始化：将已有数字转为位掩码
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = int(board[i][j])
                mask = 1 << (num - 1)  # 第num-1位设为1
                rows[i] |= mask
                cols[j] |= mask
                boxes[(i // 3) * 3 + (j // 3)] |= mask
    
    backtrack_bitmask(board, rows, cols, boxes)


def backtrack_bitmask(board, rows, cols, boxes):
    """位运算回溯"""
    # 找到第一个空格
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                box_idx = (i // 3) * 3 + (j // 3)
                
                # 计算可用数字：三个掩码的并集取反，再取低9位
                used = rows[i] | cols[j] | boxes[box_idx]
                available = (~used) & 0x1FF  # 0x1FF = 111111111（9个1）
                
                # 遍历所有可用数字
                for num in range(1, 10):
                    mask = 1 << (num - 1)
                    if available & mask:  # 该数字可用
                        # 填入数字
                        board[i][j] = str(num)
                        rows[i] |= mask
                        cols[j] |= mask
                        boxes[box_idx] |= mask
                        
                        if backtrack_bitmask(board, rows, cols, boxes):
                            return True
                        
                        # 回溯
                        board[i][j] = '.'
                        rows[i] ^= mask
                        cols[j] ^= mask
                        boxes[box_idx] ^= mask
                
                return False
    
    return True


# 优化版本3：最少选择优先（MRV启发式）
"""
MRV (Minimum Remaining Values) 启发式：
优先选择可填数字最少的格子，可以大幅减少搜索分支

示例：
  格子A可填：[1,2,3,4,5]（5个选择）
  格子B可填：[7,8]（2个选择）
  优先填B，因为分支更少
"""


def solveSudoku_mrv(board: List[List[str]]) -> None:
    """
    最少选择优先（MRV）优化版⭐⭐⭐
    每次选择可填数字最少的空格，减少搜索分支
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    
    # 初始化
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = int(board[i][j])
                mask = 1 << (num - 1)
                rows[i] |= mask
                cols[j] |= mask
                boxes[(i // 3) * 3 + (j // 3)] |= mask
    
    backtrack_mrv(board, rows, cols, boxes)


def backtrack_mrv(board, rows, cols, boxes):
    """MRV回溯：每次找可填数字最少的空格"""
    
    # 找到可填数字最少的空格
    min_options = 10
    best_i, best_j = -1, -1
    best_available = 0
    
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                box_idx = (i // 3) * 3 + (j // 3)
                used = rows[i] | cols[j] | boxes[box_idx]
                available = (~used) & 0x1FF
                
                # 统计可用数字个数
                count = bin(available).count('1')
                
                if count < min_options:
                    min_options = count
                    best_i, best_j = i, j
                    best_available = available
                    
                    # 如果只有1个选择，直接选它（最优情况）
                    if count == 1:
                        break
        if min_options == 1:
            break
    
    # 没有空格了，成功
    if best_i == -1:
        return True
    
    # 在找到的位置尝试所有可用数字
    i, j = best_i, best_j
    box_idx = (i // 3) * 3 + (j // 3)
    available = best_available
    
    for num in range(1, 10):
        mask = 1 << (num - 1)
        if available & mask:
            board[i][j] = str(num)
            rows[i] |= mask
            cols[j] |= mask
            boxes[box_idx] |= mask
            
            if backtrack_mrv(board, rows, cols, boxes):
                return True
            
            board[i][j] = '.'
            rows[i] ^= mask
            cols[j] ^= mask
            boxes[box_idx] ^= mask
    
    return False


# 优化版本4：迭代填充（确定性格子优先）
"""
迭代填充策略：
1. 先找出所有只能填一个数字的格子（确定性格子）
2. 填入这些格子，更新约束
3. 重复直到没有确定性格子
4. 对剩余格子使用回溯

这样可以大幅减少回溯的搜索空间
"""


def solveSudoku_iterative(board: List[List[str]]) -> None:
    """
    迭代填充 + 回溯 混合版
    先填确定性格子，再对剩余格子回溯
    """
    rows = [0] * 9
    cols = [0] * 9
    boxes = [0] * 9
    
    # 初始化
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = int(board[i][j])
                mask = 1 << (num - 1)
                rows[i] |= mask
                cols[j] |= mask
                boxes[(i // 3) * 3 + (j // 3)] |= mask
    
    # 迭代填充确定性格子
    changed = True
    while changed:
        changed = False
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    box_idx = (i // 3) * 3 + (j // 3)
                    used = rows[i] | cols[j] | boxes[box_idx]
                    available = (~used) & 0x1FF
                    
                    # 如果只有一个可选数字，直接填入
                    if bin(available).count('1') == 1:
                        num = (available & -available).bit_length()  # 获取最低位的1的位置
                        board[i][j] = str(num)
                        mask = 1 << (num - 1)
                        rows[i] |= mask
                        cols[j] |= mask
                        boxes[box_idx] |= mask
                        changed = True
    
    # 对剩余格子使用MRV回溯
    backtrack_mrv(board, rows, cols, boxes)


# 优化版本5：数组代替哈希集合
"""
对于Python，使用列表/数组代替集合可能更快
因为列表的索引访问是O(1)，且常数更小
"""


def solveSudoku_array(board: List[List[str]]) -> None:
    """
    使用数组代替集合的版本⭐⭐⭐
    rows[i][num] = True 表示第i行已使用数字num
    """
    # 使用二维数组：rows[row][num] = True/False
    rows = [[False] * 10 for _ in range(9)]  # 索引1-9
    cols = [[False] * 10 for _ in range(9)]
    boxes = [[False] * 10 for _ in range(9)]
    
    # 初始化
    for i in range(9):
        for j in range(9):
            if board[i][j] != '.':
                num = int(board[i][j])
                rows[i][num] = True
                cols[j][num] = True
                boxes[(i // 3) * 3 + (j // 3)][num] = True
    
    backtrack_array(board, rows, cols, boxes)


def backtrack_array(board, rows, cols, boxes):
    """数组版回溯"""
    for i in range(9):
        for j in range(9):
            if board[i][j] == '.':
                box_idx = (i // 3) * 3 + (j // 3)
                
                for num in range(1, 10):
                    # O(1)检查
                    if not (rows[i][num] or cols[j][num] or boxes[box_idx][num]):
                        board[i][j] = str(num)
                        rows[i][num] = True
                        cols[j][num] = True
                        boxes[box_idx][num] = True
                        
                        if backtrack_array(board, rows, cols, boxes):
                            return True
                        
                        board[i][j] = '.'
                        rows[i][num] = False
                        cols[j][num] = False
                        boxes[box_idx][num] = False
                
                return False
    
    return True