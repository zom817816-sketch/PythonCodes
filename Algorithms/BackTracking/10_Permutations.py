"""
给定一个不含重复数字的数组 nums，返回其 所有可能的全排列。你可以 按任意顺序 返回答案。

解题思路：

本题是回溯算法的经典题目，属于「排列问题」。

核心特点：
  - 排列问题：考虑元素的顺序，[1,2] 和 [2,1] 是不同的排列
  - 组合问题：不考虑顺序，[1,2] 和 [2,1] 是相同的组合

与组合问题的关键区别：
  - 组合问题：使用 start_index 控制，避免重复选择，保证顺序
  - 排列问题：使用 used 数组标记，每个元素只能用一次，但每次都可以从头开始选

算法流程（以 nums=[1,2,3] 为例）：

  第0层：path=[]
      选1 → path=[1], used=[T,F,F] → 递归
          第1层：path=[1]
              选2 → path=[1,2], used=[T,T,F] → 递归
                  第2层：path=[1,2]
                      选3 → path=[1,2,3], len==3, 记录 [1,2,3] ✅
              选3 → path=[1,3], used=[T,F,T] → 递归
                  第2层：path=[1,3]
                      选2 → path=[1,3,2], len==3, 记录 [1,3,2] ✅
      选2 → path=[2], used=[F,T,F] → 递归
          ... 得到 [2,1,3], [2,3,1]
      选3 → path=[3], used=[F,F,T] → 递归
          ... 得到 [3,1,2], [3,2,1]

搜索树可视化：

                      []
                   /   |   \
                 1      2     3
               / \    / \   / \
              2   3  1   3 1   2
              |   |  |   | |   |
              3   2  3   1 2   1

结果：[1,2,3], [1,3,2], [2,1,3], [2,3,1], [3,1,2], [3,2,1]


回溯算法三要素：


1. 递归参数：
   - used 数组：标记哪些元素已经被使用

2. 终止条件：
   - len(path) == n：所有元素都已使用，得到一个完整排列

3. 单层逻辑：
   - 遍历所有元素（从 0 开始，不是 start_index）
   - 跳过已使用的元素（if used[i]: continue）
   - 标记使用 → 加入路径 → 递归 → 回溯 → 取消标记


关键注意点：


1. 排列问题每次都要从头遍历（range(n)），不是从 start_index 开始
2. 用 used 数组标记哪些元素已使用，避免重复使用
3. 树枝去重：used[i] 为 True 表示在当前路径上已使用


复杂度分析：


时间复杂度：O(N × N!)
  - 共有 N! 个排列
  - 每个排列需要 O(N) 时间复制 path[:]

空间复杂度：O(N)
  - 递归深度为 N
  - used 数组大小为 N
  - path 数组大小为 N
"""

from typing import List


# 解法1：used 数组法（推荐）
def permute(nums: List[int]) -> List[List[int]]:
    """
    返回数组的所有全排列⭐⭐⭐
    
    参数：
        nums: 不含重复数字的数组
    
    返回：
        所有可能的全排列列表
    """
    res = []           # 存储所有结果
    path = []          # 存储当前路径
    n = len(nums)
    used = [False] * n # 标记每个位置是否已使用

    def backtrack():
        """
        回溯函数
        """
        # 终止条件 
        # 当路径长度等于数组长度，说明得到一个完整排列
        if len(path) == n:
            res.append(path[:])  # 注意：必须用切片复制
            return
        
        # 单层搜索逻辑 
        # 排列问题：每次都从头开始遍历（不是 start_index）
        for i in range(n):
            # 如果当前元素已经使用过，跳过（树枝去重）
            if used[i]:
                continue
            
            # 1. 处理节点：标记为已使用，加入路径
            used[i] = True
            path.append(nums[i])
            
            # 2. 递归搜索
            backtrack()
            
            # 3. 回溯：撤销选择，恢复状态
            path.pop()
            used[i] = False
    
    backtrack()
    return res


# 解法2：交换法（空间复杂度更低）
def permute_swap(nums: List[int]) -> List[List[int]]:
    """
    使用交换法生成全排列⭐⭐⭐
    
    核心思想：
      通过交换元素，将每个元素都放到当前位置，然后递归处理后面
      不需要 used 数组和 path 数组，直接在原数组上操作
    
    示例：[1,2,3]
      第0位可以选 1,2,3：
        - 选1（不交换）→ 递归处理 [1,2,3] 的第1位
        - 选2（交换1,2）→ 递归处理 [2,1,3] 的第1位
        - 选3（交换1,3）→ 递归处理 [3,2,1] 的第1位
    """
    res = []
    n = len(nums)
    
    def backtrack(start: int):
        """
        回溯函数
        
        参数：
            start: 当前要确定的位置
        """
        # 终止条件：所有位置都已确定
        if start == n:
            res.append(nums[:])  # 复制当前排列
            return
        
        # 将 start 位置与 [start, n-1] 每个位置交换
        for i in range(start, n):
            # 交换：将 nums[i] 放到 start 位置
            nums[start], nums[i] = nums[i], nums[start]
            
            # 递归：确定下一个位置
            backtrack(start + 1)
            
            # 回溯：恢复数组状态，让其他分支能从正确的初始状态开始
            nums[start], nums[i] = nums[i], nums[start]
    
    backtrack(0)
    return res


# 解法3：插入法（迭代）
def permute_insert(nums: List[int]) -> List[List[int]]:
    """
    使用插入法生成全排列（迭代实现）⭐
    
    核心思想：
      逐个插入元素，每次将新元素插入到已有排列的所有可能位置
    
    示例：[1,2,3]
      初始：[[1]]
      插入2：[[2,1], [1,2]]
      插入3：
        - 在 [2,1] 中插入3：[3,2,1], [2,3,1], [2,1,3]
        - 在 [1,2] 中插入3：[3,1,2], [1,3,2], [1,2,3]
    """
    if not nums:
        return []
    
    # 初始：只有一个元素的排列
    res = [[nums[0]]]
    
    # 逐个插入后面的元素
    for i in range(1, len(nums)):
        new_res = []
        # 对每个已有排列
        for perm in res:
            # 在排列的所有位置插入新元素
            for j in range(len(perm) + 1):
                new_perm = perm[:j] + [nums[i]] + perm[j:]
                new_res.append(new_perm)
        res = new_res
    
    return res


# 解法4：集合法（有局限性）
def permute_set(nums: List[int]) -> List[List[int]]:
    """
    使用集合进行树枝去重（仅适用于无重复元素的数组）⭐
    
    核心思想：
      用集合存储已使用的元素值，快速判断元素是否在当前路径上
    
    局限性：
      - 无法处理有重复元素的数组（如 [1,1,2]）
      - 集合只存值不存位置，相同值的元素会被误判
    
    示例：[1,2,3]
      第0层：used_set=set()
          选1 → used_set={1} → 递归
          选2 → used_set={2} → 递归
          选3 → used_set={3} → 递归
    """
    res = []
    path = []
    n = len(nums)
    
    def backtrack(used_set: set):
        """
        回溯函数
        
        参数：
            used_set: 存储当前路径已使用的元素值
        """
        # 终止条件：得到一个完整排列
        if len(path) == n:
            res.append(path[:])
            return
        
        # 遍历所有元素
        for num in nums:
            # 如果当前元素已在集合中，跳过（树枝去重）
            if num in used_set:
                continue
            
            # 1. 处理节点：加入集合和路径
            used_set.add(num)
            path.append(num)
            
            # 2. 递归搜索
            backtrack(used_set)
            
            # 3. 回溯：从集合和路径中移除
            path.pop()
            used_set.remove(num)  # 必须从集合中移除！
    
    backtrack(set())
    return res
