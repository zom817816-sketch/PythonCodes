"""给你一个 非严格递增排列 的数组 nums ,请你 原地 删除重复出现的元素,使每个元素 只出现一次 ,返回删除后数组的新长度。元素的 相对顺序 应该保持 一致 。然后返回 nums 中唯一元素的个数。
考虑 nums 的唯一元素的数量为 k。去重后,返回唯一元素的数量 k。
nums 的前 k 个元素应包含 排序后 的唯一数字。下标 k - 1 之后的剩余元素可以忽略。
判题标准:
系统会用下面的代码来测试你的题解:
int[] nums = [...]; // 输入数组
int[] expectedNums = [...]; // 长度正确的期望答案
int k = removeDuplicates(nums); // 调用
assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}
如果所有断言都通过,那么您的题解将被 通过。"""

def removeDuplicates(nums: list): 
    """
    双指针法 时间复杂度O(n) 空间复杂度O(1)
    """
    if not nums: 
        return 0 
    
    slow = 0 # 慢指针,指向已去重部分的最后一个元素 

    for fast in range(1, len(nums)): # 快指针：遍历数组
        if nums[slow] != nums[fast]: # 发现新元素
            slow += 1 
            nums[slow] = nums[fast] # 将新元素放到慢指针下一个位置

    return slow + 1

def removeDuplicates_1(nums: list): 
    """
    pop删除 pop(i)时间复杂度O(n),总复杂度为O(n^2)
    """
    i = 1
    while i < len(nums): 
        if nums[i] == nums[i-1]: 
            nums.pop(i) 
        else: 
            i += 1
    return len(nums)

# 测试
if __name__ == "__main__":
    nums1 = [1, 1, 2]
    k1 = removeDuplicates(nums1)
    print(f"k={k1}, nums={nums1[:k1]}")  # k=2, nums=[1, 2]
    
    nums2 = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
    k2 = removeDuplicates(nums2)
    print(f"k={k2}, nums={nums2[:k2]}")  # k=5, nums=[0, 1, 2, 3, 4]