from src.datamodels.labs import LinalLab11Request

LINAL_LAB11_VARIANTS = [
    LinalLab11Request(
        coefficients=[
            [1, 3, -6],
            [2, 5, -8],
            [1, 2, -1]
        ],
        results=[1, 2, 3]
    ),
    LinalLab11Request(
        coefficients=[
            [1, 2, -5],
            [2, 3, -5],
            [1, 1, 1]
        ],
        results=[1, 3, 2]
    )
]