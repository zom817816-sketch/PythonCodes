"""
给定一个二叉树的 根节点 root，请找出该二叉树的 最底层 最左边 节点的值。
假设二叉树中至少有一个节点。

示例：
    输入：
        2
       / \
      1   3

    输出：1

    输入：
          1
         / \
        2   3
       /   / \
      4   5   6
         /
        7

    输出：7
"""

from typing import Optional


class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def findLeftBottomVal(root: Optional[TreeNode]) -> int:
    """
    BFS迭代方法：层序遍历找最底层最左边节点
    
    核心思想：
    1. 使用队列进行层序遍历
    2. 每层遍历时，记录该层第一个节点（最左边节点）的值
    3. 遍历结束后，最后一层记录的值就是答案
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(N)，最坏情况下队列存储所有节点
    
    Args:
        root: 二叉树根节点
        
    Returns:
        最底层最左边节点的值
    """
    if not root:
        return 0
    
    from collections import deque
    
    # 使用队列进行层序遍历
    queue = deque([root])
    left_val = 0  # 记录每层最左边节点的值

    # 层序遍历
    while queue:
        level_size = len(queue)
        
        # 遍历当前层的所有节点
        for i in range(level_size):
            node = queue.popleft()
            
            # 当前层第一个节点就是该层最左边的节点
            if i == 0:
                left_val = node.val
            
            # 将左右子节点加入队列（下一层）
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
    
    # 遍历结束后，left_val 就是最后一层最左边节点的值
    return left_val


def findLeftBottomValRecursive(root: Optional[TreeNode]) -> int:
    """
    DFS递归方法：先序遍历找最底层最左边节点
    
    核心思想：
    1. 使用先序遍历（根→左→右），保证同层级中左边的节点先被访问
    2. 维护两个变量：
       - max_depth：记录遍历到的最大深度
       - result：记录对应深度的节点值
    3. 每次发现更深的叶子节点时，更新这两个变量
    4. 由于先序遍历的特性，同一深度第一个被访问的叶子节点就是最左边的
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，H为树高，递归栈深度
    
    Args:
        root: 二叉树根节点
        
    Returns:
        最底层最左边节点的值
    """
    if not root:
        return 0
    
    # 使用 nonlocal 声明，允许在嵌套函数中修改外部变量
    nonlocal_variables = {
        'result': root.val,  # 初始化为根节点值
        'max_depth': 1       # 初始深度为1（根节点）
    }
    
    def dfs(node: Optional[TreeNode], depth: int) -> None:
        """
        深度优先遍历辅助函数
        
        Args:
            node: 当前遍历的节点
            depth: 当前节点的深度（根节点深度为1）
        """
    if not root:
        return 0
    
    # 使用列表存储状态变量，便于在嵌套函数中修改
    result = [root.val]  # result[0] 存储结果
    max_depth = [1]       # max_depth[0] 存储最大深度
    
    def dfs(node: Optional[TreeNode], depth: int) -> None:
        if not node:
            return
        
        # 遇到叶子节点
        if not node.left and not node.right:
            if depth > max_depth[0]:
                max_depth[0] = depth
                result[0] = node.val
                return
        
        # 先序遍历：根→左→右
        if node.left:
            dfs(node.left, depth + 1)
        if node.right:
            dfs(node.right, depth + 1)
    
    dfs(root, 1)
    
    return result[0]


if __name__ == "__main__":
    # 测试用例1
    #       2
    #      / \
    #     1   3
    root1 = TreeNode(2)
    root1.left = TreeNode(1)
    root1.right = TreeNode(3)
    
    print(f"  BFS方法结果: {findLeftBottomVal(root1)}")
    print(f"  递归方法结果: {findLeftBottomValRecursive(root1)}")

