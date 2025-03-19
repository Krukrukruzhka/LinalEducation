from pydantic import BaseModel


class LinalLab1Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]
    alpha: int
    beta: int


class LinalLab1Response(BaseModel):
    answer_matrix: list[list[int]]


class LinalLab2Request(BaseModel):
    pass


class LinalLab2Response(BaseModel):
    pass


class LinalLab3Request(BaseModel):
    matrix_a: list[list[int]]
    coefficients: list[int]


class LinalLab3Response(BaseModel):
    step_1_matrix_1: list[list[int]]
    step_1_matrix_2: list[list[int]]
    step_1_matrix_3: list[list[int]]
    step_2_matrix_1: list[list[int]]


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


class LinalLab6Request(BaseModel):
    pass


class LinalLab6Response(BaseModel):
    pass


class LinalLab7Request(BaseModel):
    pass


class LinalLab7Response(BaseModel):
    pass


class LinalLab8Request(BaseModel):
    pass


class LinalLab8Response(BaseModel):
    pass


class LinalLab9Request(BaseModel):
    pass


class LinalLab9Response(BaseModel):
    pass


class LinalLab10Request(BaseModel):
    pass


class LinalLab10Response(BaseModel):
    pass


class LinalLab11Request(BaseModel):
    pass


class LinalLab11Response(BaseModel):
    pass


class LinalLab12Request(BaseModel):
    pass


class LinalLab12Response(BaseModel):
    pass


class LinalLab13Request(BaseModel):
    pass


class LinalLab13Response(BaseModel):
    pass


class LinalLab14Request(BaseModel):
    pass


class LinalLab14Response(BaseModel):
    pass


class LinalLab15Request(BaseModel):
    pass


class LinalLab15Response(BaseModel):
    pass
