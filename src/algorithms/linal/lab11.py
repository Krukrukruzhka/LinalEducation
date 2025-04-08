import numpy as np

from src.datamodels.labs import LinalLab11Request, LinalLab11Response


def calculate_det_3(matrix: list[list[int]]):
     return matrix[0][0]*matrix[1][1]*matrix[2][2] + matrix[1][0]*matrix[0][2]*matrix[2][1] +\
        matrix[0][1]*matrix[2][0]*matrix[1][2] - matrix[0][2]*matrix[1][1]*matrix[2][0] -\
        matrix[2][2]*matrix[0][1]*matrix[1][0] - matrix[0][0]*matrix[1][2]*matrix[2][1]


def check_lab(condition: LinalLab11Request, user_answer: LinalLab11Response) -> bool:
    det = calculate_det_3(condition.coefficients)

    det_1 = calculate_det_3([[condition.results[row] if column == 0 else condition.coefficients[row][column] for column in range(3)] for row in range(3)])
    det_2 = calculate_det_3([[condition.results[row] if column == 1 else condition.coefficients[row][column] for column in range(3)] for row in range(3)])
    det_3 = calculate_det_3([[condition.results[row] if column == 2 else condition.coefficients[row][column] for column in range(3)] for row in range(3)])

    x1 = det_1 / det
    x2 = det_2 / det
    x3 = det_3 / det

    step_1_is_correct = user_answer.step_1_det == det
    step_2_is_correct = user_answer.step_2_det_1 == det_1 and user_answer.step_2_det_2 == det_2 and user_answer.step_2_det_3 == det_3
    step_3_is_correct = abs(user_answer.step_3_x_1 - x1) < 0.001 and abs(user_answer.step_3_x_2 - x2) < 0.001 and abs(user_answer.step_3_x_3 - x3) < 0.001

    return step_1_is_correct and step_2_is_correct and step_3_is_correct
