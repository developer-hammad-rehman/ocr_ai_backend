import fitz
import pandas as pd

from app.models import ReviewResult
def upload_file(filename:str , content:bytes):
    file_path = f"uploads/{filename}"
    with open(file_path, "wb") as f:
        f.write(content)
    return file_path

def extract_text_from_pdf(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    extracted_text = ""
    for page in doc:
        extracted_text += page.get_text() # type: ignore
    return extracted_text

def cross_reference_data(extracted_text: str, data_df: pd.DataFrame) -> ReviewResult:
    discrepancies = {}
    missing_information = {}

    # Example cross-referencing logic (to be tailored to specific needs)
    for column in data_df.columns:
        if column not in extracted_text:
            missing_information[column] = "Not found in extracted text"
        else:
            for index, row in data_df.iterrows():
                if str(row[column]) not in extracted_text:
                    discrepancies[f"{column}_{index}"] = row[column]

    return ReviewResult(discrepancies=discrepancies, missing_information=missing_information)