from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from dotenv import load_dotenv
from endpointFunc import run_prowler_check ,export_prowler_file_report
# Load environment variables Using Temporary Credentials
#If you’re using AWS Identity and Access Management (IAM) roles or temporary security credentials, you’ll need to include:
load_dotenv()

#PORT = int(os.environ.get("PORT", 8000))



app = FastAPI(
    title="Prowler Security Assessment API",
    description="API for running Prowler security assessments on AWS",
    version="1.0.0"
)

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

@app.get("/")
async def root():
    return {"message": "Welcome to the Prowler Security Assessment API"}

# prowler aws  --output-formats json-asff --output-filename prowler_scan --output-directory ./results     --compliance aws_well_architected_framework_security_pillar_aws --region us-east-1
@app.get("/api/run-prowler-generate-checks-report-fundings", response_model=ProwlerResponse)
async def run_prowler_check01_fundings():#param from Expects request body data  
    run_prowler_check()
    return export_prowler_file_report('findings')



        
@app.get("/api/export-compliance-report")
async def export_prowler_file_report_compliance():
    run_prowler_check()
    return export_prowler_file_report('compliance')


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)