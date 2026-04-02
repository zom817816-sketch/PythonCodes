"""
二叉树的层序遍历

题目：给你一个二叉树，请你返回其按层序遍历得到的节点值。（即逐层地，从左到右访问所有节点）。

示例：
    二叉树：[3,9,20,null,null,15,7]
    
        3
       / \
      9  20
        /  \
       15   7
    
    返回：[[3], [9, 20], [15, 7]]

本题提供两种解法：
1. 队列法（BFS，迭代）- 最常用，时间 O(n)，空间 O(w)
2. 递归法（DFS）- 利用递归深度记录层级，时间 O(n)，空间 O(h)
"""

from typing import List, Optional
from collections import deque


class TreeNode:
    """二叉树节点定义"""
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

# 解法一：队列法（BFS，广度优先搜索）
def levelOrder_queue(root: TreeNode) -> List[List[int]]:
    """
    层序遍历 - 队列法（迭代实现）
    
    核心思想：
    - 使用队列（FIFO）保证先访问的节点的子节点也先被访问
    - 通过记录每层节点数，实现按层分组
    
    算法步骤：
    1. 根节点入队
    2. 当队列不为空时：
       a. 记录当前队列长度（即当前层的节点数）
       b. 依次处理当前层的所有节点（出队、记录值、子节点入队）
       c. 将当前层的结果加入最终结果
    
    时间复杂度：O(n) - 每个节点恰好入队出队一次
    空间复杂度：O(w) - w 为树的最大宽度，队列最多存储一层的节点数
    
    适用场景：
    - 需要按层处理节点（如求每层的最大值、平均值）
    - 求树的最小深度（BFS 找到的第一个叶子节点就是最短路径）
    """
    if not root:
        return []
    
    result = []
    # 使用双端队列作为普通队列（从队尾入队，队头出队）
    queue = deque([root])
    
    while queue:
        # 记录当前层的节点数
        # 这很重要！因为后续会把下一层的节点也加入队列
        # 如果不记录，就无法区分当前层和下一层
        level_size = len(queue)
        
        # 存储当前层的所有节点值
        current_level = []
        
        # 处理当前层的所有节点（共 level_size 个）
        for _ in range(level_size):
            # 从队头取出节点
            node = queue.popleft()
            current_level.append(node.val)
            
            # 将子节点加入队尾（下一层）
            # 先左后右，保证从左到右的顺序
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # 当前层处理完毕，加入结果
        result.append(current_level)
    
    return result


# 解法二：递归法（DFS，深度优先搜索）
def levelOrder_recursive(root: TreeNode) -> List[List[int]]:
    """
    层序遍历 - 递归法（DFS实现）
    
    核心思想：
    - 利用递归的深度来记录当前节点所在的层数
    - 将同一层的节点值放入结果列表的同一子列表中
    
    算法步骤：
    1. 定义辅助递归函数，参数为 (节点, 层数)
    2. 如果当前层的结果列表还不存在，先创建
    3. 将当前节点值加入对应层的结果列表
    4. 递归处理左右子节点（层数+1）
    
    时间复杂度：O(n) - 每个节点访问一次
    空间复杂度：O(h) - h 为树的高度，递归栈的深度
    
    适用场景：
    - 已经熟悉 DFS，想换一种思路
    - 不需要按层逐个处理，只需要最终的分层结果
    
    注意：虽然结果是按层分组的，但处理顺序是深度优先，不是广度优先！
    """
    result = []
    
    def dfs(node: TreeNode, level: int):
        """
        深度优先遍历，按层级记录节点值
        
        参数:
            node: 当前节点
            level: 当前节点所在的层数（从0开始）
        """
        if not node:
            return
        
        # 如果当前层的结果列表还不存在，先创建
        # len(result) 表示当前已有的层数
        # 如果 level >= len(result)，说明是第一次访问这一层
        if level >= len(result):
            result.append([])
        
        # 将当前节点值加入对应层的结果列表
        result[level].append(node.val)
        
        # 递归处理左右子节点，层数+1
        # 注意：先左后右，保证同一层内从左到右的顺序
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)
    
    # 从根节点开始，层数为0
    dfs(root, 0)
    
    return result



# 自底向上的层序遍历
def levelOrder_bottom_up(root: TreeNode) -> List[List[int]]:
    """
    自底向上的层序遍历
    
    思路：
    - 先进行普通的层序遍历
    - 最后将结果反转
    
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    result = levelOrder_queue(root)
    result.reverse()
    return result


# 锯齿形层序遍历
def levelOrder_zigzag(root: TreeNode) -> List[List[int]]:
    """
    锯齿形层序遍历
    
    思路：
    - 奇数层从左到右，偶数层从右到左
    - 用双端队列，奇数层从尾部添加，偶数层从头部添加
    
    时间复杂度：O(n)
    空间复杂度：O(n)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    is_left_to_right = True  # 第一层从左到右
    
    while queue:
        level_size = len(queue)
        current_level = deque()
        
        for _ in range(level_size):
            node = queue.popleft()
            
            # 根据方向决定从哪边添加
            if is_left_to_right:
                current_level.append(node.val)
            else:
                current_level.appendleft(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(list(current_level))
        is_left_to_right = not is_left_to_right  # 切换方向
    
    return result


# 二叉树每层最大值
def levelOrder_max_value(root: TreeNode) -> List[int]:
    """
    二叉树每层最大值
    
    思路：
    - 层序遍历，记录每层的最大值
    
    时间复杂度：O(n)
    空间复杂度：O(w)
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level_max = float('-inf')
        
        for _ in range(level_size):
            node = queue.popleft()
            level_max = max(level_max, node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level_max)
    
    return result

# 填充每个节点的下一个右侧节点指针
class TreeNodeNext:
    """
    带 next 指针的二叉树节点
    
    next 指针指向同层的下一个右侧节点，如果没有则为 None
    """
    def __init__(self, val: int = 0, 
                 left: 'TreeNodeNext' = None, 
                 right: 'TreeNodeNext' = None, 
                 next: 'TreeNodeNext' = None):
        self.val = val
        self.left = left
        self.right = right
        self.next = next


def connect_next_pointer_bfs(root: TreeNodeNext) -> TreeNodeNext:
    """
    填充每个节点的 next 指针，指向其下一个右侧节点
    
    解法一：BFS 层序遍历（队列法）
    
    思路：
    - 使用层序遍历，每次处理一层的节点
    - 在同一层内，将前一个节点的 next 指向当前节点
    - 每层的最后一个节点，next 指向 None
    
    时间复杂度：O(n) - 每个节点访问一次
    空间复杂度：O(w) - w 为树的最大宽度，队列存储
    
    示例：
        完美二叉树：
              1
             / \
            2   3
           / \ / \
          4  5 6  7
        
        连接后：
        第1层：1 → None
        第2层：2 → 3 → None
        第3层：4 → 5 → 6 → 7 → None
    """
    if not root:
        return None
    
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        prev = None
        
        for _ in range(level_size):
            cur = queue.popleft()
            
            # 连接前一个节点到当前节点
            if prev:
                prev.next = cur
            prev = cur
            
            # 将子节点加入队列（完美二叉树一定有两个子节点或没有）
            if cur.left:
                queue.append(cur.left)
            if cur.right:
                queue.append(cur.right)
    
    return root


def connect_next_pointer_dfs(root: TreeNodeNext) -> TreeNodeNext:
    """
    填充每个节点的 next 指针，指向其下一个右侧节点
    
    解法二：DFS 递归（利用已建立的 next 指针）
    
    思路：
    - 对于完美二叉树，每个父节点都有两个子节点
    - 对于节点 node：
      - node.left.next = node.right（左子节点的 next 就是右子节点）
      - node.right.next = node.next.left（右子节点的 next 是父节点 next 的左子节点）
    
    时间复杂度：O(n) - 每个节点访问一次
    空间复杂度：O(h) - h 为树的高度，递归栈深度
    
    优点：不需要额外空间（不需要队列）
    """
    if not root:
        return None
    
    def connect(node: TreeNodeNext):
        """递归连接以 node 为根的子树"""
        if not node or not node.left:
            # 叶子节点或空节点，无需处理
            return
        
        # 1. 连接当前节点的左右子节点
        node.left.next = node.right
        
        # 2. 连接右子节点到下一个节点的左子节点
        if node.next:
            node.right.next = node.next.left
        else:
            node.right.next = None
        
        # 3. 递归处理左右子树
        connect(node.left)
        connect(node.right)
    
    connect(root)
    return root


def connect_next_pointer_iterative(root: TreeNodeNext) -> TreeNodeNext:
    """
    填充每个节点的 next 指针，指向其下一个右侧节点
    
    解法三：迭代法（利用已建立的 next 指针，O(1) 空间）
    
    思路：
    - 从根节点开始，处理每一层的 next 指针
    - 利用上一层已经建立好的 next 指针，来遍历当前层
    - 不需要队列，空间复杂度 O(1)
    
    时间复杂度：O(n)
    空间复杂度：O(1) - 只使用常数额外空间
    """
    if not root:
        return None
    
    # 从根节点开始，逐层处理
    leftmost = root  # 每一层最左边的节点
    
    while leftmost.left:
        # 遍历当前层，连接下一层的节点
        head = leftmost  # 当前层的遍历指针
        
        while head:
            # 连接当前节点的左右子节点
            head.left.next = head.right
            
            # 连接右子节点到下一个节点的左子节点
            if head.next:
                head.right.next = head.next.left
            
            # 移动到当前层的下一个节点
            head = head.next
        
        # 移动到下一层的最左节点
        leftmost = leftmost.left
    
    return root

def connect_next_pointer_dfs_ii(root: TreeNodeNext) -> TreeNodeNext: 
    """
    给定一个二叉树：
    struct Node {
    int val;
    Node *left;
    Node *right;
    Node *next;
    }
    填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL 。
    初始状态下，所有 next 指针都被设置为 NULL 。
    递归法
    """ 
    if not root: 
        return None

    def connect_(node): 
        # 节点为空或者为叶节点则不需要处理
        if not node or (not node.left and not node.right): 
            return 
        # 找到当前子树最右侧的节点（需要连接的目标）
        if node.right: 
            last = node.right
        elif node.left: 
            last = node.left
        else: 
            last = None
        # 连接左右节点
        if node.left and node.right: 
            node.left.next = node.right
        # 将last连接到右侧子树的第一个节点
        if last: 
            cur = node.next 
            while cur: 
                if cur.left: 
                    last.next = cur.left
                    break
                elif cur.right:
                    last.next = cur.right
                    break
                cur = cur.next
        #head = head.next 遍历当前层时， 依赖的是已经建立好的 next 指针 ，所以必须先建立右侧的 next 指针
        connect_(node.right)
        connect_(node.left)
    connect_(root)
    return root

def connect_next_pointer_iter_ii(root: TreeNodeNext) -> TreeNodeNext: 
    """
    给定一个二叉树：
    struct Node {
    int val;
    Node *left;
    Node *right;
    Node *next;
    }
    填充它的每个 next 指针，让这个指针指向其下一个右侧节点。如果找不到下一个右侧节点，则将 next 指针设置为 NULL 。
    初始状态下，所有 next 指针都被设置为 NULL 。
    迭代法
    """ 
    if not root: 
        return None 
    queue = deque([root])
    while queue: 
        level_size = len(queue) 
        prev = None
        for _ in range(level_size): 
            cur = queue.popleft() 
            if prev:
                prev.next = cur
            prev = cur 
            # 将当前节点的左右子节点添加到队列末尾
            if cur.left: 
                queue.append(cur.left)
            if cur.right: 
                queue.append(cur.right)
    return root

def maxdepth(root: TreeNode) -> int:
    """
    二叉树的最大深度
    
    题目：给定一个二叉树 root，返回其最大深度。
    二叉树的最大深度是指从根节点到最远叶子节点的最长路径上的节点数。
    
    示例：
        二叉树：
            3
           / \
          9  20
            /  \
           15   7
        
        最大深度为 3（路径：3 → 20 → 15 或 3 → 20 → 7）
    
    解法：递归（DFS）
    
    思路：
    - 空节点的深度为 0
    - 当前节点的深度 = max(左子树深度, 右子树深度) + 1
    - 递归计算左右子树的深度，取较大值加 1
    
    时间复杂度：O(n) - 每个节点访问一次
    空间复杂度：O(h) - h 为树的高度，递归栈的深度
    
    递归过程示例：
        对于树：
            3
           / \
          9  20
            /  \
           15   7
        
        maxdepth(3)
        = max(maxdepth(9), maxdepth(20)) + 1
        = max(1, max(maxdepth(15), maxdepth(7)) + 1) + 1
        = max(1, max(1, 1) + 1) + 1
        = max(1, 2) + 1
        = 3
    """
    # 基准情况：空节点的深度为 0
    if not root:
        return 0
    
    # 递归计算左子树的深度
    left_depth = maxdepth(root.left)
    
    # 递归计算右子树的深度
    right_depth = maxdepth(root.right)
    
    # 当前节点的深度 = 左右子树深度的最大值 + 1（当前节点本身）
    return max(left_depth, right_depth) + 1


def maxdepth_iterative(root: TreeNode) -> int:
    """
    二叉树的最大深度 - 迭代解法（BFS层序遍历）
    
    思路：
    - 使用层序遍历，每遍历一层，深度加 1
    - 遍历完所有层后，得到的层数就是最大深度
    
    时间复杂度：O(n)
    空间复杂度：O(w) - w 为树的最大宽度
    """
    if not root:
        return 0
    
    from collections import deque
    queue = deque([root])
    depth = 0
    
    while queue:
        # 当前层的节点数
        level_size = len(queue)
        
        # 处理当前层的所有节点
        for _ in range(level_size):
            node = queue.popleft()
            
            # 将子节点加入队列
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        # 当前层处理完毕，深度加 1
        depth += 1
    
    return depth

def minDepth_iter(root: Optional[TreeNode]) -> int:
    """
    给定一个二叉树，找出其最小深度。
    最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
    说明：叶子节点是指没有子节点的节点。
    
    使用 BFS（广度优先搜索）层序遍历实现
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(W)，W 为树的最大宽度，即队列的最大长度
    """
    # 如果根节点为空，深度为 0
    if not root: 
        return 0 
    
    from collections import deque
    # 初始化队列，将根节点加入队列
    queue = deque([root])
    # 初始化当前深度为 0
    depth = 0
    
    # 开始 BFS 层序遍历
    while queue: 
        # 获取当前层的节点数量
        size = len(queue)
        
        # 遍历当前层的所有节点
        for _ in range(size): 
            # 取出队首节点
            node = queue.popleft()
            
            # 如果当前节点是叶子节点（没有左右子节点），返回当前深度 + 1
            # 由于是 BFS，第一次遇到的叶子节点一定是最小深度
            if not node.left and not node.right: 
                return depth + 1
            
            # 将左子节点加入队列，准备下一层遍历
            if node.left: 
                queue.append(node.left)
            
            # 将右子节点加入队列，准备下一层遍历
            if node.right: 
                queue.append(node.right)
        
        # 当前层所有节点处理完毕，深度加 1
        depth += 1
    
    return depth


def minDepth_Recursive(root: Optional[TreeNode]) -> int:
    """
    给定一个二叉树，找出其最小深度（递归版本）。
    最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
    说明：叶子节点是指没有子节点的节点。
    
    使用 DFS（深度优先搜索）递归实现
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(H)，H 为树的高度，即递归栈的深度
    """
    # 如果根节点为空，深度为 0
    if not root:
        return 0
    
    # 如果当前节点是叶子节点，返回深度 1
    if not root.left and not root.right:
        return 1
    
    # 如果只有左子树，返回左子树的最小深度 + 1
    if not root.right:
        return minDepthRecursive(root.left) + 1
    
    # 如果只有右子树，返回右子树的最小深度 + 1
    if not root.left:
        return minDepthRecursive(root.right) + 1
    
    # 如果左右子树都存在，返回两者中的最小值 + 1
    return min(minDepthRecursive(root.left), minDepthRecursive(root.right)) + 1