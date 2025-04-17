import numpy as np

from src.datamodels.labs import LinalLab2Request, LinalLab2Response


def check_lab(condition: LinalLab2Request, user_answer: LinalLab2Response) -> bool:
    step_1_matrix_1 = np.matrix(condition.matrix_a) * np.matrix(condition.vector_x).T * np.matrix(condition.vector_y)

    return np.allclose(step_1_matrix_1, np.matrix(user_answer.step_1_matrix_1)) and int(step_1_matrix_1.trace()) == user_answer.step_2_tr
