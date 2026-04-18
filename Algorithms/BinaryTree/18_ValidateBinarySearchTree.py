"""
给你一个二叉树的根节点 root，判断其是否是一个有效的二叉搜索树。
有效二叉搜索树定义如下：
    - 节点的左子树只包含 严格小于 当前节点的数。
    - 节点的右子树只包含 严格大于 当前节点的数。
    - 所有左子树和右子树自身必须也是二叉搜索树。

题目分析：
- BST的核心性质：左子树的所有节点 < 当前节点 < 右子树的所有节点
- 不仅仅是直接子节点，而是整个子树都要满足这个约束
- 需要传递上下界信息来约束每个节点的有效范围

示例：
    输入：
        2
       / \
      1   3
    输出：true

    输入：
        5
       / \
      1   4
         / \
        3   6
    输出：false
    解释：根节点是5，右子树中的3 < 5，违反了BST的性质

    输入：
        10
       /
      5
       \
        15
    输出：false
    解释：15在10的左子树中，但15 > 10，违反了BST的性质
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def isValidBST(root: Optional[TreeNode]) -> bool:
    """
    递归方法：使用上下界约束验证BST
    
    核心思想：
    - 为每个节点定义一个有效范围 (min_val, max_val)
    - 根节点范围：(-∞, +∞)
    - 左子节点范围：(-∞, parent.val)
    - 右子节点范围：(parent.val, +∞)
    - 递归时传递这些约束，确保每个节点都在正确范围内
    
    递归三原则：
    1. 函数功能：判断以root为根的子树是否为有效的BST
    2. 终止条件：
       - root为空，返回True（空树是有效的BST）
       - root.val不在有效范围内，返回False
    3. 递归关系：
       - 递归左子树，更新上界为root.val
       - 递归右子树，更新下界为root.val
       - 返回左右子树的逻辑与结果
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，H为树高，递归栈深度
    
    Args:
        root: 二叉树的根节点
        
    Returns:
        如果是有效的BST返回True，否则返回False
    """
    def validate(node: Optional[TreeNode], min_val: float, max_val: float) -> bool:
        """
        辅助函数：验证节点值是否在有效范围内
        
        Args:
            node: 当前节点
            min_val: 节点值的最小边界（不包含）
            max_val: 节点值的最大边界（不包含）
            
        Returns:
            是否在有效范围内
        """
        if not node:
            return True
        
        # 检查当前节点值是否在有效范围内
        if node.val <= min_val or node.val >= max_val:
            return False
        
        # 递归验证左右子树
        # 左子树的上界变为当前节点值
        # 右子树的下界变为当前节点值
        return (validate(node.left, min_val, node.val) and 
                validate(node.right, node.val, max_val))
    
    # 根节点的范围是(-∞, +∞)
    return validate(root, float('-inf'), float('inf'))


def isValidBST_iter(root: Optional[TreeNode]) -> bool:
    """
    迭代方法：使用栈进行中序遍历
    
    核心思想：
    - BST的中序遍历结果是严格递增的
    - 利用这个性质，遍历时检查每个节点是否大于前一个节点
    - 使用显式栈模拟递归，避免递归深度限制
    
    算法步骤：
    1. 使用栈进行中序遍历（左->根->右）
    2. 记录前一个访问的节点值
    3. 每次访问新节点时，检查是否大于前一个节点值
    4. 如果出现 <= 的情况，说明不是BST
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，栈的深度
    
    Args:
        root: 二叉树的根节点
        
    Returns:
        如果是有效的BST返回True，否则返回False
    """
    if not root:
        return True
    
    stack = []
    current = root
    prev_val = None  # 记录前一个节点值
    
    while stack or current:
        # 一直向左走，将路径上的节点压入栈
        while current:
            stack.append(current)
            current = current.left
        
        # 弹出栈顶节点（中序遍历的顺序）
        current = stack.pop()
        
        # 检查是否严格递增
        if prev_val is not None and current.val <= prev_val:
            return False
        
        prev_val = current.val
        
        # 转向右子树
        current = current.right
    
    return True


def isValidBST_inorder_recursive(root: Optional[TreeNode]) -> bool:
    """
    递归中序遍历方法
    
    核心思想：
    - BST的中序遍历结果是严格递增的
    - 递归进行中序遍历，同时检查是否严格递增
    - 使用类成员变量或全局变量记录前一个节点值
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，递归栈深度
    
    Args:
        root: 二叉树的根节点
        
    Returns:
        如果是有效的BST返回True，否则返回False
    """
    prev_val = None  # 记录前一个节点值
    is_valid = True  # 记录是否有效
    
    def inorder(node: Optional[TreeNode]) -> None:
        """
        中序遍历辅助函数
        
        Args:
            node: 当前节点
        """
        nonlocal prev_val, is_valid
        
        if not node or not is_valid:
            return
        
        # 遍历左子树
        inorder(node.left)
        
        # 处理当前节点
        if prev_val is not None and node.val <= prev_val:
            is_valid = False
            return
        
        prev_val = node.val
        
        # 遍历右子树
        inorder(node.right)
    
    inorder(root)
    return is_valid


def isValidBST_minmax(root: Optional[TreeNode]) -> bool:
    """
    递归方法V2：计算子树的最大最小值
    
    核心思想：
    - 对于每个节点，验证其左子树的最大值 < 节点值
    - 验证其右子树的最小值 > 节点值
    - 递归计算每个子树的最小值和最大值
    
    算法步骤：
    1. 递归计算左子树的最小值和最大值
    2. 递归计算右子树的最小值和最大值
    3. 验证左子树最大值 < 当前节点值 < 右子树最小值
    
    时间复杂度：O(N²)，最坏情况下每个节点都要遍历整个子树
    空间复杂度：O(H)，递归栈深度
    
    注意：此方法时间复杂度较高，不推荐使用
    
    Args:
        root: 二叉树的根节点
        
    Returns:
        如果是有效的BST返回True，否则返回False
    """
    if not root:
        return True
    
    # 计算左子树的最大值
    def get_max(node: Optional[TreeNode]) -> int:
        """获取子树的最大值"""
        if not node:
            return float('-inf')
        return max(node.val, get_max(node.left), get_max(node.right))
    
    # 计算右子树的最小值
    def get_min(node: Optional[TreeNode]) -> int:
        """获取子树的最小值"""
        if not node:
            return float('inf')
        return min(node.val, get_min(node.left), get_min(node.right))
    
    # 验证当前节点
    left_max = get_max(root.left)
    right_min = get_min(root.right)
    
    if left_max >= root.val or right_min <= root.val:
        return False
    
    # 递归验证左右子树
    return isValidBST_minmax(root.left) and isValidBST_minmax(root.right)
