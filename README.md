# Prowler Security Assessment API

This API provides an interface to run Prowler security assessments on AWS environments and generate compliance reports based on AWS Well-Architected Framework Security Pillar. It allows you to perform security checks and receive detailed findings through a REST API.

## Features

- Run Prowler security assessments on AWS environments
- Generate compliance reports mapped to AWS Well-Architected Framework Security Pillar
- Export findings in multiple formats (JSON, Text)
- Automated security checks for various AWS services
- Detailed remediation recommendations
- Severity-based findings classification

## Setup

### Prerequisites

- Python 3.8+
- AWS Account with appropriate permissions
- Prowler CLI installed

### Option 1: Running with Docker

You can either build the image locally or pull the pre-built image from a container registry.

#### Option A: Using Pre-built Image

1. Pull the image from Docker Hub:
```bash
docker pull ahmadjallab/ahmadjallab-prowler_aws:latest
```

Or pull from AWS ECR Public:
```bash
docker pull public.ecr.aws/b1s1h1d1/ahmadjallab/ahmadjallab-prowler_aws:latest
```

2. Run the container (using either image):
```bash
# Using Docker Hub image
docker run -p 8000:8000 --env-file .env ahmadjallab/ahmadjallab-prowler_aws:latest

# Or using AWS ECR image
docker run -p 8000:8000 --env-file .env public.ecr.aws/b1s1h1d1/ahmadjallab/ahmadjallab-prowler_aws:latest
```

#### Option B: Building Locally

1. Build the Docker image:
```bash
docker build -t prowler-api .
```

2. Run the container using either method:

With environment variables:
```bash
docker run -p 8000:8000 \
  -e AWS_ACCESS_KEY_ID=your_access_key \
  -e AWS_SECRET_ACCESS_KEY=your_secret_key \
  prowler-api
```

Or with .env file:
```bash
docker run -p 8000:8000 --env-file .env prowler-api
```

The API will be available at http://localhost:8000
  - When running the API using Docker, use `host="0.0.0.0"` in the `docker run` command to allow connections from outside the container.

### Option 2: Running Locally

1. Configure AWS credentials in `.env` file:
```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token  # Optional
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
uvicorn main:app --reload --port 8000
```

The API will be available at http://localhost:8000

## API Endpoints

### 1. Root Endpoint
- **GET /** 
  - Welcome message and API status
  - Response: `{"message": "Welcome to the Prowler Security Assessment API"}`

### 2. Run Security Checks
- **GET /run-prowler-generate-checks-report-fundings**
  - Runs Prowler security checks and generates findings report
  - Generates ASFF format JSON report
  - Returns findings with status

### 3. Export Compliance Report
- **GET /export-compliance-report**
  - Generates compliance report mapped to AWS Well-Architected Framework
  - Maps findings to Security Pillars (SEC01, SEC02, SEC03)
  - Returns formatted compliance report

## File Structure

```
plowerappdev/
├── main.py                 # FastAPI application and endpoints
├── endpointFunc.py        # Endpoint implementation functions
├── utils/
│   ├── ReportGenerationPipeline.py    # Report generation orchestration
│   ├── parseFindings_prowlerScan.py   # Prowler findings parser
│   └── scan_mapping_findings_func.py   # Security pillar mapping logic
├── compliance_filecheck/
│   └── RequirementIDs_for_corresponding_checks_pillar_sec01_sec03.json  # Mapping configuration
├── results/               # Generated reports directory
├── output/
│   └── compliance/       # Compliance reports output
└── .env                  # Environment configuration
```

## Response Formats

### Findings Report
```json
{
    "status": "success",
    "results": {
        "findings": [
            {
                "check_id": "ec2_instance_managed_by_ssm",
                "title": "Check Title",
                "severity": "MEDIUM",
                "status": "FAILED",
                "remediation_text": "Remediation steps..."
            }
        ]
    }
}
```

### Compliance Report
```json
{
    "status": "success",
    "results": {
        "SEC01": [...],  // Security Pillar 1 findings
        "SEC02": [...],  // Security Pillar 2 findings
        "SEC03": [...]   // Security Pillar 3 findings
    }
}
```

## Error Handling

The API handles various error scenarios:
- Invalid AWS credentials
- Prowler execution failures
- Missing report files
- Invalid configuration

Each error response includes:
- HTTP status code
- Error message
- Error details when available

## Documentation

- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc
- Prowler Documentation: https://docs.prowler.com/

## Running the Application

Start the server:
```bash
uvicorn main:app --reload --port 8000
```

Access the API at http://localhost:8000

## Supported Services

You can run checks for various AWS services including:
- s3
- ec2
- iam
- rds
- And many more!

## Error Handling

The API returns appropriate error messages when:
- AWS credentials are invalid
- Prowler execution fails
- Invalid service or check names are provided

https://docs.prowler.com/projects/prowler-open-source/en/latest/#__tabbed_2_8


[text](http://127.0.0.1:8000/docs/)

uvicorn main:app --reload --port 8000


The error indicates that the --compliance and --service flags cannot be used together in a single command. This is because Prowler treats these as mutually exclusive options:

--compliance: Runs checks based on a specific compliance framework.
--service: Runs checks for specific AWS services.

cmd 
prowler aws  --output-formats json-asff --output-filename prowler_scan --output-directory ./results     --compliance aws_well_architected_framework_security_pillar_aws --region us-east-1
 
 prowler aws  --output-formats json-asff --output-filename prowler_scan --output-directory ./results   --service  ec2  --region us-east-1  
prowler --output-formats json-asff --output-filename prowler_scan --output-directory ./results --region us-east-1

prowler --compliance aws_well_architected_framework_security_pillar_aws

prowler --list-compliance
- aws_account_security_onboarding_aws
- aws_audit_manager_control_tower_guardrails_aws
- aws_foundational_security_best_practices_aws
- aws_foundational_technical_review_aws
- aws_well_architected_framework_reliability_pillar_aws
- aws_well_architected_framework_security_pillar_aws
- cis_1.4_aws
- cis_1.5_aws
- cis_2.0_aws
- cis_3.0_aws
- cisa_aws
- ens_rd2022_aws
- fedramp_low_revision_4_aws
- fedramp_moderate_revision_4_aws
- ffiec_aws
- gdpr_aws
- gxp_21_cfr_part_11_aws
- gxp_eu_annex_11_aws
- hipaa_aws
- iso27001_2013_aws
- kisa_isms_p_2023_aws
- kisa_isms_p_2023_korean_aws
- mitre_attack_aws
- nist_800_171_revision_2_aws
- nist_800_53_revision_4_aws
- nist_800_53_revision_5_aws
- nist_csf_1.1_aws
- pci_3.2.1_aws
- rbi_cyber_security_framework_aws
- soc2_aws

### Install Docker on ec2 instance depenting on your distrobution 
- sudo bash 
- sudo yum update -y 
- root@ip-10-0-5-157:/home/ubuntu# yum update -y 
- root@ip-10-0-5-157:/home/ubuntu# apt-get update -y 
- root@ip-10-0-5-157:/home/ubuntu# apt update -y
- sudo yum update -y

- sudo yum -y install docker
 
- sudo service docker start
- sudo  docker run -p 8000:8000     ahmadjallab/ahmadjallab-prowler_aws:v2

- sudo yum install    nginx
- sudo yum install  -y  python3-pip
- sudo vim /etc/nginx/sites-enabled/fastapi_nginx

server {
        listen 80;
        server_name 3.83.14.33 ;
        location / {
                proxy_pass http//172.17.0.1:8000;
        }
}
:wq  -> save command
:qa! -> quit command
-http//172.17.0.1:8000; access to from you in local machine as  (nginx) proxy pass to the container (fastapi) http://0.0.0.0:8000;