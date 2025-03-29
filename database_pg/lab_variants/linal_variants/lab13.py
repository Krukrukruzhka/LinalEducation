from src.datamodels.labs import LinalLab13Request

LINAL_LAB13_VARIANTS = [
    LinalLab13Request(
        matrix_a=[
            [-1, 1],
            [-4, 3]
        ],
        matrix_b=[
            [1, 1],
            [-1, 1]
        ],
        matrix_c=[
            [0, 2, 3],
            [2, 3, 6],
            [3, 6, 8]
        ]
    ),
    LinalLab13Request(
        matrix_a=[
            [-2, 2],
            [-8, 6]
        ],
        matrix_b=[
            [2, 1],
            [-1, 2]
        ],
        matrix_c=[
            [1, 1, -3],
            [4, 1, -6],
            [-2, -1, 2]
        ]
    )
]