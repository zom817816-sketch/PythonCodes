"""
给你一个 无重复元素 的整数数组 candidates 和一个目标整数 target，
找出 candidates 中可以使数字和为目标数 target 的 所有 不同组合，并以列表形式返回。
你可以按 任意顺序 返回这些组合。

candidates 中的 同一个 数字可以 无限制重复被选取。
如果至少一个数字的被选数量不同，则两种组合是不同的。
对于给定的输入，保证和为 target 的不同组合数少于 150 个。

解题思路：

本题是回溯算法的经典题目，属于「组合问题」的变体。

核心特点：
  - 数字可以无限制重复使用（与 LeetCode 77 不同）
  - 需要求和等于 target（增加了剪枝条件）
  - 数组无重复元素，但结果需要去重（通过 start_index 控制）

与前面题目的区别：
  - LeetCode 77（组合）：每个数字只能用一次
  - LeetCode 17（电话号码）：每个数字必须且只能选一个字母
  - 本题（组合总和）：每个数字可以无限次使用

算法流程（以 candidates=[2,3,6,7], target=7 为例）：

  第1层（start_index=0, 可选 2,3,6,7）：
      选 2 → sum=2, path=[2] → 递归（start_index=0，还可以选 2）
          选 2 → sum=4, path=[2,2] → 递归
              选 2 → sum=6, path=[2,2,2] → 递归
                  选 2 → sum=8 > 7，剪枝，返回
                  选 3 → sum=9 > 7，剪枝，返回
                  ...
              选 3 → sum=7 == target，记录 [2,2,3] ✅
          选 3 → sum=7 == target，记录 [2,3,2] ❌（重复的，但通过 start_index 避免）
      选 3 → sum=3, path=[3] → 递归
          ...
      选 7 → sum=7 == target，记录 [7] ✅

搜索结果：[[2,2,3], [7]]

搜索树可视化（部分）：

                    [2,3,6,7] target=7
                   /    |    \
                 2      3     6    7
                /|\    /|\    |    |
               2 3... 2 3...  ...  ✅[7]
              /|
             2 3...
            /
           2(剪枝，sum>7)

回溯算法三要素：

1. 递归参数：
   - start_index：当前从哪个位置开始选（保证不重复选之前的组合）
   - current_sum：当前路径的和（用于判断终止条件）

2. 终止条件：
   - current_sum > target：超出目标，剪枝返回
   - current_sum == target：找到有效组合，记录结果

3. 单层逻辑：
   - 从 start_index 开始遍历 candidates
   - 选择当前数字（sum += num, path.append(num)）
   - 递归（注意：还是传 i，因为可以重复选当前数字）
   - 回溯（sum -= num, path.pop()）

关键注意点：

1. 可以重复选择：递归时传 i 而不是 i+1
   - backtracking(i, ...) 表示还可以选 candidates[i]
   - 如果传 i+1，就变成每个数字只能用一次了

2. 剪枝优化：
   - current_sum > target 时直接返回，不再继续搜索
   - 可以先对 candidates 排序，然后当 current_sum + candidates[i] > target 时 break

3. 避免重复组合：
   - 使用 start_index 控制，保证组合是有序的（非递减）
   - 这样 [2,2,3] 和 [2,3,2] 不会同时出现

复杂度分析：

时间复杂度：O(S)
  - S 为所有可行解的长度之和
  - 最坏情况下是指数级的，但由于剪枝，实际会小很多

空间复杂度：O(target / min(candidates))
  - 递归深度最多为 target / min(candidates)
  - 即全选最小数字时的递归层数
"""

from typing import List


def combinationSum(candidates: List[int], target: int) -> List[List[int]]:
    """
    返回所有和为 target 的组合⭐⭐
    
    参数：
        candidates: 无重复元素的整数数组
        target: 目标和
    
    返回：
        所有和为 target 的组合列表
    """
    res = []   # 存储所有满足条件的组合
    path = []  # 存储当前正在构建的组合
    
    def backtracking(start_index: int, current_sum: int):
        """
        回溯函数
        
        参数：
            start_index: 当前从 candidates 的哪个索引开始选择
            current_sum: 当前 path 中所有数字的和
        """
        # 终止条件 1：超出目标值，剪枝 
        # 如果当前和已经超过 target，这条路径不可能得到解
        if current_sum > target:
            return
        
        # 终止条件 2：找到目标组合 
        # 如果当前和等于 target，说明找到一个有效组合
        if current_sum == target:
            res.append(path[:])  # 注意：必须用切片复制
            return
        
        # 单层搜索逻辑 
        # 从 start_index 开始遍历，保证不重复选之前的数字
        for i in range(start_index, len(candidates)):
            # 获取当前数字
            num = candidates[i]
            
            # 1. 处理节点：将当前数字加入路径，更新当前和
            current_sum += num
            path.append(num)
            
            # 2. 递归搜索：继续选择数字
            #    注意：这里传 i 而不是 i+1，因为可以重复选择当前数字
            backtracking(i, current_sum)
            
            # 3. 回溯操作：撤销当前选择，恢复状态
            current_sum -= num  # 恢复当前和
            path.pop()          # 从路径中移除当前数字
    
    # 从第 0 个数字开始搜索，初始和为 0
    backtracking(0, 0)
    return res


#  剪枝优化版本（可选）
# 先对数组排序，可以在循环中提前终止
def combinationSum_optimized(candidates: List[int], target: int) -> List[List[int]]:
    """
    剪枝优化版本：先排序，当 sum + candidates[i] > target 时提前终止⭐⭐⭐
    """
    res = []
    path = []
    
    # 先排序，为了剪枝优化
    candidates.sort()
    
    def backtracking(start_index: int, current_sum: int):
        if current_sum == target:
            res.append(path[:])
            return
        
        for i in range(start_index, len(candidates)):
            num = candidates[i]
            
            # 剪枝：如果当前和加上这个数字已经超过 target，后面的都大了，直接 break
            if current_sum + num > target:
                break
            
            path.append(num)
            backtracking(i, current_sum + num)
            path.pop()
    
    backtracking(0, 0)
    return res
