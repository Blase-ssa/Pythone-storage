#!/usr/bin/python3
"""search target in matrix, algorithm 2: from sides to middle"""
import time
from globals import *  # import global variables


def matrix_to_middle(matrix: list, target: int) -> bool:
    """Search in every line from sides to middle"""
    for i in range(0, len(matrix)):
        l = 0
        r = len(matrix[i]) - 1
        while l <= r:
            mid = l + r - 1 // 2
            if matrix[i][mid] == target:
                return True
            if matrix[i][mid] > target:
                r = mid - 1
            else:
                l = mid + 1
    return False


if __name__ == "__main__":
    start_time = time.time_ns()
    m1_result = matrix_to_middle(MATRIX_1, TARGET_1)
    end_time = time.time_ns()
    m1_time = end_time - start_time

    start_time = time.time_ns()
    m2_result = matrix_to_middle(MATRIX_2, TARGET_2)
    end_time = time.time_ns()
    m2_time = end_time - start_time

    start_time = time.time_ns()
    m3_result = matrix_to_middle(MATRIX_3, TARGET_3)
    end_time = time.time_ns()
    m3_time = end_time - start_time

    print("matrix 1: \n\tresult =", m1_result, "\n\ttime = ", m1_time, "ns")
    print("matrix 2: \n\tresult =", m2_result, "\n\ttime = ", m2_time, "ns")
    print("matrix 3: \n\tresult =", m3_result, "\n\ttime = ", m3_time, "ns")
    print("\naverage time =", (m1_time + m2_time + m3_time) / 3, "ns")
