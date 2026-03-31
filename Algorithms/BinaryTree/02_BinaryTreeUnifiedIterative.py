"""
二叉树遍历的统一迭代实现（标记法）

核心思想：
- 使用栈存储 (节点, 是否已访问) 的元组
- 未访问节点：展开其子树（按遍历顺序的逆序入栈）
- 已访问节点：加入结果

三种遍历的区别只在于入栈顺序！
""" 


class TreeNode: 
    """二叉树节点""" 
    def __init__(self, val=0, left=None, right=None):
        self.val = val 
        self.left = left 
        self.right = right 

def binary_tree_unified_traversal(root, order='preorder'): 
    """
    统一迭代遍历框架 - 标记法
    
    参数:
        root: 二叉树根节点
        order: 遍历顺序，可选 "preorder"/"inorder"/"postorder"
    
    返回:
        遍历结果的列表
    
    核心思想：
    1. 栈中存储 (节点, 是否已访问) 的元组
    2. 未访问节点（False）：展开其子树
    3. 已访问节点（True）：加入结果
    
    时间复杂度：O(n) - 每个节点入栈出栈各一次
    空间复杂度：O(h) - h 为树的高度
    """ 

    if not root: 
        return [] 

    res = [] 
    # 栈中存储元组：(节点，是否访问) True表示已处理完，可以访问；False表示是第一次入栈，需要处理子树
    stack = [(root, False)] 

    while stack: 
        node, visited = stack.pop() 

        if not node: 
            continue 

        if visited: 
            # 已访问过，说明子树已处理完，现在可以直接访问 
            res.append(node.val) 

        else: 
            # 未访问，需要按遍历顺序展开其子树
            # 注意：栈是后进先出，所以入栈顺序是遍历顺序的逆序
            if order == 'preorder': 
                # 前序遍历：根 → 左 → 右
                # 入栈顺序：右 → 左 → 根（逆序）
                stack.append((node.right, False)) 
                stack.append(node.left, False) 
                stack.append((node, True)) # 根节点标记为已访问 
            elif order == 'inorder': 
                # 中序遍历：左 → 根 → 右
                # 入栈顺序：右 → 根 → 左（逆序）
                stack.append((node.right, False)) 
                stack.append((node, True)) # 根节点标记为已访问
                stack.append((node.left, False))
            elif order == 'postorder': 
                # 后序遍历：左 → 右 → 根
                # 入栈顺序：根 → 右 → 左（逆序）
                stack.append((node, True)) # 根节点标记为已访问
                stack.append((node.right, False)) 
                stack.append((node.left, False)) 
    return res 