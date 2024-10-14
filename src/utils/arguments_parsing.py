import argparse

from pydantic import BaseModel


def build_arguments_name(name: str) -> str:
    return f'--{name.replace("_", "-")}'


def enrich_parser(parser: argparse.ArgumentParser, model: BaseModel):
    for field_name, field_value in model.model_fields.items():
        parser.add_argument(
            build_arguments_name(field_name),
            dest=field_name,
            type=field_value.json_schema_extra['type'],
            default=field_value.default,
            help=field_value.description,
        )
