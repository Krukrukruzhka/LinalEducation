import copy

from src.datamodels.labs import LinalLab7Request, LinalLab7Response
from src.algorithms.utils.matrix import matrices_is_similar


def check_lab(condition: LinalLab7Request, user_answer: LinalLab7Response) -> bool:
    matrix_a = copy.deepcopy(condition.matrix_a)

    step_1_matrix_1 = copy.deepcopy(matrix_a)

    for row_index in range(1, len(step_1_matrix_1)):
        for column_index in range(len(step_1_matrix_1[row_index])-1, -1, -1):
            step_1_matrix_1[row_index][column_index] = step_1_matrix_1[0][0] * step_1_matrix_1[row_index][column_index] - step_1_matrix_1[0][column_index] * step_1_matrix_1[row_index][0]

    step_1_matrix_2 = copy.deepcopy(step_1_matrix_1)

    for row_index in range(2, len(step_1_matrix_2)):
        for column_index in range(len(step_1_matrix_2[row_index])-1, -1, -1):
            step_1_matrix_2[row_index][column_index] = step_1_matrix_2[1][1] * step_1_matrix_2[row_index][column_index] - step_1_matrix_2[1][column_index] * step_1_matrix_2[row_index][1]

    rank = 0

    for row in step_1_matrix_2:
        for element in row:
            if element != 0:
                rank += 1
                break

    return matrices_is_similar(step_1_matrix_1, user_answer.step_1_matrix_1) and matrices_is_similar(step_1_matrix_2, user_answer.step_1_matrix_2) and rank == user_answer.step_2_rank
