from langchain_community.document_loaders import (
    BSHTMLLoader,
    DirectoryLoader,
    JSONLoader,
    PyPDFLoader,
    RecursiveUrlLoader,
    WebBaseLoader,
)
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.sitemap import SitemapLoader

DEFAULT_PDF_LOADER = PyPDFLoader

LOADERS_MAP = {
    "directory": DirectoryLoader,
    "csv": CSVLoader,
    "web": WebBaseLoader,
    "recursive_url": RecursiveUrlLoader,
    "sitemap": SitemapLoader,
    "pdf": DEFAULT_PDF_LOADER,
    "pypdf": PyPDFLoader,
    "json": JSONLoader,
    "html": BSHTMLLoader,
}


def get_loader(loader_type: str, **kwargs):
    loader_class = LOADERS_MAP.get(loader_type)

    if not loader_class:
        raise ValueError(f"Loader type '{loader_type}' is not supported.")
    return loader_class(**kwargs)
