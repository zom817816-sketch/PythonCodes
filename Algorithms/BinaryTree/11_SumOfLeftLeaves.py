"""
给定二叉树的根节点 root ，返回所有左叶子之和。
左叶子是指某个节点的左子节点，且该左子节点没有子节点。

示例：
    输入：
        3
       / \
      9  20
        /  \
       15   7

    输出：24

    解释：在这个二叉树中，有两个左叶子：9 和 15，所以返回 9 + 15 = 24
"""

# 问题理解：
# 左叶子定义：某个节点的左子节点，且该左子节点本身是叶子节点（没有左右子节点）。
# 核心思路：
# 递归遍历二叉树，对于每个节点，判断其左子节点是否为叶子节点，如果是，则累加其值；否则，继续递归遍历。
# 递归三原则：
# 1. 递归终止条件：当节点为空时，返回0。
# 2. 递归调用：对于每个节点，递归调用 sumOfLeftLeaves 函数，分别计算其左子树和右子树的左叶子之和。
# 3. 递归返回值：将左子树和右子树的左叶子之和相加，得到当前节点的左叶子之和。


from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def sumOfLeftLeaves(root):
    """
    递归方法：计算二叉树中所有左叶子之和

    递归三原则应用：
    1. 函数功能：返回以当前节点为根的子树中所有左叶子之和
    2. 终止条件：
       - 当前节点为空，返回0
       - 当前节点是叶子节点（无子节点），返回0（因为叶子节点本身不是左叶子）
    3. 递归关系：
       - 如果当前节点的左子节点是叶子节点，加上左子节点值并递归右子树
       - 否则，递归左右子树并返回和

    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，H为树高，递归栈深度

    Args:
        root: 二叉树根节点

    Returns:
        所有左叶子节点值之和
    """
    if not root:
        return 0

    if not root.left and not root.right:
        return 0

    if root.left and not root.left.left and not root.left.right:
        return root.left.val + sumOfLeftLeaves(root.right)

    return sumOfLeftLeaves(root.left) + sumOfLeftLeaves(root.right)


def sumOfleftLeaves_recursive_improved(root):
    """
    递归方法改进版：使用辅助函数跟踪是否为左子节点

    递归三原则应用：
    1. 函数功能：返回以当前节点为根的子树中所有左叶子之和
       辅助函数功能：返回以当前节点为根的子树中左叶子之和，当前节点是否为左子节点
    2. 终止条件：
       - 当前节点为空，返回0
       - 当前节点是叶子节点，如果是左子节点返回节点值，否则返回0
    3. 递归关系：左子树结果 + 右子树结果

    相比原版改进：
    - 逻辑更清晰，通过is_left参数明确标记是否为左子节点
    - 避免了重复判断左子节点是否为叶子节点

    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，H为树高，递归栈深度

    Args:
        root: 二叉树根节点

    Returns:
        所有左叶子节点值之和
    """

    def helper(node: TreeNode, is_left: bool) -> int:
        """
        辅助函数：返回以当前节点为根的子树中左叶子之和，当前节点是否为左子节点

        Args:
            node: 当前节点
            is_left: 当前节点是否为左子节点

        Returns:
            左叶子之和
        """
        if not node:
            return 0
        # 叶子节点：如果是左子节点则返回其值，否则返回0
        if not node.left and not node.right:
            return node.val if is_left else 0

        # 递归：左子节点标记为True，右子节点标记为False
        left_sum = helpful(node.left, True)
        right_sum = helpful(node.right, False)

        return left_sum + right_sum

    return helper(root, False)


def sumOfLeftLeaves_iterative(root: "TreeNode") -> int:
    """
    迭代DFS方法：使用栈模拟递归，深度优先遍历

    核心思想：
    - 使用栈实现深度优先遍历（DFS）
    - 栈元素：(节点, 是否为左子节点)
    - 遍历时检查每个叶子节点，如果是左子节点则累加其值

    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(N)，最坏情况下栈存储所有节点

    Args:
        root: 二叉树根节点

    Returns:
        所有左叶子节点值之和
    """
    if not root:
        return 0

    stack = [(root, False)]
    total = 0

    while stack:
        node, is_left = stack.pop()
        # 叶子节点：如果是左子节点则累加
        if not node.left and not node.right:
            if is_left:
                total += node.val
                continue
        # 压栈：先压右子节点再压左子节点(左子节点先处理)
        if node.right:
            stack.append((node.right, False))
        if node.left:
            stack.append((node.left, True))

    return total


def sumOfLeftLeaves_bfs(root: "TreeNode") -> int:
    """
    BFS迭代方法：使用队列进行层序遍历

    核心思想：
    - 使用队列实现广度优先遍历（BFS）
    - 队列元素：(节点, 是否为左子节点)
    - 按层级遍历，检查每个叶子节点，如果是左子节点则累加其值

    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(N)，最坏情况下队列存储所有节点

    Args:
        root: 二叉树根节点

    Returns:
        所有左叶子节点值之和
    """
    if not root:
        return 0

    from collections import deque

    queue = deque([root, False])
    total = 0

    while queue:
        node, is_left = queue.popleft()
        # 叶子节点：如果是左子节点则累加其值
        if not node.left and not node.right:
            if is_left:
                total += node.val
            continue
        # 入队：先入左子节点，再入右子节点（BFS按层级从左到右）
        if node.left:
            queue.append((node.left, True))
        if node.right:
            queue.append((node.right, False))

    return total
