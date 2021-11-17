import shutil
import easyocr
from fastapi import FastAPI, File, UploadFile
from utils.decorators import timer_func
from spellchecker import SpellChecker
import requests
import json
import configparser
from pydantic import BaseModel
from typing import Optional

config = configparser.ConfigParser()
config.read('settings.env')
token = config.get('access-token', 'tempToken')

app = FastAPI()
reader = easyocr.Reader(['en'])
spell = SpellChecker('en')
CONFIDENCE_THRESHOLD = 80

class Card(BaseModel):
    projectId: int
    boardId: int
    title: str
    description: Optional[str] = None


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
    ''' This handle returns the list of boards and their id and project id to which they belong'''
    return {"boards": [getBoards()]}

@app.post("/post-ppCard")
def post_projectPlace_card(card: Card):
    ''' This handle takes a projectId, boardId and card title and description for new card and posts a projectPlace card'''
    response  = postCard(card.projectId, card.boardId, card.title, card.description)
    return response


@timer_func
def imageToText(image):
    import re
    result = reader.readtext(image, paragraph=False, decoder="wordbeamsearch", batch_size=3)
    text = ''
    for detection in result:
        word = detection[1]
        word = re.sub(' +', ' ', word)
        # If confidence level is lesser than 80% run spell check on the word
        if detection[2] * 100 < CONFIDENCE_THRESHOLD:
            word = " ".join([spell.correction(token) for token in word.split(" ")])

        text = text +" "+ word
    text = text.strip()
    return text


def getBoards():
    session = requests.Session()
    session.headers.update({'Authorization': f"Bearer {token}"})
    response = session.get('https://service.projectplace.com/api/v1/user/me/boards')
    boardList = []

    #creates list of board and board-Id
    for boards in response.json():
        boardList.append((boards.get('name'), f"boardId = {boards.get('id')}", f"projectId = {boards.get('project_id')}"))

    return boardList 
    # sample output::: [('Generac Pursuit', 'boardId = 1094435', 'projectId = 1127607142'), ('board3', 'boardId = 1308404', 'projectId = 1109821908')]


def postCard(projectId, boardId, title, description):
    header = {"content-type": "application/json"}
    session = requests.Session()
    session.headers.update({'Authorization': f"Bearer {token}"})
    #creates new card with title
    payload = {'board_id':boardId ,'column_id': 0, 'title': title}
    responsePostCard = session.post(f'https://service.projectplace.com/api/v1/projects/{projectId}/cards/create-new' , data=json.dumps(payload), headers=header)
    cardId = responsePostCard.json().get('id')

    #updates description of card
    responseUpdate = session.put(f'https://service.projectplace.com/api/v1/cards/{cardId}' , data=json.dumps({'description' : description}), headers=header)
    return responseUpdate.json()

