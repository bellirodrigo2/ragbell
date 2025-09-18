from langchain.text_splitter import SpacySentenceSplitter
from pydantic import BaseModel

# python -m spacy download en_core_web_sm
# python -m spacy download pt_core_news_sm


class SentenceSplitter(BaseModel):

    language_model: str  # e.g., "en_core_web_sm", "pt_core_news_sm"

    def execute(self, text: str) -> list[str]:
        splitter = SpacySentenceSplitter(pipeline=self.language_model)
        return splitter.split_text(text)
