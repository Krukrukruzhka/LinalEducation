import numpy as np

from src.datamodels.labs import LinalLab4Request, LinalLab4Response


def check_lab(condition: LinalLab4Request, user_answer: LinalLab4Response) -> bool:
    A, B = np.matrix(condition.matrix_a), np.matrix(condition.matrix_b)

    correct_answer = (A[0, 0] * A[1, 1] - A[1, 0] * A[0, 1]) * (B[0, 0] * B[1, 1] - B[1, 0] * B[0, 1])

    return int(correct_answer) == user_answer.answer_matrix_det
