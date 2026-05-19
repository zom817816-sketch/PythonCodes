"""
给你一个整数数组 nums 和一个整数 k ，请你返回其中出现频率前 k 高的元素。
你可以按任意顺序返回答案。

示例 1：
输入：nums = [1,1,1,2,2,3], k = 2
输出：[1,2]

示例 2：
输入：nums = [1], k = 1
输出：[1]

示例 3：
输入：nums = [1,2,1,2,1,2,3,1,3,2], k = 2
输出：[1,2]

解题思路：
1. 首先统计每个元素的出现频率
2. 然后找出频率最高的 k 个元素

不同解法的时间复杂度：
- 解法1：使用 Counter.most_common() - O(n log n)
- 解法2：使用排序 - O(n log n)
- 最优解：使用最小堆 - O(n log k)，当 k << n 时更优
"""

import heapq
from collections import Counter


def topKFrequent(nums: list, k: int) -> list:
    """
    解法1：使用 Counter 的 most_common 方法

    思路：
    - 使用 Counter 统计每个元素的频率
    - 使用 most_common(k) 直接获取频率最高的 k 个元素

    时间复杂度：O(n log n) - most_common 内部使用排序
    空间复杂度：O(n) - 存储频率字典

    优点：代码简洁，Pythonic
    缺点：时间复杂度不是最优
    """
    # 统计每个元素的频率
    counter = Counter(nums)
    # 获取频率最高的 k 个元素（返回 [(元素, 频率), ...]）
    top_k = counter.most_common(k)
    # 提取元素值
    return [item[0] for item in top_k]


def topKFrequent_1(nums: list, k: int) -> list:
    """
    解法2：手动统计频率 + 排序

    思路：
    - 手动遍历统计每个元素的频率
    - 将元素按频率降序排序
    - 取前 k 个元素

    时间复杂度：O(n log n) - 排序 dominates
    空间复杂度：O(n) - 存储频率字典

    优点：不依赖 Counter，展示底层逻辑
    缺点：手动实现较繁琐，时间复杂度不是最优
    """
    # 手动统计频率
    counter = {}
    for num in nums:
        counter[num] = counter.get(num, 0) + 1

    # 转换为列表并按频率降序排序
    # 降序排序
    items = list(counter.items())
    items.sort(key=lambda x: x[1], reverse=True)

    # 取前 k 个元素
    top_k = items[:k]
    return [item[0] for item in top_k]


def topKFrequent_optimized(nums: list, k: int) -> list:
    """
    解法3：最小堆优化（最优解法）

    思路：
    - 统计每个元素的频率
    - 维护一个大小为 k 的最小堆
    - 堆中存储 (频率, 元素)，堆顶是频率第 k 大的元素
    - 遍历所有元素，如果当前频率大于堆顶，则替换堆顶

    时间复杂度：O(n log k)
      - 统计频率：O(n)
      - 建堆：O(n)（使用 heapify）或 O(n log k)（逐个插入）
      - 维护堆：O(n log k)
    空间复杂度：O(n) - 存储频率字典，堆占用 O(k)

    适用场景：当 k << n 时，比 O(n log n) 的解法快很多
    例如：n = 1000000, k = 10 时，log k = 3.3, log n = 20
    """
    if k == 0 or not nums:
        return []

    # 统计频率
    counter = Counter(nums)

    # 使用最小堆维护前 k 个高频元素
    # 堆中存储 (频率, 元素)，Python 默认按第一个元素（频率）比较
    min_heap = []

    for num, freq in counter.items():
        if len(min_heap) < k:
            # 堆未满，直接插入
            heapq.heappush(min_heap, (freq, num))
        elif freq > min_heap[0][0]:
            # 当前频率大于堆顶（第 k 大的频率），替换堆顶
            heapq.heapreplace(min_heap, (freq, num))

    # 提取结果
    return [item[1] for item in min_heap]


def topKFrequent_bucket_sort(nums: list, k: int) -> list:
    """
    解法4：桶排序（计数排序思想）

    思路：
    - 统计每个元素的频率
    - 使用桶数组，索引表示频率，值是具有该频率的元素列表
    - 从高频到低频遍历桶，收集元素

    时间复杂度：O(n) - 线性时间
    空间复杂度：O(n) - 桶数组

    适用场景：当频率范围不大时，可以达到线性时间
    限制：需要额外的空间存储桶
    """
    if k == 0 or not nums:
        return []

    # 统计频率
    counter = Counter(nums)

    # 找到最大频率，创建桶数组
    max_freq = max(counter.values())
    buckets = [[] for _ in range(max_freq + 1)]

    # 将元素放入对应频率的桶中
    for num, freq in counter.items():
        buckets[freq].append(num)

    # 从高频率到低频率收集元素
    res = []
    for freq in range(max_freq, 0, -1):
        if buckets[freq]:
            res.extend(buckets[freq])
            if len(res) >= k:
                return res[:k]

    return res[:k]


class SimpleMinHeap:
    """
    手动实现的最小堆（简化版）

    堆是用列表实现的完全二叉树，满足：
    - 父节点的值 <= 子节点的值（最小堆性质）
    - 索引 i 的节点：
      - 左子节点：2*i + 1
      - 右子节点：2*i + 2
      - 父节点：(i-1) // 2
    """

    def __init__(self, capacity):
        self.capacity = capacity  # 堆的最大容量
        self.data = []  # 存储堆元素

    def parent(self, i):
        """获取父节点索引"""
        return (i - 1) // 2

    def left_child(self, i):
        """获取左子节点索引"""
        return 2 * i + 1

    def right_child(self, i):
        """获取右子节点索引"""
        return 2 * i + 2

    def size(self):
        """返回堆的大小"""
        return len(self.data)

    def is_empty(self):
        """判断堆是否为空"""
        return len(self.data) == 0

    def is_full(self):
        """判断堆是否已满"""
        return len(self.data) >= self.capacity

    def peek(self):
        """查看堆顶元素（不移除）"""
        if self.is_empty():
            return None
        return self.data[0]

    def _swap(self, i, j):
        """交换两个位置的元素"""
        self.data[i], self.data[j] = self.data[j], self.data[i]

    def _heapify_up(self, i):
        """
        向上调整：从位置 i 开始，向上调整保持堆性质
        用于插入操作后恢复堆
        """
        # 如果当前节点不是根节点，且小于父节点，则交换
        while i > 0 and self.data[i] < self.data[self.parent(i)]:
            self._swap(i, self.parent(i))
            i = self.parent(i)

    def _heapify_down(self, i):
        """
        向下调整：从位置 i 开始，向下调整保持堆性质
        用于删除堆顶后恢复堆
        """
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)

        # 找出当前节点和左右子节点中最小的
        if left < self.size() and self.data[left] < self.data[min_index]:
            min_index = left
        if right < self.size() and self.data[right] < self.data[min_index]:
            min_index = right

        # 如果当前节点不是最小的，交换并继续向下调整
        if i != min_index:
            self._swap(i, min_index)
            self._heapify_down(min_index)

    def push(self, item):
        """
        插入元素到堆中
        步骤：1. 放到末尾  2. 向上调整
        """
        if self.is_full():
            raise Exception("堆已满")
        self.data.append(item)
        self._heapify_up(self.size() - 1)

    def pop(self):
        """
        弹出堆顶元素（最小值）
        步骤：1. 首尾交换  2. 删除末尾  3. 向下调整
        """
        if self.is_empty():
            raise Exception("堆为空")

        # 交换堆顶和最后一个元素
        self._swap(0, self.size() - 1)
        # 移除最后一个元素（原堆顶）
        min_val = self.data.pop()
        # 向下调整新的堆顶
        if not self.is_empty():
            self._heapify_down(0)
        return min_val

    def replace(self, item):
        """
        替换堆顶元素
        步骤：1. 直接替换堆顶  2. 向下调整
        比 pop + push 更高效
        """
        if self.is_empty():
            raise Exception("堆为空")

        self.data[0] = item
        self._heapify_down(0)

    def __repr__(self):
        return f"MinHeap({self.data})"


def topKFrequent_manual_heap(nums: list, k: int) -> list:
    """
    解法5：使用手动实现的最小堆

    思路和解法3相同，但使用自己实现的 SimpleMinHeap
    帮助理解堆的内部工作原理

    时间复杂度：O(n log k)
    空间复杂度：O(k) - 堆占用
    """
    if k == 0 or not nums:
        return []

    # 统计频率
    counter = Counter(nums)

    # 创建容量为 k 的最小堆
    min_heap = SimpleMinHeap(k)

    for num, freq in counter.items():
        if not min_heap.is_full():
            # 堆未满，直接插入 (频率, 元素)
            min_heap.push((freq, num))
        elif freq > min_heap.peek()[0]:
            # 当前频率大于堆顶，替换堆顶
            min_heap.replace((freq, num))

    # 提取结果
    return [item[1] for item in min_heap.data]


# 测试代码
if __name__ == "__main__":
    test_cases = [
        ([1, 1, 1, 2, 2, 3], 2),
        ([1], 1),
        ([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2),
    ]

    for nums, k in test_cases:
        print(f"\n输入：nums = {nums}, k = {k}")
        print(f"解法1 (Counter): {topKFrequent(nums, k)}")
        print(f"解法2 (排序): {topKFrequent_1(nums, k)}")
        print(f"解法3 (最小堆): {topKFrequent_optimized(nums, k)}")
        print(f"解法4 (桶排序): {topKFrequent_bucket_sort(nums, k)}")
        print(f"解法5 (手动堆): {topKFrequent_manual_heap(nums, k)}")

    # 演示手动堆的操作
    print("\n" + "=" * 50)
    print("手动堆操作演示：")
    heap = SimpleMinHeap(5)
    for item in [(3, "C"), (1, "A"), (4, "D"), (2, "B")]:
        print(f"插入 {item}，堆状态: ", end="")
        heap.push(item)
        print(heap)
    print(f"堆顶元素: {heap.peek()}")
    print(f"弹出堆顶: {heap.pop()}，堆状态: {heap}")
