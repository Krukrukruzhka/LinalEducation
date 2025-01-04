import numpy as np
import random

from src.datamodels.labs import Lab1Request, Lab1Response


def generate_variant() -> Lab1Request:
    a_n, a_m = 3, 2
    b_n, b_m = 2, 3
    alpha, beta = 0, 0

    while alpha == 0:
        alpha = random.randint(-10, 10)

    while beta == 0:
        beta = random.randint(-10, 10)

    A = [[random.randint(-9, 9) for _ in range(a_n)] for _ in range(a_m)]
    B = [[random.randint(-9, 9) for _ in range(b_n)] for _ in range(b_m)]

    return Lab1Request(matrix_a = A, matrix_b = B, alpha = alpha, beta = beta)


def check_lab(condition: Lab1Request, user_answer: Lab1Response) -> bool:
    alpha, beta = condition.alpha, condition.beta
    A, B = np.matrix(condition.matrix_a), np.matrix(condition.matrix_b)

    correct_answer = alpha * A * B + beta * B.T * A.T

    return np.allclose(correct_answer, np.matrix(user_answer.answer_matrix))
