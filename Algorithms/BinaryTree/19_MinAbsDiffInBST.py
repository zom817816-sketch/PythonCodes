"""
给你一个二叉搜索树的根节点 root，返回树中任意两不同节点值之间的最小差值。
差值是一个正数，其数值等于两值之差的绝对值。

题目分析：
- 需要找到BST中任意两个节点之间的最小绝对值差
- BST的有序性质可以简化这个问题
- BST中序遍历结果是严格递增的，相邻节点差值最小

核心思想：
方法1：利用BST中序遍历的有序性
- BST的中序遍历结果是一个严格递增的序列
- 在有序序列中，最小差值一定出现在相邻元素之间
- 因此只需要比较中序遍历中相邻节点的差值

方法2：利用BST的搜索性质
- 对于每个节点，找到其前驱节点和后继节点
- 最小差值一定出现在节点与前驱或后继之间
- 时间复杂度：O(N log N)

示例：
    输入：
        4
       / \
      2   6
     / \   \
    1   3   7
    输出：1
    解释：最小差值是 2-1=1 或 3-2=1 或 4-3=1

    输入：
        1
         \
          3
         /
        2
    输出：1
    解释：中序遍历为 [1, 2, 3]，最小差值为 1
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def getMinimumDiff_iter(root: Optional[TreeNode]) -> int:
    """
    迭代方法：使用栈进行中序遍历⭐⭐⭐
    
    核心思想：
    - BST的中序遍历结果是严格递增的
    - 在有序序列中，最小差值一定出现在相邻元素之间
    - 使用栈模拟递归进行中序遍历，同时记录前一个节点值
    
    算法步骤：
    1. 使用栈进行中序遍历（左->根->右）
    2. 记录前一个访问的节点值
    3. 每次访问新节点时，计算与前一个节点的差值
    4. 更新最小差值
    
    注意事项：
    - 使用 is not None 显式检查，避免节点值为0时被误判为False
    - 计算差值时使用绝对值，虽然BST中序遍历是递增的，但显式使用abs更清晰
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，栈的深度等于树高
    
    Args:
        root: BST的根节点
        
    Returns:
        任意两不同节点值之间的最小差值
    """
    if not root:
        return 0
    
    min_diff = float("inf")  # 初始化最小差值为无穷大
    stack = []              # 显式栈，用于模拟递归
    current = root           # 当前指针，指向正在处理的节点
    prev_val = None        # 记录前一个访问的节点值
    
    while stack or current:
        # 阶段1：一直向左走，将路径上的节点压入栈
        while current:
            stack.append(current)
            current = current.left
        
        # 阶段2：弹出栈顶节点（中序遍历顺序：先左后根）
        current = stack.pop()
        
        # 阶段3：计算与前一个节点的绝对值差
        # 使用 is not None 显式检查，避免节点值为0时被误判为False
        # 例如：root=[100000,0]，访问到节点100000时，prev_val=0
        # if prev_val: 会判断为False，跳过计算，导致错误结果
        if prev_val is not None:
            diff = abs(current.val - prev_val)
            if diff < min_diff:
                min_diff = diff
        
        # 更新前一个节点值
        prev_val = current.val
        
        # 阶段4：转向右子树，准备下一轮循环
        current = current.right
    
    return min_diff


def getMinimumDiff_recursive(root: Optional[TreeNode]) -> int:
    """
    递归方法：使用中序遍历⭐⭐⭐
    
    核心思想：
    - 递归进行中序遍历（左->根->右）
    - 使用闭包变量记录前一个节点值和最小差值
    - 访问每个节点时，计算与前一个节点的差值并更新最小差值
    
    递归三原则：
    1. 函数功能：对以root为根的子树进行中序遍历，同时计算最小差值
    2. 终止条件：节点为空时返回
    3. 递归关系：左子树 -> 处理当前节点 -> 右子树
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，递归栈深度
    
    Args:
        root: BST的根节点
        
    Returns:
        任意两不同节点值之间的最小差值
    """
    if not root:
        return 0
    
    # 使用闭包变量在递归调用间共享状态
    min_diff = float("inf")
    prev_val = None
    
    def inorder(node: Optional[TreeNode]) -> None:
        """
        中序遍历辅助函数
        
        Args:
            node: 当前节点
        """
        nonlocal min_diff, prev_val
        
        if not node:
            return
        
        # 遍历左子树
        inorder(node.left)
        
        # 处理当前节点
        if prev_val is not None:
            diff = abs(node.val - prev_val)
            if diff < min_diff:
                min_diff = diff
        
        prev_val = node.val
        
        # 遍历右子树
        inorder(node.right)
    
    inorder(root)
    return min_diff


def getMinimumDiff_bruteforce(root: Optional[TreeNode]) -> int:
    """
    暴力方法：中序遍历后计算所有相邻差值
    
    核心思想：
    - 先进行中序遍历，得到有序数组
    - 然后遍历数组，计算所有相邻元素的差值
    - 返回最小差值
    
    优点：
    - 逻辑清晰，易于理解
    - 将问题分解为两个独立步骤
    
    缺点：
    - 需要额外的O(N)空间存储数组
    - 时间复杂度相同但常数因子较大
    
    时间复杂度：O(N)
    空间复杂度：O(N)，存储中序遍历结果
    
    Args:
        root: BST的根节点
        
    Returns:
        任意两不同节点值之间的最小差值
    """
    if not root:
        return 0
    
    # 中序遍历，得到有序数组
    values = []
    
    def inorder(node: Optional[TreeNode]) -> None:
        if not node:
            return
        inorder(node.left)
        values.append(node.val)
        inorder(node.right)
    
    inorder(root)
    
    # 计算相邻元素的差值，取最小值
    min_diff = float("inf")
    for i in range(1, len(values)):
        diff = abs(values[i] - values[i - 1])
        if diff < min_diff:
            min_diff = diff
    
    return min_diff


def getMinimumDiff_two_pointers(root: Optional[TreeNode]) -> int:
    """
    双指针方法：Morris中序遍历（空间O(1)）
    
    核心思想：
    - 使用Morris中序遍历，空间复杂度降到O(1)
    - Morris遍历通过临时修改树结构实现中序遍历
    - 遍历过程中记录前一个节点值，计算差值
    
    Morris遍历原理：
    - 对于当前节点，如果左子树为空，访问当前节点，转向右子树
    - 如果左子树不为空，找到左子树的最右节点（前驱节点）
      - 如果前驱节点的右子树为空，将其指向当前节点（建立临时链接）
      - 如果前驱节点的右子树指向当前节点（已访问），恢复为空，访问当前节点
    
    时间复杂度：O(N)，每个节点最多被访问两次
    空间复杂度：O(1)，只使用常量额外空间
    
    Args:
        root: BST的根节点
        
    Returns:
        任意两不同节点值之间的最小差值
    """
    if not root:
        return 0
    
    min_diff = float("inf")
    prev_val = None
    current = root
    
    while current:
        if not current.left:
            # 左子树为空，访问当前节点
            if prev_val is not None:
                diff = abs(current.val - prev_val)
                if diff < min_diff:
                    min_diff = diff
            prev_val = current.val
            current = current.right
        else:
            # 找到左子树的最右节点（前驱节点）
            predecessor = current.left
            while predecessor.right and predecessor.right != current:
                predecessor = predecessor.right
            
            if not predecessor.right:
                # 建立临时链接
                predecessor.right = current
                current = current.left
            else:
                # 恢复树结构，访问当前节点
                predecessor.right = None
                if prev_val is not None:
                    diff = abs(current.val - prev_val)
                    if diff < min_diff:
                        min_diff = diff
                prev_val = current.val
                current = current.right
    
    return min_diff