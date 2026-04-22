"""
二叉搜索树（BST）删除节点
给定一个二叉搜索树的根节点 root 和一个值 key，删除二叉搜索树中的 key 对应的节点，
并保证二叉搜索树的性质不变。返回二叉搜索树（有可能被更新）的根节点的引用。

二叉搜索树性质：
- 左子树所有节点值 < 根节点值
- 右子树所有节点值 > 根节点值
- 左右子树也分别是二叉搜索树

删除节点的三种情况：
1. 叶子节点（无子节点）：直接删除
2. 只有一个子节点：用子节点替换
3. 有两个子节点：用后继节点（或前驱节点）替换，保持BST性质
"""

from typing import Optional


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right    # 右子节点


def deleteInBST(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    递归删除BST中的节点⭐⭐⭐
    
    算法思路：
    1. 如果 key < root.val，说明目标在左子树，递归到左子树删除
    2. 如果 key > root.val，说明目标在右子树，递归到右子树删除
    3. 如果 key == root.val，找到目标节点，处理三种情况：
       - 叶子节点：直接删除（返回None）
       - 只有一个子节点：用唯一子节点替换
       - 有两个子节点：找到后继节点（右子树最左节点/最小值），替换当前节点
    
    时间复杂度：O(h)，h为树高度
    空间复杂度：O(h)，递归调用栈深度
    """
    # 基础情况：空树或遍历完未找到
    if root is None:
        return None
    
    # 情况1：key 在左子树  
    if key < root.val:
        # 递归在左子树删除，删除后更新左子树连接
        root.left = deleteInBST(root.left, key)
    
    # 情况2：key 在右子树  
    elif key > root.val:
        # 递归在右子树删除，删除后更新右子树连接
        root.right = deleteInBST(root.right, key)
    
    # 找到目标节点（key == root.val） 
    else:
        # 情况1.1：叶子节点  
        if root.left is None and root.right is None:
            return None  # 直接删除，返回None让其父节点断开连接
        
        # 情况1.2：只有一个子节点  
        if root.left is None:
            # 只有右子节点，用右子节点替换
            return root.right
        if root.right is None:
            # 只有左子节点，用左子节点替换
            return root.left
        
        # 情况1.3：两个子节点都有  
        # 找后继节点（右子树中的最小值，即右子树最左边的节点）
        successor = root.right
        while successor.left is not None:
            successor = successor.left
        
        # 用后继节点的值替换当前节点的值
        root.val = successor.val
        
        # 在右子树中删除后继节点（后继节点一定没有左子节点）
        root.right = deleteInBST(root.right, successor.val)
    
    return root


#       
# 方法二：递归法 - 使用前驱节点替换
#       
def deleteInBST_with_predecessor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    递归删除BST中的节点，使用前驱节点替换⭐⭐⭐
    
    前驱节点：左子树中的最大值（即左子树最右边的节点）
    适用于右子树较高的情况，可能平衡树的高度
    """
    if root is None:
        return None
    
    if key < root.val:
        root.left = deleteInBST_with_predecessor(root.left, key)
    elif key > root.val:
        root.right = deleteInBST_with_predecessor(root.right, key)
    else:
        # 找到目标节点
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        
        # 两个子节点都有：找前驱节点（左子树最大值）
        predecessor = root.left
        while predecessor.right is not None:
            predecessor = predecessor.right
        
        # 用前驱节点的值替换
        root.val = predecessor.val
        
        # 在左子树中删除前驱节点
        root.left = deleteInBST_with_predecessor(root.left, predecessor.val)
    
    return root


#       
# 方法三：迭代法（更直观的空间优化版本）
#       
def deleteInBST_iterative(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    迭代法删除BST中的节点⭐⭐⭐
    
    方法：
    1. 先找到要删除的节点及其父节点
    2. 根据情况处理删除
    3. 如果有两个子节点，用后继节点替换
    
    时间复杂度：O(h)
    空间复杂度：O(1)，不使用递归
    """
    if root is None:
        return None
    
    # 步骤1：找到目标节点和其父节点
    parent = None
    current = root
    target = root
    
    # 搜索目标节点
    while current is not None and current.val != key:
        parent = current
        if key < current.val:
            current = current.left
        else:
            current = current.right
    
    # 没找到
    if current is None:
        return root
    
    target = current  # 保存目标节点引用
    
    # 步骤2：处理目标节点的删除
    
    # 情况1：有两个子节点
    if target.left is not None and target.right is not None:
        # 找后继节点
        successor = target.right
        successor_parent = target
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left
        
        # 用后继节点的值替换目标
        target.val = successor.val
        
        # 更新target和parent引用，准备删除后继节点
        target = successor
        parent = successor_parent
    
    # 情况2或3：只有一个子节点或叶子节点
    # 确定要替换的子节点（如果有）
    child = target.left if target.left is not None else target.right
    
    # 步骤3：断开目标节点的连接
    if parent is None:
        # 要删除的是根节点
        root = child
    elif parent.left is target:
        parent.left = child
    else:
        parent.right = child
    
    return root


#       
# 方法四：双指针迭代法（处理边界更优雅）
#       
def deleteInBST_two_pointers(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    使用双指针的迭代法，更优雅地处理根节点删除⭐⭐⭐
    
    技巧：使用虚拟父节点(dummy)避免单独处理根节点
    """
    if root is None:
        return None
    
    # 创建虚拟父节点
    dummy = TreeNode(0, right=root)
    parent = dummy
    
    # 搜索目标节点
    current = root
    while current is not None:
        if current.val == key:
            break
        parent = current
        if key < current.val:
            current = current.left
        else:
            current = current.right
    
    # 没找到
    if current is None:
        return root
    
    # 处理找到的节点
    
    # 情况1：两个子节点 -> 找后继替换
    if current.left and current.right:
        successor = current.right
        successor_parent = current
        while successor.left:
            successor_parent = successor
            successor = successor.left
        
        current.val = successor.val
        current = successor
        parent = successor_parent
    
    # 现在current最多只有一个子节点
    child = current.left if current.left else current.right
    
    # 断开连接
    if parent.left is current:
        parent.left = child
    else:
        parent.right = child
    
    return dummy.right