import shutil
from urllib import request
from urllib.request import urlopen
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="html")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/")
async def upload_file(file: UploadFile = File(...)):
    with open(file.filename, 'wb') as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}