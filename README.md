<div align="center">

# Python Codes

**算法实现 & 数据结构学习代码仓库**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Topics](https://img.shields.io/badge/Topics-13-blueviolet?style=flat-square)](#目录)
[![Solutions](https://img.shields.io/badge/Solutions-136%2B-brightgreen?style=flat-square)](#目录)
[![LeetCode](https://img.shields.io/badge/LeetCode-Problems-FFA116?style=flat-square&logo=leetcode&logoColor=white)](https://leetcode.cn/)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](#许可证)

从基础数据结构到动态规划，配套 **知识点总结 · 详细注释 · 多种解法对比**

数组 · 哈希表 · 链表 · 字符串 · 栈 · 单调栈 · 二叉树 · 双指针 · 回溯 · 贪心 · DFS · BFS · 动态规划

</div>

---

## 目录

| # | 专题 | 核心内容 | 文件数 |
|:-:|:-----|:---------|:-----:|
| 01 | [数组 Array](#数组-array) | 二分查找 · 双指针 · 滑动窗口 | 7 |
| 02 | [哈希表 HashTable](#哈希表-hashtable) | 空间换时间 · 去重计数 · 求和系列 | 9 |
| 03 | [链表 LinkedList](#链表-linkedlist) | 虚拟头节点 · 反转 · 判环 · 相交 | 8 |
| 04 | [字符串 String](#字符串-string) | 反转替换 · KMP · 重复子串 | 8 |
| 05 | [栈 Stack](#栈-stack) | 队列栈互拟 · 括号匹配 · 单调队列 · Top K | 7 |
| 06 | [单调栈 MonotonicStack](#单调栈-monotonicstack) | 每日温度 · 接雨水 · 柱状图矩形 | 6 |
| 07 | [二叉树 BinaryTree](#二叉树-binarytree) | 遍历 · 深度 · 路径 · BST 全套 | 28 |
| 08 | [双指针 TwoPointer](#双指针-twopointer) | 替换数字 | 2 |
| 09 | [回溯算法 BackTracking](#回溯算法-backtracking) | 组合 · 排列 · 子集 · 切割 · 棋盘 | 15 |
| 10 | [贪心算法 Greedy](#贪心算法-greedyalgorithms) | 股票 · 跳跃 · 区间调度 | 18 |
| 11 | [深度优先搜索 DFS](#深度优先搜索-deepfirstsearch) | 跳跃游戏 III · 记忆化搜索 | 1 |
| 12 | [广度优先搜索 BFS](#广度优先搜索-breadthfirstsearch) | 跳跃游戏 IV · 双向 BFS | 1 |
| 13 | [动态规划 DP](#动态规划-dynamicplanning) | 背包 · 股票 · 打家劫舍 · 子序列 · 编辑距离 | 38 |

> 📓 [学习笔记 py_codes](#学习笔记py_codes) · 💡 [算法知识点速查](#算法知识点速查) · 🚀 [使用说明](#使用说明) · 📚 [学习建议](#学习建议)

---

## 算法专题

### 数组 Array

> `Algorithms/Array` · 二分查找 / 双指针 / 滑动窗口

<details>
<summary><b>📂 查看全部文件（7 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_BinarySearch.py`](./Algorithms/Array/01_BinarySearch.py) | 二分查找 |
| [`02_RemoveElements.py`](./Algorithms/Array/02_RemoveElements.py) | 移除元素 |
| [`03_SquaresOfOrderedList.py`](./Algorithms/Array/03_SquaresOfOrderedList.py) | 有序数组平方 |
| [`04_ShortestSubArray.py`](./Algorithms/Array/04_ShortestSubArray.py) | 最短子数组 |
| [`05_RemoveRepeatedElements.py`](./Algorithms/Array/05_RemoveRepeatedElements.py) | 移除重复元素 |
| [`数组.md`](./Algorithms/Array/数组.md) | 📝 数组知识点总结 |
| [`排序算法.md`](./Algorithms/Array/排序算法.md) | 📝 排序算法总结 |

</details>

### 哈希表 HashTable

> `Algorithms/HashTable` · 空间换时间 / 去重计数 / 求和系列

<details>
<summary><b>📂 查看全部文件（9 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_AnagramDetection.py`](./Algorithms/HashTable/01_AnagramDetection.py) | 变位词检测 |
| [`02_IntersectionOfTwo.py`](./Algorithms/HashTable/02_IntersectionOfTwo.py) | 两个数组的交集 |
| [`03_HappyNum.py`](./Algorithms/HashTable/03_HappyNum.py) | 快乐数 |
| [`04_SumOfTwo.py`](./Algorithms/HashTable/04_SumOfTwo.py) | 两数之和 |
| [`05_FourSumCount.py`](./Algorithms/HashTable/05_FourSumCount.py) | 四数相加 |
| [`06_Ransom.py`](./Algorithms/HashTable/06_Ransom.py) | 赎金信 |
| [`07_SumOfThree.py`](./Algorithms/HashTable/07_SumOfThree.py) | 三数之和 |
| [`08_SumOfFour.py`](./Algorithms/HashTable/08_SumOfFour.py) | 四数之和 |
| [`哈希表.md`](./Algorithms/HashTable/哈希表.md) | 📝 哈希表知识点总结 |

</details>

### 链表 LinkedList

> `Algorithms/LinkedList` · 虚拟头节点 / 反转 / 判环 / 相交

<details>
<summary><b>📂 查看全部文件（8 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_linkedlist_base.py`](./Algorithms/LinkedList/01_linkedlist_base.py) | 链表基础 |
| [`02_linkedlist_design.py`](./Algorithms/LinkedList/02_linkedlist_design.py) | 链表设计 |
| [`03_linkedlist_reverse.py`](./Algorithms/LinkedList/03_linkedlist_reverse.py) | 链表反转 |
| [`04_exchange_pairs.py`](./Algorithms/LinkedList/04_exchange_pairs.py) | 交换节点对 |
| [`05_RemoveNthFromEnd.py`](./Algorithms/LinkedList/05_RemoveNthFromEnd.py) | 删除链表的倒数第 N 个节点（LeetCode 19） |
| [`06_IntersectionOfTwoLinkedLists.py`](./Algorithms/LinkedList/06_IntersectionOfTwoLinkedLists.py) | 相交链表（LeetCode 160） |
| [`07_LinkedListCycleII.py`](./Algorithms/LinkedList/07_LinkedListCycleII.py) | 环形链表 II（LeetCode 142） |
| [`链表.md`](./Algorithms/LinkedList/链表.md) | 📝 链表知识点总结 |

</details>

### 字符串 String

> `Algorithms/String` · 反转替换 / KMP / 重复子串

<details>
<summary><b>📂 查看全部文件（8 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_ReverseString.py`](./Algorithms/String/01_ReverseString.py) | 反转字符串 |
| [`02_ReverseSting2.py`](./Algorithms/String/02_ReverseSting2.py) | 反转字符串 II |
| [`03_ReplaceString.py`](./Algorithms/String/03_ReplaceString.py) | 替换字符串 |
| [`04_ReverseString2.py`](./Algorithms/String/04_ReverseString2.py) | 反转字符串（另一种实现） |
| [`05_Strstr.py`](./Algorithms/String/05_Strstr.py) | 字符串查找（KMP算法） |
| [`06_RepeatedSubstring.py`](./Algorithms/String/06_RepeatedSubstring.py) | 重复子字符串检测 |
| [`07_RepeatedStringMatch.py`](./Algorithms/String/07_RepeatedStringMatch.py) | 重复字符串匹配 |
| [`字符串.md`](./Algorithms/String/字符串.md) | 📝 字符串知识点总结 |

</details>

### 栈 Stack

> `Algorithms/Stack` · 队列栈互拟 / 括号匹配 / 单调队列 / 堆

<details>
<summary><b>📂 查看全部文件（7 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_QueueByStacks.py`](./Algorithms/Stack/01_QueueByStacks.py) | 用栈实现队列 |
| [`02_StackByQueues.py`](./Algorithms/Stack/02_StackByQueues.py) | 用队列实现栈 |
| [`03_BracketsMatch.py`](./Algorithms/Stack/03_BracketsMatch.py) | 括号匹配 |
| [`04_RemoveDuplicateStr.py`](./Algorithms/Stack/04_RemoveDuplicateStr.py) | 删除相邻重复项 |
| [`05_EvalReversePolishNotation.py`](./Algorithms/Stack/05_EvalReversePolishNotation.py) | 逆波兰表达式求值 |
| [`06_SlidingWindowMax.py`](./Algorithms/Stack/06_SlidingWindowMax.py) | 滑动窗口最大值（单调队列） |
| [`07_TopKFrequent.py`](./Algorithms/Stack/07_TopKFrequent.py) | 前K个高频元素（堆/桶排序） |

</details>

### 单调栈 MonotonicStack

> `Algorithms/MonotonicStack` · 每日温度 / 接雨水 / 柱状图矩形

<details>
<summary><b>📂 查看全部文件（6 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_DailyTemperature.py`](./Algorithms/MonotonicStack/01_DailyTemperature.py) | 每日温度（LeetCode 739，单调栈） |
| [`02_NextGreaterelement_i.py`](./Algorithms/MonotonicStack/02_NextGreaterelement_i.py) | 下一个更大元素 I（LeetCode 496，单调栈 + 哈希表） |
| [`03_NextGreaterElement_ii.py`](./Algorithms/MonotonicStack/03_NextGreaterElement_ii.py) | 下一个更大元素 II（LeetCode 503，循环数组 + 单调栈） |
| [`04_TrappingInRainWater.py`](./Algorithms/MonotonicStack/04_TrappingInRainWater.py) | 接雨水（LeetCode 42） |
| [`05_LargestRectangleInHistogram.py`](./Algorithms/MonotonicStack/05_LargestRectangleInHistogram.py) | 柱状图中最大的矩形（LeetCode 84） |
| [`单调栈.md`](./Algorithms/MonotonicStack/单调栈.md) | 📝 单调栈知识点总结 |

</details>

### 二叉树 BinaryTree

> `Algorithms/BinaryTree` · 遍历 / 深度 / 路径 / BST 增删改查

<details>
<summary><b>📂 查看全部文件（28 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_BinaryTreeTraversal.py`](./Algorithms/BinaryTree/01_BinaryTreeTraversal.py) | 二叉树遍历（前序/中序/后序/层序） |
| [`02_BinaryTreeUnifiedIterative.py`](./Algorithms/BinaryTree/02_BinaryTreeUnifiedIterative.py) | 二叉树遍历统一迭代实现（标记法） |
| [`03_BinaryTreeLayerLevelTraversal.py`](./Algorithms/BinaryTree/03_BinaryTreeLayerLevelTraversal.py) | 二叉树层序遍历及相关算法 |
| [`04_InvertBinaryTree.py`](./Algorithms/BinaryTree/04_InvertBinaryTree.py) | 翻转二叉树 |
| [`05_SymmetricBinaryTree.py`](./Algorithms/BinaryTree/05_SymmetricBinaryTree.py) | 对称二叉树检测 |
| [`06_MaxDepthBinaryTree.py`](./Algorithms/BinaryTree/06_MaxDepthBinaryTree.py) | 二叉树最大深度（含N叉树） |
| [`07_MinDepthBinaryTree.py`](./Algorithms/BinaryTree/07_MinDepthBinaryTree.py) | 二叉树最小深度 |
| [`08_CountCompleteTreeNodes.py`](./Algorithms/BinaryTree/08_CountCompleteTreeNodes.py) | 完全二叉树节点计数 |
| [`09_BalancedBinaryTree.py`](./Algorithms/BinaryTree/09_BalancedBinaryTree.py) | 平衡二叉树检测 |
| [`10_BinaryTreePaths.py`](./Algorithms/BinaryTree/10_BinaryTreePaths.py) | 二叉树所有路径 |
| [`11_SumOfLeftLeaves.py`](./Algorithms/BinaryTree/11_SumOfLeftLeaves.py) | 左叶子之和 |
| [`12_LeftBottomValue.py`](./Algorithms/BinaryTree/12_LeftBottomValue.py) | 左下角的值 |
| [`13_BinaryTreePathSum.py`](./Algorithms/BinaryTree/13_BinaryTreePathSum.py) | 路径总和 |
| [`14_BuildBinaryTree.py`](./Algorithms/BinaryTree/14_BuildBinaryTree.py) | 根据中序和后序遍历构造二叉树 |
| [`15_MaximumBinaryTree.py`](./Algorithms/BinaryTree/15_MaximumBinaryTree.py) | 二叉树的最大节点 |
| [`16_MergeTwoBinaryTrees.py`](./Algorithms/BinaryTree/16_MergeTwoBinaryTrees.py) | 合并两个二叉树 |
| [`17_SearchInBinaryTrees.py`](./Algorithms/BinaryTree/17_SearchInBinaryTrees.py) | BST查找节点 |
| [`18_ValidateBinarySearchTree.py`](./Algorithms/BinaryTree/18_ValidateBinarySearchTree.py) | 验证二叉搜索树 |
| [`19_MinAbsDiffInBST.py`](./Algorithms/BinaryTree/19_MinAbsDiffInBST.py) | BST最小绝对差值 |
| [`20_FindModeInBST.py`](./Algorithms/BinaryTree/20_FindModeInBST.py) | BST众数查找 |
| [`21_LowestCommonAncestorOfBinaryTree.py`](./Algorithms/BinaryTree/21_LowestCommonAncestorOfBinaryTree.py) | 二叉树最近公共祖先 |
| [`22_TrimBinaryTree.py`](./Algorithms/BinaryTree/22_TrimBinaryTree.py) | 修剪二叉搜索树 |
| [`23_InsertIntoBST.py`](./Algorithms/BinaryTree/23_InsertIntoBST.py) | BST插入节点 |
| [`24_DeleteInBST.py`](./Algorithms/BinaryTree/24_DeleteInBST.py) | BST删除节点 |
| [`25_ConvertSortedArrayToBST.py`](./Algorithms/BinaryTree/25_ConvertSortedArrayToBST.py) | 有序数组转BST（高度平衡） |
| [`26_ConvertBSTToGreaterTree.py`](./Algorithms/BinaryTree/26_ConvertBSTToGreaterTree.py) | BST转累加树 |
| [`binary-tree.md`](./Algorithms/BinaryTree/binary-tree.md) | 📝 二叉树知识点总结 |
| [`check_binary_tree.py`](./Algorithms/BinaryTree/check_binary_tree.py) | 🧪 二叉树测试工具 |

</details>

### 双指针 TwoPointer

> `Algorithms/TwoPointer` · 替换数字

<details>
<summary><b>📂 查看全部文件（2 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_ReplaceNumbers.py`](./Algorithms/TwoPointer/01_ReplaceNumbers.py) | 替换数字 |
| [`双指针.md`](./Algorithms/TwoPointer/双指针.md) | 📝 双指针知识点总结 |

</details>

### 回溯算法 BackTracking

> `Algorithms/BackTracking` · 组合 / 排列 / 子集 / 切割 / 棋盘

<details>
<summary><b>📂 查看全部文件（15 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_Combinations.py`](./Algorithms/BackTracking/01_Combinations.py) | 组合问题（LeetCode 77） |
| [`02_CombinationSum3.py`](./Algorithms/BackTracking/02_CombinationSum3.py) | 组合总和 III（LeetCode 216） |
| [`03_LetterCombinationsOfAPhoneNumber.py`](./Algorithms/BackTracking/03_LetterCombinationsOfAPhoneNumber.py) | 电话号码的字母组合（LeetCode 17） |
| [`04_CombinationSum.py`](./Algorithms/BackTracking/04_CombinationSum.py) | 组合总和（LeetCode 39） |
| [`05_CombinationSum2.py`](./Algorithms/BackTracking/05_CombinationSum2.py) | 组合总和 II（LeetCode 40） |
| [`06_PalindromePartitioning.py`](./Algorithms/BackTracking/06_PalindromePartitioning.py) | 分割回文串（LeetCode 131） |
| [`07_RestoreIPAddresses.py`](./Algorithms/BackTracking/07_RestoreIPAddresses.py) | 恢复 IP 地址（LeetCode 93） |
| [`08_Subsets.py`](./Algorithms/BackTracking/08_Subsets.py) | 子集问题（LeetCode 78） |
| [`09_NonDecreasingSubsequences.py`](./Algorithms/BackTracking/09_NonDecreasingSubsequences.py) | 非递减子序列（LeetCode 491） |
| [`10_Permutations.py`](./Algorithms/BackTracking/10_Permutations.py) | 全排列（LeetCode 46） |
| [`11_Permutaions_ii.py`](./Algorithms/BackTracking/11_Permutaions_ii.py) | 全排列 II（LeetCode 47，含重复元素） |
| [`12_Subsets_ii.py`](./Algorithms/BackTracking/12_Subsets_ii.py) | 子集 II（LeetCode 90，含重复元素） |
| [`13_NQueens.py`](./Algorithms/BackTracking/13_NQueens.py) | N 皇后问题（LeetCode 51） |
| [`14_Sudoku.py`](./Algorithms/BackTracking/14_Sudoku.py) | 解数独（LeetCode 37） |
| [`回溯.md`](./Algorithms/BackTracking/回溯.md) | 📝 回溯算法理论基础 |

</details>

### 贪心算法 GreedyAlgorithms

> `Algorithms/GreedyAlgorithms` · 局部最优 / 股票 / 跳跃 / 区间调度

<details>
<summary><b>📂 查看全部文件（18 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_AssignCookies.py`](./Algorithms/GreedyAlgorithms/01_AssignCookies.py) | 分发饼干（LeetCode 455） |
| [`02_WiggleSubsequence.py`](./Algorithms/GreedyAlgorithms/02_WiggleSubsequence.py) | 摆动序列（LeetCode 376） |
| [`03_MaxSubArray.py`](./Algorithms/GreedyAlgorithms/03_MaxSubArray.py) | 最大子数组和（LeetCode 53） |
| [`04_BestTimeToSellAndBuyStock.py`](./Algorithms/GreedyAlgorithms/04_BestTimeToSellAndBuyStock.py) | 买卖股票的最佳时机 II（LeetCode 122） |
| [`05_JumpGame.py`](./Algorithms/GreedyAlgorithms/05_JumpGame.py) | 跳跃游戏（LeetCode 55） |
| [`06_JumpGame_ii.py`](./Algorithms/GreedyAlgorithms/06_JumpGame_ii.py) | 跳跃游戏 II（LeetCode 45，贪心 + BFS + 回溯 + DP 四种解法） |
| [`07_MaximizeSumOfArrayAfterKNegations.py`](./Algorithms/GreedyAlgorithms/07_MaximizeSumOfArrayAfterKNegations.py) | 最大化数组取反后的和（LeetCode 1005，贪心 + 排序 + 最小堆三种解法） |
| [`08_GasStation.py`](./Algorithms/GreedyAlgorithms/08_GasStation.py) | 加油站（LeetCode 134，贪心算法） |
| [`09_Candy.py`](./Algorithms/GreedyAlgorithms/09_Candy.py) | 分发糖果（LeetCode 135） |
| [`10_LemonadeChange.py`](./Algorithms/GreedyAlgorithms/10_LemonadeChange.py) | 柠檬水找零（LeetCode 860） |
| [`11_ReconstructQueue.py`](./Algorithms/GreedyAlgorithms/11_ReconstructQueue.py) | 根据身高重建队列（LeetCode 406） |
| [`12_FindMinArrowShots.py`](./Algorithms/GreedyAlgorithms/12_FindMinArrowShots.py) | 用最少数量的箭引爆气球（LeetCode 452） |
| [`13_NonOverlappingIntervals.py`](./Algorithms/GreedyAlgorithms/13_NonOverlappingIntervals.py) | 无重叠区间（LeetCode 435） |
| [`14_PartitionLabels.py`](./Algorithms/GreedyAlgorithms/14_PartitionLabels.py) | 划分字母区间（LeetCode 763） |
| [`15_MergeIntervals.py`](./Algorithms/GreedyAlgorithms/15_MergeIntervals.py) | 合并区间（LeetCode 56，三种贪心解法） |
| [`16_MonotoneIncreasingDigits.py`](./Algorithms/GreedyAlgorithms/16_MonotoneIncreasingDigits.py) | 单调递增的数字（LeetCode 738，四种解法） |
| [`17_BinaryTreeCameras.py`](./Algorithms/GreedyAlgorithms/17_BinaryTreeCameras.py) | 监控二叉树（LeetCode 968，贪心算法） |
| [`贪心算法.md`](./Algorithms/GreedyAlgorithms/贪心算法.md) | 📝 贪心算法知识点总结 |

</details>

### 深度优先搜索 DeepFirstSearch

> `Algorithms/DeepFirstSearch` · DFS / 记忆化搜索

<details>
<summary><b>📂 查看全部文件（1 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_JumpGame_iii.py`](./Algorithms/DeepFirstSearch/01_JumpGame_iii.py) | 跳跃游戏 III（LeetCode 1306，DFS + BFS + 记忆化搜索 + 迭代DFS 四种解法） |

</details>

### 广度优先搜索 BreadthFirstSearch

> `Algorithms/BreadthFirstSearch` · BFS / 双向 BFS

<details>
<summary><b>📂 查看全部文件（1 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_JumpGame_iv.py`](./Algorithms/BreadthFirstSearch/01_JumpGame_iv.py) | 跳跃游戏 IV（LeetCode 1345，BFS + 同值分组 + 逐层处理 + 双向BFS 三种解法） |

</details>

### 动态规划 DynamicPlanning

> `Algorithms/DynamicPlanning` · 背包 / 股票 / 打家劫舍 / 子序列 / 编辑距离

<details>
<summary><b>📂 查看全部文件（38 个）</b></summary>

| 文件 | 说明 |
|:---|:---|
| [`01_BestTimeToSellAndBuyStock_i.py`](./Algorithms/DynamicPlanning/01_BestTimeToSellAndBuyStock_i.py) | 买卖股票的最佳时机（LeetCode 121） |
| [`02_FibonacciNumber.py`](./Algorithms/DynamicPlanning/02_FibonacciNumber.py) | 斐波那契数（LeetCode 509，四种解法） |
| [`03_ClimbingStairs.py`](./Algorithms/DynamicPlanning/03_ClimbingStairs.py) | 爬楼梯（LeetCode 70，四种解法） |
| [`04_MinCostClimbingStairs.py`](./Algorithms/DynamicPlanning/04_MinCostClimbingStairs.py) | 使用最小花费爬楼梯（LeetCode 746，五种解法） |
| [`05_UniquePaths.py`](./Algorithms/DynamicPlanning/05_UniquePaths.py) | 不同路径（LeetCode 62，三种解法） |
| [`06_UniquePaths.py`](./Algorithms/DynamicPlanning/06_UniquePaths.py) | 不同路径 II（LeetCode 63，含障碍物，三种解法） |
| [`07_IntegerBreak.py`](./Algorithms/DynamicPlanning/07_IntegerBreak.py) | 整数拆分（LeetCode 343，四种解法） |
| [`08_UniqueBST.py`](./Algorithms/DynamicPlanning/08_UniqueBST.py) | 不同的二叉搜索树（LeetCode 96，四种解法） |
| [`09_MaxResearchMaterials.py`](./Algorithms/DynamicPlanning/09_MaxResearchMaterials.py) | 研究材料选择（0-1背包问题，四种解法） |
| [`10_PartitionEqualSubsetSum.py`](./Algorithms/DynamicPlanning/10_PartitionEqualSubsetSum.py) | 分割等和子集（LeetCode 416，四种解法） |
| [`11_LastStoneWeight_ii.py`](./Algorithms/DynamicPlanning/11_LastStoneWeight_ii.py) | 最后一块石头的重量 II（LeetCode 1049，四种解法） |
| [`12_TargetSum.py`](./Algorithms/DynamicPlanning/12_TargetSum.py) | 目标和（LeetCode 494，四种解法） |
| [`13_OnesAndZeros.py`](./Algorithms/DynamicPlanning/13_OnesAndZeros.py) | 一和零（LeetCode 474，四种解法） |
| [`14_CoinChange_ii.py`](./Algorithms/DynamicPlanning/14_CoinChange_ii.py) | 零钱兑换 II（LeetCode 518，完全背包求组合数） |
| [`15_CombinationSum_iv.py`](./Algorithms/DynamicPlanning/15_CombinationSum_iv.py) | 组合总和 IV（LeetCode 377，求排列数） |
| [`16_ClimbStairs.py`](./Algorithms/DynamicPlanning/16_ClimbStairs.py) | 爬楼梯扩展版（每次可爬至多 m 阶） |
| [`17_CoinChange.py`](./Algorithms/DynamicPlanning/17_CoinChange.py) | 零钱兑换（LeetCode 322，完全背包求最小值） |
| [`18_PerfectSquares.py`](./Algorithms/DynamicPlanning/18_PerfectSquares.py) | 完全平方数（LeetCode 279，含 Lagrange 四平方定理） |
| [`19_WorkBreak.py`](./Algorithms/DynamicPlanning/19_WorkBreak.py) | 单词拆分（LeetCode 139，布尔型 DP） |
| [`20_HouseRobber.py`](./Algorithms/DynamicPlanning/20_HouseRobber.py) | 打家劫舍（LeetCode 198，经典线性 DP） |
| [`21_HouseRobber_ii.py`](./Algorithms/DynamicPlanning/21_HouseRobber_ii.py) | 打家劫舍 II（LeetCode 213，环形数组，三种解法） |
| [`22_HouseRobber_iii.py`](./Algorithms/DynamicPlanning/22_HouseRobber_iii.py) | 打家劫舍 III（LeetCode 337，树形 DP） |
| [`23_BestTimeToBuyAndSellStock_iii.py`](./Algorithms/DynamicPlanning/23_BestTimeToBuyAndSellStock_iii.py) | 买卖股票的最佳时机 III（LeetCode 123，最多两笔交易，三种解法） |
| [`24_BestTimeTobuyAndSellStock_iv.py`](./Algorithms/DynamicPlanning/24_BestTimeTobuyAndSellStock_iv.py) | 买卖股票的最佳时机 IV（LeetCode 188，最多 k 笔交易，三种解法） |
| [`25_BestTimeTobuyAndSellStockWithTransactionFee.py`](./Algorithms/DynamicPlanning/25_BestTimeTobuyAndSellStockWithTransactionFee.py) | 买卖股票的最佳时机含手续费（LeetCode 714） |
| [`26_BestTImeToSellStockWithColdown.py`](./Algorithms/DynamicPlanning/26_BestTImeToSellStockWithColdown.py) | 买卖股票的最佳时机含冷冻期（LeetCode 309） |
| [`27_LongestIncreasingSubsequence.py`](./Algorithms/DynamicPlanning/27_LongestIncreasingSubsequence.py) | 最长递增子序列（LeetCode 300） |
| [`28_LongestContinuousIncreasingSubsequence.py`](./Algorithms/DynamicPlanning/28_LongestContinuousIncreasingSubsequence.py) | 最长连续递增子序列（LeetCode 674） |
| [`29_MaxRepeatedSubarr.py`](./Algorithms/DynamicPlanning/29_MaxRepeatedSubarr.py) | 最长重复子数组（LeetCode 718） |
| [`30_UncrossedLines.py`](./Algorithms/DynamicPlanning/30_UncrossedLines.py) | 不相交的线（LeetCode 1035，等价于最长公共子序列） |
| [`31_MaximumSubarr.py`](./Algorithms/DynamicPlanning/31_MaximumSubarr.py) | 最大子数组和（LeetCode 53） |
| [`32_IsSubsequence.py`](./Algorithms/DynamicPlanning/32_IsSubsequence.py) | 判断子序列（LeetCode 392，双指针/DP/二分查找四种解法） |
| [`33_DistinctSubsequences.py`](./Algorithms/DynamicPlanning/33_DistinctSubsequences.py) | 不同的子序列（LeetCode 115，字符串匹配型 DP） |
| [`34_DeleteOperationForTwoStrings.py`](./Algorithms/DynamicPlanning/34_DeleteOperationForTwoStrings.py) | 两个字符串的删除操作（LeetCode 583，回溯/记忆化/DP 五种解法） |
| [`35_EditDistance.py`](./Algorithms/DynamicPlanning/35_EditDistance.py) | 编辑距离（LeetCode 72，插入/删除/替换三种操作） |
| [`36_Palindromic-Substrings.py`](./Algorithms/DynamicPlanning/36_Palindromic-Substrings.py) | 回文子串（LeetCode 647，区间 DP/中心扩展/暴力三种解法） |
| [`37_LongestPalindromicSubsequence.py`](./Algorithms/DynamicPlanning/37_LongestPalindromicSubsequence.py) | 最长回文子序列（LeetCode 516，区间 DP） |
| [`动态规划.md`](./Algorithms/DynamicPlanning/动态规划.md) | 📝 动态规划知识点总结 |

</details>

---

## 学习笔记（py_codes）

> 《数据结构与算法》课程学习笔记与课后练习

### Chapter03 数据结构基础

| 文件 | 说明 |
|:---|:---|
| [`AnagramDetection.py`](./py_codes/Chapter03/AnagramDetection.py) | 变位词检测 |
| [`Chapter03.ipynb`](./py_codes/Chapter03/Chapter03.ipynb) | 📝 第3章笔记 |
| [`Chapter03Questions.ipynb`](./py_codes/Chapter03/Chapter03Questions.ipynb) | 第3章习题 |
| [`ClassTrial.py`](./py_codes/Chapter03/ClassTrial.py) | 类的试验 |
| [`DictTrial.py`](./py_codes/Chapter03/DictTrial.py) | 字典试验 |
| [`PerformanceTest.py`](./py_codes/Chapter03/PerformanceTest.py) | 性能测试 |
| [`QueueWithTwoStacks.py`](./py_codes/Chapter03/QueueWithTwoStacks.py) | 用两个栈实现队列 |
| [`Sqrt.py`](./py_codes/Chapter03/Sqrt.py) | 平方根计算 |
| [`UnorderedList.py`](./py_codes/Chapter03/UnorderedList.py) | 无序列表 |

### Chapter04 递归算法

| 文件 | 说明 |
|:---|:---|
| [`Recursion.md`](./py_codes/Chapter04/Recursion.md) | 📝 递归算法笔记 |
| [`maze.txt`](./py_codes/Chapter04/maze.txt) | 迷宫数据 |
| [`maze_search.py`](./py_codes/Chapter04/maze_search.py) | 迷宫搜索 |
| [`recmc.py`](./py_codes/Chapter04/recmc.py) | 递归找零 |

---

## 算法知识点速查

| 专题 | 核心要点 |
|:---|:---|
| **数组** | 二分查找：有序数组的 O(log n) 查找<br>双指针：快慢指针、对撞指针<br>滑动窗口：子数组问题 |
| **链表** | 虚拟头节点：简化边界处理<br>双指针：找中点、判环<br>反转链表：迭代与递归 |
| **哈希表** | 空间换时间：O(1) 查询<br>常见应用：去重、计数、快速查找 |
| **字符串** | KMP 算法：O(n+m) 字符串匹配<br>双指针：反转、替换 |
| **栈与队列** | 括号匹配：栈的经典应用<br>单调栈/队列：Next Greater Element、滑动窗口最大值<br>堆：Top K 问题 |
| **单调栈** | 核心思想：维护单调递增/递减序列，高效解决"下一个更大/更小"问题<br>时间复杂度：O(n)，每个元素最多入栈出栈一次<br>适用场景：下一个更大元素、每日温度、柱状图中最大矩形、接雨水<br>分类：单调递增栈（找右边更小元素）、单调递减栈（找右边更大元素） |
| **二叉树** | 遍历：前序/中序/后序/层序（统一迭代标记法）<br>递归三要素：终止条件、返回值、单层逻辑<br>属性：对称、平衡（自顶向下 O(n²) / 自底向上 O(n)）、最大/最小深度、完全二叉树计数 O(log²n)、N 叉树扩展<br>路径与构造：所有路径、路径总和、左叶子之和、左下角值、中序+后序构造、合并两树<br>BST 系列：中序有序性、查找/验证/插入/删除（五种情况）/修剪/累加树、众数、最小差值、最近公共祖先、有序数组转平衡 BST<br>层序进阶：锯齿形遍历、每层最大值、连接右侧节点 |
| **回溯算法** | 核心思想：DFS 深搜 + 试错 + 剪枝，三部曲：选择 → 递归 → 回溯<br>组合：组合总和 I/II/III，注意去重与剪枝<br>切割：分割回文串，可用 DP 预处理优化判断<br>子集：路径记录所有节点；子集 II 需排序 + 去重<br>排列：used 数组标记；全排列 II 去重三法（排序剪枝/哈希/计数器）<br>非递减子序列：同层去重 + 非递减约束剪枝<br>棋盘：N 皇后、解数独（二维递归）<br>时间复杂度：通常 O(N!) 或 O(2^N) |
| **贪心算法** | 核心思想：局部最优 → 全局最优，无需回溯<br>适用场景：最优子结构、无后效性<br>常见题型：分发饼干、摆动序列、最大子数组和、买卖股票、跳跃游戏<br>区间问题：最少箭数引爆气球、无重叠区间、划分字母区间<br>解题步骤：分解子问题 → 确定贪心策略 → 求解 |
| **动态规划** | 核心思想：最优子结构 + 重叠子问题<br>DP 五部曲：dp 数组含义 → 递推公式 → 初始化 → 遍历顺序 → 打印验证<br>常见题型：股票买卖、背包问题（0-1背包、完全背包）、打家劫舍、子序列问题、分割等和子集、目标和、一和零 |

---

## 使用说明

### 运行算法文件

```bash
# 数组
python Algorithms/Array/01_BinarySearch.py

# 栈
python Algorithms/Stack/06_SlidingWindowMax.py

# 二叉树
python Algorithms/BinaryTree/14_BuildBinaryTree.py

# 回溯
python Algorithms/BackTracking/01_Combinations.py

# 贪心
python Algorithms/GreedyAlgorithms/01_AssignCookies.py

# 动态规划
python Algorithms/DynamicPlanning/01_BestTimeToSellAndBuyStock_i.py

# 单调栈
python Algorithms/MonotonicStack/01_DailyTemperature.py
```

### 运行学习笔记

```bash
jupyter notebook py_codes/Chapter03/Chapter03.ipynb
```

---

## 学习建议

1. **先看知识点总结** —— 每个目录下的 `.md` 文件整理了核心概念
2. **理解后再动手** —— 代码文件包含详细注释，建议先读注释再运行
3. **自己实现一遍** —— 看懂后尝试不看代码自己实现
4. **对比多种解法** —— 很多题目提供了多种解法（暴力 → 优化 → 最优）

---

## 许可证

本项目采用 [MIT](https://opensource.org/licenses/MIT) 许可证。

---

<div align="center">

<sub>如果这个仓库对你有帮助，欢迎点一个 ⭐ Star</sub>

</div>
