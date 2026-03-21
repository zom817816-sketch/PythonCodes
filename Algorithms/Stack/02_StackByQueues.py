"""使用队列实现栈的下列操作：
    push(x) -- 元素 x 入栈
    pop() -- 移除栈顶元素
    top() -- 获取栈顶元素
    empty() -- 返回栈是否为空"""

from collections import deque

class StackWithTwoQueues: 
    def __init__(self): 
        """
        使用双向队列,只执行popleft和append(),因为deque可以用索引访问,可以实现peek相似的功能
        """
        self.queue_in = deque() 
        self.queue_out = deque() 
    
    def push(self, x): 
        self.queue_in.append(x) 

    def empty(self): 
        return not self.queue_in # 只有in存储数据

    def pop(self): 
        """
        首先确认不为空
        现将queue_in的所有元素(除了最后一个)依次放入queue_out
        交换in和out,此时out里只有一个元素 
        将out里的元素pop出来,即是原队列的最后一个
        """
        if self.empty(): 
            return None 
        for _ in range(len(self.queue_in)-1): 
            self.queue_out.append(self.queue_in.popleft())
        self.queue_in, self.queue_out = self.queue_out, self.queue_in # 交换in和out 
        return self.queue_out.popleft() 

    def top(self): 
        """ 
        确认不为空
        先把queue_in中的所有元素(除了最后一个),依次放入queue_out
        交换in和out,此时out中只有一个元素
        再把out中的元素pop出来,即是原队列的最后一个,暂存
        把暂存元素放到in的末尾
        """
        if self.empty(): 
            return None 
        for _ in range(len(self.queue_in)-1): 
            self.queue_out.append(self.queue_in.popleft()) 
        self.queue_in, self.queue_out = self.queue_out, self.queue_in 
        temp = self.queue_out.popleft() 
        self.queue_in.append(temp)
        return temp 

class StackWithOneQueue: 
    def __init__(self): 
        self.queque = deque() 
    
    def push(self, x): 
        self.queque.append(x) 

    def pop(self): 
        if self.empty(): 
            return None
        for _ in range(len(self.queque)-1): 
            self.queque.append(self.queque.popleft()) 
        return self.queque.popleft() 

    def empty(self): 
        return not self.queque 
    
    def top(self): 
        if self.empty(): 
            return None
        for _ in range(len(self.queque)-1): 
            self.queque.append(self.queque.popleft()) 
        temp = self.queque.popleft() 
        self.queque.append(temp) 
        return temp 


if __name__ == '__main__':
    stack_1 = StackWithOneQueue()
    stack_1.push(1)
    stack_1.push(2)
    print(stack_1.top())
    stack_1.pop()
    print(stack_1.empty())
    stack_1.push(3)
    print(stack_1.top())

    stack_2 = StackWithTwoQueues()
    stack_2.push(1)
    stack_2.push(2)
    print(stack_2.top())
    stack_2.pop()
    print(stack_2.empty())
    stack_2.push(3)
    print(stack_2.top())
