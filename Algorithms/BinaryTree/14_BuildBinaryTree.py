"""
根据一棵树的中序遍历与后序遍历构造二叉树。
注意: 你可以假设树中没有重复的元素。
例如，给出

    中序遍历 inorder = [9,3,15,20,7]
    后序遍历 postorder = [9,15,7,20,3]

构造出的二叉树为：
       3
      / \
     9  20
       /  \
      15   7

解题思路：
1. 后序遍历的最后一个元素是根节点
2. 在中序遍历中找到根节点的位置，将数组分为左右两部分
3. 递归构造左右子树
"""

from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def buildTree(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    方法一：递归解法（基础版）
    时间复杂度：O(n²)，每次查找根节点在中序遍历中的位置需要 O(n)
    空间复杂度：O(n)，递归栈的深度最坏为 n
    
    Args:
        inorder: 中序遍历数组
        postorder: 后序遍历数组
    
    Returns:
        TreeNode: 构造的二叉树根节点
    """
    if not inorder or not postorder:
        return None
    
    # 后序遍历的最后一个元素是根节点
    root_val = postorder[-1]
    root = TreeNode(root_val)
    
    # 在中序遍历中找到根节点的位置
    root_index = inorder.index(root_val)
    
    # 计算左子树的元素个数
    left_size = root_index
    
    # 递归构造左子树
    # 左子树的中序：inorder[0:root_index]
    # 左子树的后序：postorder[0:left_size]
    root.left = buildTree(inorder[:root_index], postorder[:left_size])
    
    # 递归构造右子树
    # 右子树的中序：inorder[root_index+1:]
    # 右子树的后序：postorder[left_size:-1]（去掉最后一个根节点）
    root.right = buildTree(inorder[root_index+1:], postorder[left_size:-1])
    
    return root


def buildTree_optimized(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    方法二：递归解法（优化版，使用哈希表）⭐⭐⭐
    时间复杂度：O(n)，使用哈希表将查找优化为 O(1)
    空间复杂度：O(n)，哈希表存储所有元素 + 递归栈
    
    Args:
        inorder: 中序遍历数组
        postorder: 后序遍历数组
    
    Returns:
        TreeNode: 构造的二叉树根节点
    """
    if not inorder or not postorder:
        return None
    
    # 构建中序遍历的值到索引的哈希表，快速查找根节点位置
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    
    # 使用索引范围避免数组切片，提高效率
    def helper(in_left: int, in_right: int, post_left: int, post_right: int) -> Optional[TreeNode]:
        """
        递归辅助函数，根据索引范围构造子树
        
        Args:
            in_left: 中序遍历的左边界索引
            in_right: 中序遍历的右边界索引
            post_left: 后序遍历的左边界索引
            post_right: 后序遍历的右边界索引
        
        Returns:
            TreeNode: 子树的根节点
        """
        if in_left > in_right or post_left > post_right:
            return None
        
        # 后序遍历的最后一个元素是当前子树的根节点
        root_val = postorder[post_right]
        root = TreeNode(root_val)
        
        # 在中序遍历中找到根节点的位置（O(1)）
        root_index = inorder_map[root_val]
        
        # 计算左子树的节点数
        left_size = root_index - in_left
        
        # 递归构造左子树
        root.left = helper(
            in_left,                    # 中序左边界
            root_index - 1,             # 中序右边界（根节点左边）
            post_left,                  # 后序左边界
            post_left + left_size - 1   # 后序右边界
        )
        
        # 递归构造右子树
        root.right = helper(
            root_index + 1,             # 中序左边界（根节点右边）
            in_right,                   # 中序右边界
            post_left + left_size,      # 后序左边界
            post_right - 1              # 后序右边界（去掉根节点）
        )
        
        return root
    
    return helper(0, len(inorder) - 1, 0, len(postorder) - 1)


def buildTree_iterative(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    方法三：迭代解法（使用栈）
    时间复杂度：O(n)
    空间复杂度：O(n)
    
    思路：
    1. 从后序遍历的最后一个元素开始构造
    2. 使用栈来保存已经构造好的节点
    3. 根据中序遍历的顺序确定父子关系
    
    Args:
        inorder: 中序遍历数组
        postorder: 后序遍历数组
    
    Returns:
        TreeNode: 构造的二叉树根节点
    """
    if not inorder or not postorder:
        return None
    
    # 构建中序遍历的值到索引的哈希表
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    
    # 后序遍历的最后一个元素是根节点
    root = TreeNode(postorder[-1])
    # 使用栈保存节点，后进先出
    stack = [root]
    # 从后序遍历倒数第二个元素开始处理
    post_index = len(postorder) - 2
    # 中序遍历的指针，用于判断当前节点应该作为左子还是右子
    inorder_index = len(inorder) - 1
    
    while post_index >= 0:
        # 从后序遍历中取出一个节点值
        node_val = postorder[post_index]
        post_index -= 1
        
        # 创建新节点
        node = TreeNode(node_val)
        
        # 如果当前节点值在中序遍历中的位置小于栈顶节点在中序遍历中的位置
        # 说明当前节点是栈顶节点的右子节点
        if inorder_map[node_val] > inorder_map[stack[-1].val]:
            stack[-1].right = node
        else:
            # 否则，需要找到当前节点应该作为哪个节点的左子节点
            # 弹出栈中所有在中序遍历中位置大于当前节点的节点
            while stack and inorder_map[node_val] < inorder_map[stack[-1].val]:
                parent = stack.pop()
            
            # 当前节点作为最后一个弹出节点的左子节点
            parent.left = node
        
        # 将当前节点压入栈中
        stack.append(node)
    
    return root


def buildTree_with_index_map(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:
    """
    方法四：使用索引数组的递归解法
    时间复杂度：O(n)
    空间复杂度：O(n)
    
    这种方法使用一个辅助数组来追踪后序遍历的索引位置
    
    Args:
        inorder: 中序遍历数组
        postorder: 后序遍历数组
    
    Returns:
        TreeNode: 构造的二叉树根节点
    """
    if not inorder or not postorder:
        return None
    
    # 构建中序遍历的值到索引的哈希表
    inorder_map = {val: idx for idx, val in enumerate(inorder)}
    # 后序遍历的指针，使用列表以便在递归中修改
    post_index = [len(postorder) - 1]
    
    def helper(in_left: int, in_right: int) -> Optional[TreeNode]:
        """
        递归辅助函数
        
        Args:
            in_left: 中序遍历的左边界
            in_right: 中序遍历的右边界
        
        Returns:
            TreeNode: 子树的根节点
        """
        if in_left > in_right:
            return None
        
        # 获取当前根节点的值（从后序遍历）
        root_val = postorder[post_index[0]]
        root = TreeNode(root_val)
        # 移动后序遍历指针
        post_index[0] -= 1
        
        # 获取根节点在中序遍历中的位置
        root_index = inorder_map[root_val]
        
        # 重要：先构造右子树，再构造左子树
        # 因为后序遍历是 左->右->根，所以倒序是 根->右->左
        root.right = helper(root_index + 1, in_right)
        root.left = helper(in_left, root_index - 1)
        
        return root
    
    return helper(0, len(inorder) - 1)
