# -- coding: utf-8 --
"""
Anagram Detection 检查两个字符串是否是变位词
"""

import re


def anagramSolution1(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    s1, s2 = s1.lower(), s2.lower()
    s1, s2 = re.sub(r"[^a-z]", "", s1), re.sub(r"[^a-z]", "", s2)
    list1, list2 = list(s1), list(s2)
    pos1 = 0
    still_ok = True
    while pos1 < len(list1) and still_ok:
        pos2 = 0
        found = False
        while pos2 < len(list2) and not found:
            if list2[pos2] == list1[pos1]:
                found = True
                list2[pos2] = None  # type: ignore
            else:
                pos2 += 1
        if found:
            pos1 += 1
        else:
            still_ok = False
    return still_ok


def anagramSolution2(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    s1, s2 = s1.lower(), s2.lower()
    s1, s2 = re.sub(r"[^a-z]", "", s1), re.sub(r"[^a-z]", "", s2)
    list1, list2 = list(s1), list(s2)
    list1.sort()
    list2.sort()
    return list1 == list2


def anagramSolution3(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    s1, s2 = s1.lower(), s2.lower()
    s1, s2 = re.sub(r"[^a-z]", "", s1), re.sub(r"[^a-z]", "", s2)
    count1 = [0] * 26
    count2 = [0] * 26
    for i in s1:
        j = ord(i) - ord("a")
        count1[j] += 1
    for i in s2:
        j = ord(i) - ord("a")
        count2[j] += 1
    return count1 == count2


def anagramSolution4(s1: str, s2: str) -> bool:
    if len(s1) != len(s2):
        return False
    s1, s2 = s1.lower(), s2.lower()
    s1, s2 = re.sub(r"[^a-z]", "", s1), re.sub(r"[^a-z]", "", s2)
    count1, count2 = {}, {}
    for i in s1:
        if i in count1:
            count1[i] += 1
        else:
            count1[i] = 1
    for i in s2:
        if i in count2:
            count2[i] += 1
        else:
            count2[i] = 1
    return count1 == count2
