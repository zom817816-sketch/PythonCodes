"""
203. 移除链表元素（Remove Linked List Elements）

题目描述：
给你一个链表的头节点 head 和一个整数 val，请你删除链表中所有满足
Node.val == val 的节点，并返回新的头节点。

输入描述：
一个链表头节点 head 和一个整数 val。
链表节点数目在范围 [0, 10^4] 内，1 <= Node.val <= 50，0 <= val <= 50。

输出描述：
返回删除所有值为 val 的节点后的链表头节点。

输入示例 1：
head = [1, 2, 6, 3, 4, 5, 6], val = 6
输出示例 1：
[1, 2, 3, 4, 5]

输入示例 2：
head = [], val = 1
输出示例 2：
[]

输入示例 3：
head = [7, 7, 7, 7], val = 7
输出示例 3：
[]

════════════════════════════════════════════════════════════════════════
核心概念：虚拟头结点（Dummy Head）
════════════════════════════════════════════════════════════════════════

链表删除的核心操作：跳过节点
    cur.next = cur.next.next
    即让前驱节点直接指向后继节点，被删节点脱离链表。

为什么需要虚拟头结点？
    链表中删除中间节点和尾部节点，操作统一：cur.next = cur.next.next。
    但删除头节点不同：头节点没有前驱，需要单独处理 head = head.next。
    如果头节点连续需要删除（如 [7,7,7,7]），就要循环处理头节点。

    虚拟头结点在真实头节点之前加一个哨兵节点 dummy，
    使得真实头节点也有"前驱"，所有删除操作统一为 cur.next = cur.next.next。

    ┌──────┐    ┌──────┐    ┌──────┐    ┌──────┐
    │dummy │───▶│  1   │───▶│  2   │───▶│  3   │───▶ None
    └──────┘    └──────┘    └──────┘    └──────┘
                 ↑ 真实头节点现在也有前驱 dummy

三种解法对比：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
递归                          O(n)            O(n)            ⭐⭐ 代码简洁
原表直接删除                   O(n)            O(1)            ⭐⭐⭐ 需处理头节点
虚拟头结点                     O(n)            O(1)            ⭐⭐⭐⭐⭐ 推荐
────────────────────────────────────────────────────────────────────────

核心思想（虚拟头结点）：
────────────────────────────────────────────────────────────────────────
创建 dummy 节点指向 head，用 cur 指针遍历。
每次检查 cur.next 是否需要删除：
    - 是 → cur.next = cur.next.next（跳过，cur 不动，因为新 cur.next 也可能要删）
    - 否 → cur = cur.next（前进）
最后返回 dummy.next。
"""


class ListNode:
    """链表节点定义"""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# ══════════════════════════════════════════════════════════
# 解法一：递归
# ══════════════════════════════════════════════════════════


def removeElements_recursion(head: ListNode | None, val: int) -> ListNode | None:
    """递归 ⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    递归地处理"当前头节点 + 后续链表"。
    先递归处理 head.next 子链表，得到清理后的结果。
    再判断 head 本身是否需要删除：
        - head.val == val → 丢弃 head，返回子链表结果
        - head.val != val → 把 head 接到子链表前面

    算法步骤：
    1. 基础情况：head 为空，返回 None。
    2. 递归处理 head.next，得到 cleaned = removeElements_recursion(head.next, val)。
    3. 如果 head.val == val，返回 cleaned（跳过 head）。
    4. 否则 head.next = cleaned，返回 head。

    时间复杂度：O(n) — 每个节点递归一次。
    空间复杂度：O(n) — 递归栈深度。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 6 -> 3 -> 4 -> 5 -> 6, val = 6

    递归展开（从后往前回溯）：
    remove(6->None)     → head.val==6, 返回 None
    remove(5->6)        → head.val!=6, 5.next=None, 返回 5
    remove(4->5)        → head.val!=6, 4.next=5,   返回 4
    remove(3->4)        → head.val!=6, 3.next=4,   返回 3
    remove(6->3)        → head.val==6, 返回 3
    remove(2->6)        → head.val!=6, 2.next=3,   返回 2
    remove(1->2)        → head.val!=6, 1.next=2,   返回 1

    结果：1 -> 2 -> 3 -> 4 -> 5 ✓
    """
    # 基础情况：空链表
    if head is None:
        return None

    # 递归处理后续链表
    head.next = removeElements_recursion(head.next, val)

    # 判断当前头节点是否需要删除
    if head.val == val:
        return head.next  # 跳过当前节点
    else:
        return head  # 保留当前节点


# ══════════════════════════════════════════════════════════
# 解法二：原表直接删除
# ══════════════════════════════════════════════════════════


def removeElements_direct(head: ListNode | None, val: int) -> ListNode | None:
    """原表直接删除 ⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    不用虚拟头结点，分两步处理：
    第一步：循环删除头部连续的值为 val 的节点。
    第二步：遍历剩余链表，删除中间和尾部的 val 节点。

    算法步骤：
    1. while head and head.val == val: head = head.next（删头）
    2. cur = head，while cur and cur.next:
       a. cur.next.val == val → cur.next = cur.next.next（跳过）
       b. 否则 cur = cur.next（前进）
    3. 返回 head。

    时间复杂度：O(n) — 最多遍历两遍。
    空间复杂度：O(1) — 只用指针变量。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 7 -> 7 -> 3 -> 7 -> 4, val = 7

    第一步删头：head 从 7→7→3，停在 3
    第二步遍历：
      cur=3, cur.next=7 → 跳过7, cur.next=4
      cur=3, cur.next=4, 4≠7 → cur=4
      cur=4, cur.next=None → 结束

    结果：3 -> 4 ✓
    """
    # 第一步：删除头部连续的 val 节点
    while head is not None and head.val == val:
        head = head.next

    # 第二步：删除中间和尾部的 val 节点
    cur = head
    while cur is not None and cur.next is not None:
        if cur.next.val == val:
            cur.next = cur.next.next  # 跳过目标节点，cur 不动
        else:
            cur = cur.next  # 前进

    return head


# ══════════════════════════════════════════════════════════
# 解法三：虚拟头结点 ⭐⭐⭐⭐⭐ 推荐
# ══════════════════════════════════════════════════════════


def removeElements(head: ListNode | None, val: int) -> ListNode | None:
    """虚拟头结点 ⭐⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    创建虚拟头结点 dummy 指向 head，使所有节点（包括头节点）
    都有统一的前驱节点，删除操作统一为 cur.next = cur.next.next。

    算法步骤：
    1. dummy = ListNode(0, head)，cur = dummy。
    2. while cur.next:
       a. cur.next.val == val → cur.next = cur.next.next（跳过，cur 不动）
       b. 否则 → cur = cur.next（前进）
    3. 返回 dummy.next。

    时间复杂度：O(n) — 遍历一遍。
    空间复杂度：O(1) — 只用 dummy 和 cur 两个指针。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 6 -> 3 -> 4 -> 5 -> 6, val = 6

    dummy -> 1 -> 2 -> 6 -> 3 -> 4 -> 5 -> 6 -> None
             ↑ cur

    cur=dummy, cur.next=1, 1≠6 → cur=1
    cur=1,     cur.next=2, 2≠6 → cur=2
    cur=2,     cur.next=6, 6==6 → 跳过, cur.next=3
    cur=2,     cur.next=3, 3≠6 → cur=3
    cur=3,     cur.next=4, 4≠6 → cur=4
    cur=4,     cur.next=5, 5≠6 → cur=5
    cur=5,     cur.next=6, 6==6 → 跳过, cur.next=None
    cur=5,     cur.next=None → 结束

    结果：1 -> 2 -> 3 -> 4 -> 5 ✓
    """
    # 创建虚拟头结点，统一所有节点的删除操作
    dummy = ListNode(0, head)
    cur = dummy

    while cur.next is not None:
        if cur.next.val == val:
            cur.next = cur.next.next  # 跳过目标节点
        else:
            cur = cur.next  # 前进

    return dummy.next


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 一、虚拟头结点法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：虚拟头结点法能正确删除链表中所有值为 val 的节点。
#
# 证明：
# （1）不变量：cur 始终指向"已确认不需要删除的最后一个节点"。
#     初始时 cur = dummy（虚拟节点，不在链表中），不变量成立。
#
# （2）删除情况：当 cur.next.val == val 时，执行 cur.next = cur.next.next。
#     被删节点脱离链表，cur 不动，因为新的 cur.next 也可能是 val。
#     不变量仍然成立（cur 指向的节点未变）。
#
# （3）前进情况：当 cur.next.val != val 时，cur = cur.next。
#     新的 cur 指向的节点确认不需要删除，不变量仍然成立。
#
# （4）终止时 cur.next == None，所有节点都已被检查。
#     dummy.next 指向清理后的真实头节点（或 None）。
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. 递归调用错误：
#    原代码 removeElements_recursion 中调用了 removeElements（非递归版），
#    应该调用自身 removeElements_recursion。
#
# 2. 删除后 cur 前进：
#    if cur.next.val == val: cur.next = cur.next.next; cur = cur.next
#    这会跳过新 cur.next 的检查。正确做法是删除后 cur 不动。
#
# 3. 处理头节点时遗漏连续删除：
#    原表直接删除法中，头节点可能连续多个都是 val（如 [7,7,7,7]），
#    必须用 while 而不是 if。
#
# 4. 空链表处理：
#    head 为 None 时，虚拟头结点法自然处理（dummy.next = None），
#    不需要特判。原表直接删除法也需检查 head is not None。
# ══════════════════════════════════════════════════════════
