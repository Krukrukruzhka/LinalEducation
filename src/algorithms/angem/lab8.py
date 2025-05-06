from src.datamodels.labs import AngemLab8Request, AngemLab8Response


def check_lab(condition: AngemLab8Request, user_answer: AngemLab8Response) -> bool:
    return