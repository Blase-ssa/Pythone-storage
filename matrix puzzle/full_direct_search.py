#!/usr/bin/python3
"""search target in matrix, algorithm 1: full direct search"""
import time
from globals import *  # import global variables


def matrix_full_search(matrix: list, target: int) -> bool:
    """full direct search"""
    for line in matrix:
        for i in line:
            if i == target:
                return True
    return False


if __name__ == "__main__":
    start_time = time.time_ns()
    m1_result = matrix_full_search(MATRIX_1, TARGET_1)
    end_time = time.time_ns()
    m1_time = end_time - start_time

    start_time = time.time_ns()
    m2_result = matrix_full_search(MATRIX_2, TARGET_2)
    end_time = time.time_ns()
    m2_time = end_time - start_time

    start_time = time.time_ns()
    m3_result = matrix_full_search(MATRIX_3, TARGET_3)
    end_time = time.time_ns()
    m3_time = end_time - start_time

    print("matrix 1: \n\tresult =", m1_result, "\n\ttime = ", m1_time, "ns")
    print("matrix 2: \n\tresult =", m2_result, "\n\ttime = ", m2_time, "ns")
    print("matrix 3: \n\tresult =", m3_result, "\n\ttime = ", m3_time, "ns")
    print("\naverage time =", (m1_time + m2_time + m3_time) / 3, "ns")
