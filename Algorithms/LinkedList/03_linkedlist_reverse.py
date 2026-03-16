class Node:
    def __init__(self, val=0, next=None) -> None:
        self.val = val
        self.next = next


def reverse_list_1(head):
    prev = None
    cur = head
    while cur:
        # 保存下一个节点
        temp = cur.next
        # 反转当前节点的指针
        cur.next = prev
        # 更新prev和cur
        prev = cur
        cur = temp
    return prev


# 递归
def reverse_list_2(head):
    # 空链表，直接返回；到达链表末尾（最后一个节点），直接返回
    if not head or not head.next:
        return head
    new_head = reverse_list_2(head.next)
    # 让下一个节点指回当前节点
    head.next.next = head
    # 断开当前节点向前的连接
    head.next = None
    # 始终返回最后一个节点
    return new_head
