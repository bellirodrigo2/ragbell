from bs4 import BeautifulSoup

from ..interfaces import ILoader


class HTMLLoader(ILoader):
    def __init__(
        self,
        chunk_size: int = -1,
        chunk_overlap: int = 0,
        include_tags: list[str] = None,
        exclude_tags: list[str] = None,
    ):
        """
        :param chunk_size: Número de linhas por chunk (-1 = todas as linhas em 1 chunk)
        :param include_tags: Lista de tags HTML a extrair (ex: ["p", "h1", "li", "article"])
        :param exclude_tags: Lista de tags HTML a remover antes da extração (ex: ["script", "style", "nav"])
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.include_tags = include_tags or [
            "p",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "li",
            "article",
            "section",
        ]
        self.exclude_tags = exclude_tags or [
            "script",
            "style",
            "head",
            "footer",
            "nav",
            "form",
            "noscript",
        ]

    def load(self, path: str) -> list[dict]:
        """
        Carrega um HTML e retorna uma lista de dicts no formato:
        {content: "...", metadata: {source: arquivo, page: índice}}
        Apenas textos das tags relevantes, ignorando as tags de exclusão.

        :param overlap: número de linhas que cada chunk deve compartilhar com o próximo
        """
        if self.chunk_size != -1 and self.chunk_overlap >= self.chunk_size:
            raise ValueError("Overlap should be lower than chunk_size")

        with open(path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

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
        filename = self._filename(path)
        for idx, chunk in enumerate(chunks):
            content = "\n".join(chunk)
            result.append(
                {"content": content, "metadata": {"source": filename, "page": idx}}
            )

        return result


if __name__ == "__main__":
    loader = HTMLLoader(chunk_size=100, chunk_overlap=20)
    data = loader.load("medium.html")
    print(data[1])
