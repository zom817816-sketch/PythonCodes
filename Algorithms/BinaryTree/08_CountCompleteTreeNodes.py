"""
给你一棵 完全二叉树 的根节点 root ，求出该树的节点个数。
完全二叉树 的定义如下：在完全二叉树中，除了最底层节点可能没填满外，其余每层节点数都达到最大值，并且最下面一层的节点都集中在该层最左边的若干位置。
若最底层为第 h 层（从第 0 层开始），则该层包含 1~ 2h 个节点。
"""

# 二叉树节点定义
class TreeNode: 
    def __init__(self, val:int=0, left:TreeNode=None, right:TreeNode=None):
        self.val = val 
        self.left = left
        self.right = right

# 迭代方法：BFS层序遍历统计节点数
def count_nodes_iter(root: TreeNode) ->int: 
    # 空树返回0
    if not root: 
        return 0 
    from collections import deque
    queue = deque([root]) 
    total = 0
    # 层序遍历，每层统计节点数
    while queue: 
        level_size = len(queue) 
        total += level_size 
        for _ in range(level_size): 
            node = queue.popleft() 
            if node.left: 
                queue.append(node.left) 
            if node.right: 
                queue.append(node.right) 
    return total

# 递归方法：普通二叉树节点计数
def count_nodes_recursive(root: TreeNode) ->int:
    # 空树返回0
    if not root: 
        return 0 
    # 叶子节点返回1
    if not root.left and not root.right: 
        return 1
    # 递归计算左右子树节点数，加上当前节点
    return count_nodes_recursive(root.left) + count_nodes_recursive(root.right) + 1

# 优化方法：利用完全二叉树特性，时间复杂度 O(log n * log n)
def count_nodes_optimized(root: TreeNode) ->int:
    # 空树返回0
    if not root: 
        return 0 
    
    # 计算树的深度（一直向左走）
    def get_depth(node):
        depth = 0
        while node:
            depth += 1
            node = node.left
        return depth
    
    left_depth = get_depth(root.left)
    right_depth = get_depth(root.right)
    
    # 如果左右子树深度相同，说明左子树是满二叉树
    if left_depth == right_depth:
        # 左子树节点数 + 右子树节点数 + 根节点
        # 满二叉树节点数公式：2^depth - 1
        return (1 << left_depth) + count_nodes_optimized(root.right)
    else:
        # 左子树深度大于右子树，说明右子树是满二叉树
        return (1 << right_depth) + count_nodes_optimized(root.left)