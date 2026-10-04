from pathlib import Path
from pypdf import PdfReader

DOCUMENTS_DIR = Path("documents")


def load_pdf(pdf_file):
    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text.strip()


def load_txt(txt_file):
    return txt_file.read_text(
        encoding="utf-8",
        errors="ignore"
    ).strip()


def load_documents():
    documents = []

    for file in DOCUMENTS_DIR.iterdir():

        if file.suffix.lower() == ".pdf":
            try:
                text = load_pdf(file)

            except Exception as e:
                print(f"Could not read PDF {file.name}: {e}")
                continue

        elif file.suffix.lower() == ".txt":
            try:
                text = load_txt(file)

            except Exception as e:
                print(f"Could not read TXT {file.name}: {e}")
                continue

        else:
            continue

        if text:
            documents.append({
                "source": file.name,
                "text": text
            })

    return documents


if __name__ == "__main__":
    docs = load_documents()

    print(f"Documents found: {len(docs)}")

    for doc in docs:
        print("\n" + "=" * 60)
        print("SOURCE:", doc["source"])
        print("=" * 60)
        print(doc["text"][:1000])