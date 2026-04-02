"""
二叉树遍历 - 递归实现

递归三原则：
1. 必须有基本情况（递归终止条件）
2. 程序必须向基本情况靠近（每次递归都更接近终止）
3. 确定单层递归的逻辑（重复执行的单元）

二叉树遍历的三种方式：
- 前序遍历：根节点 → 左子树 → 右子树
- 中序遍历：左子树 → 根节点 → 右子树  
- 后序遍历：左子树 → 右子树 → 根节点

时间复杂度：O(n) - 每个节点访问一次
空间复杂度：O(h) - h 是树的高度，递归栈的深度
"""

from typing import List, Optional


# 定义二叉树节点
class TreeNode:
    """
    二叉树节点类
    
    属性：
        val: 节点的值
        left: 左子节点
        right: 右子节点
    """
    def __init__(self, val: int = 0, 
                 left: Optional['TreeNode'] = None, 
                 right: Optional['TreeNode'] = None):
        self.val = val      # 节点存储的值
        self.left = left    # 指向左子节点
        self.right = right  # 指向右子节点


# 前序遍历（根-左-右）
def preorderTraversal(root: TreeNode) -> List[int]:
    """
    前序遍历：根节点 → 左子树 → 右子树
    
    遍历顺序示意图：
            1
           / \
          2   3
         / \
        4   5
    
    前序遍历结果：[1, 2, 4, 5, 3]
    
    应用场景：
    - 复制二叉树
    - 序列化二叉树
    - 表达式树的前缀表达式
    
    时间复杂度：O(n)
    空间复杂度：O(h)，h 为树的高度
    """
    res = []  # 存储遍历结果

    def dfs(node: TreeNode):
        """
        深度优先搜索 - 前序遍历
        
        递归终止条件：当前节点为空
        单层递归逻辑：访问根 → 递归左 → 递归右
        """
        # 基本情况：空节点直接返回（递归终止条件）
        if not node:
            return
        
        # 1. 访问根节点（将当前节点值加入结果）
        res.append(node.val)
        
        # 2. 递归遍历左子树
        dfs(node.left)
        
        # 3. 递归遍历右子树
        dfs(node.right)

    dfs(root)  # 从根节点开始遍历
    return res


# 中序遍历（左-根-右）
def inorderTraversal(root: TreeNode) -> List[int]:
    """
    中序遍历：左子树 → 根节点 → 右子树
    
    遍历顺序示意图：
            1
           / \
          2   3
         / \
        4   5
    
    中序遍历结果：[4, 2, 5, 1, 3]
    
    应用场景：
    - 二叉搜索树的中序遍历是有序的！
    - 得到升序排列
    - 表达式树的中缀表达式
    
    时间复杂度：O(n)
    空间复杂度：O(h)
    """
    res = []

    def dfs(node: TreeNode):
        """
        深度优先搜索 - 中序遍历
        
        递归终止条件：当前节点为空
        单层递归逻辑：递归左 → 访问根 → 递归右
        """
        if not node:
            return
        
        # 1. 递归遍历左子树
        dfs(node.left)
        
        # 2. 访问根节点
        res.append(node.val)
        
        # 3. 递归遍历右子树
        dfs(node.right)
    
    dfs(root)
    return res


# 后序遍历（左-右-根）
def postorderTraversal(root: TreeNode) -> List[int]:
    """
    后序遍历：左子树 → 右子树 → 根节点
    
    遍历顺序示意图：
            1
           / \
          2   3
         / \
        4   5
    
    后序遍历结果：[4, 5, 2, 3, 1]
    
    应用场景：
    - 删除二叉树（先删子节点，再删根）
    - 计算目录大小（先算子目录，再汇总）
    - 表达式树的后缀表达式（逆波兰式）
    
    时间复杂度：O(n)
    空间复杂度：O(h)
    """
    res = []

    def dfs(node: TreeNode):
        """
        深度优先搜索 - 后序遍历
        
        递归终止条件：当前节点为空
        单层递归逻辑：递归左 → 递归右 → 访问根
        """
        if not node:
            return
        
        # 1. 递归遍历左子树
        dfs(node.left)
        
        # 2. 递归遍历右子树
        dfs(node.right)
        
        # 3. 访问根节点
        res.append(node.val)
    
    dfs(root)
    return res


# 迭代实现（使用栈）
def preorderTraversal_iterative(root: TreeNode) -> List[int]:
    """
    前序遍历 - 迭代实现（使用栈）
    
    思路：
    - 用栈模拟递归过程
    - 先访问根，然后右子树入栈，左子树入栈
    - 这样出栈顺序就是左 → 右
    
    时间复杂度：O(n)
    空间复杂度：O(h)
    """
    if not root:
        return []
    
    res = []
    stack = [root]  # 栈，用于存储待访问的节点
    
    while stack:
        node = stack.pop()  # 弹出栈顶节点
        res.append(node.val)  # 访问当前节点
        
        # 先右后左入栈，这样出栈顺序就是先左后右
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return res


def inorderTraversal_iterative(root: TreeNode) -> List[int]:
    """
    中序遍历 - 迭代实现（使用栈）
    
    思路：
    - 一直向左走到头，把路径上的节点都入栈
    - 走到尽头后弹出栈顶访问，然后转向右子树
    - 重复上述过程
    
    时间复杂度：O(n)
    空间复杂度：O(h)
    """
    res = []
    stack = []
    cur = root
    
    while cur or stack:
        # 一直向左走，把节点入栈
        while cur:
            stack.append(cur)
            cur = cur.left
        
        # 走到尽头，弹出栈顶访问
        cur = stack.pop()
        res.append(cur.val)
        
        # 转向右子树
        cur = cur.right
    
    return res


def postorderTraversal_iterative(root: TreeNode) -> List[int]:
    """
    后序遍历 - 迭代实现（使用栈）
    
    技巧：
    - 后序是 左-右-根
    - 可以改成 根-右-左（类似前序，只是先右后左）
    - 然后反转结果，就得到 左-右-根
    
    时间复杂度：O(n)
    空间复杂度：O(h)
    """
    if not root:
        return []
    
    res = []
    stack = [root]
    
    while stack:
        node = stack.pop()
        res.append(node.val)
        
        # 先左后右入栈，这样出栈就是先右后左
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)
    
    # 反转得到后序遍历结果
    return res[::-1]


# 测试代码
if __name__ == "__main__":
    """
    构建测试二叉树：
            1
           / \
          2   3
         / \
        4   5
    """
    root = TreeNode(1)
    root.left = TreeNode(2)
    root.right = TreeNode(3)
    root.left.left = TreeNode(4)
    root.left.right = TreeNode(5)
    
    print("=" * 50)
    print("递归实现：")
    print(f"前序遍历：{preorderTraversal(root)}")      # [1, 2, 4, 5, 3]
    print(f"中序遍历：{inorderTraversal(root)}")       # [4, 2, 5, 1, 3]
    print(f"后序遍历：{postorderTraversal(root)}")     # [4, 5, 2, 3, 1]
    
    print("=" * 50)
    print("迭代实现：")
    print(f"前序遍历：{preorderTraversal_iterative(root)}")   # [1, 2, 4, 5, 3]
    print(f"中序遍历：{inorderTraversal_iterative(root)}")    # [4, 2, 5, 1, 3]
    print(f"后序遍历：{postorderTraversal_iterative(root)}")  # [4, 5, 2, 3, 1]

