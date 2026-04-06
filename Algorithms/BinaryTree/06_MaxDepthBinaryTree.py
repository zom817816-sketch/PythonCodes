"""
给定一个二叉树 root ，返回其最大深度。
二叉树的 最大深度 是指从根节点到最远叶子节点的最长路径上的节点数。
"""

# 二叉树节点定义
class TreeNode: 
    def __init__(self, val:int=0, left:TreeNode=None, right:TreeNode=None):
        self.val = val 
        self.left = left
        self.right = right

# 递归方法求最大深度
def maxdepth(root: TreeNode) ->int: 
    if not root: 
        return 0 
    # 递归求左右子树的最大深度，取最大值加1
    return max(maxdepth(root.left), maxdepth(root.right)) + 1 

# 迭代方法求最大深度（BFS层序遍历）
def maxdepth_iter(root: TreeNode) ->int: 
    if not root: 
        return 0 

    from collections import deque
    queue = deque([root]) 
    depth = 0

    while queue: 
        level_size = len(queue) 
        for _ in range(level_size): 
            node = queue.popleft() 
            if node.left: 
                queue.append(node.left) 
            if node.right: 
                queue.append(node.right) 
        depth += 1
    
    return depth

"""
给定一个 N 叉树，找到其最大深度。
最大深度是指从根节点到最远叶子节点的最长路径上的节点总数。
N 叉树输入按层序遍历序列化表示，每组子节点由空值分隔（请参见示例）。
"""

class NTreeNode: 
    def __init__(self, val:int=0, children:list[NTreeNode]=None): 
        self.val = val 
        self.children = children 

def max_depth_n_tree(root: NTreeNode): 
    if not root: 
        return 0 
    if not root.children: 
        return 1 
    return max(max_depth_n_tree(child) for child in root.children) + 1

# 迭代方法
def max_depth_n_tree_iter(root: Node) -> int:
    if not root:
        return 0
    
    from collections import deque
    queue = deque([root])
    depth = 0
    
    while queue:
        level_size = len(queue)
        for _ in range(level_size):
            node = queue.popleft()
            queue.extend(node.children)
        depth += 1
    
    return depth