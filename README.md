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

#### Python Environment Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/prowler-api.git
cd prowler-api
```

2. Create and activate virtual environment:

For Windows:
```bash
python -m venv venv
.\venv\Scripts\activate
```

For Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure AWS credentials in `.env` file:
```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_SESSION_TOKEN=your_session_token  # Optional
```

5. Run the application:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at http://localhost:8000

## Accessing the API

### Option 1: Public EC2 Instance

The API is publicly accessible at:
```
http://ec2-44-202-156-36.compute-1.amazonaws.com
```

#### API Endpoints
- Documentation: `http://ec2-44-202-156-36.compute-1.amazonaws.com/docs`
- Security Checks: `http://ec2-44-202-156-36.compute-1.amazonaws.com/api/run-prowler-generate-checks-report-fundings`
- Compliance Report: `http://ec2-44-202-156-36.compute-1.amazonaws.com/api/export-compliance-report`

#### Infrastructure Setup

1. EC2 Configuration:
   - Amazon Linux 2/Ubuntu instance
   - Security Group: 
     - Inbound: HTTP (80), HTTPS (443)
     - Outbound: All traffic

2. Install Dependencies:
```bash
# Update system packages
sudo yum update -y   # For Amazon Linux
# OR
sudo apt update -y   # For Ubuntu

# Install Docker
sudo yum install -y docker   # For Amazon Linux
# OR
sudo apt install -y docker.io   # For Ubuntu

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Install Nginx
sudo yum install -y nginx   # For Amazon Linux
# OR
sudo apt install -y nginx   # For Ubuntu
```

3. Run Docker Container:
```bash
# Pull and run the container
sudo docker run -d \
  -p 8000:8000 \
  --name prowler-api \
  --restart unless-stopped \
  --env-file .env \
  ahmadjallab/ahmadjallab-prowler_aws:latest
```

4. Configure Nginx:
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-enabled/default   # For Ubuntu
# OR
sudo nano /etc/nginx/nginx.conf     # For Amazon Linux
```

Add this configuration:
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name ec2-44-202-156-36.compute-1.amazonaws.com;

    location / {
        proxy_pass http://localhost:8000;
       
    }
}
```

5. Start Nginx:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

6. Verify Setup:
```bash
# Check Docker container
sudo docker ps
sudo docker logs prowler-api

# Check Nginx status
sudo systemctl status nginx

# Test API
curl http://localhost:8000
curl http://ec2-44-202-156-36.compute-1.amazonaws.com
```

#### Troubleshooting

1. If Nginx fails to start:
```bash
sudo nginx -t                    # Test configuration
sudo journalctl -u nginx        # Check logs
```

2. If Docker container fails:
```bash
sudo docker logs prowler-api    # Check container logs
sudo docker restart prowler-api # Restart container
```

3. Common Issues:
   - Port 80 already in use: Check and stop conflicting services
   - Permission denied: Ensure proper file permissions
   - Connection refused: Check security group settings

## Accessing the API

### Option 2: Private Access via AWS Client VPN

Access the API securely through AWS Client VPN when the EC2 instance is in a private subnet:
```
http://10.0.132.64:80
```

#### Prerequisites
- AWS VPN Client (Desktop application)
- Client configuration file (Contact administrator for the file)
- Valid certificates (Generated using Easy-RSA)

#### VPC and VPN Setup

1. VPC Configuration:
   - Private subnet: 10.0.128.0/20
   - VPN CIDR range: 192.168.0.0/22
   

2. Install AWS VPN Client:
   - Download from [AWS VPN Client](https://aws.amazon.com/vpn/client-vpn-download/)
   - Available for Windows, macOS, and Linux

3. Configure VPN Connection:
   - Import the provided client configuration file
   - Certificate authentication using Easy-RSA generated certificates
   - Configuration file contains:
     - VPN endpoint
     - Certificate information
     - Routing configuration

4. Connect to VPN:
   ```bash
   # 1. Open AWS VPN Client
   # 2. Import configuration file
   # 3. Click Connect
   # 4. Verify connection status
   ```

5. Access the API:
   - After VPN connection is established:
   ```
   http://10.0.132.64:80/           # API root
   http://10.0.132.64:80/docs       # API documentation
   ```

#### Security Benefits
- Private subnet isolation
- Certificate-based authentication
- Encrypted traffic
- Access control through security groups
- VPN session monitoring

#### Troubleshooting VPN Connection

1. Certificate Issues:
```bash
# Check certificate validity
openssl verify -CAfile ca.crt client.crt
```

2. Connection Problems:
- Verify VPN endpoint is reachable
- Check security group allows VPN traffic
- Ensure route tables are properly configured

3. Common VPN Client Errors:
   - Certificate validation failed
   - Unable to reach VPN endpoint
   - Authentication timeout
   - Route conflicts

#### Request Access

To request VPN access:
1. Contact administrator for:
   - Client configuration file
   - Client certificate
   - Connection instructions
2. Provide your:
   - IP address range
   - Purpose of access
   - Duration needed

Note: The VPN client configuration file and certificates are sensitive security materials. They will be provided through secure channels upon request.

## API Endpoints

### Root Endpoint
- **GET /** 
  - Landing page with API documentation
  - Response: HTML page with API overview and documentation link

### Security Assessment
- **GET /api/run-prowler-generate-checks-report-fundings**
  - Runs Prowler security checks and generates findings report
  - Response Format:
    ```json
    {
        "status": "success",
        "results": {
            "findings": [
                {
                    "check_id": "string",
                    "title": "string",
                    "severity": "string",
                    "status": "string",
                    "remediation_text": "string"
                }
            ]
        }
    }
    ```

### Compliance Report
- **GET /api/export-compliance-report**
  - Generates compliance report mapped to AWS Well-Architected Framework
  - Response Format:
    ```json
    {
        "status": "success",
        "results": {
            "SEC01": [],
            "SEC02": [],
            "SEC03": []
        }
    }
    ```

## Project Structure
```
plowerappdev/
├── .github/
│   └── workflows/
│       └── docker-publish.yml    # GitHub Actions workflow
├── static/
│   └── index.html               # Landing page
├── utils/
│   ├── ReportGenerationPipeline.py    # Report generation logic
│   ├── parseFindings_prowlerScan.py   # Findings parser
│   └── scan_mapping_findings_func.py   # Security mapping
├── compliance_filecheck/
│   └── RequirementIDs_for_corresponding_checks_pillar_sec01_sec03.json
├── results/                     # Generated reports
│   └── prowler_scan.asff.json
├── output/
│   └── compliance/             # Compliance reports
├── .dockerignore               # Docker ignore rules
├── .env                        # Environment variables
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker build instructions
├── LICENSE                    # Project license
├── README.md                  # Project documentation
├── endpointFunc.py           # API endpoint functions
├── main.py                   # FastAPI application
└── requirements.txt          # Python dependencies
```

### Key Components

1. **API Layer** (`main.py`, `endpointFunc.py`)
   - FastAPI application setup
   - API endpoint definitions
   - Request/response handling

2. **Security Assessment** (`utils/`)
   - Prowler integration
   - Findings parsing
   - Report generation

3. **Compliance Mapping** (`compliance_filecheck/`)
   - Security pillar mappings
   - Compliance requirements

4. **Infrastructure** (`Dockerfile`, `docker-publish.yml`)
   - Container configuration
   - CI/CD pipeline
   - Deployment automation

5. **Documentation** (`static/`, `README.md`)
   - API documentation
   - Setup instructions
   - Usage guides

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
- sudo  docker run -p 8000:8000  --env-file .env     ahmadjallab/ahmadjallab-prowler_aws:v2

- sudo yum install    nginx

- sudo vim /etc/nginx/sites-enabled/fastapi_nginx
- include /etc/nginx/sites-enabled/fastapi_nginx; in /etc/nginx/nginx.conf
- or can start with default conf server in /etc/nginx/sites-enabled/default
-  use nano for edit file in /etc/nginx/sites-enabled/default
- sudo systemctl start nginx
- sudo systemctl restart nginx
- sudo systemctl enable nginx


server {
        listen 80;
        server_name 3.83.14.33 ;
        location / {
                proxy_pass http://localhost:8000;
        }
}
:wq  -> save command
:qa! -> quit command
-http//172.17.0.1:8000; access to from you in local machine as  (nginx) proxy pass to the container (fastapi) http://0.0.0.0:8000;

-test for docker run  curl http://localhost:8000 -> in cli base 

## GitHub Actions Workflow

This project includes automated Docker image building and publishing using GitHub Actions. The workflow is triggered on:
- Push to main branch
- New version tags (v*.*.*)
- Pull requests to main branch

### Workflow Configuration

The workflow configuration is located in `.github/workflows/docker-publish.yml`:

```yaml
name: Docker Build and Push

on:
  push:
    branches: [ "main" ]
    tags: [ 'v*.*.*' ]
  pull_request:
    branches: [ "main" ]

env:
  REGISTRY: docker.io
  IMAGE_NAME: ahmadjallab/ahmadjallab-prowler_aws
```

### Available Docker Images

The Docker image is published to two registries:

1. Docker Hub:
```bash
docker pull ahmadjallab/ahmadjallab-prowler_aws:latest
```

2. AWS ECR Public:
```bash
docker pull public.ecr.aws/b1s1h1d1/ahmadjallab/ahmadjallab-prowler_aws:latest
```

### Image Tags

The workflow automatically generates several tags for each image:
- `latest`: For the main branch
- `v*.*.*`: For version releases
- `sha-XXXXXXX`: For each commit
- Branch name: For feature branches

### Setting up GitHub Actions

To enable the workflow, add these secrets to your GitHub repository:

1. Go to your repository settings
2. Navigate to Secrets and Variables > Actions
3. Add the following secrets:
   - `DOCKERHUB_USERNAME`: Your Docker Hub username
   - `DOCKERHUB_TOKEN`: Your Docker Hub access token (not password)

### Manual Workflow Dispatch

You can also manually trigger the workflow:
1. Go to Actions tab in your repository
2. Select "Docker Build and Push" workflow
3. Click "Run workflow"
4. Choose the branch to build from