from fileinput import filename
from http.client import HTTPException
from io import BytesIO
import os
import shutil
from urllib import request
from urllib.request import urlopen
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from convert import convert

app = FastAPI()

templates = Jinja2Templates(directory="html")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        file_name = file.filename[:-4]
        new_excel = convert(file.filename)
    except:
        raise HTTPException(status_code=400, detail=f"O arquivo {file.filename} não é PDF")
    os.remove(file.filename)
    # new_excel_buffer = BytesIO(new_excel.tobytes())

    headers = {
        'Content-Disposition': f'attachment; filename={file_name}.xlsx'
    }
    return StreamingResponse(new_excel, headers=headers, media_type="application/xlsx")