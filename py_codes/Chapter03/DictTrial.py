import collections 
import string 
import random 

# 有序字典，可以记住元素插入顺序 
ordered_dict = collections.OrderedDict() 
ordered_dict['a'] = 1 
ordered_dict['b'] = 2 
ordered_dict['c'] = 3 
print(ordered_dict)
print(ordered_dict.keys())
print(ordered_dict.values()) 
print(type(ordered_dict)) 


# defaultdict可以设置默认值 
x = string.ascii_letters + string.digits + string.punctuation 
y = ''.join([random.choice(x) for _ in range(100)]) 
frequences = collections.defaultdict(int) 
for item in y: 
    frequences[item] += 1     
print(frequences)
print(frequences.keys())
print(frequences.values())
print(type(frequences)) 

# Counter类可以更快地实现频次统计 
counter = collections.Counter(y) 
print(counter)
print(counter.keys())
print(counter.values())
print(type(counter)) 

# collections中的双端队列 
deque = collections.deque(range(5)) 
deque.append(1) 
deque.append(2) 
deque.append(3) 
print(deque)
print(deque.popleft())
print(deque) 
deque.rotate(2) 
print(deque)


def demo(n):
    def is_prime(x): 
        if x < 2: 
            return False 
        else: 
            for i in range(2, int(x**0.5) + 1): 
                if x % i == 0: 
                    return False 
        return True 
    if isinstance(n, int) and n > 0 and n % 2 == 0:
        for i in range(2, n//2 + 1): 
            if is_prime(i) and is_prime(n - i):
                print(f'{n}可以表示为{i}和{n - i}的和') 
# 求两个正整数的最大公约数和最小公倍数 
def gcd_lcm(a, b): 
    x = a * b 
    while a % b != 0: 
        a, b = b, a % b 
    return (b, x // b) 

def exchange(x:list, n:int): 
    x1 = [i for i in x if i < n] 
    x2 = [i for i in x if i > n] 
    return x1 + [n] + x2  

def efficient_exchange(x:list, n:int): 
    x1 = [] 
    x2 = [] 
    for item in x: 
        if item < n: 
            x1.append(item) 
        elif item > n: 
            x2.append(item) 
    return x1 + [n] + x2  

def typing_acc(user_inputs, true_inputs): 
    if not isinstance(user_inputs, str) or not isinstance(true_inputs, str): 
        raise TypeError('输入参数必须为字符串') 
    if not len(user_inputs) == len(true_inputs): 
        raise ValueError('输入参数长度必须相等') 
    acc = sum([1 for i, j in zip(user_inputs, true_inputs) if i == j]) / len(user_inputs)
    print(f'输入{user_inputs}的准确率为{acc:.2%}') 

if __name__ == '__main__':
    demo(50) 
    print(gcd_lcm(12, 18))
    print(exchange([1, 2, 3, 4, 5, 6], 3))
    print(efficient_exchange([1, 2, 3, 4, 5, 6], 3))
    print(typing_acc('hello', 'hillo'))