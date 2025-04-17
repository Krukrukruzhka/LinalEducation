import numpy as np

from src.datamodels.labs import LinalLab5Request, LinalLab5Response


def check_lab(condition: LinalLab5Request, user_answer: LinalLab5Response) -> bool:
    matrix_a, matrix_b = [], []

    for row in condition.matrix_a:
        matrix_a.append([])
        for element in row:
            matrix_a[-1].append(int(element))

    for row in condition.matrix_b:
        matrix_b.append([])
        for element in row:
            if "cos" in element:
                matrix_b[-1].append(1)
            elif "sin" in element:
                matrix_b[-1].append(0)
            else:
                matrix_b[-1].append(int(element))

    matrix_a_det = round(np.linalg.det(matrix_a))
    matrix_b_det = round(np.linalg.det(matrix_b))

    return matrix_a_det == user_answer.matrix_a_res and matrix_b_det == user_answer.matrix_b_res
