"""
给你一棵二叉树的根节点 root ，翻转这棵二叉树，并返回其根节点。
"""

class TreeNode: 
    def __init__(self, val: int=0, left: TreeNode=None, right: TreeNode=None): 
        self.val = val
        self.left = left
        self.right = right

def invertBinaryTree(root: TreeNode) -> TreeNode: 
    """
    翻转二叉树（BFS 层序遍历版本）
    
    使用队列进行层序遍历，逐层交换每个节点的左右子节点
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(W)，W 为树的最大宽度，即队列的最大长度
    """
    # 如果根节点为空，直接返回 None
    if not root: 
        return None 

    from collections import deque
    # 初始化队列，将根节点加入队列
    queue = deque([root]) 

    # 开始 BFS 层序遍历
    while queue: 
        # 取出队首节点
        node = queue.popleft() 
        
        # 交换当前节点的左右子节点
        temp = node.left 
        node.left = node.right
        node.right = temp 
        
        # 将左子节点加入队列（交换后的原右子节点）
        if node.left:
            queue.append(node.left)
        
        # 将右子节点加入队列（交换后的原左子节点）
        if node.right:
            queue.append(node.right)
    
    return root


def invertBinaryTreeRecursive(root: TreeNode) -> TreeNode: 
    """
    翻转二叉树（递归版本）
    
    使用 DFS（深度优先搜索）递归实现，自底向上翻转
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(H)，H 为树的高度，即递归栈的深度
    """
    # 递归终止条件：如果节点为空，直接返回
    if not root: 
        return None 

    # 递归翻转左子树
    left = invertBinaryTreeRecursive(root.left)
    
    # 递归翻转右子树
    right = invertBinaryTreeRecursive(root.right)
    
    # 交换左右子树
    root.left = right
    root.right = left
    
    return root


def invertBinaryTreeDFS(root: TreeNode) -> TreeNode: 
    """
    翻转二叉树（DFS 迭代版本）
    
    使用栈进行深度优先遍历，逐个交换节点的左右子节点
    时间复杂度：O(N)，每个节点最多被访问一次
    空间复杂度：O(H)，H 为树的高度，即栈的最大深度
    """
    # 如果根节点为空，直接返回 None
    if not root: 
        return None 

    from collections import deque
    # 使用栈进行 DFS 遍历
    stack = deque([root]) 

    # 开始 DFS 遍历
    while stack: 
        # 弹出栈顶节点
        node = stack.pop() 
        
        # 交换当前节点的左右子节点
        temp = node.left 
        node.left = node.right
        node.right = temp 
        
        # 将右子节点压入栈（先压右，这样左子节点会先被处理）
        if node.right:
            stack.append(node.right)
        
        # 将左子节点压入栈
        if node.left:
            stack.append(node.left)
    
    return root
