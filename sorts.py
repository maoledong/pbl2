"""
sorts.py
--------
Implementation of two quadratic sorting algorithms.

Both algoritms are completly independant from the POLICY.
The policy is passed as a parameter so you can swap it without rewriting the sort.

Available functions :
    - selection_sort(planes, policy) : selection sort
    - insertion_sort(planes, policy) : insertion sort
    - compare_algorithms(planes, policy) : runs both and compares results
"""

import copy
import time


# --------------------------------------------------------------
# SELECTION SORT -- O(n2)
# At each step, find the most priority plane in the remaining list
# and put it in the correct position
# --------------------------------------------------------------

def selection_sort(planes: list, policy) -> tuple:
    """
    Selection sort applied to a list of planes using the given policy.

    At each iteration we search for the most prioritary plane in the unsorted part
    and swap it to the front. This always does exactly n*(n-1)/2 comparisions.

    Parameters
    ----------
    planes : list of dict -- aircraft to sort (original is not modified)
    policy : function(a1, a2) -> bool -- priority comparator

    Returns
    -------
    (sorted_list, nb_comparisons) : tuple
    """
    lst = copy.deepcopy(planes)
    n = len(lst)
    nb_comparisons = 0

    for i in range(n - 1):
        # find the most prioritary plane in lst[i:]
        best = i
        for j in range(i + 1, n):
            nb_comparisons += 1
            if policy(lst[j], lst[best]):
                best = j
        # swap it to position i
        lst[i], lst[best] = lst[best], lst[i]

    return lst, nb_comparisons


# --------------------------------------------------------------
# INSERTION SORT -- O(n2)
# Insert each plane into its correct position in the already sorted part
# This is stable : equal planes keep their orignal relative order
# --------------------------------------------------------------

def insertion_sort(planes: list, policy) -> tuple:
    """
    Insertion sort applied to a list of planes using the given policy.

    We iterate through the list and for each plane we move it left
    until it is in the right position. Prefered over selection sort
    in the simulation because it is stable and faster on partialy sorted data.

    Parameters
    ----------
    planes : list of dict -- aircraft to sort (original is not modified)
    policy : function(a1, a2) -> bool -- priority comparator

    Returns
    -------
    (sorted_list, nb_comparisons) : tuple
    """
    lst = copy.deepcopy(planes)
    n = len(lst)
    nb_comparisons = 0

    for i in range(1, n):
        current = lst[i]
        j = i - 1
        # move current plane left as long as it is more prioritary than its neighbor
        while j >= 0 and policy(current, lst[j]):
            nb_comparisons += 1
            lst[j + 1] = lst[j]
            j -= 1
        if j >= 0:
            nb_comparisons += 1  # the comparison that stoped the loop
        lst[j + 1] = current

    return lst, nb_comparisons


# --------------------------------------------------------------
# ALGORITHM COMPARISON
# Runs both sorts on the same data and measures comparisons and runtime
# --------------------------------------------------------------

def compare_algorithms(planes: list, policy) -> dict:
    """
    Runs both sorting algorithms on the same dataset and compares their performance.

    Parameters
    ----------
    planes : list of dict
    policy : function(a1, a2) -> bool

    Returns
    -------
    dict with keys "selection" and "insertion", each containing :
        "list"        : sorted list of planes
        "comparisons" : number of comparisons made
        "time_s"      : runtime in seconds
    """
    start = time.perf_counter()
    list_sel, comp_sel = selection_sort(planes, policy)
    time_sel = time.perf_counter() - start

    start = time.perf_counter()
    list_ins, comp_ins = insertion_sort(planes, policy)
    time_ins = time.perf_counter() - start

    return {
        "selection": {"list": list_sel, "comparisons": comp_sel, "time_s": round(time_sel, 6)},
        "insertion": {"list": list_ins, "comparisons": comp_ins, "time_s": round(time_ins, 6)},
    }
