"""
给你一个二叉树的根节点 root ，按 任意顺序 ，返回所有从根节点到叶子节点的路径。
叶子节点 是指没有子节点的节点。

题目要求：
1. 从根节点出发
2. 遍历到每个叶子节点
3. 记录每条路径的节点值，用"->"连接

示例：
    输入：root = [1,2,3,null,5]
    输出：["1->2->5","1->3"]
"""

from typing import List, Optional

class TreeNode: 
    def __init__(self, val:int=0, left:Optional['TreeNode']=None, right:Optional['TreeNode']=None):
        self.val = val 
        self.left = left
        self.right = right


def get_paths_dfs(root: Optional[TreeNode]) -> List[str]: 
    """
    DFS递归方法：深度优先遍历二叉树
    
    递归三原则应用：
    1. 函数功能：返回从当前节点到所有叶子节点的路径
    2. 终止条件：遇到叶子节点，返回包含当前节点的路径
    3. 递归关系：当前节点路径 + 左子树路径 + 右子树路径
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，H为树高，递归栈深度
    
    Args:
        root: 二叉树根节点
        
    Returns:
        所有的根节点到叶子节点的路径列表
    """
    if not root: 
        return [] 
    
    res = []
    
    def dfs(node: Optional[TreeNode], path: str) -> None:
        """
        深度优先遍历辅助函数
        
        Args:
            node: 当前遍历的节点
            path: 从根节点到当前节点父节点的路径字符串
        """
        # 构建当前路径：将当前节点值拼接到已有路径
        current_path = path + str(node.val)

        # 终止条件：叶子节点（没有左右子节点）
        if not node.left and not node.right: 
            res.append(current_path) 
            return
        
        # 非叶子节点：添加箭头并继续递归
        current_path += "->"
        
        # 递归遍历左子树
        if node.left: 
            dfs(node.left, current_path)
        
        # 递归遍历右子树
        if node.right: 
            dfs(node.right, current_path)
    
    # 从根节点开始DFS遍历
    dfs(root, "")
    return res


def get_paths_dfs_iter(root: Optional[TreeNode]) -> List[str]: 
    """
    DFS迭代方法：使用栈模拟递归，避免递归栈溢出
    
    栈元素：(节点, 当前路径)
    栈的特点：后进先出（LIFO），保证深度优先
    
    时间复杂度：O(N)
    空间复杂度：O(N)，最坏情况下栈存储所有节点
    
    Args:
        root: 二叉树根节点
        
    Returns:
        所有的根节点到叶子节点的路径列表
    """
    if not root: 
        return [] 
    
    res = []
    # 栈存储元组：(节点, 从根到该节点的路径)
    stack = [(root, str(root.val))]

    while stack: 
        # 弹出栈顶元素（后进先出）
        node, path = stack.pop()

        # 终止条件：叶子节点，将路径加入结果
        if not node.left and not node.right: 
            res.append(path)
            continue
            
        # 压栈：先压右子节点，再压左子节点
        # 这样弹栈时左子节点先处理（DFS的左优先）
        if node.right:
            stack.append((node.right, f"{path}->{node.right.val}"))
        if node.left: 
            stack.append((node.left, f"{path}->{node.left.val}"))
        
    return res


def get_paths_bfs_iter(root: Optional[TreeNode]) -> List[str]: 
    """
    BFS迭代方法：使用队列进行层序遍历
    
    队列元素：(节点, 当前路径)
    队列的特点：先进先出（FIFO），保证广度优先
    
    时间复杂度：O(N)
    空间复杂度：O(N)，最坏情况下队列存储所有节点
    
    Args:
        root: 二叉树根节点
        
    Returns:
        所有的根节点到叶子节点的路径列表
    """
    if not root: 
        return []
    
    res = []
    # 队列存储元组：(节点, 从根到该节点的路径)
    queue = [(root, str(root.val))]

    while queue: 
        # 出队（先进先出）
        node, path = queue.pop(0)

        # 终止条件：叶子节点，将路径加入结果
        if not node.left and not node.right:
            res.append(path)
            continue
            
        # 入队：先入左子节点，再入右子节点
        # BFS按层级遍历，同一层级从左到右处理
        if node.left: 
            queue.append((node.left, f"{path}->{node.left.val}"))
        if node.right:
            queue.append((node.right, f"{path}->{node.right.val}"))
    
    return res


def get_paths_backtrack(root: Optional[TreeNode]) -> List[str]: 
    """
    回溯法：使用路径列表动态维护当前路径
    
    回溯核心思想：
    1. 做选择：将当前节点加入路径
    2. 递归：进入下一层
    3. 撤销选择：将当前节点移出路径（回溯）
    
    相比字符串拼接，使用列表可以减少字符串复制开销
    
    时间复杂度：O(N)
    空间复杂度：O(H)，路径列表长度不超过树高
    
    Args:
        root: 二叉树根节点
        
    Returns:
        所有的根节点到叶子节点的路径列表
    """
    if not root: 
        return []
    
    res = []
    # 使用列表存储当前路径，便于动态添加和删除
    path = []

    def backtrack(node: Optional[TreeNode]) -> None:
        """
        回溯递归函数
        
        Args:
            node: 当前遍历的节点
        """
        # 做选择：将当前节点值加入路径
        path.append(str(node.val))

        # 终止条件：叶子节点
        if not node.left and not node.right: 
            # 将路径列表用"->"连接后加入结果
            res.append("->".join(path))
        else:
            # 递归处理左子树
            if node.left:
                backtrack(node.left)
            
            # 递归处理右子树
            if node.right:
                backtrack(node.right)

        # 撤销选择（回溯）：移除当前节点，恢复到递归前的状态
        # 这样返回父节点时，path列表只包含到父节点的路径
        path.pop()
    
    backtrack(root)
    return res