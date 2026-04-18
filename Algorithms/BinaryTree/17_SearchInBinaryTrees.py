"""
给定二叉搜索树（BST）的根节点 root 和一个整数值 val。
你需要在 BST 中找到节点值等于 val 的节点。返回以该节点为根的子树。如果节点不存在，则返回 null 。

题目分析：
- 二叉搜索树（BST）的性质：
  - 左子树的所有节点值 < 当前节点值
  - 右子树的所有节点值 > 当前节点值
  - 左右子树也都是BST

- 利用BST的有序性，可以进行高效的查找，每次比较都能排除一半的节点

示例：
    输入：root = [4,2,7,1,3], val = 2
        4
       / \
      2   7
     / \
    1   3
    输出：[2,1,3]
    解释：找到节点2，返回以2为根的子树

    输入：root = [4,2,7,1,3], val = 5
    输出：[]
    解释：节点5不存在，返回null
"""

from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right

def searchBST(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    递归方法：在BST中查找值为val的节点
    
    核心思想：
    - 利用BST的有序性进行二分查找
    - 每次递归都能排除一半的节点
    
    递归三原则：
    1. 函数功能：在以root为根的BST中查找值为val的节点
    2. 终止条件：
       - root为空，返回None（未找到）
       - root.val == val，返回root（找到目标）
    3. 递归关系：
       - root.val > val，递归左子树
       - root.val < val，递归右子树
    
    时间复杂度：O(log n)，平衡BST的情况；最坏O(n)，退化为链表
    空间复杂度：O(log n)，递归栈深度；最坏O(n)
    
    Args:
        root: BST的根节点
        val: 要查找的目标值
        
    Returns:
        找到的节点（以该节点为根的子树），未找到返回None
    """
    if not root:
        return None
    if root.val == val: 
        return None 
    elif root.val > val: 
        searchBST(root.left, val)
    elif root.val < val: 
        searchBST(root.right, val)


def searchBST_iter(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    迭代方法：在BST中查找值为val的节点⭐⭐⭐
    
    核心思想：
    - 使用while循环代替递归
    - 避免递归栈溢出的风险
    - 每次比较后直接移动到左子树或右子树
    
    算法步骤：
    1. 从根节点开始
    2. 比较当前节点值与val
    3. 根据比较结果向左或向右移动
    4. 直到找到目标或遇到空节点
    
    时间复杂度：O(log n)，平衡BST的情况；最坏O(n)
    空间复杂度：O(1)，只使用了常量级别的额外空间
    
    Args:
        root: BST的根节点
        val: 要查找的目标值
        
    Returns:
        找到的节点，未找到返回None
    """
    current = root
    
    while current:
        if current.val == val:
            return current
        elif current.val > val:
            current = current.left
        else:
            current = current.right
    
    return None 