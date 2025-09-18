from langchain.text_splitter import CharacterTextSplitter
from pydantic import BaseModel

from ..interfaces import ISplitter


class CharacterSplitter(BaseModel, ISplitter):

    chunk_size: int
    chunk_overlap: int

    def execute(self, text: str) -> list[str]:
        splitter = CharacterTextSplitter(
            chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap
        )

        return splitter.split_text(text)
