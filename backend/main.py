from typing import Optional
from pydantic import BaseModel

from fastapi import FastAPI

app = FastAPI()

class Image(BaseModel):
    title: str

@app.get("/")
def read_root():
    return {"Key": "Something Interesting is cooking !"}

@app.post("/image-to-text")
def image_to_text(image: Image):
    ''' This handle takes the image in binary and then extracts the text out of it '''
    return {"extracted_text": "An extracted text from the image", "title": f"{image.title}"}

@app.get("/get-boards/{workspace-id}")
def get_boards(workspace_id: int):
    ''' This handle takes workspace id and returns the list of boards'''
    return {"boards": []}

