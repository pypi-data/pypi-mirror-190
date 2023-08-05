from typing import TypedDict
from .utils import file_ext
import enum

class ExportDataType(str, enum.Enum):
    pandas = "pandas"
    s3 = "s3"
    database = "database"
    raw = "raw"

class ExportData(TypedDict):
    name: str
    type: ExportDataType
    value: str

def load_export(export: ExportData):
    match export["type"]:
        case ExportDataType.pandas:
            return _load_pandas(export)

        case ExportDataType.s3:
            # load s3
            pass

        case ExportDataType.database:
            # load database
            pass

        case ExportDataType.raw:
            # load raw
            return _load_raw()

        case _:
            raise ValueError("Unknown export type")

def _load_pandas(export: ExportData):
    import pandas as pd
    match file_ext(export["value"]):
        case "csv":
            return pd.read_csv(export["value"])
        case "tsv":
            return pd.read_csv(export["value"], sep="\t")
        case "json":
            return pd.read_json(export["value"])
        case _:
            raise ValueError("Unknown pandas file type")

def _load_raw(export: ExportData):
    return export["value"]