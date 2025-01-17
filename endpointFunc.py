import subprocess
import os
from pydantic import BaseModel
from utils.ReportGenerationPipeline import generate_compliance_report_pipeline
from fastapi.responses import FileResponse, JSONResponse
class ProwlerResponse(BaseModel):
    status: str
    results: dict = None
    error: dict = None

def run_prowler_check():#param from Expects request body data  
    try:

   
        
        cmd = ["prowler", "aws","--output-formats",  "json-asff" ,"--output-filename", "prowler_scan","--output-directory", "./results","--service","ec2",  "--region", "us-east-1"]# "--compliance", "aws_well_architected_framework_security_pillar_aws",
        # If the file already exists, the report has been generated before.
        # Delete the existing file to avoid affecting the report generation pipeline.
        #to not make duplicate report in SAME JSON FILE 
        if os.path.exists("./results/prowler_scan.asff.json"):
            os.remove("./results/prowler_scan.asff.json")
        try:
            #chack for throw error if command fails 
            # capture_output=True to capture command output
            # text=True to convert output binary to string
            result = subprocess.run(
            cmd,
            #check=True,
            #capture_output=True,
            #text=True
            )
     
            if result.returncode == 0:
                 print("Command executed successfully!")
                 print(result.stdout)  # Display command output
            else:
                 print("Error:", result.stderr)
        except subprocess.CalledProcessError as e:
            return ProwlerResponse(
            status="error",
             error=f"Prowler cmd execution failed: {str(e)}"
        )

        #check file exists
        if os.path.exists("./results/prowler_scan.asff.json"):
            return ProwlerResponse(
                status="success",
                results={
                    "report": "./results/prowler_scan.asff.json"}
            ) 

        else:
            return ProwlerResponse(
                status="error",
                error={"Error running Prowler for generating report":"file not generated"}
            )
            
    except Exception as e:
        return ProwlerResponse(
            status="error",
            error=f"Error running Prowler: {str(e)}"
        )



def export_prowler_file_report(file_type):
    '''Export Prowler file report
    
    Args:
        file_type (str): The type of report to export. Can be 'compliance' or 'findings'. Default is 'compliance'.

    Returns:
        FileResponse: A file response containing the exported report.
    '''
    file_name_compliance = "compliance_report.txt"
    file_name_findings = "finding_report.txt"
    strReport = generate_compliance_report_pipeline()
    try: 
        if file_type == 'compliance':
            file_path = f"output/compliance/{file_name_compliance}"
            filename = file_name_compliance
        elif file_type == 'findings':
            file_path = f"output/compliance/{file_name_findings}"
            filename = file_name_findings
        if os.path.exists(file_path):
            return FileResponse(
                path=file_path,
                media_type="text/plain",
                filename=filename,
                headers={
                    "Content-Disposition": f"attachment; filename={filename}"
                }
            )
        else:
            return JSONResponse(
                status_code=404,
                content={
                    "status": "error",
                    "error": "Report file not found. Please run the security check first."
                }
            )
            
    except Exception as e:
        return JSONResponse (
            status_code=500,
            content={
                "status": "error",
                "error": f"Error retrieving report: {str(e)}"
            }
        )