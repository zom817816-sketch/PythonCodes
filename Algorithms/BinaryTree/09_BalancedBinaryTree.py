"""
给定一个二叉树，判断它是否是平衡二叉树(平衡二叉树 是指该树所有节点的左右子树的高度相差不超过 1。)
"""

# 二叉树节点定义
class TreeNode: 
    def __init__(self, val:int=0, left:TreeNode=None, right:TreeNode=None):
        self.val = val 
        self.left = left
        self.right = right

def get_height(node: TreeNode) ->int: 
    """
    递归三原则应用：
    1. 函数功能：计算以node为根的树的高度
    2. 终止条件：node为空时返回0
    3. 递归关系：树的高度 = max(左子树高度, 右子树高度) + 1
    """
    if not node: 
        return 0 
    return max(get_height(node.left), get_height(node.right)) + 1

def isInstanced(root: TreeNode) ->bool: 
    """
    自顶向下递归方法
    时间复杂度O(n^2) 每个节点都要计算高度，每次高度计算的时间复杂度为O(n)
    
    递归三原则应用：
    1. 函数功能：判断以root为根的树是否是平衡二叉树
    2. 终止条件：root为空时返回True（空树是平衡的）
    3. 递归关系：当前节点平衡 && 左子树平衡 && 右子树平衡
    """ 
    if not root: 
        return True
    
    # 计算左右子树的高度
    left_height = get_height(node.left)
    right_height = get_height(node.right)

    # 检查左右子树之差
    if abs(left_height - right_height) > 1: 
        return False

    # 递归检查左右子树
    return isInstanced(root.left) and isInstanced(root.right)

def is_balanced_optimized(root: TreeNode) ->bool: 
    """ 
    自底向上递归方法，在计算高度的同时检查是否符合平衡二叉树
    时间复杂度O(n) 空间复杂度O(h)
    
    递归三原则应用：
    1. 函数功能：返回树的高度，如果不平衡则返回-1
    2. 终止条件：node为空时返回0
    3. 递归关系：当前高度 = max(左子树高度, 右子树高度) + 1，不平衡时返回-1
    """ 
    def check_height(node):
        if not node: 
            return 0
        
        # 递归检查左子树
        left_height = check_height(node.left) 
        if left_height == -1: 
            return -1 
        
        # 递归检查右子树
        right_height = check_height(node.right) 
        if right_height == -1: 
            return -1
        
        # 检查当前节点是否平衡 
        if abs(left_height - right_height) > 1: 
            return -1
        
        # 返回当前节点的高度
        return max(left_height, right_height) + 1

    return check_height(root) != -1

def is_balanced_iter(root: TreeNode) -> bool: 
    """
    迭代方法：使用栈模拟后序遍历
    时间复杂度O(n) 空间复杂度O(n)
    
    递归三原则的迭代实现：
    1. 函数功能：判断树是否平衡
    2. 终止条件：遇到不平衡节点立即返回False
    3. 递归关系：通过后序遍历自底向上计算高度并检查平衡性
    """ 
    if not root: 
        return True
    
    # 后序遍历：左 -> 右 -> 根
    heights = {} 
    stack = [(root, False)]

    while stack: 
        node, visited = stack.pop() 

        if not node: 
            heights[None] = 0 
            continue

        if visited: 
            # 计算当前节点高度
            left_height = heights.get(node.left, 0) 
            right_height = heights.get(node.right, 0) 

            # 检查平衡性 
            if abs(left_height - right_height) > 1: 
                return False
            
            heights[node] = max(left_height, right_height) + 1
        
        else: 
            # 后序遍历顺序：右 -> 左 -> 根（栈是后进先出）
            stack.append((node, True))
            stack.append((node.right, False))
            stack.append((node.left, False))
    
    return True