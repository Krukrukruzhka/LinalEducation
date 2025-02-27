import numpy as np
import random

from src.datamodels.labs import LinalLab7Request, LinalLab7Response


def generate_variant() -> LinalLab7Request:
    a_n, a_m = 2, 2
    b_n, b_m = 2, 2

    A = [[] for _ in range(a_m)]
    for row in A:
        for _ in range(a_n):
            k = 0
            while k == 0:
                k = random.randint(-9, 9)
            row.append(k)

    B = [[] for _ in range(b_m)]
    for row in B:
        for _ in range(b_n):
            k = 0
            while k == 0:
                k = random.randint(-9, 9)
            row.append(k)

    return LinalLab7Request(matrix_a = A, matrix_b = B)


def check_lab(condition: LinalLab7Request, user_answer: LinalLab7Response) -> bool:
    A, B = np.matrix(condition.matrix_a), np.matrix(condition.matrix_b)

    correct_answer = (A[0, 0] * A[1, 1] - A[1, 0] * A[0, 1]) * (B[0, 0] * B[1, 1] - B[1, 0] * B[0, 1])

    return int(correct_answer) == user_answer.answer_matrix_det
