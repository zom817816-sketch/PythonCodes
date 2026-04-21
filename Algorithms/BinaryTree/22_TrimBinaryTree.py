"""
给你二叉搜索树的根节点 root ，同时给定最小边界low 和最大边界 high。通过修剪二叉搜索树，使得所有节点的值在[low, high]中。修剪树 不应该 改变保留在树中的元素的相对结构 (即，如果没有被移除，原有的父代子代关系都应当保留)。 可以证明，存在 唯一的答案 。
所以结果应当返回修剪好的二叉搜索树的新的根节点。注意，根节点可能会根据给定的边界发生改变。
"""

from typing import Optional, List


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


def trimBST_Recursive(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    递归法修剪BST - 利用二叉搜索树的性质进行优化⭐⭐⭐
    
    BST性质：左子树所有节点 < 根节点 < 右子树所有节点
    
    核心思路：
    1. 如果当前节点值 < low，说明当前节点及其左子树都太小，全部丢弃
       → 只需要在右子树中继续修剪
    2. 如果当前节点值 > high，说明当前节点及其右子树都太大，全部丢弃
       → 只需要在左子树中继续修剪  
    3. 如果 low <= 当前节点值 <= high，当前节点保留
       → 递归修剪左右子树，并接回当前节点
    
    为什么可以直接丢弃一整棵子树？
    - 利用BST的有序性，如果root.val < low，则左子树所有值 < root.val < low，都不符合要求
    - 同理，如果root.val > high，则右子树所有值 > root.val > high，都不符合要求
    
    时间复杂度：O(N) - 最坏情况遍历所有节点
    空间复杂度：O(H) - 递归栈深度，H为树高
    """
    # 【终止条件】
    # 当前节点为空，无需修剪，直接返回
    if not root:
        return None
    
    # 【情况1：当前节点值太小】
    # root.val < low，说明当前节点和整个左子树都小于low
    # 根据BST性质，左子树所有值 < root.val < low，全都不符合条件
    # 所以直接丢弃当前节点和左子树，只在右子树中继续修剪
    if root.val < low:
        return trimBST_Recursive(root.right, low, high)
    
    # 【情况2：当前节点值太大】
    # root.val > high，说明当前节点和整个右子树都大于high
    # 根据BST性质，右子树所有值 > root.val > high，全都不符合条件
    # 所以直接丢弃当前节点和右子树，只在左子树中继续修剪
    if root.val > high:
        return trimBST_Recursive(root.left, low, high)
    
    # 【情况3：当前节点值在范围内】
    # low <= root.val <= high，当前节点保留
    # 递归修剪左右子树，将结果接回当前节点
    root.left = trimBST_Recursive(root.left, low, high)
    root.right = trimBST_Recursive(root.right, low, high)
    
    return root


def trimBST_General(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    通用递归法 - 不依赖BST性质，适用于任意二叉树⭐
    
    核心思路：
    1. 后序遍历：先处理左右子树，再处理当前节点
    2. 对于每个节点，检查其值是否在[low, high]范围内
    3. 如果不在范围内，需要"删除"当前节点，并合并左右子树
    
    删除节点的处理：
    - 当前节点值 < low：返回右子树（右子树中可能有符合条件的节点）
    - 当前节点值 > high：返回左子树（左子树中可能有符合条件的节点）
    
    注意：这种方法比方法一多做了很多无用功，因为不能利用BST性质剪枝
    
    时间复杂度：O(N) - 遍历所有节点
    空间复杂度：O(H) - 递归栈深度
    """
    # 【终止条件】
    if not root:
        return None
    
    # 【后序遍历：先处理子树】
    # 递归修剪左子树，得到新的左子树根节点
    root.left = trimBST_General(root.left, low, high)
    # 递归修剪右子树，得到新的右子树根节点
    root.right = trimBST_General(root.right, low, high)
    
    # 【处理当前节点】
    # 当前节点值小于下界，返回右子树（左子树已经处理过，但当前节点和左子树都太小）
    if root.val < low:
        return root.right
    
    # 当前节点值大于上界，返回左子树
    if root.val > high:
        return root.left
    
    # 当前节点值在范围内，保留当前节点
    return root


def trimBST_Iterative(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    迭代法修剪BST⭐
    
    核心思路：
    1. 首先找到新的根节点（第一个值在[low, high]范围内的节点）
    2. 然后分别修剪左子树（删除小于low的节点）和右子树（删除大于high的节点）
    
    为什么分两步？
    - 第一步：根节点可能不在范围内，需要找到新的根
    - 第二步：对于在范围内的根，只需要单向修剪（左子树只可能太小，右子树只可能太大）
    
    时间复杂度：O(N) - 每个节点最多访问一次
    空间复杂度：O(1) - 只使用常数额外空间
    """
    # 【第一步：找到新的根节点】
    # 根节点可能不在[low, high]范围内，需要调整
    # 如果root.val < low，根及其左子树都太小，向右移动
    # 如果root.val > high，根及其右子树都太大，向左移动
    while root and (root.val < low or root.val > high):
        if root.val < low:
            root = root.right  # 当前根太小，右子树可能有符合条件的节点
        else:
            root = root.left   # 当前根太大，左子树可能有符合条件的节点
    
    # 如果树为空，直接返回
    if not root:
        return None
    
    # 【第二步：修剪左子树】
    # 左子树中的节点只可能太小（< low），需要删除
    # 对于BST，左子树所有值 < 根节点值，而根节点值 >= low
    # 所以左子树中可能有部分节点 < low，需要修剪
    node = root
    while node.left:
        if node.left.val < low:
            # node.left及其左子树都太小，直接丢弃，接回右子树
            node.left = node.left.right
        else:
            # node.left符合要求，继续检查其左子树
            node = node.left
    
    # 【第三步：修剪右子树】
    # 右子树中的节点只可能太大（> high），需要删除
    node = root
    while node.right:
        if node.right.val > high:
            # node.right及其右子树都太大，直接丢弃，接回左子树
            node.right = node.right.left
        else:
            # node.right符合要求，继续检查其右子树
            node = node.right
    
    return root


def trimBST_Stack(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:
    """
    使用栈的迭代法 - 模拟递归过程⭐⭐⭐
    
    核心思路：
    使用栈保存需要处理的节点，对于每个节点：
    1. 如果值 < low，只处理右子树
    2. 如果值 > high，只处理左子树
    3. 如果在范围内，处理左右子树
    
    与方法三的区别：
    - 方法三是利用BST性质进行优化的高效迭代
    - 本方法更通用，思路更接近递归版本
    
    时间复杂度：O(N)
    空间复杂度：O(N) - 栈空间
    """
    if not root:
        return None
    
    # 处理根节点，找到第一个在范围内的节点作为新根
    while root and (root.val < low or root.val > high):
        if root.val < low:
            root = root.right
        else:
            root = root.left
    
    if not root:
        return None
    
    # 使用栈进行DFS
    stack = [root]
    
    while stack:
        node = stack.pop()
        
        # 修剪左子树：左子树只可能太小
        # 当前节点的左子节点值 < low，需要跳过（及其左子树）
        while node.left and node.left.val < low:
            node.left = node.left.right  # 接回右子树
        
        # 修剪右子树：右子树只可能太大
        # 当前节点的右子节点值 > high，需要跳过（及其右子树）
        while node.right and node.right.val > high:
            node.right = node.right.left  # 接回左子树
        
        # 将子节点入栈继续处理
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    return root
