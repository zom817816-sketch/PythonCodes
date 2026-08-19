"""
206. 反转链表（Reverse Linked List）

题目描述：
给你单链表的头节点 head，请你反转链表，并返回反转后的链表。

输入描述：
一个单链表头节点 head。
链表中节点的数目范围是 [0, 5000]，-5000 <= Node.val <= 5000。

输出描述：
返回反转后的链表头节点。

输入示例 1：
head = [1, 2, 3, 4, 5]
输出示例 1：
[5, 4, 3, 2, 1]

输入示例 2：
head = [1, 2]
输出示例 2：
[2, 1]

输入示例 3：
head = []
输出示例 3：
[]

════════════════════════════════════════════════════════════════════════
核心概念：指针翻转
════════════════════════════════════════════════════════════════════════

反转链表的本质：把每个节点的 next 指针从"指向后一个"改为"指向前一个"。

迭代法用三个指针：prev（已反转部分的头）、cur（当前处理节点）、temp（暂存下一个）。

    反转前：None ← prev    cur → temp → ... → None
                          ↑ 需要把 cur.next 指向 prev

    反转后：None ← prev ← cur    temp → ... → None
                                  ↑ 新的 prev=cur, 新的 cur=temp

递归法的核心洞察：
    反转链表 = 反转头节点 + 反转剩余链表，然后把头节点接到反转后链表的末尾。
    head.next.next = head（让下一个节点指回当前节点）
    head.next = None（断开当前节点向前的连接）

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
迭代（双指针）                 O(n)            O(1)            ⭐⭐⭐⭐⭐ 推荐
递归                          O(n)            O(n)            ⭐⭐⭐ 代码简洁
────────────────────────────────────────────────────────────────────────

核心思想（迭代）：
────────────────────────────────────────────────────────────────────────
用 prev 和 cur 双指针，逐个翻转 next 指针。
每次循环：保存 cur.next → 翻转 cur.next → prev 前进 → cur 前进。
prev 最终指向原链表的尾节点（反转后的头节点）。
"""


class ListNode:
    """链表节点定义"""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# ══════════════════════════════════════════════════════════
# 解法一：迭代（双指针）⭐⭐⭐⭐⭐ 推荐
# ══════════════════════════════════════════════════════════


def reverseList(head: ListNode | None) -> ListNode | None:
    """迭代（双指针）⭐⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    用 prev 和 cur 两个指针遍历链表。
    每次将 cur.next 指向 prev（翻转指针方向），
    然后 prev 和 cur 同时前进一步。

    算法步骤：
    1. prev = None, cur = head。
    2. while cur:
       a. temp = cur.next（保存下一个节点）
       b. cur.next = prev（翻转指针）
       c. prev = cur（prev 前进）
       d. cur = temp（cur 前进）
    3. 返回 prev（原尾节点，新头节点）。

    时间复杂度：O(n) — 遍历一遍。
    空间复杂度：O(1) — 只用三个指针变量。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 3 -> 4 -> 5 -> None

    初始:  prev=None, cur=1

    第1轮: temp=2, 1.next=None, prev=1, cur=2
           None ← 1    2 -> 3 -> 4 -> 5 -> None

    第2轮: temp=3, 2.next=1, prev=2, cur=3
           None ← 1 ← 2    3 -> 4 -> 5 -> None

    第3轮: temp=4, 3.next=2, prev=3, cur=4
           None ← 1 ← 2 ← 3    4 -> 5 -> None

    第4轮: temp=5, 4.next=3, prev=4, cur=5
           None ← 1 ← 2 ← 3 ← 4    5 -> None

    第5轮: temp=None, 5.next=4, prev=5, cur=None
           None ← 1 ← 2 ← 3 ← 4 ← 5

    cur=None → 结束，返回 prev=5

    结果：5 -> 4 -> 3 -> 2 -> 1 -> None ✓
    """
    prev = None
    cur = head

    while cur:
        temp = cur.next  # 保存下一个节点
        cur.next = prev  # 翻转指针方向
        prev = cur  # prev 前进
        cur = temp  # cur 前进

    return prev


# ══════════════════════════════════════════════════════════
# 解法二：递归 ⭐⭐⭐
# ══════════════════════════════════════════════════════════


def reverseList_recursion(head: ListNode | None) -> ListNode | None:
    """递归 ⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    递归反转 head.next 子链表，得到反转后的新头节点 new_head。
    此时 head.next 仍是子链表反转后的尾节点。
    执行 head.next.next = head（让尾节点指回 head），
    再执行 head.next = None（断开 head 向前的连接）。

    算法步骤：
    1. 基础情况：head 为空或只有一个节点，返回 head。
    2. new_head = reverseList_recursion(head.next)（反转子链表）。
    3. head.next.next = head（子链表尾节点指回 head）。
    4. head.next = None（断开 head 向前连接）。
    5. 返回 new_head。

    时间复杂度：O(n) — 每个节点递归一次。
    空间复杂度：O(n) — 递归栈深度。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 3 -> None

    递归展开：
    reverse(1) → reverse(2) → reverse(3) → 3 是尾节点，返回 3

    回溯 reverse(2):
      new_head = 3
      head.next.next = head → 2.next.next = 2 → 3.next = 2
      head.next = None → 2.next = None
      结果: 3 -> 2 -> None, 返回 3

    回溯 reverse(1):
      new_head = 3
      head.next.next = head → 1.next.next = 1 → 2.next = 1
      head.next = None → 1.next = None
      结果: 3 -> 2 -> 1 -> None, 返回 3

    结果：3 -> 2 -> 1 -> None ✓
    """
    # 基础情况：空链表或只有一个节点
    if head is None or head.next is None:
        return head

    # 递归反转子链表
    new_head = reverseList_recursion(head.next)

    # head.next 是子链表反转后的尾节点
    # 让它指回 head，完成翻转
    head.next.next = head
    # 断开 head 向前的连接
    head.next = None

    return new_head


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 一、迭代法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：迭代法正确反转链表，返回原尾节点作为新头节点。
#
# 证明（循环不变量）：
# （1）不变量：在每次循环开始时，prev 指向已反转部分的头节点，
#     cur 指向未反转部分的头节点。prev 及其左侧的所有节点已反转，
#     cur 及其右侧的所有节点尚未反转。
#
# （2）初始：prev = None（已反转部分为空），cur = head（全部未反转）。
#     不变量成立。
#
# （3）保持：每次循环中：
#     - temp = cur.next 保存未反转部分的第二个节点。
#     - cur.next = prev 将 cur 接到已反转部分头部。
#     - prev = cur 使 prev 指向新的已反转部分头。
#     - cur = temp 使 cur 指向未反转部分的新头。
#     不变量仍然成立。
#
# （4）终止：cur = None，所有节点都已反转。
#     prev 指向最后一个被处理的节点 = 原尾节点 = 新头节点。
#
#
# 二、递归法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 用数学归纳法：
# （1）基础：空链表或单节点，直接返回 head，正确。
# （2）归纳：假设 reverseList_recursion 能正确反转长度 < n 的链表。
#     对于长度 n 的链表，head.next 子链表长度 n-1，递归正确反转。
#     new_head 是反转后的头（原尾节点）。
#     head.next 此时指向子链表反转后的尾节点（原 head.next）。
#     head.next.next = head 让原 head.next 指回 head。
#     head.next = None 断开向前连接。
#     结果：head 变为新链表的尾节点，指针方向全部正确。
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. 迭代法忘记保存 cur.next：
#    直接 cur.next = prev 后，原 cur.next 丢失，无法继续遍历。
#    必须先 temp = cur.next。
#
# 2. 迭代法返回 head 而不是 prev：
#    循环结束时 cur = None，head 仍指向原头节点（现在是尾节点）。
#    应返回 prev（新头节点）。
#
# 3. 递归法顺序错误：
#    必须先递归再翻转：head.next.next = head。
#    如果先 head.next = None 再 head.next.next = head 会空指针。
#
# 4. 递归法忘记 head.next = None：
#    不断开的话，新链表尾部形成环（head ↔ head.next）。
# ══════════════════════════════════════════════════════════
