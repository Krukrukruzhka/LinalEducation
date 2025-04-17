from src.datamodels.labs import LinalLab12Request

LINAL_LAB12_VARIANTS = [
    LinalLab12Request(
        coefficients=[
            [1, 3, 2, 0],
            [1, 10, 3, 1],
            [4, 19, 9, 1]
        ],
        results=[0, -5, -5]
    ),
    LinalLab12Request(
        coefficients=[
            [1, 4, 2, 0],
            [4, 13, 3, 1],
            [1, 1, -3, 1]
        ],
        results=[1, 0, -3]
    )
]