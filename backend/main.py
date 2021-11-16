from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, File, UploadFile
import shutil
import easyocr

app = FastAPI()

class Image(BaseModel):
    title: str

@app.get("/")
def read_root():
    return {"Key": "Something Interesting is cooking !"}

@app.post("/image-to-text")
def image_to_text(file: UploadFile = File(...)):
    ''' This handle takes the image in binary and then extracts the text out of it '''
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    text = imageToText(file_location)

    return {"extracted_text": text}

@app.get("/get-boards/{workspace-id}")
def get_boards(workspace_id: int):
    ''' This handle takes workspace id and returns the list of boards'''
    return {"boards": []}


def imageToText(image):
    reader = easyocr.Reader(['en']) 
    result = reader.readtext(image)
    text = ''
    for detection in result: 
        text = text +" "+ detection[1]
    return text


