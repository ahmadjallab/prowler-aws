from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from endpointFunc import run_prowler_check ,export_prowler_file_report,LLM_gemini_summery_LLM_compliance_report
# Load environment variables Using Temporary Credentials
#If you’re using AWS Identity and Access Management (IAM) roles or temporary security credentials, you’ll need to include:
load_dotenv()

#PORT = int(os.environ.get("PORT", 8000))



app = FastAPI(
    title="Prowler Security Assessment API",
    description="API for running Prowler security assessments on AWS",
    version="1.0.0"
)

# Mount the static directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize templates
templates = Jinja2Templates(directory="templates")

# Store the report content globally (you might want to use a proper caching solution in production)
report_content = {"content": ""}

# Sample data model


class ProwlerCheck(BaseModel):
    service: str
    output_file: str
    region: Optional[str] = None
    checks: Optional[List[str]] = None

class ProwlerResponse(BaseModel):
    status: str
    results: Optional[dict] = None
    error: Optional[str] = None

#class response_model that return file if exists else return error
class ProwlerFileResponse(BaseModel):
    status: str
    results: Optional[dict] = None  # Will contain the file content
    error: Optional[str] = None
    file_path: Optional[str] = None
    file_type: Optional[str] = None

# In-memory storage
items = []

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# prowler aws  --output-formats json-asff --output-filename prowler_scan --output-directory ./results     --compliance aws_well_architected_framework_security_pillar_aws --region us-east-1
@app.get("/api/run-prowler-generate-checks-report-fundings", response_model=ProwlerResponse)
async def run_prowler_check01_fundings():#param from Expects request body data  
    run_prowler_check()
    return export_prowler_file_report('findings')



        
@app.get("/api/export-compliance-report")
async def export_prowler_file_report_compliance():
    run_prowler_check()
    return export_prowler_file_report('compliance')


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)


@app.get("/report/compliance", response_class=HTMLResponse)
async def show_compliance_report(request: Request):
    return templates.TemplateResponse(
        "compliance_report.html",
        {"request": request, "content": report_content["content"]}
    )

@app.get("/api/LLM_gemini_summery_compliance_report")
async def LLM_gemini_summery_compliance_report():
    # Get the markdown content from the LLM
    report_content["content"] = LLM_gemini_summery_LLM_compliance_report()
    
    # Return JSON response with the content
    return JSONResponse({
        "status": "success",
        "content": report_content["content"]
    })


@app.get("/docs_page", response_class=HTMLResponse)
async def show_docs(request: Request):
    return FileResponse("static/docs.html", media_type="text/html")