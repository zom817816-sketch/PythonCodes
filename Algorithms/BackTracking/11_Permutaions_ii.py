"""
给定一个可包含重复数字的序列 nums ，按任意顺序 返回所有不重复的全排列。

示例 1：
输入：nums = [1,1,2]
输出：
[[1,1,2],
 [1,2,1],
 [2,1,1]]

示例 2：
输入：nums = [1,2,3]
输出：[[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

解题思路总结：

┌─────────────────────────────────────────────────────────────┐
│                      全排列 II 问题                          │
│              （数组可包含重复数字，结果去重）                    │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  核心挑战：如何避免生成重复的排列？                               │
│                                                             │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │
│  │   方法一     │    │   方法二     │    │   方法三     │     │
│  │  排序+剪枝   │    │  哈希集合去重 │    │   计数器法   │     │
│  ├─────────────┤    ├─────────────┤    ├─────────────┤     │
│  │ 1. 先排序    │    │ 1. 不排序    │    │ 1. 统计频次  │     │
│  │ 2. 相邻去重  │    │ 2. 每层用set │    │ 2. 按频次选  │     │
│  │ 3. used数组  │    │ 3. 记录已选值│    │ 3. 天然去重  │     │
│  └─────────────┘    └─────────────┘    └─────────────┘     │
│                                                             │
│  决策树示例（nums=[1,1,2]）:                                  │
│                                                             │
│                      开始                                    │
│                       │                                      │
│         ┌─────────────┼─────────────┐                       │
│         │             │             │                       │
│        1a            1b(剪枝)        2                      │
│         │                           │                       │
│     ┌───┴───┐                   ┌───┴───┐                   │
│     │       │                   │       │                   │
│    1b       2                   1a      1b                  │
│     │       │                   │       │                   │
│     2       1b                  1b      1a                  │
│                                                             │
│  剪枝原理：                                                   │
│  - 当 1a 和 1b 相同时，如果 1a 还没选，就不能选 1b                │
│  - 这样可以保证相同值的元素按顺序被选择，避免重复                   │
│                                                             │
│                                                             │
└─────────────────────────────────────────────────────────────┘

回溯算法模板：

def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return
    
    for 选择 in 选择列表:
        if 剪枝条件:    # 可选
            continue
        做选择
        backtrack(路径, 选择列表)
        撤销选择
"""

from typing import List


def permuteUnique(nums: List[int]) -> List[List[int]]:
    """
    方法一：回溯法 + 排序去重
    
    核心思想：
    1. 先对数组排序，让相同的数字相邻
    2. 使用 used 数组标记每个位置是否已被使用
    3. 剪枝：当遇到重复数字时，如果前一个相同的数字还没被使用，则跳过当前数字
    
    剪枝条件解释：
    - i > 0: 确保不是第一个元素
    - nums[i] == nums[i-1]: 当前元素与前一个元素相同
    - used[i-1] == False: 前一个相同的元素还没有被使用
    
    为什么要用 used[i-1] == False 而不是 used[i-1] == True？
    - used[i-1] == False 表示在同一层（同一深度）中，前一个相同的数字还没被选择
    - 这意味着如果我们选择当前数字，会产生重复的组合
    - 例如 [1a, 1b, 2]，如果 1a 还没选就选 1b，会和先选 1a 再选 1b 的情况重复
    
    时间复杂度：O(n × n!)，其中 n 是数组长度
    空间复杂度：O(n)，递归栈和 used 数组的空间
    """
    res = []
    path = []
    n = len(nums)
    used = [False] * n
    
    # 必须先排序！否则相同的数字不会相邻，剪枝条件无法生效
    nums.sort()

    def backtrack():
        # 递归终止条件：路径长度等于数组长度，说明找到了一个完整排列
        if len(path) == n:
            res.append(path[:]) # 必须使用 path[:] 或 path.copy() 创建副本
            return
        
        for i in range(n):
            # 剪枝条件：跳过重复元素
            # 如果当前元素与前一个元素相同，且前一个元素还没被使用，则跳过
            if i > 0 and nums[i] == nums[i-1] and not used[i-1]:
                continue
            
            # 如果当前元素还没被使用
            if not used[i]:
                # 做选择：将当前元素加入路径
                path.append(nums[i])
                used[i] = True
                
                # 进入下一层决策树
                backtrack()
                
                # 撤销选择：回溯
                path.pop()
                used[i] = False
    
    backtrack()
    return res


def permuteUnique_hash(nums: List[int]) -> List[List[int]]:
    """
    方法二：回溯法 + 哈希集合去重（不排序）
    
    核心思想：
    在每一层递归中，使用集合记录已经使用过的数字值，避免在同一层选择相同的数字
    
    优点：不需要预先排序
    缺点：每层都要创建集合，有一定开销
    
    时间复杂度：O(n × n!)
    空间复杂度：O(n)
    """
    res = []
    path = []
    n = len(nums)
    used = [False] * n

    def backtrack():
        if len(path) == n:
            res.append(path[:])
            return
        
        # 使用集合记录本层已经使用过的数字值
        used_in_this_level = set()
        
        for i in range(n):
            # 如果当前位置已被使用，或当前数字值在本层已使用过，跳过
            if used[i] or nums[i] in used_in_this_level:
                continue
            
            # 记录当前数字值在本层已使用
            used_in_this_level.add(nums[i])
            
            # 做选择
            path.append(nums[i])
            used[i] = True
            backtrack()
            # 撤销选择
            path.pop()
            used[i] = False
    
    backtrack()
    return res


def permuteUnique_counter(nums: List[int]) -> List[List[int]]:
    """
    方法三：回溯法 + 计数器（最优空间复杂度）
    
    核心思想：
    使用 Counter 统计每个数字出现的次数，递归时根据计数来选择数字
    
    优点：
    - 不需要 used 数组
    - 天然去重，不需要额外剪枝条件
    
    时间复杂度：O(n × n!)
    空间复杂度：O(n)，主要是递归栈
    """
    from collections import Counter
    
    res = []
    path = []
    n = len(nums)
    
    # 统计每个数字的出现次数
    count = Counter(nums)
    # 获取所有唯一的数字
    unique_nums = list(count.keys())

    def backtrack():
        if len(path) == n:
            res.append(path[:])
            return
        
        # 遍历所有唯一的数字
        for num in unique_nums:
            # 如果该数字还有剩余次数
            if count[num] > 0:
                # 做选择
                path.append(num)
                count[num] -= 1
                
                backtrack()
                
                # 撤销选择
                path.pop()
                count[num] += 1
    
    backtrack()
    return res