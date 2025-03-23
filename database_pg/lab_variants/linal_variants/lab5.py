from src.datamodels.labs import LinalLab5Request

LINAL_LAB5_VARIANTS = [
    LinalLab5Request(
        matrix_a=[
            ["1", "2", "-1"],
            ["2", "4", "3"],
            ["-5", "-2", "1"]
        ],
        matrix_b=[
            ["2", "3", "cos(a)"],
            ["-3", "2", "sin(a)"],
            ["cos(a)", "sin(a)", "3"]
        ]
    ),
    LinalLab5Request(
        matrix_a=[
            ["2", "3", "-2"],
            ["3", "4", "5"],
            ["-2", "-5", "1"]
        ],
        matrix_b=[
            ["4", "cos(a)", "sin(a)"],
            ["cos(a)", "5", "-3"],
            ["sin(a)", "3", "5"]
        ]
    ),
    LinalLab5Request(
        matrix_a=[
            ["4", "3", "-2"],
            ["2", "1", "3"],
            ["-3", "-2", "5"]
        ],
        matrix_b=[
            ["3", "sin(a)", "4"],
            ["sin(a)", "-2", "cos(a)"],
            ["-4", "cos(a)", "3"]
        ]
    )
]