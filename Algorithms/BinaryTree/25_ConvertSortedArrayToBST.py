"""
给你一个整数数组 nums ，其中元素已经按 升序 排列，请你将其转换为一棵 平衡 二叉搜索树。

核心思路：
- BST性质：左子树所有节点 < 根节点 < 右子树所有节点
- 平衡BST要求：左右子树高度差不超过1
- 有序数组的中值作为根节点，能保证树的平衡性

为什么这样是对的？
- 有序数组的中值分割后，左右两部分长度相差不超过1
- 这样递归构建的树，左右子树高度差不超过1
- 中值作为根节点，满足BST的有序性
"""

from typing import Optional, List


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


# 方法一：递归法（中值作为根）
def sortedArrayToBST_Recursive(nums: List[int]) -> Optional[TreeNode]:
    """
    递归法将有序数组转换为平衡BST⭐⭐
    
    核心思路：
    1. 选择数组的中值作为根节点
    2. 递归处理左半部分数组，构建左子树
    3. 递归处理右半部分数组，构建右子树
    
    为什么能保证平衡？
    - 中值分割后，左右两部分长度相差不超过1
    - 这样递归构建的左右子树高度差不超过1
    
    时间复杂度：O(N) - 每个元素都被访问一次
    空间复杂度：O(logN) - 递归栈深度，等于树的高度
    """
    # 【终止条件】
    # 数组为空，返回None
    if not nums:
        return None
    
    # 【选择中值作为根节点】
    # 使用整数除法，对于奇数长度数组，选择中间位置
    # 对于偶数长度数组，选择偏左的中间位置
    root_index = len(nums) // 2
    root_val = nums[root_index]
    
    # 【创建根节点】
    root = TreeNode(root_val)
    
    # 【递归构建左子树】
    # 左子树由左半部分数组构成
    root.left = sortedArrayToBST_Recursive(nums[:root_index])
    
    # 【递归构建右子树】
    # 右子树由右半部分数组构成
    root.right = sortedArrayToBST_Recursive(nums[root_index + 1:])
    
    return root


# 方法二：递归法（使用索引范围，避免切片）
def sortedArrayToBST_Recursive_Index(nums: List[int]) -> Optional[TreeNode]:
    """
    递归法 - 使用索引范围避免数组切片，更高效⭐⭐⭐
    
    核心思路与方法一相同，但使用左右指针来界定范围
    优点：避免了数组切片的开销，空间复杂度更低
    
    时间复杂度：O(N)
    空间复杂度：O(logN)
    """
    # 辅助函数，处理指定范围的数组
    def helper(left: int, right: int) -> Optional[TreeNode]:
        # 【终止条件】
        # 左指针超过右指针，范围为空
        if left > right:
            return None
        
        # 【选择中值作为根节点】
        mid = (left + right) // 2
        root = TreeNode(nums[mid])
        
        # 【递归构建左右子树】
        # 左子树：[left, mid-1]
        root.left = helper(left, mid - 1)
        # 右子树：[mid+1, right]
        root.right = helper(mid + 1, right)
        
        return root
    
    # 初始调用，处理整个数组范围
    return helper(0, len(nums) - 1)


# 方法三：迭代法（模拟递归）
def sortedArrayToBST_Iterative(nums: List[int]) -> Optional[TreeNode]:
    """
    迭代法将有序数组转换为平衡BST⭐⭐
    
    核心思路：
    使用栈模拟递归过程，栈中存储(左边界, 右边界, 父节点, 左/右标志)
    1. 初始时将整个数组范围压入栈
    2. 弹出栈顶元素，计算中值，创建节点
    3. 处理右子树和左子树（先右后左，保持与递归顺序一致）
    4. 将创建的节点连接到父节点
    
    时间复杂度：O(N)
    空间复杂度：O(logN) - 栈的深度
    """
    if not nums:
        return None
    
    # 栈元素：(left, right, parent, is_left)
    stack = [(0, len(nums) - 1, None, False)]
    root = None
    
    while stack:
        left, right, parent, is_left = stack.pop()
        
        if left > right:
            continue
        
        # 计算中值
        mid = (left + right) // 2
        current = TreeNode(nums[mid])
        
        # 第一次处理时，current就是根节点
        if not root:
            root = current
        # 否则连接到父节点
        else:
            if is_left:
                parent.left = current
            else:
                parent.right = current
        
        # 先处理右子树，再处理左子树（栈是后进先出）
        # 右子树：[mid+1, right]
        stack.append((mid + 1, right, current, False))
        # 左子树：[left, mid-1]
        stack.append((left, mid - 1, current, True))
    
    return root


# 方法四：递归法（选择不同的中值）
def sortedArrayToBST_Different_Mid(nums: List[int]) -> Optional[TreeNode]:
    """
    递归法 - 选择不同的中值策略⭐
    
    对于偶数长度的数组，可以选择不同的中值：
    - 方法一：选择偏左的中间位置 (left + right) // 2
    - 方法四：选择偏右的中间位置 (left + right + 1) // 2
    
    不同的选择会生成不同的平衡BST，但都是正确的
    
    时间复杂度：O(N)
    空间复杂度：O(logN)
    """
    def helper(left: int, right: int) -> Optional[TreeNode]:
        if left > right:
            return None
        
        # 选择偏右的中间位置（对于偶数长度数组）
        mid = (left + right + 1) // 2
        root = TreeNode(nums[mid])
        
        root.left = helper(left, mid - 1)
        root.right = helper(mid + 1, right)
        
        return root
    
    return helper(0, len(nums) - 1)


# 方法五：分治+队列（广度优先构建）
def sortedArrayToBST_Queue(nums: List[int]) -> Optional[TreeNode]:
    """
    分治法 + 队列构建⭐
    
    核心思路：
    1. 使用队列存储待处理的区间
    2. 每个区间对应一个父节点和左右标志
    3. 广度优先处理每个区间，构建树的结构
    
    这种方法更直观地展示了分治的过程
    
    时间复杂度：O(N)
    空间复杂度：O(N) - 队列空间
    """
    if not nums:
        return None
    
    # 队列元素：(left, right, parent, is_left)
    from collections import deque
    queue = deque()
    
    # 初始区间
    left, right = 0, len(nums) - 1
    mid = (left + right) // 2
    root = TreeNode(nums[mid])
    
    # 左右子区间入队
    queue.append((left, mid - 1, root, True))
    queue.append((mid + 1, right, root, False))
    
    while queue:
        l, r, parent, is_left = queue.popleft()
        
        if l > r:
            continue
        
        # 计算中值
        m = (l + r) // 2
        current = TreeNode(nums[m])
        
        # 连接到父节点
        if is_left:
            parent.left = current
        else:
            parent.right = current
        
        # 子区间入队
        queue.append((l, m - 1, current, True))
        queue.append((m + 1, r, current, False))
    
    return root
