from pydantic import BaseModel


class LinalLab1Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]
    alpha: int
    beta: int


class LinalLab1Response(BaseModel):
    answer_matrix: list[list[int]]


class LinalLab7Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]


class LinalLab7Response(BaseModel):
    answer_matrix_det: int
