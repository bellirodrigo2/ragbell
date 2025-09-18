from pypdf import PdfReader

from .utils import extract_filename


class PDFLoader:
    def execute(self, path: str) -> list[dict]:
        reader = PdfReader(path)
        file_name = extract_filename(path)
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
