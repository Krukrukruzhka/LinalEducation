from pydantic import BaseModel


class LinalLab1Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]
    alpha: int
    beta: int


class LinalLab1Response(BaseModel):
    answer_matrix: list[list[int]]


class LinalLab2Request(BaseModel):
    vector_x: list[int]
    vector_y: list[int]
    matrix_a: list[list[int]]


class LinalLab2Response(BaseModel):
    step_1_matrix_1: list[list[int]]
    step_2_tr: int


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
    matrix_a: list[list[str]]
    matrix_b: list[list[str]]


class LinalLab5Response(BaseModel):
    matrix_a_res: int
    matrix_b_res: int


class LinalLab6Request(BaseModel):
    matrix_a: list[list[int]]


class LinalLab6Response(BaseModel):
    step_1: list[int]
    step_2: int


class LinalLab7Request(BaseModel):
    matrix_a: list[list[int]]


class LinalLab7Response(BaseModel):
    step_1: list[list[int]]
    step_2: list[list[int]]


class LinalLab8Request(BaseModel):
    matrix_b: list[list[int]]


class LinalLab8Response(BaseModel):
    step_1: list[list[int]]
    step_2: list[list[int]]
    step_3: list[list[int]]


class LinalLab9Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]


class LinalLab9Response(BaseModel):
    pass


class LinalLab10Request(BaseModel):
    equation_1_matrix_1: list[list[int]]
    equation_1_matrix_2: list[list[int]]
    equation_1_coefficient: int
    equation_2_matrix_1: list[list[int]]
    equation_2_matrix_2: list[list[int]]
    equation_2_coefficient: int
    equation_3_matrix_1: list[list[int]]
    equation_3_matrix_2: list[list[int]]
    equation_3_matrix_3: list[list[int]]


class LinalLab10Response(BaseModel):
    pass


class LinalLab11Request(BaseModel):
    coefficients: list[list[int]]
    results: list[int]


class LinalLab11Response(BaseModel):
    step_1_det: float
    step_2_det_1: float
    step_2_det_2: float
    step_2_det_3: float
    step_3_x_1: float
    step_3_x_2: float
    step_3_x_3: float


class LinalLab12Request(BaseModel):
    coefficients: list[list[int]]
    results: list[int]


class LinalLab12Response(BaseModel):
    pass


class LinalLab13Request(BaseModel):
    matrix_a: list[list[int]]
    matrix_b: list[list[int]]
    matrix_c: list[list[int]]


class LinalLab13Response(BaseModel):
    pass


class LinalLab14Request(BaseModel):
    coefficients: list[list[float]]


class LinalLab14Response(BaseModel):
    pass


class LinalLab15Request(BaseModel):
    coefficients: list[list[list[str]]]


class LinalLab15Response(BaseModel):
    pass
