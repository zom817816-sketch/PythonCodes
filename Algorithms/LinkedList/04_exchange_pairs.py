"""
24. 两两交换链表中的节点（Swap Nodes in Pairs）

题目描述：
给定一个链表，两两交换其中相邻的节点，并返回交换后的链表。
你不能只是单纯的改变节点内部的值，而是需要实际的进行节点交换。

输入描述：
一个链表头节点 head。
链表中节点的数目在范围 [0, 100] 内，0 <= Node.val <= 100。

输出描述：
返回两两交换后的链表头节点。

输入示例 1：
head = [1, 2, 3, 4]
输出示例 1：
[2, 1, 4, 3]

输入示例 2：
head = []
输出示例 2：
[]

输入示例 3：
head = [1]
输出示例 3：
[1]

════════════════════════════════════════════════════════════════════════
核心概念：虚拟头结点 + 局部指针操作
════════════════════════════════════════════════════════════════════════

两两交换的关键：每次处理三个节点的指针关系。
    cur → node1 → node2 → node3
    交换后：cur → node2 → node1 → node3

需要修改 3 条指针：
    1. cur.next = node2（cur 指向第二个节点）
    2. node1.next = node3（第一个节点指向后续）
    3. node2.next = node1（第二个节点指回第一个）

注意顺序！必须先保存 node3，否则 node2.next = node1 后 node3 丢失。

    操作前：  cur → [1] → [2] → [3] → ...
    步骤1：   保存 first=cur.next(1), second=first.next(2), temp=second.next(3)
    步骤2：   cur.next = second         → cur → [2] → [3] → ...
    步骤3：   second.next = first       → cur → [2] → [1] → [3] → ...
    步骤4：   first.next = temp         → cur → [2] → [1] → [3] → ...
    步骤5：   cur = first（cur 移到交换后的第二个节点）

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
迭代（虚拟头结点）              O(n)            O(1)            ⭐⭐⭐⭐⭐ 推荐
递归                          O(n)            O(n)            ⭐⭐⭐⭐ 代码简洁
────────────────────────────────────────────────────────────────────────

核心思想（迭代）：
────────────────────────────────────────────────────────────────────────
用虚拟头结点统一处理头节点交换。
每次交换 cur 后面的两个节点，然后 cur 前进两步。
循环条件：cur.next 和 cur.next.next 都存在（至少两个节点可交换）。
"""


class ListNode:
    """链表节点定义"""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# ══════════════════════════════════════════════════════════
# 解法一：迭代（虚拟头结点）⭐⭐⭐⭐⭐ 推荐
# ══════════════════════════════════════════════════════════


def swapPairs(head: ListNode | None) -> ListNode | None:
    """迭代（虚拟头结点）⭐⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    用虚拟头结点统一处理。每次交换 cur 后面的两个节点，
    交换后 cur 前进到交换后的第二个节点（即原来的 first）。

    算法步骤：
    1. dummy = ListNode(0, head), cur = dummy。
    2. while cur.next and cur.next.next:
       a. first = cur.next, second = first.next, temp = second.next
       b. cur.next = second（cur 指向第二个）
       c. second.next = first（第二个指向第一个）
       d. first.next = temp（第一个指向后续）
       e. cur = first（前进到交换后的第二个位置）
    3. 返回 dummy.next。

    时间复杂度：O(n) — 每两个节点处理一次，共 n/2 次。
    空间复杂度：O(1) — 只用常数个指针。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 3 -> 4 -> None

    dummy -> 1 -> 2 -> 3 -> 4 -> None
     ↑ cur

    第1轮: first=1, second=2, temp=3
      cur.next = 2:     dummy -> 2    1 -> 3 -> 4
      second.next = 1:  dummy -> 2 -> 1 -> 3 -> 4
      first.next = 3:   dummy -> 2 -> 1 -> 3 -> 4 -> None
      cur = 1:
      dummy -> 2 -> 1 -> 3 -> 4 -> None
                     ↑ cur

    第2轮: first=3, second=4, temp=None
      cur.next = 4:     ... 1 -> 4    3 -> None
      second.next = 3:  ... 1 -> 4 -> 3 -> None
      first.next = None: ... 1 -> 4 -> 3 -> None
      cur = 3:
      dummy -> 2 -> 1 -> 4 -> 3 -> None
                              ↑ cur

    cur.next = None → 结束

    结果：2 -> 1 -> 4 -> 3 ✓
    """
    dummy = ListNode(0, head)
    cur = dummy

    while cur.next and cur.next.next:
        # 保存三个关键节点
        first = cur.next  # 第一个节点
        second = first.next  # 第二个节点
        temp = second.next  # 交换后的后续节点

        # 交换：cur → second → first → temp
        cur.next = second
        second.next = first
        first.next = temp

        # cur 前进到交换后的第二个节点（first）
        cur = first

    return dummy.next


# ══════════════════════════════════════════════════════════
# 解法二：递归 ⭐⭐⭐⭐
# ══════════════════════════════════════════════════════════


def swapPairs_recursion(head: ListNode | None) -> ListNode | None:
    """递归 ⭐⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    交换前两个节点，然后递归处理剩余链表。
    head 和 head.next 是要交换的一对节点。
    递归处理 head.next.next 子链表，得到结果 sub。
    交换：head.next.next = head, head.next = sub。
    新的头节点是原来的第二个节点。

    算法步骤：
    1. 基础情况：head 为空或只有一个节点，返回 head。
    2. new_head = head.next（交换后第二个节点变成头）。
    3. sub = swapPairs_recursion(new_head.next)（递归处理剩余）。
    4. head.next = sub（head 接到子链表前面）。
    5. new_head.next = head（第二个节点指回第一个）。
    6. 返回 new_head。

    时间复杂度：O(n) — 每两个节点递归一次。
    空间复杂度：O(n) — 递归栈深度 n/2。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 3 -> 4 -> None

    递归展开：
    swap(1) → swap(3) → swap(None) 返回 None

    回溯 swap(3):
      new_head = 4, sub = None
      3.next = None
      4.next = 3
      结果: 4 -> 3 -> None, 返回 4

    回溯 swap(1):
      new_head = 2, sub = 4 -> 3
      1.next = 4 -> 3
      2.next = 1
      结果: 2 -> 1 -> 4 -> 3, 返回 2

    结果：2 -> 1 -> 4 -> 3 ✓
    """
    # 基础情况：空链表或只剩一个节点
    if head is None or head.next is None:
        return head

    # 第二个节点变成新头
    new_head = head.next

    # 递归处理剩余链表
    sub = swapPairs_recursion(new_head.next)

    # 交换：head 接到子链表前，new_head 指回 head
    head.next = sub
    new_head.next = head

    return new_head


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 一、迭代法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：迭代法正确两两交换所有相邻节点对。
#
# 证明（循环不变量）：
# （1）不变量：cur 始终指向"已处理部分的最后一个节点"。
#     cur.next 和 cur.next.next 是待交换的一对。
#     cur 之前的所有节点已完成两两交换。
#
# （2）初始：cur = dummy，已处理部分为空，不变量成立。
#
# （3）保持：交换 first 和 second 后：
#     - cur.next = second（cur 连到交换后的头）
#     - second.next = first（交换后第二个指回第一个）
#     - first.next = temp（第一个连到后续未处理部分）
#     - cur = first（first 是交换后的尾 = 已处理部分的新末尾）
#     不变量成立。
#
# （4）终止：cur.next 或 cur.next.next 为 None，
#     剩余 0 或 1 个节点不需要交换。
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. 指针修改顺序错误：
#    如果先 second.next = first 再 first.next = temp，
#    则 temp 原本通过 second.next 访问，但现在 second.next 已改，
#    temp 丢失。必须先保存 temp = second.next。
#
# 2. 忘记虚拟头结点：
#    不用虚拟头结点时，交换第一对节点需要特殊处理头指针。
#    用虚拟头结点后所有操作统一。
#
# 3. 递归法返回值错误：
#    应返回 new_head（原第二个节点），不是 head。
#    head 在交换后变成了第二个节点。
#
# 4. 奇数个节点：
#    最后一个节点没有配对，不交换。
#    循环条件 cur.next and cur.next.next 确保至少两个才交换。
# ══════════════════════════════════════════════════════════
