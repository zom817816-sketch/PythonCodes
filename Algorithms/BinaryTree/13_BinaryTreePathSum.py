"""
给你二叉树的根节点 root 和一个表示目标和的整数 targetSum 。判断该树中是否存在 根节点到叶子节点 的路径，
这条路径上所有节点值相加等于目标和 targetSum 。如果存在，返回 true ；否则，返回 false 。
叶子节点 是指没有子节点的节点。
"""

from typing import Optional
from collections import deque

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def pathSum(root: TreeNode, targetSum: int) -> bool:
    """
    方法一：使用栈的迭代解法（DFS 深度优先搜索）
    时间复杂度：O(n)，n 为节点数
    空间复杂度：O(h)，h 为树的高度（栈的最大深度）
    
    Args:
        root: 二叉树的根节点
        targetSum: 目标和
    
    Returns:
        bool: 是否存在路径和等于 targetSum
    """
    if not root:
        return False
    
    # 栈中存储元组：(节点, 从根节点到当前节点的路径和)
    stack = [(root, root.val)]

    while stack:
        # 弹出栈顶元素（后进先出，实现 DFS）
        node, total = stack.pop()
        
        if not node:
            continue
        
        # 判断是否为叶子节点（左右子节点都为空）
        if not node.left and not node.right:
            # 检查路径和是否等于目标值
            if total == targetSum:
                return True
        
        # 先压入右子节点，再压入左子节点（保证左子节点先被处理）
        if node.right:
            stack.append((node.right, total + node.right.val))
        if node.left:
            stack.append((node.left, total + node.left.val))
    
    return False


def pathSum_backtrack(root: TreeNode, targetSum: int) -> bool:
    """
    方法二：回溯解法
    时间复杂度：O(n)
    空间复杂度：O(h)，h 为树的高度（递归深度）
    
    Args:
        root: 二叉树的根节点
        targetSum: 目标和
    
    Returns:
        bool: 是否存在路径和等于 targetSum
    """
    if not root:
        return False
    
    # values 存储当前路径上的节点值
    values = []

    def backtrack(node):
        """
        回溯函数，遍历所有路径
        
        Args:
            node: 当前节点
        """
        # 做选择：将当前节点值加入路径
        values.append(node.val)
        
        # 判断是否为叶子节点
        if not node.left and not node.right:
            # 计算当前路径和
            total = sum(values)
            if total == targetSum:
                return True
        else:
            # 尝试左子树
            if node.left:
                if backtrack(node.left):
                    return True
            # 尝试右子树
            if node.right:
                if backtrack(node.right):
                    return True
        
        # 撤销选择：回溯，移除当前节点值
        values.pop()
        return False
    
    return backtrack(root)


def pathSum_recursive(root: TreeNode, targetSum: int) -> bool:
    """
    方法三：递归解法（DFS 深度优先搜索）- 推荐
    时间复杂度：O(n)
    空间复杂度：O(h)，h 为树的高度
    
    Args:
        root: 二叉树的根节点
        targetSum: 目标和
    
    Returns:
        bool: 是否存在路径和等于 targetSum
    """
    if not root:
        return False
    
    # 递归终止条件：到达叶子节点
    if not root.left and not root.right:
        return root.val == targetSum
    
    # 递归判断左右子树，目标值减去当前节点值
    # 使用 or 运算，只要有一个子树满足条件即可
    return (pathSum_recursive(root.left, targetSum - root.val) or 
            pathSum_recursive(root.right, targetSum - root.val))


def pathSum_BFS(root: TreeNode, targetSum: int) -> bool:
    """
    方法四：BFS 广度优先搜索解法（使用队列）
    时间复杂度：O(n)
    空间复杂度：O(n)，最坏情况下队列中存储所有节点
    
    Args:
        root: 二叉树的根节点
        targetSum: 目标和
    
    Returns:
        bool: 是否存在路径和等于 targetSum
    """
    if not root:
        return False
    
    # 队列中存储元组：(节点, 从根节点到当前节点的路径和)
    queue = deque([(root, root.val)])

    while queue:
        # 弹出队首元素（先进先出，实现 BFS）
        node, total = queue.popleft()
        
        # 判断是否为叶子节点
        if not node.left and not node.right:
            if total == targetSum:
                return True
        
        # 先加入左子节点，再加入右子节点
        if node.left:
            queue.append((node.left, total + node.left.val))
        if node.right:
            queue.append((node.right, total + node.right.val))
    
    return False


def pathSum_recursive_optimized(root: TreeNode, targetSum: int) -> bool:
    """
    方法五：优化的递归解法（提前终止）
    在找到匹配路径后立即返回，避免不必要的递归
    
    Args:
        root: 二叉树的根节点
        targetSum: 目标和
    
    Returns:
        bool: 是否存在路径和等于 targetSum
    """
    if not root:
        return False
    
    # 减去当前节点值，传递给子节点
    targetSum -= root.val
    
    # 叶子节点判断
    if not root.left and not root.right:
        return targetSum == 0
    
    # 优先检查左子树（如果存在）
    if root.left:
        if pathSum_recursive_optimized(root.left, targetSum):
            return True
    
    # 检查右子树
    if root.right:
        if pathSum_recursive_optimized(root.right, targetSum):
            return True
    
    return False


def pathSum_sum_dfs(root: TreeNode, targetSum: int) -> bool:
    """
    方法六：前缀和解法（适用于需要返回所有路径的情况）
    时间复杂度：O(n)
    空间复杂度：O(n)
    
    Args:
        root: 二叉树的根节点
        targetSum: 目标和
    
    Returns:
        bool: 是否存在路径和等于 targetSum
    """
    if not root:
        return False
    
    # 前缀和哈希表：记录从根节点到当前节点的路径和的出现次数
    prefix_sum = {0: 1}  # 初始：路径和为0出现1次（根节点之前）
    
    def dfs(node, current_sum):
        """
        深度优先搜索
        
        Args:
            node: 当前节点
            current_sum: 从根节点到当前节点的路径和
        
        Returns:
            bool: 是否找到匹配的路径
        """
        if not node:
            return False
        
        # 计算当前路径和
        current_sum += node.val
        
        # 检查是否存在 (current_sum - targetSum) 的前缀和
        found = (current_sum - targetSum) in prefix_sum
        
        # 更新前缀和哈希表
        prefix_sum[current_sum] = prefix_sum.get(current_sum, 0) + 1
        
        # 递归处理子节点
        result = False
        if not node.left and not node.right:
            # 叶子节点
            result = found
        else:
            if node.left:
                if dfs(node.left, current_sum):
                    result = True
            if node.right and not result:
                if dfs(node.right, current_sum):
                    result = True
        
        # 回溯：恢复前缀和哈希表
        prefix_sum[current_sum] -= 1
        if prefix_sum[current_sum] == 0:
            del prefix_sum[current_sum]
        
        return result
    
    return dfs(root, 0)