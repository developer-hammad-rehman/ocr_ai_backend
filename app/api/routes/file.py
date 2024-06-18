import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import pandas as pd
import fitz  # PyMuPDF
from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse
from jose import JWTError
from app.api.deps import OAUTHDEP
from app.core.file import upload_file  # type: ignore
from app.core.openai import client, wait_on_run
from app.core.token import decode_token
import PyPDF2

file_router = APIRouter(tags=["AI Routes"])


@file_router.post("/upload/")
async def upload_file_route(file: UploadFile):
    reader = PyPDF2.PdfReader(file.file)
    text_content = ""
    for page in reader.pages:
        text_content = text_content + page.extract_text()
    return text_content.replace(".", "")


@file_router.post("/get-report")
async def get_report(file: UploadFile, token: OAUTHDEP):
    try:
        token = decode_token(token)  # type: ignore
        if not file:
            raise HTTPException(status_code=404, detail="File is requried")
        else:
            encoded_content = await file.read()
            file_path = upload_file(filename=file.filename, content=encoded_content)  # type: ignore
            vector_store = client.beta.vector_stores.create(name="Ocr store")
            file_paths = [file_path]
            file_streams = [open(path, "rb") for path in file_paths]
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                files=file_streams, vector_store_id=vector_store.id
            )
            assistant = client.beta.assistants.create(
                name="Ocr AI",
                model="gpt-3.5-turbo-1106",
                instructions="You have to act like spread sheet content generater . Generate the spread sheet content using the given pdf document ",
                tools=[{"type": "file_search"}],
                tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
            )
            thread = client.beta.threads.create(
                messages=[
                    {
                        "role": "user",
                        "content": "Generate Spread sheet content",
                    }
                ],
            )
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant.id,
            )
            wait_on_run(run, thread)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            for msg in reversed(messages.data):
                print(msg.content[0].text.value)  # type: ignore
        return msg.content[0].text.value  # type: ignore
    except JWTError as je:
        raise HTTPException(status_code=404, detail=str(je))




class ReviewResult(BaseModel):
    discrepancies: dict
    missing_information: dict

@file_router.post("/upload-review")
async def upload_documents(pdf: UploadFile = File(...), data_file: UploadFile = File(...)):
    if not pdf.filename.endswith(".pdf") or not data_file.filename.endswith(".csv"): # type: ignore
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

    # Clean up temporary files

    return review_result

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
    report_encode = json.dumps(ReviewResult(discrepancies=discrepancies, missing_information=missing_information).model_dump())
    open_ai_report = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            {"role":"system" , "content":"You are the report generater ai . Genrate me the detail report in simple word"},
            {"role":"user" , "content":f"Generate me the report using {report_encode}"}
        ],
    )
    return open_ai_report.choices[0].message.content # type: ignore