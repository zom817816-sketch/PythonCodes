"""
给定二叉搜索树（BST）的根节点 root 和要插入树中的值 value ，将值插入二叉搜索树。 返回插入后二叉搜索树的根节点。 输入数据 保证 ，新值和原始二叉搜索树中的任意节点值都不同。

注意，可能存在多种有效的插入方式，只要树在插入后仍保持为二叉搜索树即可。 你可以返回 任意有效的结果 。

BST插入的核心思路：
- BST性质：左子树所有节点 < 根节点 < 右子树所有节点
- 插入新值时，从根节点开始比较：
  - 如果 value < 当前节点值，去左子树
  - 如果 value > 当前节点值，去右子树
  - 如果当前节点为空，就在这个位置插入新节点

题目说明可以返回任意有效结果，说明插入位置不唯一
通常的做法是：找到第一个空位置（叶子节点的左或右）插入
"""

from typing import Optional, List


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


def insertIntoBST_Recursive(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    递归法插入BST⭐⭐⭐
    
    核心思路：
    1. 如果当前节点为空，说明找到了插入位置，创建新节点返回
    2. 如果 value < 当前节点值，递归在左子树插入，结果接回当前节点的左子树
    3. 如果 value > 当前节点值，递归在右子树插入，结果接回当前节点的右子树
    
    为什么这样是对的？
    - 递归会一直走到空节点，这个空节点就是正确的插入位置
    - 插入后，通过返回值将新节点"接回"到父节点
    
    时间复杂度：O(H) - H为树高，平衡树O(logN)，最坏O(N)
    空间复杂度：O(H) - 递归栈深度
    """
    # 【终止条件：找到插入位置】
    # 当前节点为空，说明找到了合适的插入位置
    # 创建新节点并返回，这个节点会被父节点接住
    if not root:
        return TreeNode(val)
    
    # 【递归插入】
    # 如果要插入的值小于当前节点值
    # 根据BST性质，应该插入左子树
    if val < root.val:
        # 递归在左子树插入，结果接回当前节点的左子树
        root.left = insertIntoBST_Recursive(root.left, val)
    # 如果要插入的值大于当前节点值
    # 根据BST性质，应该插入右子树
    else:
        # 递归在右子树插入，结果接回当前节点的右子树
        root.right = insertIntoBST_Recursive(root.right, val)
    
    # 返回当前节点（根节点不变）
    return root


def insertIntoBST_Iterative(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    迭代法插入BST - 记录父节点⭐⭐⭐
    
    核心思路：
    1. 如果树为空，直接创建新节点作为根
    2. 从根节点开始遍历，记录父节点
    3. 根据value与当前节点值的大小关系，决定向左还是向右
    4. 找到空位置后，根据最后一步的方向，插入到父节点的左或右
    
    时间复杂度：O(H) - 只需从根走到插入位置
    空间复杂度：O(1) - 只使用常数额外空间
    """
    # 【特殊情况：空树】
    # 如果树为空，直接创建新节点作为根
    if not root:
        return TreeNode(val)
    
    # 【遍历寻找插入位置】
    parent = None  # 记录父节点
    cur = root     # 当前节点
    
    # 从根节点开始遍历，直到找到空节点
    while cur:
        parent = cur  # 更新父节点
        
        # 如果要插入的值小于当前节点值，向左走
        if val < cur.val:
            cur = cur.left
        # 如果要插入的值大于当前节点值，向右走
        else:
            cur = cur.right
    
    # 【插入新节点】
    # 此时cur为空，parent是最后一个非空节点
    # 根据最后一步的方向，决定插入到parent的左还是右
    if val < parent.val:
        # 插入到父节点的左子树
        parent.left = TreeNode(val)
    else:
        # 插入到父节点的右子树
        parent.right = TreeNode(val)
    
    # 返回原根节点
    return root


def insertIntoBST_Iterative_Simple(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    迭代法插入BST - 不记录父节点⭐⭐⭐
    
    核心思路：
    与方法二相同，但实现更简洁
    直接使用root指针遍历，找到空位置后直接插入
    
    为什么可以这样？
    - Python中参数传递的是引用，可以直接修改root.left或root.right
    - 但需要注意不能直接修改root本身（因为是局部变量）
    
    时间复杂度：O(H)
    空间复杂度：O(1)
    """
    # 【特殊情况：空树】
    if not root:
        return TreeNode(val)
    
    # 【遍历寻找插入位置】
    cur = root
    while cur:
        # 如果要插入的值小于当前节点值
        if val < cur.val:
            # 如果左子节点为空，找到插入位置
            if not cur.left:
                cur.left = TreeNode(val)
                break
            # 否则继续向左走
            cur = cur.left
        # 如果要插入的值大于当前节点值
        else:
            # 如果右子节点为空，找到插入位置
            if not cur.right:
                cur.right = TreeNode(val)
                break
            # 否则继续向右走
            cur = cur.right
    
    return root


def insertIntoBST_Iterative_Pointer(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    迭代法插入BST - 指针的指针思想⭐⭐
    
    核心思路：
    使用一个指针cur，始终指向"当前应该检查的位置"
    初始时cur指向root，如果root为空，直接插入
    否则，根据value与cur.val的关系，让cur指向cur.left或cur.right
    当cur为空时，说明找到了插入位置，直接赋值
    
    这种写法的优势：
    - 不需要记录父节点
    - 代码简洁优雅
    - 思路清晰：cur始终指向"下一个要检查的位置"
    
    时间复杂度：O(H)
    空间复杂度：O(1)
    """
    # 【特殊情况：空树】
    if not root:
        return TreeNode(val)
    
    # 【遍历寻找插入位置】
    cur = root
    while True:
        # 如果要插入的值小于当前节点值
        if val < cur.val:
            # 如果左子节点为空，找到插入位置
            if not cur.left:
                cur.left = TreeNode(val)
                break
            # 否则让cur指向左子节点
            cur = cur.left
        # 如果要插入的值大于当前节点值
        else:
            # 如果右子节点为空，找到插入位置
            if not cur.right:
                cur.right = TreeNode(val)
                break
            # 否则让cur指向右子节点
            cur = cur.right
    
    return root


def insertIntoBST_Recursive_Alternative(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    递归法插入BST - 另一种写法⭐⭐
    
    与方法一思路相同，但代码结构略有不同
    显式处理空树情况，逻辑更清晰
    
    时间复杂度：O(H)
    空间复杂度：O(H)
    """
    # 【终止条件：找到插入位置】
    if not root:
        return TreeNode(val)
    
    # 【递归插入】
    if val < root.val:
        # 如果左子树为空，直接插入
        if not root.left:
            root.left = TreeNode(val)
        # 否则递归插入左子树
        else:
            insertIntoBST_Recursive_Alternative(root.left, val)
    else:
        # 如果右子树为空，直接插入
        if not root.right:
            root.right = TreeNode(val)
        # 否则递归插入右子树
        else:
            insertIntoBST_Recursive_Alternative(root.right, val)
    
    return root


def insertIntoBST_BFS(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """
    BFS插入BST - 使用队列进行层次遍历⭐
    
    核心思路：
    使用队列进行层次遍历，找到第一个可以插入的空位置
    虽然BFS也能找到插入位置，但不是最优的
    因为BST的有序性，DFS（递归或迭代）更高效
    
    时间复杂度：O(N) - 最坏情况需要遍历所有节点
    空间复杂度：O(W) - W为树的最大宽度
    
    注意：这种方法不推荐，因为无法利用BST的有序性
    """
    # 【特殊情况：空树】
    if not root:
        return TreeNode(val)
    
    # 【BFS遍历】
    from collections import deque
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        # 检查左子树
        if val < node.val:
            if not node.left:
                node.left = TreeNode(val)
                break
            queue.append(node.left)
        # 检查右子树
        else:
            if not node.right:
                node.right = TreeNode(val)
                break
            queue.append(node.right)
    
    return root
