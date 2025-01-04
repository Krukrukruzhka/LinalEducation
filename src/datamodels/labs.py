from pydantic import BaseModel


class Lab1Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]
    alpha: int
    beta: int


class Lab1Response(BaseModel):
    answer_matrix: list[list[int]]
