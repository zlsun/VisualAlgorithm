
from time import sleep
from copy import deepcopy
from random import randrange

from structures import List

N = 100
lst = [randrange(N) for _ in range(N)]
L = List(lst)
n = len(L)

L.bind('i', 0x00ff00)
L.bind('j', 0x0000ff)
L.bind('p', 0xff0000)
L.bind('r', 0xffff00)
L.bind('max', 0xff0000)


def bubble_sort(L):
    for i in range(n - 1, 0, -1):
        for j in range(0, i):
            if L[j] > L[j + 1]:
                L[j + 1], L[j] = L[j], L[j + 1]

bubble_sort(deepcopy(L))

sleep(1)


def selection_sort(L):
    for i in range(n - 1, 0, -1):
        max = i
        for j in range(0, i):
            if L[j] > L[max]:
                max = j
        L[max], L[i] = L[i], L[max]

selection_sort(deepcopy(L))

sleep(1)


def insertion_sort(L):
    for i in range(1, n):
        x = L[i]
        for j in range(i - 1, -1, -1):
            if L[j] < x:
                break
            L[j + 1] = L[j]
            L[j] = x

insertion_sort(deepcopy(L))

sleep(1)


def merge_sort(L, p=0, r=n - 1):
    if p < r:
        mid = (p + r) / 2
        merge_sort(L, p, mid)
        merge_sort(L, mid + 1, r)
        L1 = L[p : mid + 1]
        L2 = L[mid + 1 : r + 1]
        i = j = 0
        while i < len(L1) and j < len(L2):
            if L1[i] < L2[j]:
                L[p] = L1[i]
                i += 1
            else:
                L[p] = L2[j]
                j += 1
            p += 1
        while i < len(L1):
            L[p] = L1[i]
            i += 1
            p += 1
        while j < len(L2):
            L[p] = L2[j]
            j += 1
            p += 1

merge_sort(deepcopy(L))

sleep(1)


def quick_sort(L, p=0, r=n - 1):
    if p < r:
        x = L[r]
        i = p
        for j in range(p, r + 1):
            if L[j] < x:
                L[i], L[j] = L[j], L[i]
                i += 1
        L[i], L[r] = L[r], L[i]
        quick_sort(L, p, i - 1)
        quick_sort(L, i + 1, r)

quick_sort(deepcopy(L))
