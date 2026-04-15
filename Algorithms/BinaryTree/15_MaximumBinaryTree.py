"""
给定一个不重复的整数数组 nums 。 最大二叉树 可以用下面的算法从 nums 递归地构建:
    创建一个根节点，其值为 nums 中的最大值。
    递归地在最大值 左边 的 子数组前缀上 构建左子树。
    递归地在最大值 右边 的 子数组后缀上 构建右子树。
返回 nums 构建的 最大二叉树 。

示例：
输入：nums = [3, 2, 1, 6, 0, 5]
输出：
       6
      / \
     3   5
      \  /
       2 0
        \
         1
"""

from typing import Optional, List
from collections import deque

class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def constructMaximumBinaryTree(nums: List[int]) -> Optional[TreeNode]:
    """
    方法一：递归解法（基础版）
    时间复杂度：O(n²)，每次递归都要遍历找最大值
    空间复杂度：O(n)，递归栈的深度最坏为 n
    
    思路：
    1. 在当前数组范围内找到最大值及其索引
    2. 用最大值创建根节点
    3. 递归构建左子树（最大值左边）和右子树（最大值右边）
    
    Args:
        nums: 不重复的整数数组
    
    Returns:
        TreeNode: 构造的最大二叉树根节点
    """
    if not nums:
        return None

    def helper(start: int, end: int) -> Optional[TreeNode]:
        """
        递归辅助函数，处理 nums[start..end] 范围内的元素
        
        Args:
            start: 当前处理的起始索引（包含）
            end: 当前处理的结束索引（包含）
        
        Returns:
            TreeNode: 子树的根节点
        """
        if start > end:
            return None

        # 在 nums[start..end] 范围内找到最大值及其索引
        max_val = nums[start]
        max_index = start
        for i in range(start + 1, end + 1):
            if nums[i] > max_val:
                max_val = nums[i]
                max_index = i

        # 用最大值创建根节点
        root = TreeNode(max_val)

        # 递归构建左子树（最大值左边的子数组）
        root.left = helper(start, max_index - 1)
        # 递归构建右子树（最大值右边的子数组）
        root.right = helper(max_index + 1, end)

        return root

    return helper(0, len(nums) - 1)


def constructMaximumBinaryTree_simple(nums: List[int]) -> Optional[TreeNode]:
    """
    方法二：递归解法（简化版，使用 max() 和 index()）
    时间复杂度：O(n²)
    空间复杂度：O(n)
    
    思路：与方法一相同，但代码更简洁，使用 Python 内置函数
    
    Args:
        nums: 不重复的整数数组
    
    Returns:
        TreeNode: 构造的最大二叉树根节点
    """
    if not nums:
        return None
    
    # 找到当前数组的最大值
    max_val = max(nums)
    # 找到最大值的索引
    max_index = nums.index(max_val)
    
    # 创建根节点
    root = TreeNode(max_val)
    
    # 递归构建左子树（最大值左边）
    root.left = constructMaximumBinaryTree_simple(nums[:max_index])
    # 递归构建右子树（最大值右边）
    root.right = constructMaximumBinaryTree_simple(nums[max_index + 1:])
    
    return root


def constructMaximumBinaryTree_stack(nums: List[int]) -> Optional[TreeNode]:
    """
    方法三：单调栈解法（最优解）⭐⭐⭐
    时间复杂度：O(n)，每个元素最多入栈出栈一次
    空间复杂度：O(n)，栈的空间
    
    核心思想：
    1. 使用单调递减栈（栈中元素从底到顶递减）
    2. 遍历数组，对于每个元素，它比栈顶元素大时，弹出栈顶元素
    3. 弹出的元素成为当前元素的左子节点
    4. 当前元素成为新栈顶元素的右子节点
    
    关键原理：
    - 新元素 < 栈顶：当前元素在栈顶右边且更小 → 应该是栈顶的右子节点
    - 新元素 > 栈顶：当前元素在栈顶右边且更大 → 应该成为栈顶的祖先
    - 一个元素的父节点是它左右两边第一个比它大的元素中较小的那个
    
    Args:
        nums: 不重复的整数数组
    
    Returns:
        TreeNode: 构造的最大二叉树根节点
    """
    if not nums:
        return None
    
    # 栈中存储 TreeNode，保持单调递减（栈底->栈顶）
    stack = []
    
    for num in nums:
        # 创建当前节点
        node = TreeNode(num)
        
        # 当栈不为空且当前元素比栈顶元素大时
        # 原理：当前元素在栈顶右边且更大 → 应该成为栈顶的祖先
        while stack and num > stack[-1].val:
            # 弹出栈顶元素，并设置其为当前节点的左子节点
            left_child = stack.pop()
            node.left = left_child
        
        # 如果栈不为空，当前节点应该成为栈顶元素的右子节点
        # 原理：当前元素在栈顶右边且更小 → 应该在栈顶的右子树中
        if stack:
            stack[-1].right = node
        
        # 将当前节点压入栈中
        stack.append(node)
    
    # 栈底元素就是最终的根节点
    return stack[0]


def constructMaximumBinaryTree_divide_conquer(nums: List[int]) -> Optional[TreeNode]:
    """
    方法五：分治法（使用辅助函数找最大值）
    时间复杂度：O(n²)
    空间复杂度：O(n)
    
    与方法一类似，但代码结构更清晰
    
    Args:
        nums: 不重复的整数数组
    
    Returns:
        TreeNode: 构造的最大二叉树根节点
    """
    if not nums:
        return None
    
    def find_max_index(start: int, end: int) -> int:
        """
        在 nums[start..end] 范围内找到最大值的索引
        
        Args:
            start: 起始索引
            end: 结束索引
        
        Returns:
            int: 最大值的索引
        """
        max_index = start
        for i in range(start + 1, end + 1):
            if nums[i] > nums[max_index]:
                max_index = i
        return max_index
    
    def build(start: int, end: int) -> Optional[TreeNode]:
        """
        递归构建子树
        
        Args:
            start: 起始索引
            end: 结束索引
        
        Returns:
            TreeNode: 子树的根节点
        """
        if start > end:
            return None
        
        # 找到最大值的索引
        max_index = find_max_index(start, end)
        
        # 创建根节点
        root = TreeNode(nums[max_index])
        
        # 递归构建左右子树
        root.left = build(start, max_index - 1)
        root.right = build(max_index + 1, end)
        
        return root
    
    return build(0, len(nums) - 1)
