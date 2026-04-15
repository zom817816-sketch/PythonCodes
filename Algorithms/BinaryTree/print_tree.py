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