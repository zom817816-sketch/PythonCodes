"""
给你一个二叉树的根节点 root ， 检查它是否轴对称。
"""

class TreeNode: 
    def __init__(self, val: int=0, left: TreeNode= None, right: TreeNode=None): 
        self.val = val 
        self.left = left
        self.right = right

def isSymmetric(root: TreeNode) -> bool: 
    """
    检查二叉树是否轴对称（递归版本）
    
    使用递归比较左子树和右子树是否对称
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(H)，H 为树的高度，即递归栈的深度
    """
    # 如果根节点为空，认为是对称的
    if not root: 
        return True
    
    # 比较左子树和右子树是否对称
    return compare(root.left, root.right)


def compare(left: TreeNode, right: TreeNode) -> bool:
    """
    比较两棵子树是否对称
    
    对称条件：
    1. 两个节点都为空，对称
    2. 一个为空一个不为空，不对称
    3. 两个节点值不同，不对称
    4. 递归比较：左子树的左子节点 vs 右子树的右子节点（外侧）
               左子树的右子节点 vs 右子树的左子节点（内侧）
    """
    # 两个节点都为空，对称
    if not left and not right: 
        return True
    
    # 一个为空一个不为空，不对称
    if not left or not right: 
        return False
    
    # 两个节点值不同，不对称
    if left.val != right.val: 
        return False
    
    # 递归比较外侧：左子树的左子节点 vs 右子树的右子节点
    outside = compare(left.left, right.right)
    
    # 递归比较内侧：左子树的右子节点 vs 右子树的左子节点
    inside = compare(left.right, right.left)
    
    # 外侧和内侧都对称，则整体对称
    return outside and inside


def isSymmetricIterative(root: TreeNode) -> bool:
    """
    检查二叉树是否轴对称（迭代版本）
    
    使用队列进行层序遍历，成对比较节点
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(W)，W 为树的最大宽度，即队列的最大长度
    """
    # 如果根节点为空，认为是对称的
    if not root:
        return True
    
    from collections import deque
    # 初始化队列，将左右子节点成对加入队列
    queue = deque([root.left, root.right])
    
    # 开始遍历
    while queue:
        # 成对取出两个节点
        left = queue.popleft()
        right = queue.popleft()
        
        # 两个节点都为空，继续下一对
        if not left and not right:
            continue
        
        # 一个为空一个不为空，不对称
        if not left or not right:
            return False
        
        # 两个节点值不同，不对称
        if left.val != right.val:
            return False
        
        # 将下一层需要比较的节点成对加入队列
        # 外侧：左子树的左子节点 vs 右子树的右子节点
        queue.append(left.left)
        queue.append(right.right)
        
        # 内侧：左子树的右子节点 vs 右子树的左子节点
        queue.append(left.right)
        queue.append(right.left)
    
    # 所有节点都比较完毕，对称
    return True


                

