"""
19. 删除链表的倒数第 N 个节点（Remove Nth Node From End of List）

题目描述：
给你一个链表，删除链表的倒数第 n 个节点，并且返回链表的头节点。
要求使用一趟扫描实现。

进阶：你能尝试使用一趟扫描实现吗？

输入描述：
一个链表头节点 head 和一个整数 n。
链表中结点的数目为 sz，1 <= sz <= 30，0 <= Node.val <= 100，1 <= n <= sz。

输出描述：
返回删除倒数第 n 个节点后的链表头节点。

输入示例 1：
head = [1, 2, 3, 4, 5], n = 2
输出示例 1：
[1, 2, 3, 5]
解释：倒数第 2 个节点是值为 4 的节点，删除后链表为 1 -> 2 -> 3 -> 5。

输入示例 2：
head = [1], n = 1
输出示例 2：
[]

输入示例 3：
head = [1, 2], n = 1
输出示例 3：
[1]

════════════════════════════════════════════════════════════════════════
核心概念：快慢指针的间距控制
════════════════════════════════════════════════════════════════════════

要删除倒数第 n 个节点，需要找到它的前驱节点（倒数第 n+1 个）。

快慢指针法：
    让 fast 先走 n+1 步，然后 fast 和 slow 同时前进。
    当 fast 到达 None（链表尾部之后）时，slow 恰好在倒数第 n+1 个位置。
    slow.next 就是要删除的节点。

为什么是 n+1 步？
    链表长度 L，倒数第 n 个 = 正数第 L-n+1 个。
    fast 先走 n+1 步，剩余 L-(n+1) = L-n-1 步。
    slow 同时走 L-n-1 步，slow 位置 = L-n-1（0-indexed）= 第 L-n 个节点。
    slow.next = 第 L-n+1 个 = 倒数第 n 个。✓

    ┌──────┐          ┌──────┐          ┌──────┐          ┌──────┐
    │dummy │──▶ ... ──│ slow │──▶ [删除] ──│      │──▶ ... ──│fast  │──▶ None
    └──────┘          └──────┘          └──────┘          └──────┘
     ↑ fast 先从这里出发，走 n+1 步到 fast 位置

为什么需要虚拟头结点？
    当要删除的是头节点（倒数第 n 个 = 第 1 个），slow = dummy，
    slow.next = head，slow.next.next = head.next。
    虚拟头结点保证删除头节点和删除中间节点操作统一。

解题思路总览：
────────────────────────────────────────────────────────────────────────
解法                          时间复杂度       空间复杂度       说明
────────────────────────────────────────────────────────────────────────
两次扫描                      O(n)            O(1)            ⭐⭐⭐ 直观
快慢指针（一趟扫描）           O(n)            O(1)            ⭐⭐⭐⭐⭐ 推荐
────────────────────────────────────────────────────────────────────────

核心思想（快慢指针）：
────────────────────────────────────────────────────────────────────────
fast 先走 n+1 步，拉开 n+1 的间距。
然后 fast 和 slow 同步前进，fast 到 None 时 slow 在倒数第 n+1 个位置。
slow.next = slow.next.next 完成删除。
"""


class ListNode:
    """链表节点定义"""

    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


# ══════════════════════════════════════════════════════════
# 解法一：两次扫描
# ══════════════════════════════════════════════════════════


def removeNthFromEnd_two_pass(head: ListNode | None, n: int) -> ListNode | None:
    """两次扫描 ⭐⭐⭐

    核心思想：
    ────────────────────────────────────────────────────────
    第一次扫描计算链表长度 L。
    倒数第 n 个 = 正数第 L-n+1 个，其前驱是第 L-n 个。
    第二次扫描走到第 L-n 个节点，删除其后继。

    算法步骤：
    1. 计算链表长度 L。
    2. dummy = ListNode(0, head)，cur = dummy。
    3. cur 走 L-n 步，到达倒数第 n 个节点的前驱。
    4. cur.next = cur.next.next。
    5. 返回 dummy.next。

    时间复杂度：O(n) — 两次遍历，总计 2n 步。
    空间复杂度：O(1)。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 3 -> 4 -> 5, n = 2
    L = 5, L - n = 3

    dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
     ↑ cur  走 3 步：
                dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
                                   ↑ cur

    cur.next = cur.next.next（跳过 4）
    结果：1 -> 2 -> 3 -> 5 ✓
    """
    # 第一次扫描：计算长度
    length = 0
    cur = head
    while cur:
        length += 1
        cur = cur.next

    # 第二次扫描：走到倒数第 n 个的前驱
    dummy = ListNode(0, head)
    cur = dummy
    for _ in range(length - n):
        cur = cur.next

    # 删除倒数第 n 个
    cur.next = cur.next.next

    return dummy.next


# ══════════════════════════════════════════════════════════
# 解法二：快慢指针（一趟扫描）⭐⭐⭐⭐⭐ 推荐
# ══════════════════════════════════════════════════════════


def removeNthFromEnd(head: ListNode | None, n: int) -> ListNode | None:
    """快慢指针（一趟扫描）⭐⭐⭐⭐⭐ 推荐

    核心思想：
    ────────────────────────────────────────────────────────
    fast 先走 n+1 步，与 slow 拉开 n+1 的间距。
    然后 fast 和 slow 同步前进，直到 fast == None。
    此时 slow 恰好在倒数第 n+1 个位置，slow.next 是要删除的节点。

    算法步骤：
    1. dummy = ListNode(0, head), slow = fast = dummy。
    2. fast 先走 n+1 步。
    3. while fast: slow 和 fast 同步前进。
    4. slow.next = slow.next.next（删除倒数第 n 个）。
    5. 返回 dummy.next。

    时间复杂度：O(n) — 一趟扫描，fast 走 n+1 + (L-n-1) = L 步。
    空间复杂度：O(1)。

    图解示例：
    ────────────────────────────────────────────────────────
    head = 1 -> 2 -> 3 -> 4 -> 5, n = 2

    初始: dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
          ↑ slow = fast

    fast 先走 n+1=3 步:
          dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
          ↑ slow              ↑ fast

    同步前进:
      fast=4, slow=1
      fast=5, slow=2
      fast=None, slow=3

    dummy -> 1 -> 2 -> 3 -> 4 -> 5 -> None
                         ↑ slow  ↑ fast(None)

    slow.next = slow.next.next（跳过 4）
    结果：1 -> 2 -> 3 -> 5 ✓

    边界验证 head=[1], n=1:
    fast 先走 2 步到 None，slow=dummy。
    while fast 不执行。
    slow.next = None，返回 dummy.next = None ✓
    """
    dummy = ListNode(0, head)
    slow = dummy
    fast = dummy

    # fast 先走 n+1 步，拉开间距
    for _ in range(n + 1):
        fast = fast.next

    # fast 和 slow 同步前进，直到 fast 到达 None
    while fast:
        slow = slow.next
        fast = fast.next

    # slow.next 就是要删除的节点
    slow.next = slow.next.next

    return dummy.next


# ══════════════════════════════════════════════════════════
# 重要说明：算法的正确性证明和易错点提示
# ══════════════════════════════════════════════════════════
#
# 一、快慢指针法的正确性证明：
# ────────────────────────────────────────────────────────
#
# 定理：fast 走 n+1 步后与 slow 同步前进，fast == None 时
# slow 恰好指向倒数第 n+1 个节点（待删节点的前驱）。
#
# 证明：
# （1）设链表长度为 L（不含 dummy）。
#     fast 从 dummy 出发走 n+1 步后，位于第 n 个真实节点（0-indexed）。
#     剩余步数 = (L+1) - (n+1) = L - n 步（到 None）。
#
# （2）slow 从 dummy 出发，同步走 L - n 步。
#     slow 位于第 L - n - 1 个真实节点（0-indexed）= 倒数第 n+1 个。
#     slow.next = 第 L - n 个 = 倒数第 n 个。✓
#
# （3）边界情况 n = L（删除头节点）：
#     fast 走 L+1 步到 None，同步阶段不执行。
#     slow = dummy，slow.next = head（第一个节点 = 倒数第 L 个）。
#     slow.next = head.next，正确删除头节点。✓
#
#
# 常见错误：
# ────────────────────────────────────────────────────────
# 1. fast 走 n 步而不是 n+1 步：
#    fast 走 n 步后同步，fast == None 时 slow 在倒数第 n 个节点本身。
#    slow.next = slow.next.next 会删错节点（删了倒数第 n-1 个）。
#    必须走 n+1 步，让 slow 停在前驱位置。
#
# 2. 不用虚拟头结点：
#    删除头节点时（n == L），slow 停在 head 位置，
#    无法删除 head 自身（没有前驱）。
#    虚拟头结点保证 slow 至少在 dummy 位置。
#
# 3. 两次扫描法中 length - n 可能为 0：
#    当 n == L 时，length - n = 0，cur = dummy 不走，
#    cur.next = head，删除正确。需要 dummy 来处理这个边界。
#
# 4. n 超出链表长度：
#    题目保证 1 <= n <= sz，但如果 n > sz，fast 走 n+1 步时会空指针。
#    实际题目不需要处理，但面试时可以加判断。
# ══════════════════════════════════════════════════════════
