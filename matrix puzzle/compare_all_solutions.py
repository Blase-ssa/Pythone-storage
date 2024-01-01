#!/usr/bin/python3
"""search target in matrix, algorithm 3: A solution optimized for a specific condition."""
import time
from globals import *  # import global variables
from full_direct_search import matrix_full_search
from search_to_middle import matrix_to_middle
from optimized_search import matrix_quick_search


def print_winner(header, s1, s2, s3):
    """Print result table and the winner algorithm"""
    print(f"{header}: \nAlgorithm\tResult\ttime")
    print(f"full search\t{s1.result}\t{s1.time} ns")
    print(f"to middle\t{s2.result}\t{s2.time} ns")
    print(f"optimized\t{s3.result}\t{s3.time} ns")
    if s3.time < s2.time and s3.time < s1.time:
        print("Winner: algorithm #3 optimized")
    elif s2.time < s3.time and s2.time < s1.time:
        print("Winner: algorithm #2 fro side to middle")
    else:
        print("Winner: algorithm #1 full search")


class f_res:
    """Result for test_func"""

    def __init__(self, f_time, result):
        self.time = f_time
        self.result = result


def test_func(func, matrix, target) -> f_res:
    """execute 'func' and return class r"""
    r_r = f_res
    r = r_r(0, 0)
    start_time = time.time_ns()
    r.result = func(matrix, target)
    end_time = time.time_ns()
    r.time = end_time - start_time
    return r


if __name__ == "__main__":
    R1 = test_func(matrix_full_search, MATRIX_1, TARGET_1)
    R2 = test_func(matrix_to_middle, MATRIX_1, TARGET_1)
    R3 = test_func(matrix_quick_search, MATRIX_1, TARGET_1)
    print_winner("matrix 1", R1, R2, R3)

    R1 = test_func(matrix_full_search, MATRIX_2, TARGET_2)
    R2 = test_func(matrix_to_middle, MATRIX_2, TARGET_2)
    R3 = test_func(matrix_quick_search, MATRIX_2, TARGET_2)
    print_winner("matrix 2", R1, R2, R3)

    R1 = test_func(matrix_full_search, MATRIX_3, TARGET_3)
    R2 = test_func(matrix_to_middle, MATRIX_3, TARGET_3)
    R3 = test_func(matrix_quick_search, MATRIX_3, TARGET_3)
    print_winner("matrix 2", R1, R2, R3)
