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


@app.post("/getDataSources", response_class=JSONResponse)
async def get_data_sources(request: Request):

        data = await request.json()

        print(data)

        data_sources = {
            "data_sources" : [
                { "value": "db1", "label": "Database 1" },
                { "value": "db2", "label": "Database 2" },
                { "value": "file1", "label": "CSV File 1" },
                { "value": "file2", "label": "Excel File 2" }
            ]
        }

        return JSONResponse(content=data_sources)



@app.post("/getDataSourceColumnsList", response_class=JSONResponse)
async def get_datasource_columns_list(request: Request):
    try:

        data = await request.json()

        data_source_one = data['DataSourceOne']
        data_source_two = data['DataSourceTwo']

        data_collection = {
            'db1': [
                "Company",
                "Account",
                "AU",
                "Currency",
                "As Of Date",
                "GL. Balance",
                "IHub Balance"
            ],
            'db2': [
                "Account",
                "Secondary Account",
                "Primary Account",
                "As Of Date"
            ],
            'file1': [
                "Company",
                "Account",
                "AU",
                "Currency",
                "As Of Date",
                "GL. Balance",
                "IHub Balance"
            ],
            'file2': [
                "Account",
                "Secondary Account",
                "Primary Account",
                "As Of Date"
            ]
        }

        dso_columns = data_collection.get(data_source_one)
        dst_columns = data_collection.get(data_source_two)

        all_columns = list(set(dso_columns + dst_columns))

        json_data = []

        for idx, value in enumerate(all_columns):
            json_data.append(
                {
                    'value': f"{idx}",
                    'label': f"{value}"
                }
            )

        response_content = {
            'COLUMNS': json_data
        }

        return JSONResponse(content=response_content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))