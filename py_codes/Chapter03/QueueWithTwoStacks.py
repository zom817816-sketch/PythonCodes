class QueueWithTwoStacks:
    """
    使用两个栈实现的队列，增加和删除操作的平均时间复杂度为O(1),仅在一种特殊情况下删除操作为O(n)
    """

    def __init__(self):
        self.input_stack = []
        self.output_stack = []

    def enqueue(self, item):
        self.input_stack.append(item)

    def dequeue(self):
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())
        if not self.output_stack:
            raise IndexError("Queue is empty")
        return self.output_stack.pop()

    def isEmpty(self):
        return not self.input_stack and not self.output_stack

    def peek(self):
        if not self.output_stack:
            while self.input_stack:
                self.output_stack.append(self.input_stack.pop())
        if not self.output_stack:
            raise IndexError("Queue is empty")
        return self.output_stack[-1]

    def size(self):
        return len(self.input_stack) + len(self.output_stack)
