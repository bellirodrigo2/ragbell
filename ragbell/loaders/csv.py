import pandas as pd
from pydantic import BaseModel


class CSVLoader(BaseModel):

    separator: str = ","
    encoding: str = "utf-8"
    chunk_size: int = -1

    def execute(self, path: str) -> list[dict]:
        df = pd.read_csv(
            path,
            sep=self.separator,
            encoding=self.encoding,
        )

        df = df.fillna("")  # Evita valores nulos

        records = df.to_dict(orient="records")

        if self.chunk_size == -1:
            chunks = [records]  # todas as linhas em um único chunk
        else:
            chunks = [
                records[i : i + self.chunk_size]
                for i in range(0, len(records), self.chunk_size)
            ]

        # Gerar saída no formato RAG
        result = []
        for idx, chunk in enumerate(chunks):
            # Transformar cada linha do chunk em texto estruturado
            content = "\n".join(
                ["; ".join([f"{col}: {row[col]}" for col in row]) for row in chunk]
            )
            filename = self._filename(path)
            result.append(
                {"content": content, "metadata": {"source": filename, "page": idx}}
            )

        return result
