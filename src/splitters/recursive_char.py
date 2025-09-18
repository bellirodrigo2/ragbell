from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel

from ..interfaces import ISplitter


class RecursiveSplitter(BaseModel, ISplitter):

    chunk_size: int
    chunk_overlap: int
    separators: list[str]

    def split(self, text: str) -> list[str]:
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=self.separators,
        )

        return splitter.split_text(text)
