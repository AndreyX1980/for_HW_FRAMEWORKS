import logging
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")
user_list = []

class User(BaseModel):
    userid: int
    name: str
    email: Optional[str] = None
    password: str

@app.get("/")
async def start():
    logger.info('Начальная страница')
    return {"Добро пожаловать в FastAPI": True}

@app.post("/user/")
async def create_user(user: User):
    logger.info('Отработан запрос POST.')
    user_list.append(user)
    logger.info(user_list)
    return user

@app.put("/user/{user_id}")
async def update_item(user_id: int, new_user: User):
    logger.info(f'Отработан запрос PUT для userid = {user_id}.')
    for i in user_list:
        if i.userid == user_id:
            i.name = new_user.name
            i.email = new_user.email
            i.password = new_user.password
    logger.info(user_list)
    return {"user_id": user_id, "user": new_user}

@app.delete("/user/{user_id}")
async def delete_item(user_id: int):
    for i in user_list:
        if i.user_id == user_id:
            user_list.remove(i)
    logger.info(user_list)
    return {"userid": user_id}

@app.get("/userlist", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("user.html", {"request": request, "user": user_list})