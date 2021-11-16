import shutil
import easyocr
from fastapi import FastAPI, File, UploadFile
from utils.decorators import timer_func
from spellchecker import SpellChecker
import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('settings.env')
token = config.get('access-token', 'tempToken')

app = FastAPI()
reader = easyocr.Reader(['en'])
spell = SpellChecker('en')
CONFIDENCE_THRESHOLD = 80

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

@app.get("/get-boards")
def get_boards():
    ''' This handle takes workspace id and returns the list of boards'''
    return {"boards": [getBoards()]}


@timer_func
def imageToText(image):
    result = reader.readtext(image, paragraph=False, decoder="wordbeamsearch")
    print(result)
    text = ''
    for detection in result:
        word = detection[1]
        # If confidence level is lesser than 80% run spell check on the word
        if detection[2] * 100 < CONFIDENCE_THRESHOLD:
            word = spell.correction(word)

        text = text +" "+ word
    text = text.strip()
    return text


def getBoards():
    session = requests.Session()
    session.headers.update({'Authorization': f"Bearer {token}"})
    response = session.get('https://service.projectplace.com/api/v1/user/me/boards')
    boardList = []

    for boards in response.json():
        boardList.append((boards.get('name'), boards.get('id')))  #creates list of board and board-Id

    return boardList # sample output::: [["Generac Pursuit",1094435],["board3",1308404],["new board",1308397]]
