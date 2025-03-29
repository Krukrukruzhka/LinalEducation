import numpy as np

from src.datamodels.labs import LinalLab6Request, LinalLab6Response


def check_lab(condition: LinalLab6Request, user_answer: LinalLab6Response) -> bool:
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
