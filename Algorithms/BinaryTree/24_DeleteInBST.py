"""
二叉搜索树（BST）删除节点
给定一个二叉搜索树的根节点 root 和一个值 key，删除二叉搜索树中的 key 对应的节点，
并保证二叉搜索树的性质不变。返回二叉搜索树（有可能被更新）的根节点的引用。

二叉搜索树性质：
- 左子树所有节点值 < 根节点值
- 右子树所有节点值 > 根节点值
- 左右子树也分别是二叉搜索树

删除节点的三种情况：
1. 叶子节点（无子节点）：直接删除，返回None
2. 只有一个子节点：用子节点替换，直接返回那个子节点
3. 有两个子节点：用后继节点（或前驱节点）替换，保持BST性质

为什么两个子节点要用后继/前驱替换？
- 后继节点是右子树中的最小值，比左子树所有值大，比右子树其他值小
- 这样替换后，BST的相对位置关系保持不变
"""

from typing import Optional


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


def deleteInBST_Successor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    递归删除BST中的节点 - 使用后继节点替换⭐⭐⭐
    
    后继节点：右子树中的最小值（即右子树最左边的节点）
    用后继节点替换后，BST性质得以保持
    
    算法步骤：
    1. 如果 key < root.val，说明目标在左子树，递归删除并更新左子树连接
    2. 如果 key > root.val，说明目标在右子树，递归删除并更新右子树连接
    3. 如果 key == root.val，找到目标节点，处理三种删除情况：
       - 叶子节点：直接删除（返回None）
       - 只有一个子节点：返回那个子节点
       - 有两个子节点：找到后继节点，替换值，然后在右子树删除后继节点
    
    时间复杂度：O(H) - H为树高
    空间复杂度：O(H) - 递归栈深度
    """
    # 【终止条件：空树或未找到】
    if root is None:
        return None
    
    # 【情况1：key 在左子树】
    # 根据BST性质，如果key小于当前节点值，目标一定在左子树
    if key < root.val:
        # 递归在左子树删除，删除后返回的新左子树根节点接回
        root.left = deleteInBST_Successor(root.left, key)
    
    # 【情况2：key 在右子树】
    elif key > root.val:
        # 递归在右子树删除，删除后返回的新右子树根节点接回
        root.right = deleteInBST_Successor(root.right, key)
    
    # 【找到目标节点：key == root.val】
    else:
        # 【情况1.1：叶子节点（无子节点）】
        # 直接删除，返回None让父节点断开连接
        if root.left is None and root.right is None:
            return None
        
        # 【情况1.2：只有一个子节点】
        # 用唯一子节点替换当前节点，直接返回那个子节点
        if root.left is None:
            # 只有右子节点，返回右子节点（替代当前节点位置）
            return root.right
        if root.right is None:
            # 只有左子节点，返回左子节点
            return root.left
        
        # 【情况1.3：两个子节点都有】
        # 策略：找到后继节点（右子树最小值）替换当前节点
        # 为什么用后继？因为后继节点的值刚好大于左子树所有值，小于右子树其他值
        
        # 找后继节点：右子树中最左边的节点（最小值）
        successor = root.right
        while successor.left is not None:
            successor = successor.left
        
        # 用后继节点的值替换当前节点的值（不是替换整个节点！）
        root.val = successor.val
        
        # 在右子树中删除后继节点
        # 注意：后继节点一定没有左子节点（因为它是最左边的）
        root.right = deleteInBST_Successor(root.right, successor.val)
    
    return root


#       
# 方法二：递归法 - 使用前驱节点替换
#       
def deleteInBST_with_predecessor(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    递归删除BST中的节点 - 使用前驱节点替换⭐⭐⭐
    
    前驱节点：左子树中的最大值（即左子树最右边的节点）
    适用于右子树比较高的场景，可能比后继方法更平衡
    
    时间复杂度：O(H)
    空间复杂度：O(H)
    """
    # 【终止条件】
    if root is None:
        return None
    
    # 【查找目标】
    if key < root.val:
        root.left = deleteInBST_Predecessor(root.left, key)
    elif key > root.val:
        root.right = deleteInBST_Predecessor(root.right, key)
    
    # 【找到目标节点】
    else:
        # 【叶子节点】
        if root.left is None:
            return root.right
        if root.right is None:
            return root.left
        
        # 【两个子节点都有 - 找前驱节点（左子树最大值）】
        predecessor = root.left
        while predecessor.right is not None:
            predecessor = predecessor.right
        
        # 用前驱节点的值替换
        root.val = predecessor.val
        
        # 在左子树中删除前驱节点
        root.left = deleteInBST_Predecessor(root.left, predecessor.val)
    
    return root


#       
# 方法三：迭代法（更直观的空间优化版本）
#       
def deleteInBST_iterative(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    迭代法删除BST中的节点⭐⭐⭐
    
    核心思路：
    1. 先找到要删除的节点及其父节点
    2. 根据目标节点的子节点情况处理删除
    3. 如果有两个子节点，用后继节点替换，然后删除后继节点
    
    优势：空间复杂度O(1)，不使用递归
    
    时间复杂度：O(H)
    空间复杂度：O(1)
    """
    if root is None:
        return None
    
    # 【第一步：找到目标节点和父节点】
    parent = None
    current = root
    
    # 遍历树寻找目标节点
    while current is not None and current.val != key:
        parent = current
        if key < current.val:
            current = current.left
        else:
            current = current.right
    
    # 没找到目标，直接返回
    if current is None:
        return root
    
    # 保存目标节点的引用
    target = current
    
    # 【第二步：处理有两个子节点的情况】
    # 需要先用后继节点替换，然后删除后继节点
    if target.left is not None and target.right is not None:
        # 找后继节点
        successor = target.right
        successor_parent = target
        while successor.left is not None:
            successor_parent = successor
            successor = successor.left
        
        # 用后继节点的值替换目标节点的值
        target.val = successor.val
        
        # 更新引用，准备删除后继节点
        target = successor
        parent = successor_parent
    
    # 【第三步：处理只有一个子节点或叶子节点的情况】
    # 确定要替换的子节点（可能为None）
    child = target.left if target.left is not None else target.right
    
    # 【第四步：断开目标节点的连接】
    if parent is None:
        # 要删除的是根节点，直接用child替换
        root = child
    elif parent.left is target:
        # 目标节点是父节点的左子节点
        parent.left = child
    else:
        # 目标节点是父节点的右子节点
        parent.right = child
    
    return root


#       
# 方法四：双指针迭代法（处理边界更优雅）
#       
def deleteInBST_two_pointers(root: Optional[TreeNode], key: int) -> Optional[TreeNode]:
    """
    迭代法删除BST - 使用虚拟父节点技巧⭐⭐⭐
    
    核心技巧：创建一个虚拟父节点(dummy)，让根节点成为它的子节点
    这样可以统一处理根节点删除的情况，无需特殊判断
    
    为什么需要虚拟父节点？
    - 如果要删除的是根节点，没有父节点可以更新
    - 使用虚拟父节点，根节点就变成了它的左子节点，处理逻辑统一
    
    时间复杂度：O(H)
    空间复杂度：O(1)
    """
    if root is None:
        return None
    
    # 创建虚拟父节点，指向根节点
    # 这样无论要删除什么节点，都有一个"父节点"可以更新
    dummy = TreeNode(0, right=root)
    parent = dummy
    
    # 【第一步：找到目标节点】
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
    
    # 【第二步：处理两个子节点的情况 - 用后继替换】
    if current.left and current.right:
        # 找后继节点
        successor = current.right
        successor_parent = current
        while successor.left:
            successor_parent = successor
            successor = successor.left
        
        # 用后继节点的值替换
        current.val = successor.val
        # 更新target为后继节点，准备删除
        current = successor
        parent = successor_parent
    
    # 【第三步：现在current最多只有一个子节点】
    # 确定要连接的子节点
    child = current.left if current.left else current.right
    
    # 【第四步：断开连接】
    if parent.left is current:
        parent.left = child
    else:
        parent.right = child
    
    # 返回真正的根节点（dummy.right）
    return dummy.right
