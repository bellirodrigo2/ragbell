import markdown2
from bs4 import BeautifulSoup

from ..interfaces import ILoader
from .html import HTMLLoader


class MDLoader(ILoader):
    def __init__(
        self,
        chunk_size: int = -1,
        chunk_overlap: int = 0,
    ):
        """
        :param chunk_size: Número de linhas por chunk (-1 = todas as linhas em 1 chunk)
        :param chunk_overlap: número de linhas que cada chunk deve compartilhar com o próximo
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def execute(self, path: str) -> list[dict]:
        """
        Carrega um HTML e retorna uma lista de dicts no formato:
        {content: "...", metadata: {source: arquivo, page: índice}}
        Apenas textos das tags relevantes, ignorando as tags de exclusão.

        :param overlap: número de linhas que cada chunk deve compartilhar com o próximo
        """
        markdown_text = markdown2.markdown_path(path)

        html_loader = HTMLLoader(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
        )

        return html_loader.from_text(markdown_text, path)


if __name__ == "__main__":
    loader = MDLoader(chunk_size=100, chunk_overlap=10)
    docs = loader.execute("example.md")
    for doc in docs:
        print(doc)
