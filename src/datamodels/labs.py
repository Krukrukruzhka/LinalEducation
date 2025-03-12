from pydantic import BaseModel


class LinalLab1Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]
    alpha: int
    beta: int


class LinalLab1Response(BaseModel):
    answer_matrix: list[list[int]]


class LinalLab4Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]


class LinalLab4Response(BaseModel):
    answer_matrix_det: int


class LinalLab5Request(BaseModel):
    matrix_a: list[list[int]]


class LinalLab5Response(BaseModel):
    step_1: list[int]
    step_2: int
