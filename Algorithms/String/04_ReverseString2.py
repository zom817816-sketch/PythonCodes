"""
给定一个字符串，逐个翻转字符串中的每个单词。
示例 1：
输入: "the sky is blue"
输出: "blue is sky the"
示例 2：
输入: "  hello world!  "
输出: "world! hello"
解释: 输入字符串可以在前面或者后面包含多余的空格，但是反转后的字符不能包括。
示例 3：
输入: "a good   example"
输出: "example good a"
解释: 如果两个单词间有多余的空格，将反转后单词间的空格减少到只含一个。
""" 

# 方法一:使用split()方法
def reverse_words_1(s: str) -> str:
    """
    时间复杂度:O(n)
    空间复杂度:O(n)
    """
    s_list = s.strip().split()
    s_list.reverse()
    return ' '.join(s_list) 

# 方法二:手动实现split()方法
def reverse_words_2(s: str) -> str:
    """
    时间复杂度:O(n)
    空间复杂度:O(n)
    """ 
    words = [] 
    word = '' 
    s += ' ' 

    for char in s: 
        if char == ' ': 
            if word:
                words.append(word)
                word = '' 
            continue
        word += char 
    words.reverse()
    return ' '.join(words) 

if __name__ == '__main__':
    s = 'the  sky is blue'
    print(reverse_words_1(s))
    print(reverse_words_2(s))