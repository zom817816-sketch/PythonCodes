# 链表节点的实现
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next


# 删除链表元素
# 递归
def remove_elements_recursion(head: Node, val: int) -> Node:
    # 基础情况，链表不需要删除
    if head is None:
        return None
    # 头节点为需要删除的节点，答案就是后续的节点递归
    elif head.data == val:
        return remove_elements(head.next, val)
    # 头节点不为需要删除的节点，答案就是头节点加上后续的节点递归
    else:
        head.next = remove_elements(head.next, val)
        return head


# 原表删除链表元素
def remove_elements(head: Node, val: int) -> Node:
    while head is not None and head.data == val:
        head = head.next
    cur = head
    while cur and cur.next:
        if cur.next.data == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head


# 通过虚拟头结点统一删除元素
def remove_elements_iteration(head: Node, val: int) -> Node:
    dummy = Node(0)
    dummy.next = head
    cur = dummy
    while cur.next:
        if cur.next.data == val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return dummy.next
