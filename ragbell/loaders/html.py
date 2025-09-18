from bs4 import BeautifulSoup
from pydantic import BaseModel

from .utils import extract_filename


class HTMLLoader(BaseModel):
    chunk_size: int = -1
    chunk_overlap: int = 0
    include_tags: list[str] = None
    exclude_tags: list[str] = None

    def from_text(self, text: str, path: str) -> list[dict]:
        soup = BeautifulSoup(text, "html.parser")

        # Remove tags de exclusão
        for tag in soup(self.exclude_tags):
            tag.decompose()

        # Extrai o texto das tags relevantes
        content_elements = soup.find_all(self.include_tags)
        lines = [
            el.get_text(separator=" ", strip=True)
            for el in content_elements
            if el.get_text(strip=True)
        ]

        chunks = []
        if self.chunk_size == -1:
            chunks = [lines]  # tudo em 1 chunk
        else:
            i = 0
            while i < len(lines):
                chunk = lines[i : i + self.chunk_size]
                chunks.append(chunk)
                i += self.chunk_size - self.chunk_overlap

        result = []
        filename = extract_filename(path)
        for idx, chunk in enumerate(chunks):
            content = "\n".join(chunk)
            result.append(
                {"content": content, "metadata": {"source": filename, "page": idx}}
            )

        return result

    def execute(self, path: str) -> list[dict]:
        """
        Carrega um HTML e retorna uma lista de dicts no formato:
        {content: "...", metadata: {source: arquivo, page: índice}}
        Apenas textos das tags relevantes, ignorando as tags de exclusão.

        :param overlap: número de linhas que cada chunk deve compartilhar com o próximo
        """
        if self.chunk_size != -1 and self.chunk_overlap >= self.chunk_size:
            raise ValueError("Overlap should be lower than chunk_size")

        with open(path, "r", encoding="utf-8") as f:
            return self.from_text(f.read(), path)
