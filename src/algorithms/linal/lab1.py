import numpy as np

from src.datamodels.labs import LinalLab1Request, LinalLab1Response


def check_lab(condition: LinalLab1Request, user_answer: LinalLab1Response) -> bool:
    alpha, beta = condition.alpha, condition.beta
    A, B = np.matrix(condition.matrix_a), np.matrix(condition.matrix_b)

    correct_answer = alpha * A * B + beta * B.T * A.T

    return np.allclose(correct_answer, np.matrix(user_answer.answer_matrix))
