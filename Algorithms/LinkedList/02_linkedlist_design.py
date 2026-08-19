"""
707. 设计链表（Design Linked List）

题目描述：
设计链表的实现。你可以选择使用单链表或双链表。
链表中的节点应该具有两个属性：val 和 next。val 是当前节点的值，
next 是指向下一个节点的指针/引用。

如果要使用双向链表，则还需要一个属性 prev 以指示链表中的上一个节点。
假设链表中的所有节点都是 0-index 的。

在链表类中实现这些功能：
    get(index)：获取链表中第 index 个节点的值。如果索引无效，则返回 -1。
    addAtHead(val)：在链表的第一个元素之前添加一个值为 val 的节点。
    addAtTail(val)：将值为 val 的节点追加到链表的最后一个元素。
    addAtIndex(index, val)：在链表中的第 index 个节点之前添加值为 val 的节点。
        - 如果 index 等于链表的长度，则该节点将附加到链表的末尾。
        - 如果 index 大于链表长度，则不会插入节点。
        - 如果 index 小于 0，则在头部插入节点。
    deleteAtIndex(index)：如果索引 index 有效，则删除链表中的第 index 个节点。

输入描述：
一系列操作指令，包括 "get"、"addAtHead"、"addAtTail"、"addAtIndex"、"deleteAtIndex"。

输出描述：
"get" 操作返回对应节点的值，其他操作无返回值。

输入示例：
["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"]
[[], [1], [3], [1, 2], [1], [1], [1]]
输出示例：
[null, null, null, null, 2, null, 3]

════════════════════════════════════════════════════════════════════════
核心概念：虚拟头结点与双向链表
════════════════════════════════════════════════════════════════════════

设计链表的关键在于"统一操作"，减少边界特判。

两种实现方式对比：
────────────────────────────────────────────────────────────────────────
维度                单链表 + 虚拟头结点         双向链表
────────────────────────────────────────────────────────────────────────
节点结构            val, next                   val, next, prev
头尾处理            虚拟头结点 dummy            head + tail 双指针
查找                O(n)，从头遍历              O(n)，可从近端遍历
插入/删除头         O(1)                        O(1)
插入/删除尾         O(n)                        O(1)
插入/删除中间        O(n)                        O(n) 查找 + O(1) 操作
空间                O(1) 额外                   O(1) 额外
适用场景            简单场景                    频繁尾部操作
────────────────────────────────────────────────────────────────────────

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
单链表 + 虚拟头结点            O(n)/操作        O(n)            ⭐⭐⭐⭐ 推荐
双向链表                      O(n)/操作        O(n)            ⭐⭐⭐⭐⭐ 最优
────────────────────────────────────────────────────────────────────────

核心思想（虚拟头结点）：
────────────────────────────────────────────────────────────────────────
用 dummy 节点统一所有插入/删除操作，包括头节点。
维护 size 变量，O(1) 判断 index 有效性。
addAtIndex 时，cur 走到第 index-1 个节点（dummy 算第 -1 个），
然后在 cur 和 cur.next 之间插入新节点。
"""


class ListNode:
    """单链表节点"""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


class DoublyListNode:
    """双向链表节点"""

    def __init__(
        self,
        val: int = 0,
        next: "DoublyListNode | None" = None,
        prev: "DoublyListNode | None" = None,
    ):
        self.val = val
        self.next = next
        self.prev = prev


# ══════════════════════════════════════════════════════════
# 解法一：单链表 + 虚拟头结点 ⭐⭐⭐⭐ 推荐
# ══════════════════════════════════════════════════════════


class MyLinkedList:
    """单链表 + 虚拟头结点 ⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    用 dummy 虚拟头结点统一所有操作，避免头节点特判。
    维护 size 变量实现 O(1) 的索引有效性判断。

    addAtIndex(index, val) 的统一逻辑：
        cur 从 dummy 出发走 index 步，到达第 index-1 个节点。
        new_node 插入到 cur 和 cur.next 之间。
        当 index == 0 时，cur = dummy，等价于头插。
        当 index == size 时，cur = 尾节点，等价于尾插。

    时间复杂度：
        get: O(index), addAtHead: O(1), addAtTail: O(n),
        addAtIndex: O(index), deleteAtIndex: O(index)
    空间复杂度：O(n) — 存储 n 个节点。

    图解示例：
    ────────────────────────────────────────────────────────
    执行操作：addAtHead(1), addAtTail(3), addAtIndex(1, 2), get(1)

    addAtHead(1):  dummy -> 1 -> None
    addAtTail(3):  dummy -> 1 -> 3 -> None
    addAtIndex(1, 2): cur 从 dummy 走 1 步到节点1
                      dummy -> 1 -> 2 -> 3 -> None
    get(1):        cur 从 dummy.next 走 1 步到节点2, 返回 2 ✓
    """

    def __init__(self) -> None:
        self.dummy = ListNode(0)  # 虚拟头结点
        self.size = 0  # 链表长度

    def get(self, index: int) -> int:
        """获取第 index 个节点的值，无效索引返回 -1"""
        if index < 0 or index >= self.size:
            return -1
        cur = self.dummy.next  # 从真实头节点开始
        for _ in range(index):
            cur = cur.next
        return cur.val

    def addAtHead(self, val: int) -> None:
        """在头部插入节点：等价于 addAtIndex(0, val)"""
        self.addAtIndex(0, val)

    def addAtTail(self, val: int) -> None:
        """在尾部插入节点：等价于 addAtIndex(size, val)"""
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index: int, val: int) -> None:
        """在第 index 个节点之前插入节点"""
        if index < 0 or index > self.size:
            return
        # cur 从 dummy 出发，走 index 步到达第 index-1 个节点
        cur = self.dummy
        for _ in range(index):
            cur = cur.next
        # 在 cur 和 cur.next 之间插入新节点
        new_node = ListNode(val, cur.next)
        cur.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        """删除第 index 个节点"""
        if index < 0 or index >= self.size:
            return
        # cur 走到第 index-1 个节点
        cur = self.dummy
        for _ in range(index):
            cur = cur.next
        # 跳过第 index 个节点
        cur.next = cur.next.next
        self.size -= 1


# ══════════════════════════════════════════════════════════
# 解法二：双向链表 ⭐⭐⭐⭐⭐ 最优
# ══════════════════════════════════════════════════════════


class MyLinkedListDoubly:
    """双向链表 ⭐⭐⭐⭐⭐ 最优

    核心思想：
    ────────────────────────────────────────────────────────
    维护 head 和 tail 双指针，从近端遍历减少查找时间。
    每个节点有 prev 和 next 指针，插入/删除时双向维护。

    优化：get(index) 时根据 index 与 size/2 的关系，
    选择从头或从尾开始遍历，最坏 O(n/2)。

    时间复杂度：
        get: O(min(index, n-index)),
        addAtHead/addAtTail: O(1),
        addAtIndex/deleteAtIndex: O(min(index, n-index))
    空间复杂度：O(n)

    图解示例：
    ────────────────────────────────────────────────────────
    双向链表结构：

    head → [1] ⇄ [2] ⇄ [3] ← tail
    None ← [1] ⇄ [2] ⇄ [3] → None

    deleteAtIndex(1) 删除节点2：
    head → [1] ⇄ [3] ← tail
    操作：node1.next = node3, node3.prev = node1
    """

    def __init__(self) -> None:
        self.head: DoublyListNode | None = None
        self.tail: DoublyListNode | None = None
        self.size = 0

    def _get_node(self, index: int) -> DoublyListNode | None:
        """获取第 index 个节点，从近端遍历"""
        if index < 0 or index >= self.size:
            return None
        if index < self.size // 2:
            # 从头遍历
            cur = self.head
            for _ in range(index):
                cur = cur.next
            return cur
        else:
            # 从尾遍历
            cur = self.tail
            for _ in range(self.size - index - 1):
                cur = cur.prev
            return cur

    def get(self, index: int) -> int:
        node = self._get_node(index)
        return node.val if node else -1

    def addAtHead(self, val: int) -> None:
        """O(1) 头插"""
        new_node = DoublyListNode(val, self.head, None)
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node  # 空链表，head 和 tail 都指向新节点
        self.head = new_node
        self.size += 1

    def addAtTail(self, val: int) -> None:
        """O(1) 尾插"""
        new_node = DoublyListNode(val, None, self.tail)
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node  # 空链表
        self.tail = new_node
        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return
        if index == 0:
            self.addAtHead(val)
        elif index == self.size:
            self.addAtTail(val)
        else:
            # 在第 index 个节点之前插入
            cur = self._get_node(index)
            new_node = DoublyListNode(val, cur, cur.prev)
            cur.prev.next = new_node
            cur.prev = new_node
            self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        node = self._get_node(index)
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next  # 删除头节点
        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev  # 删除尾节点
        self.size -= 1


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 一、虚拟头结点法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：虚拟头结点法的所有操作均正确维护链表结构和 size。
#
# 证明：
# （1）addAtIndex(index, val)：
#     cur 从 dummy（第 -1 个节点）走 index 步，到达第 index-1 个节点。
#     new_node 插入到 cur 和 cur.next 之间。
#     - index=0: cur=dummy，在 dummy 和 head 之间插入 = 头插。✓
#     - index=size: cur=尾节点，在尾节点和 None 之间插入 = 尾插。✓
#     - 0<index<size: 在中间插入。✓
#     size += 1 保持正确。
#
# （2）deleteAtIndex(index, val)：
#     cur 走到第 index-1 个节点，cur.next = cur.next.next 跳过第 index 个。
#     size -= 1 保持正确。
#
# （3）边界条件：
#     - 空链表 addAtTail: addAtIndex(0, val)，cur=dummy，插入正确。
#     - 删除唯一节点: cur=dummy，cur.next = None，正确。
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. addAtIndex 的 index 上界判断：
#    应该是 index > size 时拒绝（index == size 允许尾插）。
#    写成 index >= size 会漏掉尾插。
#
# 2. 双向链表删除时忘记维护 prev 指针：
#    只写 cur.next = cur.next.next 不够，
#    还需要 cur.next.next.prev = cur（如果 cur.next.next 存在）。
#
# 3. 双向链表空链表时 head 和 tail 同步：
#    插入第一个节点时 head = tail = new_node。
#    删除最后一个节点时 head = tail = None。
#
# 4. get 的索引越界：
#    index < 0 或 index >= size 时返回 -1，不能遍历否则会空指针。
# ══════════════════════════════════════════════════════════
