from ..interfaces import ILoader
from .csv import CSVLoader
from .html import HTMLLoader
from .pdf import PDFLoader

LOADER_MAP = {
    "pdf": PDFLoader,
    "html": HTMLLoader,
    "csv": CSVLoader,
}


def get_loader(loader_type: str, **kwargs) -> ILoader:
    loader_class = LOADER_MAP.get(loader_type)
    if not loader_class:
        raise ValueError(f"Loader type '{loader_type}' is not supported.")
    return loader_class(**kwargs)
