#!/usr/bin/python3
"""search target in matrix, algorithm 3: A solution optimized for a specific condition."""
import time
from globals import *  # import global variables


def matrix_quick_search(matrix, target):
    """A solution optimized for a specific condition."""
    i = 0
    j = len(matrix[i]) - 1
    while i < len(matrix) and j >= 0:
        if matrix[i][j] == target:
            return True
        elif matrix[i][j] > target:
            j -= 1
        else:
            i += 1
    return False


if __name__ == "__main__":
    start_time = time.time_ns()
    m1_result = matrix_quick_search(MATRIX_1, TARGET_1)
    end_time = time.time_ns()
    m1_time = end_time - start_time
    print("\nmatrix 1: \n\tresult =", m1_result, "\n\ttime = ", m1_time, "ns")

    start_time = time.time_ns()
    m2_result = matrix_quick_search(MATRIX_2, TARGET_2)
    end_time = time.time_ns()
    m2_time = end_time - start_time
    print("\nmatrix 2: \n\tresult =", m2_result, "\n\ttime = ", m2_time, "ns")

    start_time = time.time_ns()
    m3_result = matrix_quick_search(MATRIX_3, TARGET_3)
    end_time = time.time_ns()
    m3_time = end_time - start_time
    print("\nmatrix 3: \n\tresult =", m3_result, "\n\ttime = ", m3_time, "ns")

    print("\naverage time =", (m1_time + m2_time + m3_time) / 3, "ns")
