import numpy as np
import random

from src.datamodels.labs import LinalLab8Request, LinalLab8Response


def generate_variant() -> LinalLab8Request:
    a_n, a_m = 4, 4

    A = [[] for _ in range(a_m)]
    for row in A:
        for _ in range(a_n):
            k = 0
            while k == 0:
                k = random.randint(-9, 9)
            row.append(k)

    return LinalLab8Request(matrix_a = A)


def check_lab(condition: LinalLab8Request, user_answer: LinalLab8Response) -> bool:
    A = np.matrix(condition.matrix_a)
    matrix_a = condition.matrix_a

    a_det = round(np.linalg.det([
        [matrix_a[1][1], matrix_a[1][2], matrix_a[1][3]],
        [matrix_a[2][1], matrix_a[2][2], matrix_a[2][3]],
        [matrix_a[3][1], matrix_a[3][2], matrix_a[3][3]]
    ]))

    b_det = round(np.linalg.det([
        [matrix_a[1][0], matrix_a[1][2], matrix_a[1][3]],
        [matrix_a[2][0], matrix_a[2][2], matrix_a[2][3]],
        [matrix_a[3][0], matrix_a[3][2], matrix_a[3][3]]
    ]))

    c_det = round(np.linalg.det([
        [matrix_a[1][0], matrix_a[1][1], matrix_a[1][3]],
        [matrix_a[2][0], matrix_a[2][1], matrix_a[2][3]],
        [matrix_a[3][0], matrix_a[3][1], matrix_a[3][3]]
    ]))

    d_det = round(np.linalg.det([
        [matrix_a[1][0], matrix_a[1][1], matrix_a[1][2]],
        [matrix_a[2][0], matrix_a[2][1], matrix_a[2][2]],
        [matrix_a[3][0], matrix_a[3][1], matrix_a[3][2]]
    ]))

    correct_answer = {
        "step_1": [a_det, b_det, c_det, d_det],
        "step_2": round(np.linalg.det(A))
    }

    return correct_answer == user_answer.model_dump()
