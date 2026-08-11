import os

from app.services.pdf_reader import read_pdf
from app.services.csv_reader import read_csv
from app.services.excel_reader import read_excel


def extract_document(path):

    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return read_pdf(path)

    elif ext == ".csv":
        return read_csv(path)

    elif ext in [".xlsx", ".xls"]:
        return read_excel(path)

    else:
        raise Exception("Unsupported file")