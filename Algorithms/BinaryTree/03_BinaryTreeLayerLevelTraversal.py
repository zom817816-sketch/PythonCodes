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
        
        # 每层的最后一个节点，next 指向 None
        prev.next = None
    
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


def serialize_with_next(root: TreeNodeNext) -> list:
    """
    序列化带 next 指针的二叉树
    
    按层序遍历，用 '#' 表示每层的结束
    示例：[1,#,2,3,#,4,5,6,7,#]
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        
        for _ in range(level_size):
            node = queue.popleft()
            result.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append('#')  # 每层结束标记
    
    return result


# ============================================
# 测试代码
# ============================================
if __name__ == "__main__":
    """
    构建测试二叉树：
            3
           / \
          9  20
            /  \
           15   7
    
    预期层序遍历结果：[[3], [9, 20], [15, 7]]
    """
    
    # 构建二叉树
    root = TreeNode(3)
    root.left = TreeNode(9)
    root.right = TreeNode(20)
    root.right.left = TreeNode(15)
    root.right.right = TreeNode(7)
    
    print("="*60)
    print("二叉树层序遍历")
    print("="*60)
    print("\n测试二叉树结构：")
    print("        3")
    print("       / \\")
    print("      9   20")
    print("         /  \\")
    print("        15   7")
    print("\n预期结果: [[3], [9, 20], [15, 7]]")
    
    # 测试队列法
    print("\n" + "="*60)
    print("解法一：队列法（BFS）")
    print("="*60)
    result_queue = levelOrder_queue(root)
    print(f"结果: {result_queue}")
    
    # 打印队列法详细过程
    print_queue_process(root)
    
    # 测试递归法
    print("\n" + "="*60)
    print("解法二：递归法（DFS）")
    print("="*60)
    result_recursive = levelOrder_recursive(root)
    print(f"结果: {result_recursive}")
    
    # 打印递归法详细过程
    result_verbose = levelOrder_recursive_verbose(root)
    print(f"\n递归法最终结果: {result_verbose}")
    
    # 验证两种方法结果一致
    print("\n" + "="*60)
    print("验证")
    print("="*60)
    print(f"队列法结果: {result_queue}")
    print(f"递归法结果: {result_recursive}")
    print(f"结果一致: {result_queue == result_recursive}")
    
    # 测试自底向上
    print("\n" + "="*60)
    print("自底向上的层序遍历")
    print("="*60)
    result_bottom = levelOrder_bottom_up(root)
    print(f"结果: {result_bottom}")
    
    # 测试锯齿形
    print("\n" + "="*60)
    print("锯齿形层序遍历")
    print("="*60)
    result_zigzag = levelOrder_zigzag(root)
    print(f"结果: {result_zigzag}")
    
    # 测试每层最大值
    print("\n" + "="*60)
    print("每层最大值")
    print("="*60)
    result_max = levelOrder_max_value(root)
    print(f"结果: {result_max}")
    
    # 测试 next 指针
    print("\n" + "="*60)
    print("填充 next 指针")
    print("="*60)
    
    # 构建完美二叉树
    #       1
    #      / \
    #     2   3
    #    / \ / \
    #   4  5 6  7
    root_next = TreeNodeNext(1)
    root_next.left = TreeNodeNext(2)
    root_next.right = TreeNodeNext(3)
    root_next.left.left = TreeNodeNext(4)
    root_next.left.right = TreeNodeNext(5)
    root_next.right.left = TreeNodeNext(6)
    root_next.right.right = TreeNodeNext(7)
    
    print("\n完美二叉树结构：")
    print("        1")
    print("       / \\")
    print("      2   3")
    print("     / \ / \\")
    print("    4  5 6  7")
    
    # 测试 BFS 解法
    connect_next_pointer_bfs(root_next)
    result_bfs = serialize_with_next(root_next)
    print(f"\nBFS 解法序列化结果: {result_bfs}")
    print(f"预期结果: [1, '#', 2, 3, '#', 4, 5, 6, 7, '#']")
    
    # 测试 DFS 解法
    root_next2 = TreeNodeNext(1)
    root_next2.left = TreeNodeNext(2)
    root_next2.right = TreeNodeNext(3)
    root_next2.left.left = TreeNodeNext(4)
    root_next2.left.right = TreeNodeNext(5)
    root_next2.right.left = TreeNodeNext(6)
    root_next2.right.right = TreeNodeNext(7)
    
    connect_next_pointer_dfs(root_next2)
    result_dfs = serialize_with_next(root_next2)
    print(f"\nDFS 解法序列化结果: {result_dfs}")
    
    # 测试迭代解法
    root_next3 = TreeNodeNext(1)
    root_next3.left = TreeNodeNext(2)
    root_next3.right = TreeNodeNext(3)
    root_next3.left.left = TreeNodeNext(4)
    root_next3.left.right = TreeNodeNext(5)
    root_next3.right.left = TreeNodeNext(6)
    root_next3.right.right = TreeNodeNext(7)
    
    connect_next_pointer_iterative(root_next3)
    result_iter = serialize_with_next(root_next3)
    print(f"迭代解法序列化结果: {result_iter}")
