"""使用栈实现队列的下列操作：
push(x) -- 将一个元素放入队列的尾部。
pop() -- 从队列首部移除元素。
peek() -- 返回队列首部的元素。
empty() -- 返回队列是否为空。"""

class QueueWithTwoStacks(): 
    def __init__(self): 
        self.stack_in = [] 
        self.stack_out = [] 

    def empty(self): 
        return not(self.stack_in or self.stack_out)

    def push(self, x): 
        self.stack_in.append(x) 

    def pop(self): 
        if self.empty(): 
            return None 
        if self.stack_out: 
            return self.stack_out.pop()
        else: 
            while self.stack_in: 
                self.stack_out.append(self.stack_in.pop()) 
            return self.stack_out.pop() 
    
    def peek(self): 
        if self.empty(): 
            return None
        first = self.pop() 
        self.stack_out.append(first) 
        return first 
