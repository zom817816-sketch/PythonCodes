"""
给定一个仅包含数字 2-9 的字符串，返回所有它能表示的字母组合。答案可以按 任意顺序 返回。
给出数字到字母的映射如下（与电话按键相同）。注意 1 不对应任何字母。
    2: "abc"    3: "def"    4: "ghi"
    5: "jkl"    6: "mno"    7: "pqrs"
    8: "tuv"    9: "wxyz"

解题思路：

本题是回溯算法的经典题目，属于「组合问题」的变体。

核心思想：
  每个数字对应多个字母，需要遍历每个数字的所有可能字母，
  通过回溯算法枚举所有可能的组合。

与 LeetCode 77（组合问题）的区别：
  - 组合问题：从 n 个数中选 k 个，每层可以选择"跳过"某些数字
  - 本题：每个数字必须选一个字母，每层都必须做选择

算法流程（以输入 "23" 为例）：

  第1层（处理数字'2'）：
      选择 'a' → path=['a'] → 递归处理下一个数字
          第2层（处理数字'3'）：
              选择 'd' → path=['a','d'] → index==2，记录 "ad"
              选择 'e' → path=['a','e'] → index==2，记录 "ae"
              选择 'f' → path=['a','f'] → index==2，记录 "af"
      选择 'b' → path=['b'] → 递归处理下一个数字
          第2层：
              选择 'd' → 记录 "bd"
              选择 'e' → 记录 "be"
              选择 'f' → 记录 "bf"
      选择 'c' → path=['c'] → 递归处理下一个数字
          第2层：
              选择 'd' → 记录 "cd"
              选择 'e' → 记录 "ce"
              选择 'f' → 记录 "cf"

搜索树可视化：

          2(abc)
         /  |  \
       'a' 'b' 'c'
       /|\ /|\ /|\
      d e f d e f d e f    ← 3(def) 对应的字母
      ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓ ↓
     ad ae af bd be bf cd ce cf

回溯算法三要素：

1. 递归参数：index 表示当前处理到第几个数字（digits 的索引）
2. 终止条件：当 index == len(digits)，说明处理完所有数字
3. 单层逻辑：获取当前数字对应的所有字母，遍历每个字母，选择→递归→回溯

关键注意点：

1. 数字到字母的映射：使用字典存储，key 可以是 str 或 int
2. 空字符串处理：如果 digits 为空，直接返回空列表
3. 结果收集：使用 "".join(path) 将列表转为字符串
4. 每层必选：本题每层都必须选择一个字母，没有"跳过"的选项

复杂度分析：

时间复杂度：O(3^N × 4^M) 
  - N 是对应 3 个字母的数字个数（2,3,4,5,6,8）
  - M 是对应 4 个字母的数字个数（7,9）
  - 最坏情况：全是 7 或 9，时间复杂度为 O(4^N)
  - 每个结果需要 O(N) 时间拼接字符串

空间复杂度：O(N)
  - N 是 digits 的长度
  - 递归调用栈深度为 N
  - path 数组同时只存一条路径，大小为 N
"""

from typing import List


def letterCombinations(digits: str) -> List[str]:
    """
    返回数字字符串能表示的所有字母组合
    
    参数：
        digits: 仅包含数字 2-9 的字符串
    
    返回：
        所有可能的字母组合列表
    """
    
    # 边界情况处理 
    # 如果输入为空字符串，直接返回空列表
    if not digits:
        return []
    
    #  数字到字母的映射表 
    # 注意：key 可以是 str 或 int，但要与 digits[index] 的类型一致
    # digits[index] 返回的是 str，所以这里用 str 作为 key
    phone_map = {
        '2': 'abc',
        '3': 'def',
        '4': 'ghi',
        '5': 'jkl',
        '6': 'mno',
        '7': 'pqrs',
        '8': 'tuv',
        '9': 'wxyz'
    }
    
    #  初始化 
    res = []   # 存储所有满足条件的字母组合
    path = []  # 存储当前正在构建的字母组合（单条路径）
    
    def backtracking(index: int):
        """
        回溯函数：递归构建字母组合
        
        参数：
            index: 当前要处理的数字在 digits 中的索引（0-based）
        """
        # 终止条件 
        # 当 index 等于 digits 的长度，说明所有数字都已处理完毕
        # 此时 path 中存储的是一个完整的字母组合
        if index == len(digits):
            # 将 path 列表中的字母拼接成字符串，加入结果
            res.append(''.join(path))
            return
        
        # 单层搜索逻辑 
        # 获取当前要处理的数字
        digit = digits[index]
        
        # 获取该数字对应的所有可选字母
        letters = phone_map[digit]
        
        # 遍历该数字的每个字母
        for letter in letters:
            # 1. 处理节点：将当前字母加入路径
            path.append(letter)
            
            # 2. 递归搜索：处理下一个数字
            #    index + 1 表示处理 digits 中的下一个字符
            backtracking(index + 1)
            
            # 3. 回溯操作：撤销当前选择，尝试下一个字母
            #    这一步确保能尝试该数字的其他字母
            path.pop()
    
    # 从第 0 个数字开始处理
    backtracking(0)
    return res
