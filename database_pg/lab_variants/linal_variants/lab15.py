from src.datamodels.labs import LinalLab15Request

LINAL_LAB15_VARIANTS = [
    LinalLab15Request(
        coefficients=[
            [["1", "a"], ["1", "a"], ["1", "a"]],
            [["1", "a"], ["3", ""], ["1", ""]],
            [["1", "a"], ["1", ""], ["1", ""]]
        ]
    ),
    LinalLab15Request(
        coefficients=[
            [["3", ""], ["-1", "a"], ["2", ""]],
            [["-1", "a"], ["-1", "a"], ["-1", "a"]],
            [["2", ""], ["-1", "a"], ["6", ""]]
        ]
    )
]