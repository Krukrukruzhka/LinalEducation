import copy
import math

import numpy as np

from src.datamodels.labs import LinalLab9Request, LinalLab9Response
from src.algorithms.utils.matrix import matrices_is_similar


# def check_lab(condition: LinalLab9Request, user_answer: LinalLab9Response) -> bool:
#     matrix_a = copy.deepcopy(condition.matrix_a)
#
#     step_1_matrix_1 = copy.deepcopy(matrix_a)
#     step_1_matrix_1_e = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
#     if step_1_matrix_1[0][0] < 0:
#         for column in range(len(step_1_matrix_1[0])):
#             step_1_matrix_1[0][column] *= -1
#             step_1_matrix_1_e[0][column] *= -1
#     for row_index in range(1, len(step_1_matrix_1)):
#         for column_index in range(len(step_1_matrix_1[row_index])-1, -1, -1):
#             step_1_matrix_1_e[row_index][column_index] = step_1_matrix_1[0][0] * step_1_matrix_1_e[row_index][column_index] - step_1_matrix_1_e[0][column_index] * step_1_matrix_1[row_index][0]
#     for row_index in range(1, len(step_1_matrix_1)):
#         for column_index in range(len(step_1_matrix_1[row_index])-1, -1, -1):
#             step_1_matrix_1[row_index][column_index] = step_1_matrix_1[0][0] * step_1_matrix_1[row_index][column_index] - step_1_matrix_1[0][column_index] * step_1_matrix_1[row_index][0]
#     print(step_1_matrix_1)
#
#     step_1_matrix_2 = copy.deepcopy(step_1_matrix_1)
#     step_1_matrix_2_e = copy.deepcopy(step_1_matrix_1_e)
#     if step_1_matrix_2[1][1] < 0:
#         for column in range(len(step_1_matrix_2[1])):
#             step_1_matrix_2[1][column] *= -1
#             step_1_matrix_2_e[1][column] *= -1
#     for row_index in range(2, len(step_1_matrix_2)):
#         for column_index in range(len(step_1_matrix_2[row_index]) - 1, -1, -1):
#             step_1_matrix_2_e[row_index][column_index] = step_1_matrix_2[1][1] * step_1_matrix_2_e[row_index][column_index] - step_1_matrix_2_e[1][column_index] * step_1_matrix_2[row_index][1]
#     for row_index in range(2, len(step_1_matrix_2)):
#         for column_index in range(len(step_1_matrix_2[row_index]) - 1, -1, -1):
#             step_1_matrix_2[row_index][column_index] = step_1_matrix_2[1][1] * step_1_matrix_2[row_index][column_index] - step_1_matrix_2[1][column_index] * step_1_matrix_2[row_index][1]
#     print(step_1_matrix_2)
#
#     step_2_matrix_1 = copy.deepcopy(step_1_matrix_2)
#     step_2_matrix_1_e = copy.deepcopy(step_1_matrix_2_e)
#     if step_2_matrix_1[2][2] < 0:
#         for column in range(len(step_2_matrix_1[2])):
#             step_2_matrix_1[2][column] *= -1
#             step_2_matrix_1_e[2][column] *= -1
#     for row_index in range(len(step_1_matrix_2)-1):
#         for column_index in range(len(step_1_matrix_2[row_index]) - 1, -1, -1):
#             step_1_matrix_2_e[row_index][column_index] = step_1_matrix_2[1][1] * step_1_matrix_2_e[row_index][column_index] - step_1_matrix_2_e[1][column_index] * step_1_matrix_2[row_index][1]
#     for row_index in range(2, len(step_1_matrix_2)):
#         for column_index in range(len(step_1_matrix_2[row_index]) - 1, -1, -1):
#             step_1_matrix_2[row_index][column_index] = step_1_matrix_2[1][1] * step_1_matrix_2[row_index][column_index] - step_1_matrix_2[1][column_index] * step_1_matrix_2[row_index][1]
#     print(step_2_matrix_1)
#
#     step_1_matrix_1_is_correct = matrices_is_similar(step_1_matrix_1, user_answer.step_1_matrix_1) and matrices_is_similar(step_1_matrix_1_e, user_answer.step_1_matrix_1_e)
#     step_1_matrix_2_is_correct = matrices_is_similar(step_1_matrix_2, user_answer.step_1_matrix_2) and matrices_is_similar(step_1_matrix_2_e, user_answer.step_1_matrix_2_e)
#     step_2_matrix_1_is_correct = matrices_is_similar(step_2_matrix_1, user_answer.step_2_matrix_1) and matrices_is_similar(step_2_matrix_1_e, user_answer.step_2_matrix_1_e)
#     step_2_matrix_2_is_correct = matrices_is_similar(step_2_matrix_2, user_answer.step_2_matrix_2) and matrices_is_similar(step_2_matrix_2_e, user_answer.step_2_matrix_2_e)
#
#     step_1_is_correct = step_1_matrix_1_is_correct and step_1_matrix_2_is_correct
#     step_2_is_correct = step_2_matrix_1_is_correct and step_2_matrix_2_is_correct
#     step_3_is_correct = matrices_is_similar(step_3_matrix_1, user_answer.step_3_matrix_1)
#
#     return step_1_is_correct and step_2_is_correct and step_3_is_correct


def check_lab(condition: LinalLab9Request, user_answer: LinalLab9Response) -> bool:
    matrix_a = copy.deepcopy(condition.matrix_a)
    matrix_a[0][0] += 2
    editable_matrix = np.array(matrix_a)
    editable_matrix_e = [[1 if row == column else 0 for column in range(len(editable_matrix))] for row in range(len(editable_matrix))]
    editable_matrix_e = np.array(editable_matrix_e)

    for row1 in range(len(editable_matrix)):
        for row2 in range(row1 + 1, len(editable_matrix)):
            nod = math.gcd(abs(editable_matrix[row1][row1]), abs(editable_matrix[row2][row1]))
            editable_matrix_e[row2] = editable_matrix_e[row2] * (editable_matrix[row1][row1] // nod) - editable_matrix_e[row1] * (editable_matrix[row2][row1] // nod)
            editable_matrix[row2] = editable_matrix[row2] * (editable_matrix[row1][row1] // nod) - editable_matrix[row1] * (editable_matrix[row2][row1] // nod)

    for row1 in range(len(editable_matrix) - 1, -1, -1):
        for row2 in range(row1 - 1, -1, -1):
            nod = math.gcd(abs(editable_matrix[row1][row1]), abs(editable_matrix[row2][row1]))
            print(editable_matrix[row1][row1], editable_matrix[row2][row1], nod)
            editable_matrix_e[row2] = editable_matrix_e[row2] * (editable_matrix[row1][row1] // nod) - editable_matrix_e[row1] * (editable_matrix[row2][row1] // nod)
            editable_matrix[row2] = editable_matrix[row2] * (editable_matrix[row1][row1] // nod) - editable_matrix[row1] * (editable_matrix[row2][row1] // nod)
        print(editable_matrix)
        print(editable_matrix_e)
        print()

    print(matrix_a)
    print(editable_matrix)
    print(editable_matrix_e)

if __name__ == "__main__":
    cond = LinalLab9Request(matrix_a=[[1, 3, -5], [-2, -5, 12], [1, 4, -4]])
    check_lab(cond, None)
