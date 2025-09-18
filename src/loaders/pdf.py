from pypdf import PdfReader

from ..interfaces import ILoader


class PDFLoader(ILoader):
    def load(self, file_path: str) -> list[dict]:
        reader = PdfReader(file_path)
        file_name = self._filename(file_path)
        doc = []
        for page in reader.pages:
            page = {
                "content": page.extract_text(),
                "metadata": {
                    "source": file_name,
                    "page": reader.pages.index(page) + 1,
                },
            }
            doc.append(page)
        return doc
