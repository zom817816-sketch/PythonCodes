# 递归 
## 何谓递归 
递归是解决问题的一种方法，它将问题不断地分成更小的子问题，直到子问题可以用普通的方法解决。通常情况下，递归会使用一个不停调用自己的函数。
循环求和函数:
```Python
def list_sum(lst): 
    if len(lst) == 1: # 基本情况
        return lst[0] 
    return lst[0] + list_sum(lst[1:]) # 缩短列表向基本情况靠近 递归调用
```
这个函数使用初始值为0的累加变量theSum，通过把列表中的数加到该变量中来计算所有数的和。
### 递归三原则 
- 递归算法必须有基本情况 
- 递归算法必须改变其状态向基本情况靠近 
- 递归算法必须递归的调用自己
### 将整数转换成任意进制的字符串
```Python
# 递归实现
def toString(n, base): 
    convertString = '01234567890ABCDEF' 
    if n < base: 
        return convertString[n] 
    return toString(n // base, base) + convertString[n % base]
# 循环实现 
def convert(n, base): 
    convertString = '01234567890ABCDEF'
    result = ''
    while n > 0: 
        remainder = n % base 
        result = convertString[remainder] + result
    return result 
```
## 栈帧：实现递归 
递归调用时，每个函数调用都会创建一个栈帧，用于保存函数的局部变量和返回地址。当递归调用结束时，栈帧会被弹出，函数的返回值会被保存在栈帧中，以便在调用者函数中使用。栈帧限定了函数所用变量的作用域。尽管反复调用相同的函数，但是每一次调用都会为函数的局部变量**创建新的作用域**。

假设不拼接递归调用toStr 的结果和convertString 的查找结果，而是在进行递归调用之前把字符串压入栈中。 
```Python 
stack = [] 
def toString(n, base): 
    convertString = '01234567890ABCDEF'
    if n < base: 
        stack.append(convertString[n])
    else: 
        stack.append(convertString[n % base])
        toString(n // base, base) 
```
## 复杂的递归问题 
### 汉诺塔
以下概述如何借助一根中间柱子，将高度为height的一叠盘子从起点柱子移到终点柱子：
- 借助终点柱子，将高度为height − 1的一叠盘子移到中间柱子； 
- 将最后一个盘子移到终点柱子； 
- 借助起点柱子，将高度为height − 1的一叠盘子从中间柱子移到终点柱子。
```Python 
def moveTower(height, fromPole, toPole, withPole): 
    if height >= 1: 
        moveTower(height - 1, fromPole, withPole, toPole) # 先将n-1个盘子从fromPole移动到withPole
        moveDisk(fromPole, toPole) # 从fromPole移动一个盘子到toPole
        moveTower(height - 1, withPole, toPole, fromPole) # 将n-1个盘子从withPole移动到toPole
        
def moveDisk(fp, tp): 
    print('moving disk from', fp, 'to', tp)
```
## 探索迷宫 
为简单起见，假设迷宫被分成许多格，每一格要么是空的，要么被墙堵上。小乌龟只能沿着空的格子爬行，如果遇到墙，就必须转变方向。它需要如下的系统化过程来找到出路。
- 从起始位置开始，首先向北移动一格，然后在新的位置再递归地重复本过程。 
- 如果第一步往北行不通，就尝试向南移动一格，然后递归地重复本过程。 
- 如果向南也行不通，就尝试向西移动一格，然后递归地重复本过程。 
- 如果向北、向南和向西都不行，就尝试向东移动一格，然后递归地重复本过程。 
- 如果4个方向都不行，就意味着没有出路。

假设递归过程的第一步是向北移动一格。根据上述过程，下一步也是向北移动一格。但是，如果北面有墙，必须根据递归过程的第二步向南移动一格。不幸的是，向南移动一格之后回到了起点。如果继续执行该递归过程，就会又向北移动一格，然后又退回来，从而陷入无限循环中。所以，必须通过一个策略来记住到过的地方。本例假设小乌龟一边爬，一边丢面包屑。如果往某个方向走一格之后发现有面包屑，就知道应该立刻退回去，然后尝试递归过程的下一步。查看这个算法的代码时会发现，退回去就是从递归函数调用中返回。
这个算法需要考虑以下4种基本情况。

- 小乌龟遇到了墙。由于格子被墙堵上，因此无法再继续探索。
- 小乌龟遇到了已经走过的格子。在这种情况下，我们不希望它继续探索，不然会陷入循环。
- 小乌龟找到了出口。
- 四个方向都行不通。
