def print_tree(root: TreeNode, level: int = 0, prefix: str = "Root: "):
    """
    可视化打印二叉树结构
    
    Args:
        root: 二叉树根节点
        level: 当前层级
        prefix: 前缀标识
    """
    if root:
        print(" " * (level * 4) + prefix + str(root.val))
        if root.left or root.right:
            if root.left:
                print_tree(root.left, level + 1, "L--- ")
            else:
                print(" " * ((level + 1) * 4) + "L--- None")
            if root.right:
                print_tree(root.right, level + 1, "R--- ")
            else:
                print(" " * ((level + 1) * 4) + "R--- None")


def level_order_traversal(root: TreeNode) -> List[int]:
    """
    层序遍历，用于验证构造的二叉树
    
    Args:
        root: 二叉树根节点
    
    Returns:
        List[int]: 层序遍历结果
    """
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        result.append(node.val)
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return result


def validate_tree(root: TreeNode) -> bool:
    """
    验证构造的二叉树是否满足最大二叉树性质
    
    Args:
        root: 二叉树根节点
    
    Returns:
        bool: 是否满足最大二叉树性质
    """
    def helper(node: TreeNode, parent_max: float) -> bool:
        if not node:
            return True
        
        # 当前节点的所有子孙节点都应该比它小
        def check_subtree(sub_node: TreeNode, max_val: int) -> bool:
            if not sub_node:
                return True
            if sub_node.val >= max_val:
                return False
            return check_subtree(sub_node.left, max_val) and check_subtree(sub_node.right, max_val)
        
        if not check_subtree(node.left, node.val):
            return False
        if not check_subtree(node.right, node.val):
            return False
        
        return helper(node.left, parent_max) and helper(node.right, parent_max)
    
    return helper(root, float('inf'))