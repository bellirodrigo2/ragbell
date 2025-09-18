from langchain.text_splitter import TokenTextSplitter
from pydantic import BaseModel

from ..interfaces import ISplitter


class TokenSplitter(BaseModel, ISplitter):

    chunk_size: int
    chunk_overlap: int
    encoding_name: str

    def split(self, text: str) -> list[str]:
        splitter = TokenTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            encoding_name=self.encoding_name,
        )

        return splitter.split_text(text)
