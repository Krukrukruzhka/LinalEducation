from src.datamodels.labs import LinalLab1Request

LINAL_LAB1_VARIANTS = [
    LinalLab1Request(
        matrix_a=[
            [1, 0, 4],
            [2, 1, 3]
        ],
        matrix_b=[
            [-1, 2],
            [2, 2],
            [3, 1]
        ],
        alpha=3,
        beta=-2
    ),
    LinalLab1Request(
        matrix_a=[
            [2, 1, 4],
            [3, -1, 0]
        ],
        matrix_b = [
            [1, 3],
            [2, 2],
            [3, 1]
        ],
        alpha = 3,
        beta = -2
    )
]