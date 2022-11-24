"""Main of todo app
"""
import math

from loguru import logger

from fastapi import FastAPI, Request, Depends, Form, status, HTTPException, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from database import init_db, get_db, Session
import models

init_db()

# pylint: disable=invalid-name
templates = Jinja2Templates(directory="templates")

app = FastAPI()

logger = logger.opt(colors=True)
# pylint: enable=invalid-name

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def home(request: Request, database: Session = Depends(get_db), page: int = Query(default=0)):
    """Main page with todo list
    """
    logger.info("In home")
    skip = page * 10
    todos = database.query(models.Todo).order_by(models.Todo.id.desc()).offset(skip).limit(10)
    pages = math.ceil(database.query(models.Todo).count()/10)
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos, "pages": pages, "skip": skip, "page": page})


@app.post("/add")
async def todo_add(request: Request, title: str = Form(default=None, max_length=500),
                   database: Session = Depends(get_db)):
    """Add new todo
    """
    if title is None or len(title.replace(' ', '')) == 0:
        raise HTTPException(status_code=404, detail="Empty request")
    todo = models.Todo(title=title, details="Your coolest details")
    logger.info(f"Creating todo: {todo}")
    database.add(todo)
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/edit/{todo_id}")
async def todo_get(request: Request, todo_id: int, database: Session = Depends(get_db)):
    """Get todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Getting todo: {todo}")
    logger.info(f"{todo.tag}")
    return templates.TemplateResponse("edit.html", {"request": request, "todo": todo, "tags": models.Tag})


@app.post("/edit/{todo_id}")
async def todo_edit(
        request: Request,
        todo_id: int,
        title: str = Form(max_length=500),
        details: str = Form(max_length=500),
        tag:str = Form(None),
        completed: bool = Form(False),
        database: Session = Depends(get_db)):
    """Edit todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Editting todo: {todo}")
    todo.title = title
    todo.details = details
    todo.completed = completed
    todo.tag = tag
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.post("/complete/{todo_id}")
async def todo_complete(
        request: Request,
        todo_id: int,
        database: Session = Depends(get_db)):
    """Complete todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Complited todo: {todo}")
    todo.completed = True
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.post("/uncomplete/{todo_id}")
async def todo_uncomplete(
        request: Request,
        todo_id: int,
        database: Session = Depends(get_db)):
    """Complete todo
    """
    todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
    logger.info(f"Complited todo: {todo}")
    todo.completed = False
    database.commit()
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)


@app.get("/delete/{todo_id}")
async def todo_delete(request: Request, todo_id: int, database: Session = Depends(get_db)):
    """Delete todo
    """
    try:
        todo = database.query(models.Todo).filter(models.Todo.id == todo_id).first()
        logger.info(f"Deleting todo: {todo}")
        database.delete(todo)
        database.commit()
    except:
        raise HTTPException(status_code=404, detail="This todo doesn't exist")
    return RedirectResponse(url=app.url_path_for("home"), status_code=status.HTTP_303_SEE_OTHER)
