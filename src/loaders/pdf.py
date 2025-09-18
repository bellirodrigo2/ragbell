from pypdf import PdfReader

from ..interfaces import ILoader


class PDFLoader(ILoader):
    def execute(self, path: str) -> list[dict]:
        reader = PdfReader(path)
        file_name = self._filename(path)
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
