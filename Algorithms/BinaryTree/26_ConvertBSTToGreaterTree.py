"""
给出二叉 搜索 树的根节点，该树的节点值各不相同，请你将其转换为累加树（Greater Sum Tree），使每个节点 node 的新值等于原树中大于或等于 node.val 的值之和。
提醒一下，二叉搜索树满足下列约束条件：
节点的左子树仅包含键 小于 节点键的节点。
节点的右子树仅包含键 大于 节点键的节点。
左右子树也必须是二叉搜索树。

相当于一个有序数组从后到前累加

核心思路：
- BST的中序遍历（左→根→右）得到升序序列
- 反中序遍历（右→根→左）得到降序序列
- 从最大的节点开始累加，逐步向左处理，实现累加树
"""

from typing import Optional, List


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


# 方法一：递归法（反中序遍历）
def convertBST_Recursive(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    递归法将BST转换为累加树 - 反中序遍历⭐⭐⭐
    
    核心思路：
    1. 反中序遍历BST（右→根→左），得到降序序列
    2. 维护一个累加变量pre，记录前一个节点的累加值
    3. 遍历过程中，将当前节点值加上pre，然后更新pre为当前新值
    
    为什么反中序遍历？
    - BST的中序遍历（左→根→右）得到升序序列
    - 反中序遍历（右→根→左）得到降序序列，从大到小处理
    - 这样可以从最大的节点开始累加，符合题目要求
    
    时间复杂度：O(N) - 每个节点只访问一次
    空间复杂度：O(H) - 递归栈深度，H为树高
    """
    # 维护累加变量，记录前一个节点的累加值
    # 使用nonlocal关键字，使其在嵌套函数中可修改
    pre = 0
    
    def traversal(cur: Optional[TreeNode]) -> None:
        """
        反中序遍历辅助函数
        
        遍历顺序：右子树 → 当前节点 → 左子树
        """
        nonlocal pre  # 引用外部函数的pre变量
        
        # 【终止条件】
        # 当前节点为空，直接返回
        if not cur:
            return
        
        # 【1. 处理右子树】
        # 先遍历右子树，因为右子树的值都比当前节点大
        traversal(cur.right)
        
        # 【2. 处理当前节点】
        # 当前节点的新值 = 原节点值 + 前一个节点的累加值
        cur.val += pre
        # 更新pre为当前节点的新值，供下一个节点使用
        pre = cur.val
        
        # 【3. 处理左子树】
        # 最后遍历左子树，因为左子树的值都比当前节点小
        traversal(cur.left)
    
    # 调用辅助函数开始遍历
    traversal(root)
    return root


# 方法二：迭代法（反中序遍历）
def convertBST_Iterative(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    迭代法将BST转换为累加树 - 反中序遍历⭐⭐⭐
    
    核心思路：
    使用栈模拟递归过程，实现反中序遍历
    1. 先将所有右子节点入栈
    2. 弹出栈顶节点，处理当前节点
    3. 处理左子节点
    
    时间复杂度：O(N)
    空间复杂度：O(H) - 栈的深度
    """
    if not root:
        return root
    
    pre = 0  # 累加变量
    stack = []
    cur = root
    
    # 迭代反中序遍历
    while stack or cur:
        # 【1. 遍历右子树】
        # 将当前节点及其所有右子节点入栈
        while cur:
            stack.append(cur)
            cur = cur.right
        
        # 【2. 处理当前节点】
        # 弹出栈顶节点（最右节点）
        cur = stack.pop()
        # 更新当前节点值
        cur.val += pre
        pre = cur.val
        
        # 【3. 处理左子树】
        # 处理左子节点
        cur = cur.left
    
    return root



# 方法三：Morris遍历（空间复杂度O(1)）
def convertBST_Morris(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    Morris遍历将BST转换为累加树 - 空间复杂度O(1)⭐⭐
    
    核心思路：
    使用Morris遍历实现反中序遍历，无需递归栈或显式栈
    1. 对于每个节点，找到其前驱节点（左子树的最右节点）
    2. 建立临时连接，实现线索化
    3. 处理节点后，恢复树的结构
    
    为什么空间复杂度O(1)？
    - 不使用递归栈或显式栈
    - 只使用常数级额外空间
    - 通过修改树的指针来实现遍历，然后恢复
    
    时间复杂度：O(N) - 每个节点最多访问两次
    空间复杂度：O(1) - 只使用常数额外空间
    """
    if not root:
        return root
    
    pre = 0  # 累加变量
    cur = root
    
    while cur:
        # 【情况1：当前节点有右子树】
        # 找到右子树的最左节点（反中序遍历的前驱节点）
        if cur.right:
            # 找前驱节点：右子树的最左节点
            predecessor = cur.right
            while predecessor.left and predecessor.left != cur:
                predecessor = predecessor.left
            
            # 【1. 首次访问：建立临时连接】
            if not predecessor.left:
                # 建立临时连接，指回当前节点
                predecessor.left = cur
                # 继续处理右子树
                cur = cur.right
                continue
            # 【2. 再次访问：处理当前节点并断开连接】
            else:
                # 断开临时连接
                predecessor.left = None
                # 处理当前节点
                cur.val += pre
                pre = cur.val
                # 处理左子树
                cur = cur.left
        # 【情况2：当前节点没有右子树】
        else:
            # 处理当前节点
            cur.val += pre
            pre = cur.val
            # 处理左子树
            cur = cur.left
    
    return root


# 方法四：递归法（类成员变量）
def convertBST_ClassVar(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    递归法 - 使用类成员变量记录累加值⭐⭐
    
    与方法一类似，但使用类成员变量代替nonlocal变量
    适用于在类中实现的场景
    
    时间复杂度：O(N)
    空间复杂度：O(H)
    """
    class Helper:
        def __init__(self):
            self.pre = 0  # 累加变量
        
        def traversal(self, cur: Optional[TreeNode]) -> None:
            if not cur:
                return
            # 处理右子树
            self.traversal(cur.right)
            # 处理当前节点
            cur.val += self.pre
            self.pre = cur.val
            # 处理左子树
            self.traversal(cur.left)
    
    helper = Helper()
    helper.traversal(root)
    return root



# 方法五：递归法（返回累加值）
def convertBST_ReturnSum(root: Optional[TreeNode]) -> Optional[TreeNode]:
    """
    递归法 - 通过返回值传递累加值⭐
    
    核心思路：
    递归函数返回处理完子树后的累加值
    1. 处理右子树，获取右子树的累加值
    2. 当前节点值 += 右子树累加值
    3. 处理左子树，传递当前累加值
    4. 返回处理完左子树后的累加值
    
    时间复杂度：O(N)
    空间复杂度：O(H)
    """
    def traversal(cur: Optional[TreeNode], pre: int) -> int:
        """
        反中序遍历，返回处理完子树后的累加值
        
        参数：
        - cur: 当前节点
        - pre: 前一个节点的累加值
        
        返回：
        - 处理完当前子树后的累加值
        """
        if not cur:
            return pre
        
        # 【1. 处理右子树】
        # 处理右子树，得到右子树的累加值
        right_sum = traversal(cur.right, pre)
        
        # 【2. 处理当前节点】
        # 当前节点的新值 = 原节点值 + 右子树累加值
        cur.val += right_sum
        
        # 【3. 处理左子树】
        # 处理左子树，传递当前节点的新值作为pre
        left_sum = traversal(cur.left, cur.val)
        
        # 返回左子树处理后的累加值
        return left_sum
    
    traversal(root, 0)
    return root
