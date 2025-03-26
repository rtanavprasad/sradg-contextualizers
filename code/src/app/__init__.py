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

from src.backend.Interface import Interface


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


@app.post("/RunReconcile", response_class=JSONResponse)
async def run_data_reconciliation(request: Request):
        INF = Interface()

        data = await request.json()

        print(data)

        # data = {
        #     "summary" : {
        #         "success": "1,245",
        #         "PotentialIssue": "42",
        #         "CriticalIssue": "18"
        #     },
        #     "Details": {
        #         "AIInsights": [
        #             "Based on historical data and current anomalies, the AI suggests:",
        #             "",
        #             "1. Implement a 15-minute delay in reconciliation for new transactions to account for processing time.",
        #             "2. Create an exception rule for status changes that occur between 2-3 AM during maintenance windows.",
        #             "3. 82% of currency mismatches involve EUR-USD pairs - consider adding automatic conversion verification."
        #         ],
        #         "AnomaliesDetectedTable": '<table> <thead> <tr> <th>ID</th> <th>Key Value</th> <th>Source 1 Value</th> <th>Source 2 Value</th> <th>Anomaly Type</th> <th>AI Comment</th> <th>Actions</th> </tr> </thead> <tbody> <tr> <td>#1001</td> <td>TXN-2023-0456</td> <td>$1,250.00</td> <td>$1,200.00</td> <td><span class="anomaly-type type-mismatch">Value Mismatch</span></td> <td>Amount difference detected. Possible fee deduction in source 2.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> <tr> <td>#1002</td> <td>CUST-78945</td> <td>Active</td> <td>Inactive</td> <td><span class="anomaly-type type-mismatch">Status Mismatch</span></td> <td>Customer status differs between systems. Check update timing.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> <tr> <td>#1003</td> <td>ORD-45612</td> <td>5 items</td> <td>Missing</td> <td><span class="anomaly-type missing-data">Missing Data</span></td> <td>Order not found in source 2. Possible synchronization delay.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> <tr> <td>#1004</td> <td>TXN-2023-0789</td> <td>USD</td> <td>EUR</td> <td><span class="anomaly-type type-mismatch">Currency Mismatch</span></td> <td>Different currencies detected. Check FX conversion process.</td> <td> <button class="btn btn-outline" style="padding: 4px 8px; font-size: 12px;"> <i class="fas fa-comment"></i> Feedback </button> </td> </tr> </tbody> </table>',
        #         "AITrendAnalysisSummary": "The anomalies show a weekly pattern with peaks on Mondays. 68% of value mismatches occur within 2 hours of system synchronization. Missing data anomalies have decreased by 24% since last month's process improvements."
        #     }
        # }

        data = INF.analyze()

        return JSONResponse(content=data)