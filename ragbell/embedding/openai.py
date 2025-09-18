from dotenv import load_dotenv
from langchain_community.embeddings import OpenAIEmbeddings

from ..interfaces import IEmbeddingModel

load_dotenv()


class OpenAIModel(IEmbeddingModel):

    def __init__(self, model_name: str):
        self.embeddings = OpenAIEmbeddings(model_name=model_name)

    def execute(self, text: str) -> list[float]:
        return self.embeddings.embed_query(text)
