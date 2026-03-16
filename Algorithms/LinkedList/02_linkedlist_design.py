# 带类型注释的链表实现
from __future__ import annotations

from typing import Optional


# 链表节点的实现
class Node:
    def __init__(
        self, data: int = 0, next: Optional[Node] = None, prev: Optional[Node] = None
    ) -> None:
        self.data: int = data
        self.next: Optional[Node] = next
        self.prev: Optional[Node] = prev


"""
在链表类中实现这些功能：

get(index)：获取链表中第 index 个节点的值。如果索引无效，则返回-1。
addAtHead(val)：在链表的第一个元素之前添加一个值为 val 的节点。插入后，新节点将成为链表的第一个节点。
addAtTail(val)：将值为 val 的节点追加到链表的最后一个元素。
addAtIndex(index,val)：在链表中的第 index 个节点之前添加值为 val  的节点。如果 index 等于链表的长度，则该节点将附加到链表的末尾。如果 index 大于链表长度，则不会插入节点。如果index小于0，则在头部插入节点。
deleteAtIndex(index)：如果索引 index 有效，则删除链表中的第 index 个节点。
"""


class MyLinkedList1:
    def __init__(self) -> None:
        self.head: Optional[Node] = None
        self.size: int = 0

    # 获取链表中第 index 个节点的值。如果索引无效，则返回-1
    def get(self, index: int) -> int:
        cur = self.head
        if index < 0 or index >= self.size:
            return -1
        for _ in range(index):
            cur = cur.next
        return cur.data

    # 在链表的第一个元素之前添加一个值为 val 的节点。插入后，新节点将成为链表的第一个节点
    def addAtHead(self, val: int) -> None:
        new_node = Node(val, next=self.head)
        self.head = new_node
        self.size += 1

    # 将值为 val 的节点追加到链表的最后一个元素
    def addAtTail(self, val: int) -> None:
        new_node = Node(val, next=None)
        if not self.head:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node
        self.size += 1

    # 在链表中的第 index 个节点之前添加值为 val  的节点
    def addAtIndex(self, index: int, val: int) -> None:
        if index > self.size:
            return
        new_node = Node(val)
        if index <= 0:
            new_node.next = self.head
            self.head = new_node
        else:
            cur = self.head
            for _ in range(index - 1):
                cur = cur.next
            new_node.next = cur.next
            cur.next = new_node
        self.size += 1

    # 如果索引 index 有效，则删除链表中的第 index 个节点
    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size or self.size == 0:
            return
        if index == 0:
            self.head = self.head.next
        else:
            cur = self.head
            for _ in range(index - 1):
                cur = cur.next
            cur.next = cur.next.next
        self.size -= 1


# 基于虚拟头结点
class MyLinkedList2:
    def __init__(self) -> None:
        self.dummy_head: Node = Node()
        self.size: int = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        cur = self.dummy_head.next
        for _ in range(index):
            cur = cur.next
        return cur.data

    def addAtHead(self, val: int) -> None:
        new_node = Node(val)
        new_node.next = self.dummy_head.next
        self.dummy_head.next = new_node
        self.size += 1

    def addAtTail(self, val: int) -> None:
        new_node = Node(val)
        cur = self.dummy_head
        while cur.next:
            cur = cur.next
        cur.next = new_node
        self.size += 1

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return
        cur = self.dummy_head
        for _ in range(index):
            cur = cur.next
        new_node = Node(val)
        new_node.next = cur.next
        cur.next = new_node
        self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        cur = self.dummy_head
        for _ in range(index):
            cur = cur.next
        cur.next = cur.next.next
        self.size -= 1


# 双向链表
class MyLinkedList3:
    def __init__(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        if index < self.size // 2:
            cur = self.head
            for i in range(index):
                cur = cur.next
            return cur.data
        else:
            cur = self.tail
            for i in range(self.size - index - 1):
                cur = cur.prev
            return cur.data

    def addAtHead(self, val: int) -> None:
        new_node = Node(val, None, self.head)
        if self.head:
            self.head.prev = new_node
        else:
            self.tail = new_node
        self.head = new_node
        self.size += 1

    def addAtTail(self, val: int) -> None:
        new_node = Node(val, self.tail, None)
        if self.tail:
            self.tail.next = new_node
        else:
            self.head = new_node
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
            if index < self.size // 2:
                cur = self.head
                for _ in range(index - 1):
                    cur = cur.next
            else:
                cur = self.tail
                for _ in range(self.size - index - 1):
                    cur = cur.prev
            new_node = Node(val, cur, cur.next)
            cur.next.prev = new_node
            cur.next = new_node
            self.size += 1

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        if index == 0:
            self.head = self.head.next
            if self.head:
                self.head.prev = None
            else:
                self.tail = None
        elif index == self.size - 1:
            self.tail = self.tail.prev
            if self.tail:
                self.tail.next = None
            else:
                self.head = None
        else:
            if index < self.size // 2:
                cur = self.head
                for _ in range(index - 1):
                    cur = cur.next
            else:
                cur = self.tail
                for _ in range(self.size - index - 1):
                    cur = cur.prev
            cur.next = cur.next.next
            if cur.next:
                cur.next.prev = cur
            else:
                self.tail = cur
        self.size -= 1
