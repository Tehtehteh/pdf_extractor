from typing import List

from dateutil import parser
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from api.processor.reader import PDFProcessor
from api.processor.date_extractor import DateExtractor
from api.models import ExtractedDateModel
from api.settings import settings
from db.engine import database, create_meta
from db.models import pdfs, pdf_extracted_dates


app = FastAPI()


app.mount("/static", StaticFiles(directory="api/static"), name="static")


@app.on_event("startup")
async def startup():
    create_meta()
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/_healthz")
def read_root():
    return {"alive": True}


@app.get("/")
def index():
    return FileResponse('api/templates/index.html')


@app.get('/files/{file_id}')
async def get_file(file_id: int):
    pdf_file = pdfs.select().where(pdfs.c.id == file_id)
    result = await database.fetch_one(pdf_file)
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return FileResponse(result[1])


@app.get('/files/{file_id}/extracted', response_model=List[ExtractedDateModel])
async def get_file(file_id: int):
    query = pdfs.select().where(pdfs.c.id == file_id)
    pdf_file = await database.fetch_one(query)
    if not pdf_file:
        raise HTTPException(status_code=404, detail="Item not found")
    query = pdf_extracted_dates.select().where(pdf_extracted_dates.c.pdf_id == file_id)
    result = await database.fetch_all(query)
    return result


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    contents = await file.read()
    file_uri = settings.storage.save(contents, file.filename)
    query = pdfs.insert().values(uri=file_uri)
    last_inserted_id = await database.execute(query)
    processor = PDFProcessor(file_uri)
    extractor = DateExtractor()
    dates = processor.run_extractor(extractor)
    if dates:
        values = [{'pdf_id': last_inserted_id, 'extracted_date': parser.parse(date.extracted_data),
                   'extracted_context': date.ctx} for date in dates]
        await database.execute(query, )
        return {'id': last_inserted_id, 'extracted_data': values}
