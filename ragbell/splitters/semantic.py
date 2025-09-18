from langchain.text_splitter import SpacyTextSplitter
from pydantic import BaseModel, Field


class SpacySemanticSplitter(BaseModel):

    laguage_model: str = Field(default="en_core_web_sm")
    chunk_size: int = Field(default=1000)
    initialized: bool = Field(default=False)

    def execute(self, text: str) -> list[str]:
        if not self.initialized:
            self.nlp = spacy.load(self.laguage_model)
            self.initialized = True

        splitter = SpacyTextSplitter(
            pipeline=self.laguage_model, chunk_size=self.chunk_size
        )
        return splitter.split_text(text)
