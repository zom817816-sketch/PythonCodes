from typing import Any, Optional


class Node:
    def __init__(self, item: Any) -> None:
        self.item: Any = item
        self.next: Optional["Node"] = None

    def set_data(self, new_data: Any) -> None:
        self.item = new_data

    def get_data(self) -> Any:
        return self.item

    def set_next(self, new_next: Optional["Node"]) -> None:
        self.next = new_next

    def get_next(self) -> Optional["Node"]:
        return self.next


class UnorderedList:
    def __init__(self) -> None:
        self.head: Optional[Node] = None

    def is_empty(self) -> bool:
        return self.head is None

    def add(self, item: Any) -> None:
        temp = Node(item)
        temp.set_next(self.head)
        self.head = temp

    def append(self, item: Any) -> None:
        temp = Node(item)
        if self.head is None:
            self.head = temp
        else:
            current = self.head
            while current.get_next() is not None:  # type: ignore
                current = current.get_next()  # type: ignore
            current.set_next(temp)  # type: ignore

    def size(self) -> int:
        current = self.head
        count = 0
        while current is not None:
            count += 1
            # 安全地获取下一个节点
            next_node = current.get_next()
            current = next_node
        return count

    def search(self, item: Any) -> bool:
        current = self.head
        found = False
        while current is not None and not found:
            if current.get_data() == item:
                found = True
            else:
                # 安全地获取下一个节点
                next_node = current.get_next()
                current = next_node
        return found

    def remove(self, item: Any) -> None:
        current: Optional[Node] = self.head
        previous: Optional[Node] = None
        found = False
        while not found:
            if current is None:
                raise ValueError(f"{item} not found in the list")
            elif current.get_data() == item:
                found = True
            else:
                previous = current
                # 安全地获取下一个节点
                next_node = current.get_next()
                current = next_node
        if previous is None:  # If the item to be removed is the head
            self.head = current.get_next()  # type: ignore
        else:
            previous.set_next(current.get_next())  # type: ignore

    def find(self, item: Any) -> int:
        current = self.head
        index = 0
        while current is not None and current.get_data() != item:
            index += 1
            # 安全地获取下一个节点
            next_node = current.get_next()
            current = next_node
        return index if current is not None else -1

    def insert(self, item: Any, position: int) -> None:
        if position < 0 or position > self.size():
            raise IndexError("Position out of range")
        new_node = Node(item)
        if position == 0:
            new_node.set_next(self.head)
            self.head = new_node
        else:
            current = self.head
            for _ in range(position - 1):
                # 安全地获取下一个节点
                next_node = current.get_next()  # type: ignore
                current = next_node
            new_node.set_next(current.get_next())  # type: ignore
            current.set_next(new_node)  # type: ignore


# 使用自定义链表实现栈
class StackWithLinkedList:
    def __init__(self):
        self.stack = UnorderedList()

    def push(self, item):
        self.stack.add(item)

    def pop(self):
        if self.stack.is_empty():
            raise IndexError("Stack is empty")
        return self.stack.remove(self.stack.size() - 1)

    def isEmpty(self):
        return self.stack.is_empty()

    def peek(self):
        if self.stack.is_empty():
            raise IndexError("Stack is empty")
        return self.stack.get_data(self.stack.size() - 1)  # type: ignore

    def size(self):
        return self.stack.size()


# 使用自定义链表实现队列
class QueueWithLinkedList:
    def __init__(self):
        self.queue = UnorderedList()

    def enqueue(self, item):
        self.queue.add(item)

    def dequeue(self):
        if self.queue.is_empty():
            raise IndexError("Queue is empty")
        return self.queue.remove(0)

    def isEmpty(self):
        return self.queue.is_empty()

    def peek(self):
        if self.queue.is_empty():
            raise IndexError("Queue is empty")
        return self.queue.get_data(0)  # type: ignore

    def size(self):
        return self.queue.size()


# 使用自定义链表实现双端队列
class DequeWithLinkedList:
    def __init__(self):
        self.deque = UnorderedList()

    def addFront(self, item):
        self.deque.add(item)

    def addRear(self, item):
        self.deque.append(item)

    def removeFront(self):
        if self.deque.is_empty():
            raise IndexError("Deque is empty")
        return self.deque.remove(0)

    def removeRear(self):
        if self.deque.is_empty():
            raise IndexError("Deque is empty")
        return self.deque.remove(self.deque.size() - 1)

    def isEmpty(self):
        return self.deque.is_empty()

    def peekFront(self):
        if self.deque.is_empty():
            raise IndexError("Deque is empty")
        return self.deque.get_data(0)  # type: ignore

    def peekRear(self):
        if self.deque.is_empty():
            raise IndexError("Deque is empty")
        return self.deque.get_data(self.deque.size() - 1)  # type: ignore

    def size(self):
        return self.deque.size()
