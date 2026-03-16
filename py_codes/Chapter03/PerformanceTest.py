import random
import string
import time

import matplotlib.pyplot as plt


# 测试字典的赋值与索引操作为常数阶
def generate_random_string(length=10):
    """
    随机生成一个长度为length的字符串
    """
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def measure_dict_operations(n, trials=500):
    """
    测量大小为n的字典的取值和赋值操作平均耗时
    """
    # 初始化字典
    dictionary = {generate_random_string(): random.randrange(1000) for _ in range(n)}
    existing_keys = list(dictionary.keys())

    # 测量取值操作
    get_total_time = 0
    for _ in range(trials):
        key = random.choice(existing_keys)
        start_time = time.perf_counter()
        _ = dictionary[key]
        end_time = time.perf_counter()
        get_total_time = get_total_time + (end_time - start_time)
    get_avg_time = get_total_time / trials

    # 测量赋值操作
    set_total_time = 0
    for _ in range(trials):
        key = generate_random_string()
        new_value = random.randrange(1000)
        start_time = time.perf_counter()
        dictionary[key] = new_value
        end_time = time.perf_counter()
        set_total_time = set_total_time + (end_time - start_time)
    set_avg_time = set_total_time / trials

    return get_avg_time, set_avg_time


# 测试不同大小的字典
sizes = [10 * i for i in range(1, 7)]
set_avg_times = []
get_avg_times = []
for size in sizes:
    get_avg_time, set_avg_time = measure_dict_operations(size)
    set_avg_times.append(set_avg_time)
    get_avg_times.append(get_avg_time)
    print(
        f"字典大小{size:>7} 平均取值耗时{get_avg_time:.8f} 平均赋值耗时{set_avg_time:.8f}"
    )

# 绘制结果
plt.figure(figsize=(10, 6))
plt.plot(sizes, get_avg_times, marker="o", linestyle="-", color="r", label="取值操作")
plt.plot(sizes, set_avg_times, marker="s", linestyle="-", color="b", label="赋值操作")
plt.xscale("log")
plt.xlabel("字典大小 (log 刻度)")
plt.ylabel("平均操作耗时 (秒)")
plt.title("字典取值与赋值操作耗时与字典大小的关系")
plt.legend()
plt.grid(True)
plt.show()
