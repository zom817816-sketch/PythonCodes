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


def levelOrder_queue_reverse(root: TreeNode) -> list[list[int]]: 
    """
    给你二叉树的根节点 root ，返回其节点值 自底向上的层序遍历 。 （即按从叶子节点所在层到根节点所在的层，逐层从左向右遍历）
    """
    res = [] 
    queue = deque([root]) 

    while queue: 
        layer_size = len(queue) 
        current_level = [] 
        for _ in range(layer_size): 
            node = queue.popleft() 
            current_level.append(node.val) 
            if node.left: 
                queue.append(node.left) 
            if node.right: 
                queue.append(node.right) 
        res.append(current_level) 
    
    left, right = 0, len(res)-1 
    while left < right: 
        res[left], res[right] = res[right], res[left] 
        left += 1 
        right -= 1 
    
    return res 


def levelOrder_queue_right(root: TreeNode) -> list[list[int]]: 
    """
    给定一个二叉树的 根节点 root，想象自己站在它的右侧，按照从顶部到底部的顺序，返回从右侧所能看到的节点值。
    """
    if not root: 
        return []
    res = [] 
    queue = deque([root]) 
    while queue: 
        layer_size = len(queue)
        for _ in range(layer_size_size): 
            last = queue.popleft()
            if last.left: 
                queue.append(last.left) 
            if last.right: 
                queue.append(last.right) 
        res.append(last.val) 
    return res

def levelOrder_queue_avg(root: TreeNode) -> list[list[int]]: 
    """ 
    给定一个非空二叉树的根节点 root , 以数组的形式返回每一层节点的平均值。与实际答案相差 10-5 以内的答案可以被接受。
    """ 
    if not root: 
        return [] 
    
    res = [] 
    from collections import deque 
    queue = deque([root]) 

    while queue: 
        layer_size = len(queue) 
        cur = []
        for _ in range(layer_size): 
            node = queue.popleft() 
            cur.append(node.val) 
            if node.left: 
                queue.append(node.left) 
            if node.right: 
                queue.append(node.right) 
        res.append(cur)

    return [sum(level) / len(level) for level in res]    