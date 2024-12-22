from pydantic import BaseModel


class AnswerLab1(BaseModel):
    step_1: list[list[int]]
    step_2: list[list[int]]
    step_3: list[list[int]]
    step_4: list[list[int]]
    step_5: list[list[int]]
    step_6: list[list[int]]
    step_7: list[list[int]]
