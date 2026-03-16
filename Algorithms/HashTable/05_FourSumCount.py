"""
给定四个包含整数的数组列表 A , B , C , D ,计算有多少个元组 (i, j, k, l) ，使得 A[i] + B[j] + C[k] + D[l] = 0。

为了使问题简单化，所有的 A, B, C, D 具有相同的长度 N，且 0 ≤ N ≤ 500 。所有整数的范围在 -2^28 到 2^28 - 1 之间，最终结果不会超过 2^31 - 1 。
""" 

def four_sum_count(A, B, C, D):
    """
    给定四个包含整数的数组列表 A , B , C , D ,计算有多少个元组 (i, j, k, l) ，使得 A[i] + B[j] + C[k] + D[l] = 0。
    
    时间复杂度: O(n^2) 空间复杂度: O(n^2)
    """
    # 使用字典存储A和B中的元素及其和
    seen = {} 
    for a in A: 
        for b in B: 
            seen[a+b] = seen.get(a+b, 0) + 1 
    # 如果 -(a+b) 存在于C和D, 存入结果
    count = 0
    for c in C: 
        for d in D: 
            if -c-d in seen: 
                count += seen[-c-d] 
    return count