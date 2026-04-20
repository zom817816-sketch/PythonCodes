"""
给你一个含重复值的二叉搜索树（BST）的根节点 root ，找出并返回 BST 中的所有 众数（即，出现频率最高的元素）。
如果树中有不止一个众数，可以按 任意顺序 返回。
假定 BST 满足如下定义：
结点左子树中所含节点的值 小于等于 当前节点的值
结点右子树中所含节点的值 大于等于 当前节点的值
左子树和右子树都是二叉搜索树

题目分析：
- 众数定义：出现频率最高的元素
- 可能有多个众数（频率相同）
- BST允许重复值（左 <= 根 <= 右）
- 利用BST的有序性可以优化空间复杂度

核心思想：
方法1：中序遍历 + 哈希表统计
- 中序遍历得到有序序列
- 使用字典统计每个值的频率
- 找出最大频率对应的所有值

方法2：中序遍历 + 实时统计（最优）
- 利用BST中序遍历的有序性，相同值连续出现
- 实时统计当前值的频率
- 值变化时，更新最大频率
- 空间复杂度O(H)，不需要存储所有值

方法3：DFS递归 + 哈希表
- 递归遍历整棵树
- 使用字典统计频率
- 找出最大频率对应的所有值

方法4：BFS层序遍历 + 哈希表
- 使用队列进行层序遍历
- 使用字典统计频率
- 找出最大频率对应的所有值

方法5：Morris遍历 + 实时统计（空间O(1)）
- 使用Morris中序遍历，空间复杂度降到O(1)
- 结合方法2的实时统计逻辑
"""

from typing import Optional, List
from collections import Counter, defaultdict, deque


class TreeNode:
    def __init__(self, val: int = 0, left: Optional['TreeNode'] = None, right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def findMode_hash(root: Optional[TreeNode]) -> List[int]:
    """
    哈希表方法：中序遍历 + 频率统计⭐⭐
    
    核心思想：
    - 先进行中序遍历，收集所有节点值
    - 使用Counter统计每个值的出现频率
    - 找出最大频率，返回对应的所有值
    
    优点：
    - 逻辑清晰，易于理解
    - 代码简洁
    
    缺点：
    - 需要O(N)额外空间存储所有值
    - 没有利用BST的有序性
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(N)，存储所有节点值和频率
    
    Args:
        root: BST的根节点
        
    Returns:
        所有众数（出现频率最高的元素）
    """
    if not root:
        return []
    
    # 收集所有节点值
    values = []
    
    def inorder(node: Optional[TreeNode]) -> None:
        """
        中序遍历辅助函数
        
        Args:
            node: 当前节点
        """
        if not node:
            return
        inorder(node.left)
        values.append(node.val)
        inorder(node.right)
    
    # 执行中序遍历
    inorder(root)
    
    # 统计每个值的频率
    freq = Counter(values)
    
    # 找出最大频率
    # 注意：max()需要调用函数，不能直接使用max.values
    max_freq = max(freq.values())
    
    # 返回所有最大频率的值
    return [val for val, count in freq.items() if count == max_freq]


def findMode_inorder(root: Optional[TreeNode]) -> List[int]:
    """
    实时统计方法：中序遍历 + 实时统计频率⭐⭐⭐
    
    核心思想：
    - 利用BST中序遍历的有序性，相同值连续出现
    - 实时统计当前值的频率
    - 值变化时，更新最大频率
    - 不需要存储所有值，节省空间
    
    算法步骤：
    1. 中序遍历BST
    2. 如果当前值等于前一个值，频率+1
    3. 如果当前值不等于前一个值，重置频率为1
    4. 比较当前频率与最大频率：
       - 如果大于，更新最大频率，重置结果列表
       - 如果等于，将当前值加入结果列表
    
    优点：
    - 空间复杂度最优O(H)
    - 充分利用BST的有序性
    - 只需遍历一次
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(H)，递归栈深度
    
    Args:
        root: BST的根节点
        
    Returns:
        所有众数
    """
    if not root:
        return []
    
    result = []        # 存储众数结果
    max_freq = 0       # 最大频率
    cur_freq = 0        # 当前值的频率
    prev_val = None     # 前一个访问的节点值
    
    def inorder(node: Optional[TreeNode]) -> None:
        """
        中序遍历辅助函数
        
        Args:
            node: 当前节点
        """
        nonlocal result, max_freq, cur_freq, prev_val
        
        if not node:
            return
        
        # 遍历左子树
        inorder(node.left)
        
        # 处理当前节点
        if node.val == prev_val:
            # 与前一个值相同，频率+1
            cur_freq += 1
        else:
            # 值变化，重置频率
            cur_freq = 1
            prev_val = node.val
        
        # 更新结果
        if cur_freq > max_freq:
            # 发现更高频率，更新最大频率和结果
            max_freq = cur_freq
            result = [node.val]
        elif cur_freq == max_freq:
            # 频率相同，加入结果列表
            result.append(node.val)
        
        # 遍历右子树
        inorder(node.right)
    
    # 执行中序遍历
    inorder(root)
    return result


def findMode_dfs(root: Optional[TreeNode]) -> List[int]:
    """
    DFS递归方法：递归遍历 + 哈希表统计⭐⭐
    
    核心思想：
    - 递归遍历整棵树（不依赖遍历顺序）
    - 使用字典统计每个值的频率
    - 遍历完成后，找出最大频率对应的所有值
    
    优点：
    - 代码简洁
    - 不依赖遍历顺序（前序、中序、后序都可以）
    
    缺点：
    - 需要O(N)额外空间存储频率
    - 没有利用BST的有序性
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(N)，存储频率统计
    
    Args:
        root: BST的根节点
        
    Returns:
        所有众数
    """
    if not root:
        return []
    
    # 使用defaultdict统计频率
    freq = defaultdict(int)
    
    def dfs(node: Optional[TreeNode]) -> None:
        """
        DFS遍历辅助函数
        
        Args:
            node: 当前节点
        """
        if not node:
            return
        
        # 统计当前节点值
        freq[node.val] += 1
        
        # 递归遍历左右子树
        dfs(node.left)
        dfs(node.right)
    
    # 执行DFS遍历
    dfs(root)
    
    # 找出最大频率
    # 注意：需要检查freq是否为空（虽然已处理root为空的情况）
    max_freq = max(freq.values()) if freq else 0
    
    # 返回所有最大频率的值
    # 注意：使用freq.items()遍历键值对
    return [val for val, count in freq.items() if count == max_freq]


def findMode_bfs(root: Optional[TreeNode]) -> List[int]:
    """
    BFS层序遍历方法：层序遍历 + 哈希表统计⭐
    
    核心思想：
    - 使用队列进行层序遍历
    - 使用字典统计每个值的频率
    - 遍历完成后，找出最大频率对应的所有值
    
    优点：
    - 代码直观，易于理解
    - 不依赖树的遍历顺序
    
    缺点：
    - 需要O(N)额外空间存储频率
    - 队列可能占用较多空间（最坏O(N)）
    - 没有利用BST的有序性
    
    时间复杂度：O(N)，每个节点访问一次
    空间复杂度：O(N)，存储频率统计和队列
    
    Args:
        root: BST的根节点
        
    Returns:
        所有众数
    """
    if not root:
        return []
    
    # 使用defaultdict统计频率
    freq = defaultdict(int)
    
    # 使用deque进行高效的层序遍历（pop(0)是O(1)）
    queue = deque([root])
    
    while queue:
        node = queue.popleft()
        
        # 统计当前节点值
        freq[node.val] += 1
        
        # 将子节点加入队列
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    # 找出最大频率
    max_freq = max(freq.values()) if freq else 0
    
    # 返回所有最大频率的值
    return [val for val, count in freq.items() if count == max_freq]


def findMode_morris(root: Optional[TreeNode]) -> List[int]:
    """
    Morris遍历方法：Morris中序遍历 + 实时统计⭐⭐
    
    核心思想：
    - 使用Morris中序遍历，空间复杂度降到O(1)
    - Morris遍历通过临时修改树结构实现中序遍历，不需要递归或栈
    - 结合实时统计方法，充分利用BST的有序性
    
    Morris遍历原理：
    1. 对于当前节点，如果左子树为空，访问当前节点，转向右子树
    2. 如果左子树不为空，找到左子树的最右节点（前驱节点）
       - 如果前驱节点的右子树为空，将其指向当前节点（建立临时链接）
       - 如果前驱节点的右子树指向当前节点（已访问），恢复为空，访问当前节点
    3. 重复上述过程直到遍历完成
    
    优点：
    - 空间复杂度O(1)，最优
    - 充分利用BST的有序性
    
    缺点：
    - 算法复杂，理解难度大
    - 临时修改树结构（遍历后恢复）
    
    时间复杂度：O(N)，每个节点最多被访问两次
    空间复杂度：O(1)，只使用常量额外空间
    
    Args:
        root: BST的根节点
        
    Returns:
        所有众数
    """
    if not root:
        return []
    
    result = []        # 存储众数结果
    max_freq = 0       # 最大频率
    cur_freq = 0        # 当前值的频率
    prev_val = None     # 前一个访问的节点值
    cur = root          # 当前指针
    
    while cur:
        if not cur.left:
            # 左子树为空，访问当前节点
            if cur.val == prev_val:
                # 与前一个值相同，频率+1
                cur_freq += 1
            else:
                # 值变化，重置频率
                cur_freq = 1
                prev_val = cur.val
            
            # 更新结果
            if cur_freq > max_freq:
                # 发现更高频率
                max_freq = cur_freq
                result = [cur.val]
            elif cur_freq == max_freq:
                # 频率相同
                result.append(cur.val)
            
            # 转向右子树
            cur = cur.right
        else:
            # 找到左子树的最右节点（前驱节点）
            predecessor = cur.left
            while predecessor.right and predecessor.right != cur:
                predecessor = predecessor.right
            
            if not predecessor.right:
                # 前驱节点右子树为空，建立临时链接
                predecessor.right = cur
                cur = cur.left
            else:
                # 前驱节点右子树指向当前节点，说明已经访问过左子树
                # 恢复树结构，访问当前节点
                predecessor.right = None
                
                if cur.val == prev_val:
                    cur_freq += 1
                else:
                    cur_freq = 1
                    prev_val = cur.val
                
                if cur_freq > max_freq:
                    max_freq = cur_freq
                    result = [cur.val]
                elif cur_freq == max_freq:
                    result.append(cur.val)
                
                cur = cur.right
    
    return result
