"""给定一个只包括 '(',')','{','}','[',']' 的字符串,判断字符串是否有效。
有效字符串需满足：
    左括号必须用相同类型的右括号闭合。
    左括号必须以正确的顺序闭合。
    注意空字符串可被认为是有效字符串。"""

# 先分析不匹配的三种情况 

def bracketsMatch(s: str): 
    stack = [] 
    brackets = {"(": 1, "[": 2, "{": 3, ")": -1, "]": -2, "}": -3}
    for char in s: 
        bracket_idx = brackets[char]
        if bracket_idx > 0: 
            stack.append(char) 
        else: 
            # 如果栈为空
            if not stack: 
                return False 
            top = stack.pop() 
            # 括号不匹配
            if brackets[top] + brackets[char] != 0: 
                return False 
    return not stack

def bracketsMatch1(s: str): 
    stack = [] 
    for char in s: 
        if char in "([{": 
            stack.append(char)
        else: 
            if not stack: 
                return False
            if char == ")": 
                if stack.pop() != "(": 
                    return False 
            elif char == "]": 
                if stack.pop() != "[": 
                    return False 
            else: 
                if stack.pop() != "{": 
                    return False 
    return not stack


if __name__ == '__main__':
    print(bracketsMatch("()"))
    print(bracketsMatch("()[]{}"))
    print(bracketsMatch1("(]"))
    print(bracketsMatch1("([)]"))
    print(bracketsMatch1("{[]}"))
