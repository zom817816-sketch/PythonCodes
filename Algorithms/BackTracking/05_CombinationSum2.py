"""
给定一个候选人编号的集合 candidates 和一个目标数 target，找出 candidates 中所有可以使数字和为 target 的组合。
candidates 中的每个数字在每个组合中只能使用 一次 。
注意：解集不能包含重复的组合。

解题思路：

本题是 LeetCode 40，与 LeetCode 39 的区别：
  - 39：每个数字可以无限次使用，数组无重复
  - 40：每个数字只能用一次，数组可能有重复，需要去重

核心难点：去重
  - 数组中有重复数字，如何避免产生重复的组合？
  - 例如：[1, 1, 2], target=3
    - 选第一个 1 和 2 → [1, 2]
    - 选第二个 1 和 2 → [1, 2] （重复！）

去重策略：树层去重
  1. 先对数组排序，让相同数字相邻
  2. 在 for 循环中，如果当前数字和前一个数字相同，且前一个数字在当前层没有被使用过，就跳过
  3. 使用 used 数组或 start_index 判断是否是同一层

树层去重图解（candidates=[1,1,2], target=3）：

        第0层 (start=0)
       /      |      \
     1(0)    1(1)    2(2)    ← 1(0)和1(1)值相同，跳过1(1)
     / \      X      /
    1   2           1
   ...  ...        ...

  - i=0，选1(0)，递归
  - i=1，发现1(1)==1(0)，且i>start_index(0)，说明是同一层的重复，跳过

回溯算法三要素：

1. 递归参数：
   - start_index：当前从哪个位置开始选（保证每个数字只用一次）
   - current_sum：当前路径的和

2. 终止条件：
   - current_sum == target：找到有效组合
   - current_sum > target：剪枝（排序后可用）

3. 单层逻辑：
   - 树层去重：if i > start_index and candidates[i] == candidates[i-1]: continue
   - 选择当前数字
   - 递归（i+1，因为每个数字只能用一次）
   - 回溯

关键注意点：

1. 必须先排序！否则无法判断重复
2. 树层去重条件：i > start_index
   - i == start_index：同一层的第一个，不可能是重复
   - i > start_index：同一层的后面的，如果和前面值相同，就是重复
3. 每个数字只能用一次：递归时传 i+1

复杂度分析：

时间复杂度：O(2^N)
  - 最坏情况下，每个数字都有选或不选两种可能
  - 去重和剪枝会大幅减少实际搜索次数

空间复杂度：O(N)
  - 递归深度最多为 N
  - path 数组大小最多为 N
"""

from typing import List

def combinationSum2(candidates: List[int], target: int) -> List[List[int]]:
    """
    返回所有和为 target 的组合（每个数字只能用一次，需要去重）
    
    参数：
        candidates: 可能有重复元素的整数数组
        target: 目标和
    
    返回：
        所有和为 target 的组合列表（无重复）
    """
    res = []   # 存储所有满足条件的组合
    path = []  # 存储当前正在构建的组合
    
    # 关键：先排序，让相同数字相邻，方便去重
    candidates.sort()
    
    def backtracking(start_index: int, current_sum: int):
        """
        回溯函数
        
        参数：
            start_index: 当前从 candidates 的哪个索引开始选择
            current_sum: 当前 path 中所有数字的和
        """
        # 终止条件1：找到目标和
        if current_sum == target:
            res.append(path[:])
            return
        
        # 终止条件2：超出目标（剪枝，排序后才有效）
        if current_sum > target:
            return
        
        # 单层搜索逻辑
        for i in range(start_index, len(candidates)):
            # 关键：树层去重
            # 如果 i > start_index，说明不是当前层的第一个
            # 且当前数字和前一个数字相同，说明是重复的，跳过
            if i > start_index and candidates[i] == candidates[i - 1]:
                continue
            
            num = candidates[i]
            
            # 剪枝：如果当前和加上这个数字已经超过 target，后面的都大了（因为排序了）
            if current_sum + num > target:
                break
            
            # 1. 处理节点：选择当前数字
            path.append(num)
            
            # 2. 递归搜索：处理下一个数字
            #    注意：传 i+1，因为每个数字只能用一次
            backtracking(i + 1, current_sum + num)
            
            # 3. 回溯：撤销选择
            path.pop()
    
    backtracking(0, 0)
    return res


# 写法2：使用 used 数组（更容易理解）
def combinationSum2_used(candidates: List[int], target: int) -> List[List[int]]:
    """
    使用 used 数组的版本，更容易理解树层去重和树枝去重
    """
    res = []
    path = []
    candidates.sort()
    used = [False] * len(candidates)  # 标记每个位置的数字是否被使用过
    
    def backtracking(start_index: int, current_sum: int):
        if current_sum == target:
            res.append(path[:])
            return
        
        for i in range(start_index, len(candidates)):
            num = candidates[i]
            
            # 剪枝
            if current_sum + num > target:
                break
            
            # 树层去重
            # used[i-1]为False时说明已经被回溯过了，为True时说明在当前的递归路径上 。
            # 如果当前数字和前一个相同，且前一个没有被使用过
            # 说明是同一层的重复，跳过
            if i > 0 and candidates[i] == candidates[i - 1] and not used[i - 1]:
                continue
            
            # 标记为已使用
            used[i] = True
            path.append(num)
            
            # 递归，从下一个位置开始
            backtracking(i + 1, current_sum + num)
            
            # 回溯
            path.pop()
            used[i] = False
    
    backtracking(0, 0)
    return res