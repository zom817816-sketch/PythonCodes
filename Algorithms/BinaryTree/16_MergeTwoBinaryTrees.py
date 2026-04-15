"""
给你两棵二叉树： root1 和 root2 。
想象一下，当你将其中一棵覆盖到另一棵之上时，两棵树上的一些节点将会重叠（而另一些不会）。你需要将这两棵树合并成一棵新二叉树。
合并的规则是：如果两个节点重叠，那么将这两个节点的值相加作为合并后节点的新值；否则，不为 null 的节点将直接作为新二叉树的节点。
返回合并后的二叉树。
注意: 合并过程必须从两个树的根节点开始。

示例：
树1：      树2：      合并后：
    1         2            3
   / \       / \          / \
  3   2     1   3      4   5
 /           / \      /     \
5           4   7    5       7
"""

from typing import Optional, List

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def mergeTrees(root1: TreeNode, root2: TreeNode) -> TreeNode:
    """
    合并两棵二叉树
    
    方法：递归解法⭐⭐⭐
    时间复杂度：O(n)，n 为两棵树中节点数的较小值
    空间复杂度：O(h)，h 为树的高度（递归栈深度）
    
    核心思路：
    1. 如果一个节点为空，直接返回另一个节点（不需要创建新节点）
    2. 如果两个节点都存在，创建新节点，值为两个节点值之和
    3. 递归处理左右子树
    
    Args:
        root1: 第一棵二叉树的根节点
        root2: 第二棵二叉树的根节点
    
    Returns:
        TreeNode: 合并后的二叉树根节点
    """
    
    # 终止条件 1：如果 root1 为空，直接返回 root2
    # 原因：不需要创建新节点，直接复用 root2 的子树
    # 例如：root1=None, root2=Node(5) → 返回 Node(5)
    if not root1:
        return root2
    
    # 终止条件 2：如果 root2 为空，直接返回 root1
    # 原因：不需要创建新节点，直接复用 root1 的子树
    # 例如：root1=Node(3), root2=None → 返回 Node(3)
    if not root2:
        return root1
    
    # 两个节点都存在，创建新节点，值为两个节点值相加
    # 这是合并的核心操作：重叠的节点值相加
    # 例如：root1.val=1, root2.val=2 → 创建 Node(3)
    root = TreeNode(root1.val + root2.val)
    
    # 递归合并左子树
    # 将 root1 的左子树和 root2 的左子树合并
    # 注意：递归内部会处理其中一个为空的情况
    root.left = mergeTrees(root1.left, root2.left)
    
    # 递归合并右子树
    # 将 root1 的右子树和 root2 的右子树合并
    # 注意：递归内部会处理其中一个为空的情况
    root.right = mergeTrees(root1.right, root2.right)
    
    # 返回当前节点（已合并左右子树）
    return root


def mergeTrees_iteration(root1: TreeNode, root2: TreeNode) -> TreeNode:
    """
    合并两棵二叉树（迭代解法，使用栈）
    时间复杂度：O(n)
    空间复杂度：O(n)
    
    思路：使用栈模拟递归，同时遍历两棵树
    
    Args:
        root1: 第一棵二叉树的根节点
        root2: 第二棵二叉树的根节点
    
    Returns:
        TreeNode: 合并后的二叉树根节点
    """
    if not root1:
        return root2
    if not root2:
        return root1
    
    # 创建新根节点
    root = TreeNode(root1.val + root2.val)
    
    # 使用栈存储待处理的节点对
    # 栈中存储元组：(root1的节点, root2的节点, 合并后的节点)
    stack = [(root1, root2, root)]
    
    while stack:
        node1, node2, merged_node = stack.pop()
        
        # 处理左子树
        if node1.left or node2.left:
            if node1.left and node2.left:
                # 两个左子节点都存在，创建新节点
                merged_node.left = TreeNode(node1.left.val + node2.left.val)
                # 将这对节点压入栈，待后续处理
                stack.append((node1.left, node2.left, merged_node.left))
            elif node1.left:
                # 只有 node1 有左子节点
                merged_node.left = node1.left
            else:
                # 只有 node2 有左子节点
                merged_node.left = node2.left
        
        # 处理右子树
        if node1.right or node2.right:
            if node1.right and node2.right:
                # 两个右子节点都存在，创建新节点
                merged_node.right = TreeNode(node1.right.val + node2.right.val)
                # 将这对节点压入栈，待后续处理
                stack.append((node1.right, node2.right, merged_node.right))
            elif node1.right:
                # 只有 node1 有右子节点
                merged_node.right = node1.right
            else:
                # 只有 node2 有右子节点
                merged_node.right = node2.right
    
    return root
