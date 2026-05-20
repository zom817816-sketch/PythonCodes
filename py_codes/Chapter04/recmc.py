# 找零问题：给定一个目标金额和一组硬币面值，求出最少需要多少枚硬币才能凑出该金额。

import time
from functools import wraps


def timer_decorator(func):
    """
    计时装饰器，用于测量函数运行时间。
    使用一个标志来避免递归调用时的重复计时。

    Args:
        func: 要计时的函数

    Returns:
        wrapper: 包装后的函数
    """
    # 使用一个线程本地或全局标志来避免递归重复计时
    # 这里使用一个简单的字典来存储计时状态
    timing_active = {"active": False}

    @wraps(func)
    def wrapper(*args, **kwargs):
        # 如果已经在计时中（递归调用），直接执行函数
        if timing_active["active"]:
            return func(*args, **kwargs)

        # 开始计时
        timing_active["active"] = True
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
        finally:
            # 确保计时状态被重置
            timing_active["active"] = False
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"函数 {func.__name__} 运行时间: {elapsed_time:.6f} 秒")
        return result

    return wrapper


@timer_decorator
def recMC(coinValueList: list, change: int) -> int:
    """
    使用递归方法解决找零问题。

    Args:
        coinValueList (list): 硬币面值列表。
        change (int): 目标金额。

    Returns:
        int: 最少需要的硬币数量。
    """
    min_coins = change
    if change in coinValueList:
        return 1
    else:
        for i in [c for c in coinValueList if c <= change]:
            num_coins = 1 + recMC(coinValueList, change - i)
            if num_coins < min_coins:
                min_coins = num_coins
    return min_coins


@timer_decorator
def recDC(coinValueList: list, change: int, knownResults: list) -> int:
    """
    使用递归和记忆化方法解决找零问题。

    Args:
        coinValueList (list): 硬币面值列表。
        change (int): 目标金额。
        knownResults (list): 已知结果列表。

    Returns:
        int: 最少需要的硬币数量。
    """
    min_coins = change
    if change in coinValueList:
        knownResults[change] = 1
        return 1
    elif knownResults[change] > 0:
        return knownResults[change]
    else:
        for i in [c for c in coinValueList if c <= change]:
            num_coins = 1 + recDC(coinValueList, change - i, knownResults)
            if num_coins < min_coins:
                min_coins = num_coins
                knownResults[change] = min_coins
    return min_coins


@timer_decorator
def recDCOptmized(coinValueList: list, change: int, knownResults: list) -> int:
    """
    使用递归和记忆化方法解决找零问题。
    子问题无解直接跳过，能够处理找零无解的情况

    Args:
        coinValueList (list): 硬币面值列表。
        change (int): 目标金额。
        knownResults (list): 已知结果列表。

    Returns:
        int: 最少需要的硬币数量。
    """
    # 1. 基准条件：金额为0，不需要硬币
    if change == 0:
        return 0
    # 2. 金额负数，直接判定无解
    if change < 0:
        return -1
    # 3. 本身就是硬币面值
    if change in coinValueList:
        knownResults[change] = 1
        return 1
    # 4. 已经算出结果，直接返回
    if change in knownResults:
        return knownResults[change]

    min_coins = float("inf")

    for coin in coinValueList:
        if coin > change:
            continue
        # 递归求子问题
        sub_min_coins = recDCOptmized(coinValueList, change - coin, knownResults)
        # 子问题无解，跳过
        if sub_min_coins == -1:
            continue
        min_coins = min(min_coins, 1 + sub_min_coins)

    # 记录结果：有解存数量，无解存-1
    if min_coins != float("inf"):
        knownResults[change] = min_coins
        return min_coins
    else:
        knownResults[change] = -1
        return -1


# 动态规划
@timer_decorator
def dpMakeChange(coinValueList: list, change: int, minCoins: list) -> int:
    """
    使用动态规划方法解决找零问题。

    Args:
        coinValueList (list): 硬币面值列表。
        change (int): 目标金额。
        minCoins (list): 已知结果列表。

    Returns:
        int: 最少需要的硬币数量。
    """
    for cents in range(change + 1):
        coinCount = cents
        for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents - j] + 1 < coinCount:
                coinCount = minCoins[cents - j] + 1
        minCoins[cents] = coinCount
    return minCoins[change]


# 动态规划并且可以处理无法找零的情况
@timer_decorator
def dpMakeChangeOptimized(coinValueList: list, change: int) -> int:
    # min_coins[i] = 凑出 i 元需要的最小硬币数
    minCoins = [change + 1] * (change + 1)
    minCoins[0] = 0  # 零元时找零零个硬币

    for i in range(1, change + 1):
        for c in coinValueList:
            if c <= i:
                minCoins[i] = min(minCoins[i], minCoins[i - c] + 1)

    return minCoins[change] if minCoins[change] != change + 1 else -1


def dpMakeChange_(coinValueList, change, minCoins, coinsUsed):
    for cents in range(change + 1):
        coinCount = cents
        new_coin = 1
        for j in [c for c in coinValueList if c <= cents]:
            if minCoins[cents - j] + 1 < coinCount:
                coinCount = minCoins[cents - j] + 1
                new_coin = j
        minCoins[cents] = coinCount
        coinsUsed[cents] = new_coin
    return minCoins[change]


def printCoins(coinsUsed, change):
    coin = change
    while coin > 0:
        thisCoin = coinsUsed[coin]
        print(thisCoin)
        coin -= thisCoin


if __name__ == "__main__":
    coinValueList = [1, 5, 10, 25]

    # 测试不同金额以展示性能差异
    test_amounts = [23, 40, 50]

    for change in test_amounts:
        print(f"\n{'=' * 50}")
        print(f"=== 找零问题算法比较 (金额: {change}) ===")
        print(f"硬币面值: {coinValueList}")
        print(f"目标金额: {change}")
        print()

        # 为每个测试重新初始化数据结构
        knownResults = [0] * (change + 1)
        minCoins = [0] * (change + 1)

        print("1. 递归方法:")
        try:
            result1 = recMC(coinValueList, change)
            print(f"最少硬币数: {result1}")
        except RecursionError:
            print("递归深度过大，无法计算！")
        print()

        print("2. 递归+记忆化方法:")
        result2 = recDC(coinValueList, change, knownResults)
        print(f"最少硬币数: {result2}")
        print()

        print("3. 动态规划方法:")
        result3 = dpMakeChange(coinValueList, change, minCoins)
        print(f"最少硬币数: {result3}")
