import numpy as np
import random

from typing import Any


def generate_variant() -> dict[str, Any]:
    a_n, a_m = 3, 2
    b_n, b_m = 2, 3
    alpha, beta = 0, 0

    while alpha == 0:
        alpha = random.randint(-10, 10)

    while beta == 0:
        beta = random.randint(-10, 10)

    A = [[random.randint(-9, 9) for _ in range(a_n)] for _ in range(a_m)]
    B = [[random.randint(-9, 9) for _ in range(b_n)] for _ in range(b_m)]

    return {
        "A": A,
        "B": B,
        "alpha": alpha,
        "beta": beta
    }


def load_variant(user_id: str) -> dict[str, Any]:
    # TODO: load variant from database
    return generate_variant()


def check_lab(user_id: str, user_answers: dict[str, list[list[int | float]]]) -> bool:
    condition = load_variant(user_id)

    alpha, beta = condition["alpha"], condition["beta"]
    A, B = np.matrix(condition["A"]), np.matrix(condition["B"])

    correct_answers = {
        "step_1": A * B,
        "step_2": alpha * A * B,
        "step_3": A.T,
        "step_4": B.T,
        "step_5": B.T * A.T,
        "step_6": beta * B.T * A.T,
        "step_7": alpha * A * B + beta * B.T * A.T
    }

    for i in range(1, len(correct_answers) + 1):
        if not np.allclose(np.matrix(user_answers[f"step_{i}"]), correct_answers[f"step_{i}"]):
            return False

    return True


if __name__ == "__main__":
    print(check_lab(1, 0), sep="\n")