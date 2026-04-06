"""
给定一个二叉树，找出其最小深度。
最小深度是从根节点到最近叶子节点的最短路径上的节点数量。
说明：叶子节点是指没有子节点的节点。
"""

# 二叉树节点定义
class TreeNode: 
    def __init__(self, val:int=0, left:TreeNode=None, right:TreeNode=None):
        self.val = val 
        self.left = left
        self.right = right

# 递归方法求最小深度
def min_depth(root: TreeNode) ->int: 
    # 空树深度为0
    if not root: 
        return 0 
    # 叶子节点深度为1
    if not root.left and not root.right: 
        return 1
    # 左子树为空，只计算右子树的最小深度
    if not root.left: 
        return min_depth(root.right) + 1
    # 右子树为空，只计算左子树的最小深度
    if not root.right: 
        return min_depth(root.left) + 1
    # 左右子树都存在，取两者最小深度的较小值加1
    if root.left and root.right: 
        return min(min_depth(root.left), min_depth(root.right)) + 1

# 迭代方法求最小深度（BFS层序遍历）
def min_depth_iter(root: TreeNode) ->int: 
    # 空树深度为0
    if not root: 
        return 0 
    from collections import deque
    queue = deque([root]) 
    depth = 0 

    while queue: 
        level_size = len(queue) 
        for _ in range(level_size): 
            node = queue.popleft() 
            # 遇到第一个叶子节点，立即返回当前深度+1
            if not node.left and not node.right: 
                return depth + 1
            if node.left: 
                queue.append(node.left)
            if node.right: 
                queue.append(node.right) 
        depth += 1
    
    return depth
