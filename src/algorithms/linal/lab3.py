import numpy as np
import random

from src.datamodels.labs import LinalLab3Request, LinalLab3Response


def generate_variant() -> LinalLab3Request:
    a_n, a_m = 2, 2

    A = [[random.randint(-9, 9) for _ in range(a_n)] for _ in range(a_m)]
    c = [random.randint(-9, 9) for _ in range(3)]

    return LinalLab3Request(matrix_a = A, coefficients=c)


def check_lab(condition: LinalLab3Request, user_answer: LinalLab3Response) -> bool:
    A = np.matrix(condition.matrix_a)
    coefficients = condition.coefficients

    correct_matrix_1 = coefficients[0] * A * A
    correct_matrix_2 = coefficients[1] * A
    correct_matrix_3 = coefficients[2] * np.eye(2).astype(int)

    correct_result = correct_matrix_1 + correct_matrix_2 + correct_matrix_3

    return np.allclose(correct_result, np.matrix(user_answer.step_2_matrix_1)) and np.allclose(correct_matrix_1, np.matrix(user_answer.step_1_matrix_1)) and np.allclose(correct_matrix_2, np.matrix(user_answer.step_1_matrix_2)) and np.allclose(correct_matrix_3, np.matrix(user_answer.step_1_matrix_3))
