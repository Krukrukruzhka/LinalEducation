from src.datamodels.labs import LinalLab3Request

LINAL_LAB3_VARIANTS = [
    LinalLab3Request(
        matrix_a=[
            [1, -2],
            [3, 1]
        ],
        coefficients=[1, -2, 3]
    ),
    LinalLab3Request(
        matrix_a=[
            [1, 2],
            [3, 1]
        ],
        coefficients=[1, 2, -5]
    )
]