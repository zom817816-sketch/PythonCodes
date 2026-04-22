"""
给定一个二叉树, 找到该树中两个指定节点的最近公共祖先。
百度百科中最近公共祖先的定义为："对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。"
"""

from typing import Optional, List


class TreeNode:
    """二叉树节点类"""
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val          # 节点值
        self.left = left        # 左子节点
        self.right = right      # 右子节点


def lowestCommonAncestor_Recursive(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    递归法求解二叉树的最近公共祖先⭐⭐⭐
    
    核心思路：
    1. 如果当前节点为空，或者当前节点就是p或q中的一个，直接返回当前节点
    2. 递归在左子树和右子树中分别查找p和q
    3. 如果左右子树都找到了（都不为空），说明当前节点就是LCA
    4. 如果只在一侧找到，返回那一侧的结果
    
    为什么这样是对的？
    - 如果p和q分别在当前节点的左右两侧，那当前节点就是LCA
    - 如果p和q都在左侧，那LCA一定在左子树中
    - 如果p和q都在右侧，那LCA一定在右子树中
    
    时间复杂度：O(N) - 最坏情况下遍历所有节点
    空间复杂度：O(H) - 递归栈深度，H为树的高度，最坏O(N)，平衡树O(logN)
    """
    # 【终止条件】
    # 1. 如果当前节点为空，说明这条路径上没找到
    # 2. 如果当前节点就是p或q，说明找到了其中一个，直接返回
    if not root or root == p or root == q:
        return root
    
    # 【递归查找】
    # 在左子树中递归查找p和q的LCA
    left = lowestCommonAncestor_Recursive(root.left, p, q)
    # 在右子树中递归查找p和q的LCA
    right = lowestCommonAncestor_Recursive(root.right, p, q)

    # 【判断结果】
    # 如果左子树和右子树都找到了结果（都不为空）
    # 说明p和q分别在当前节点的左右两侧，当前节点就是LCA
    if left and right:
        return root
    
    # 如果只有左子树找到了，说明p和q都在左子树，返回左子树的结果
    # 如果只有右子树找到了，说明p和q都在右子树，返回右子树的结果
    # 如果都没找到，返回None（实际上不会发生，因为p和q一定存在）
    return left if left else right


def lowestCommonAncestor_Hash(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    使用哈希表存储父节点的解法⭐⭐
    
    核心思路：
    1. 从根节点开始遍历整棵树，用哈希表记录每个节点的父节点
    2. 从p节点开始向上遍历，将所有祖先节点存入集合
    3. 从q节点开始向上遍历，第一个出现在集合中的节点就是LCA
    
    这种方法类似于求两个链表的交点
    
    时间复杂度：O(N) - 遍历整棵树 + 遍历祖先链
    空间复杂度：O(N) - 哈希表存储所有节点的父节点 + 祖先集合
    """
    # 【第一步：建立父节点映射表】
    # parent字典存储每个节点 -> 它的父节点的映射
    # 根节点没有父节点，所以值为None
    parent = {root: None}
    # 使用栈进行DFS遍历
    stack = [root]

    # 遍历树，直到p和q都找到了它们的父节点链
    # 注意：这里不需要遍历完整棵树，只需要确保p和q都在parent字典中即可
    while p not in parent or q not in parent:
        # 弹出栈顶节点
        node = stack.pop()
        
        # 如果左子节点存在，记录其父节点并入栈
        if node.left:
            parent[node.left] = node
            stack.append(node.left)
        
        # 如果右子节点存在，记录其父节点并入栈
        if node.right:
            parent[node.right] = node
            stack.append(node.right)
    
    # 【第二步：记录p的所有祖先节点】
    # 使用集合存储p的所有祖先（包括p自己）
    ancestors = set()
    while p:
        ancestors.add(p)      # 将当前节点加入集合
        p = parent[p]         # 移动到父节点
    
    # 【第三步：找q的祖先中第一个在集合中的节点】
    # 从q开始向上遍历，第一个出现在ancestors中的节点就是LCA
    while q not in ancestors:
        q = parent[q]         # 移动到父节点
    
    # q现在就是LCA
    return q


def lowestCommonAncestor_Path(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    DFS记录路径法求解LCA
    
    核心思路：
    1. 分别找到从根节点到p和从根节点到q的路径
    2. 这两条路径的最后一个公共节点就是LCA
    
    例如：
    - 根到p的路径：[3, 5, 6]
    - 根到q的路径：[3, 5, 2, 4]
    - 最后一个公共节点是5，所以5是LCA
    
    时间复杂度：O(N) - 遍历两次树来找路径
    空间复杂度：O(N) - 存储两条路径
    """
    # 【内部函数：查找从root到target的路径】
    def find_path(root: Optional[TreeNode], target: TreeNode) -> Optional[List[TreeNode]]:
        """
        递归查找从根节点到目标节点的路径
        
        返回值：
        - 如果找到，返回路径列表（包含起点root和终点target）
        - 如果没找到，返回None
        """
        # 终止条件1：当前节点为空，说明这条路径上找不到
        if not root:
            return None
        
        # 终止条件2：当前节点就是目标节点，返回只包含当前节点的路径
        if root == target:
            return [root]
        
        # 递归在左子树中查找
        left = find_path(root.left, target)
        if left:
            # 如果在左子树找到了，当前节点是路径的一部分
            # 将当前节点添加到路径开头
            return [root] + left
        
        # 递归在右子树中查找
        right = find_path(root.right, target)
        if right:
            # 如果在右子树找到了，当前节点是路径的一部分
            return [root] + right
        
        # 左右子树都没找到，返回None
        return None
    
    # 【获取两条路径】
    # 找从根节点到p的路径
    path_p = find_path(root, p)
    # 找从根节点到q的路径
    path_q = find_path(root, q)
    
    # 【找最后一个公共节点】
    # 同时遍历两条路径，直到出现不同的节点
    i = 0
    # 循环条件：索引有效且两个路径上的节点相同
    while i < len(path_p) and i < len(path_q) and path_p[i] == path_q[i]:
        i += 1
    
    # 此时i指向第一个不同的位置，或者超出某条路径的长度
    # 所以i-1就是最后一个相同的节点，即LCA
    return path_p[i - 1]

# ============================================================
# BST的最近公共祖先（利用BST性质优化）
# ============================================================

"""
给定一个二叉搜索树, 找到该树中两个指定节点的最近公共祖先。
百度百科中最近公共祖先的定义为："对于有根树 T 的两个节点 p、q，最近公共祖先表示为一个节点 x，满足 x 是 p、q 的祖先且 x 的深度尽可能大（一个节点也可以是它自己的祖先）。"

BST的LCA问题比普通二叉树更简单，因为可以利用BST的有序性：
- 左子树所有节点值 < 根节点值
- 右子树所有节点值 > 根节点值

核心洞察：
对于BST中的两个节点p和q（假设p.val <= q.val）：
1. 如果 root.val > q.val，说明p和q都在左子树，LCA在左子树
2. 如果 root.val < p.val，说明p和q都在右子树，LCA在右子树
3. 如果 p.val <= root.val <= q.val，说明p和q分别在两侧（或当前节点就是p或q），当前节点就是LCA
"""


def lowestCommonAncestorBST(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    BST的最近公共祖先 - 递归法⭐⭐⭐
    
    利用BST性质，不需要遍历整棵树，时间复杂度O(H)，H为树高
    
    时间复杂度：O(H) - 只需从根走到LCA，平衡树O(logN)，最坏O(N)
    空间复杂度：O(H) - 递归栈深度
    """
    # 【确保 p.val <= q.val】
    # 这样方便后续判断，只需考虑p在左、q在右的情况
    if p.val > q.val:
        p, q = q, p
    
    # 【情况1：当前节点值比p和q都大】
    # root.val > q.val >= p.val，说明p和q都在当前节点的左子树
    # 根据BST性质，左子树所有值 < root.val，所以去左子树查找
    if root.val > q.val:
        return lowestCommonAncestorBST(root.left, p, q)
    
    # 【情况2：当前节点值比p和q都小】
    # root.val < p.val <= q.val，说明p和q都在当前节点的右子树
    # 根据BST性质，右子树所有值 > root.val，所以去右子树查找
    elif root.val < p.val:
        return lowestCommonAncestorBST(root.right, p, q)
    
    # 【情况3：当前节点值在p和q之间】
    # p.val <= root.val <= q.val，说明：
    # - p在左子树或p就是当前节点，q在右子树或q就是当前节点
    # - 当前节点就是p和q的分叉点，即LCA
    # 这个条件也涵盖了p或q就是当前节点的情况（节点可以是自己的祖先）
    else:
        return root


def lowestCommonAncestorBST_iter(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    """
    BST的最近公共祖先 - 迭代法⭐⭐⭐
    
    与递归法思路完全相同，但用循环实现，空间复杂度O(1)
    
    核心逻辑：
    从根节点出发，根据当前节点值与p、q的大小关系决定向左还是向右，
    直到找到分叉点（即LCA）
    
    时间复杂度：O(H) - 只需从根走到LCA
    空间复杂度：O(1) - 只使用常数额外空间
    """
    while root:
        # 【情况1：当前节点值比p和q都大】
        # p和q都在左子树，向左移动
        if root.val > p.val and root.val > q.val:
            root = root.left
        
        # 【情况2：当前节点值比p和q都小】
        # p和q都在右子树，向右移动
        elif root.val < p.val and root.val < q.val:
            root = root.right
        
        # 【情况3：当前节点值在p和q之间（或等于其中一个）】
        # 找到LCA，返回当前节点
        # 包括以下子情况：
        # - p.val <= root.val <= q.val（p在左或就是root，q在右或就是root）
        # - q.val <= root.val <= p.val（同上，只是p和q交换）
        else:
            return root
    
    # 如果树为空，返回None（理论上不会发生，因为p和q一定存在）
    return None