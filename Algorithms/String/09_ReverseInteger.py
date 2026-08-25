"""
给你一个 32 位的有符号整数 x ，返回将 x 中的数字部分反转后的结果。
如果反转后整数超过 32 位的有符号整数的范围 [−231,  231 − 1] ，就返回 0。
假设环境不允许存储 64 位整数（有符号或无符号）。

示例 1：
输入：x = 123
输出：321

示例 2：
输入：x = -123
输出：-321

示例 3：
输入：x = 120
输出：21

示例 4：
输入：x = 0
输出：0
"""

def reverse_integer(x: int) -> int:
    # 记录符号
    sign = -1 if x < 0 else 1
    # 取绝对值转字符串，反转，再转回整数（自动去掉前导零）
    reversed_str = str(abs(x))[::-1]
    result = int(reversed_str) * sign  # int() 会自动忽略前导零
    
    # 检查 32 位溢出
    if result < -2**31 or result > 2**31 - 1:
        return 0
    return result
        