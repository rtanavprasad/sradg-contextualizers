import os
import sys
from fastapi import FastAPI, Request, Form, HTTPException, Response
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

PROJECT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.abspath(
    os.path.join(
        PROJECT_DIR,
        os.pardir,
        os.pardir
    )
)

sys.path.append(ROOT_DIR)

static_path = os.path.join(PROJECT_DIR, 'static')
template_path = os.path.join(PROJECT_DIR, 'templates')

app = FastAPI()

# ADD STATICS PATH
app.mount("/static", StaticFiles(directory=static_path), name="static")

# ADD TEMPLATES PATH
templates = Jinja2Templates(directory=template_path)


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
async def index(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

