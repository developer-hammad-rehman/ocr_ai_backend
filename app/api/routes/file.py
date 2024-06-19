import json
from fastapi import UploadFile , HTTPException
from jose import  JWTError
import pandas as pd
from fastapi import APIRouter, HTTPException, UploadFile
from app.api.deps import OAUTHDEP
from app.core.file import cross_reference_data, extract_text_from_pdf, upload_file  # type: ignore
from app.core.openai import client
from app.core.token import decode_token
import PyPDF2

# =============================================================================================================================#

file_router = APIRouter(tags=["AI Routes"])

# ============================================================================================================================#


@file_router.post("/upload/")
async def upload_file_route(file: UploadFile , token:OAUTHDEP):
    reader = PyPDF2.PdfReader(file.file)
    text_content = ""
    for page in reader.pages:
        text_content = text_content + page.extract_text()
    return text_content.replace(".", "")


# ==========================================================================================================================#


@file_router.post("/upload-review")
async def upload_documents(pdf: UploadFile, data_file: UploadFile , token:OAUTHDEP):
 try:
    token = decode_token(token=token) # type: ignore
    if not pdf.filename.endswith(".pdf") or not data_file.filename.endswith(".csv"):  # type: ignore
        raise HTTPException(status_code=400, detail="Invalid file format")
    # Save the uploaded files
    pdf_path = f"./uploads/{pdf.filename}"
    data_file_path = f"./uploads/{data_file.filename}"
    with open(pdf_path, "wb") as f:
        f.write(await pdf.read())
    with open(data_file_path, "wb") as f:
        f.write(await data_file.read())

    # Process the PDF to extract text
    extracted_text = extract_text_from_pdf(pdf_path)

    # Process the CSV data file
    data_df = pd.read_csv(data_file_path)

    # Cross-reference extracted text with the CSV data
    review_result = cross_reference_data(extracted_text, data_df)

    report_encode = json.dumps(review_result.model_dump())
    open_ai_report = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {
                "role": "system",
                "content": "You are the report generater ai . Genrate me the detail report in simple word",
            },
            {
                "role": "user",
                "content": f"Generate me the report using {report_encode}",
            },
        ],
    )
    return open_ai_report.choices[0].message.content  # type: ignore
 except JWTError as je:
    raise HTTPException(status_code=401, detail=str(je))
 except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))


# ===================================================================================================================================#
