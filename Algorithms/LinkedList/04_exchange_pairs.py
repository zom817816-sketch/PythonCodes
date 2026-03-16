"""
给定一个链表，两两交换其中相邻的节点，并返回交换后的链表
"""


class Node:
    def __init__(self, val=0, next=None) -> None:
        self.val = val
        self.next = next


# 迭代
def exchange_pairs(head):
    dummy_head = Node(next=head)
    cur = dummy_head
    while cur.next and cur.next.next:
        temp1 = cur.next.next.next
        temp2 = cur.next
        cur.next = cur.next.next
        cur.next.next = temp2
        temp2.next = temp1
        cur = cur.next.next
    return dummy_head.next


# 递归
def exchange_pairs_1(head):
    # 空链表，直接返回；到达链表末尾（最后一个节点），直接返回
    if not head or not head.next:
        return head
    # 递归调用：处理后面的子链表
    new_head = exchange_pairs_1(head.next.next)
    # 执行交换操作
    # 让下一个节点指回当前节点
    head.next.next = head
    # 断开当前节点向前的连接
    head.next = new_head
    # 返回新的头节点
    return head.next
