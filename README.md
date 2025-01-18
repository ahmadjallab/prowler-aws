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

### AWS IAM Configuration

#### Option 1: IAM User Configuration

1. Create an IAM User:
   ```bash
   aws iam create-user --user-name ProwlerSecurityAuditor
   ```

2. Required IAM Permissions:
   Create a policy file `prowler-security-policy.json`:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Action": [
                   "access-analyzer:List*",
                   "account:Get*",
                   "acm:Describe*",
                   "acm:List*",
                   "apigateway:GET",
                   "cloudtrail:GetEventSelectors",
                   "cloudtrail:GetTrailStatus",
                   "cloudtrail:LookupEvents",
                   "cloudwatch:GetMetricData",
                   "cloudwatch:GetMetricStatistics",
                   "cloudwatch:ListMetrics",
                   "config:BatchGetResourceConfig",
                   "config:List*",
                   "ec2:Describe*",
                   "ecr:Describe*",
                   "ecr:List*",
                   "ecs:Describe*",
                   "ecs:List*",
                   "eks:Describe*",
                   "eks:List*",
                   "elasticloadbalancing:Describe*",
                   "iam:Get*",
                   "iam:List*",
                   "kms:Describe*",
                   "kms:Get*",
                   "kms:List*",
                   "rds:Describe*",
                   "rds:List*",
                   "s3:Get*",
                   "s3:List*",
                   "secretsmanager:List*",
                   "securityhub:Get*",
                   "securityhub:List*",
                   "sns:List*",
                   "sqs:List*"
               ],
               "Resource": "*"
           }
       ]
   }
   ```

3. Create and Attach Policy:
   ```bash
   aws iam create-policy --policy-name ProwlerSecurityAuditPolicy --policy-document file://prowler-security-policy.json
   aws iam attach-user-policy --user-name ProwlerSecurityAuditor --policy-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:policy/ProwlerSecurityAuditPolicy
   ```

4. Create Access Keys:
   ```bash
   aws iam create-access-key --user-name ProwlerSecurityAuditor
   ```

#### Option 2: IAM Role Configuration

1. Create Trust Policy:
   Create `trust-policy.json`:
   ```json
   {
       "Version": "2012-10-17",
       "Statement": [
           {
               "Effect": "Allow",
               "Principal": {
                   "Service": "ec2.amazonaws.com"
               },
               "Action": "sts:AssumeRole"
           }
       ]
   }
   ```

2. Create Role:
   ```bash
   aws iam create-role --role-name ProwlerAuditRole --assume-role-policy-document file://trust-policy.json
   ```

3. Attach Policy:
   ```bash
   aws iam attach-role-policy --role-name ProwlerAuditRole --policy-arn arn:aws:iam::<YOUR_ACCOUNT_ID>:policy/ProwlerSecurityAuditPolicy
   ```

#### Environment Configuration

Add AWS credentials to your `.env` file:
```bash
AWS_ACCESS_KEY_ID=<your_access_key>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
AWS_REGION=<your_region>
# If using a role
AWS_ROLE_ARN=arn:aws:iam::<YOUR_ACCOUNT_ID>:role/ProwlerAuditRole
```

**Note**: It's recommended to use IAM roles instead of access keys for enhanced security, especially in production environments.

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

## AI Endpoint Documentation

### VPN Access Requirements

The AI endpoints in this application require secure VPN access to ensure data protection and maintain compliance with security standards. Below are the key endpoints and their access requirements:

#### 1. AI Security Assessment Summary Endpoint
```
GET /api/LLM_gemini_summery_compliance_report
```

**Access Requirements:**
- VPN Connection Required: Yes
- Authentication: Required
- Role-Based Access: Security Analyst or above

**Description:**  
This endpoint leverages Gemini LLM to generate an intelligent summary of security compliance reports. It processes Prowler security assessment data and provides actionable insights.

**Response Format:**
```json
{
    "status": "success",
    "content": "<markdown formatted security analysis>"
}
```

**Security Considerations:**
- All requests must originate from within the approved VPN network
- Rate limiting is applied to prevent API abuse
- Sensitive security findings are encrypted in transit
- Access logs are maintained for audit purposes

**Usage Notes:**
1. Ensure VPN connection is established before making API calls



For technical support or access issues, contact the security operations team.

## Project Structure
```
prowler-appdev/
├── .github/
│   └── workflows/
│       └── docker-publish.yml    # GitHub Actions workflow
├── LLM/
│   └── gemini_summery_LLM_compliance_report.py    # Gemini AI integration for report analysis
|
├── output/
│   └── compliance/              # Generated compliance reports
├── results/
│   └── prowler_scan.asff.json   # Prowler scan results
├── static/
│   └── docs/                     # API documentation
├── templates/
│   ├── index.html              # main page
│   └── compliance_report.html   # Report template
├── utils/
│   ├── ReportGenerationPipeline.py    # Report generation logic
│   ├── parseFindings_prowlerScan.py   # Findings parser
│   └── scan_mapping_findings_func.py   # Security mapping
├── compliance_filecheck/
│   └── RequirementIDs_for_corresponding_checks_pillar_sec01_sec03.json # Compliance mapping
├── results/                     # Generated reports 
│   └── prowler_scan.asff.json
├── output/
│   └── compliance/             # Compliance reports
├── .dockerignore               # Docker ignore rules
├── .env                        # Environment variables
├── .gitignore                 # Git ignore rules
├── Dockerfile                 # Docker configuration
├── endpointFunc.py           # API endpoint functions
├── main.py                   # FastAPI application entry point
├── requirements.txt          # Python dependencies
└── version.json             # Application version info for GitHub Actions workflow mechanism to update flag version
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
   - pipeline integration for report generation

3. **Compliance Mapping** (`compliance_filecheck/`)
   - Security pillar mappings
   - Compliance requirements for each pillar section (SEC01, SEC02, SEC03) aws well-architected framework security pillars compliance

4. **Infrastructure** (`Dockerfile`, `docker-publish.yml`)
   - Container configuration
   - CI/CD pipeline
   - Deployment automation using GitHub Actions workflow mechanism in docker hub

5. **Documentation** (`static/`, `README.md`)
   - API documentation
   - Setup instructions
   - Usage guides
   - Troubleshooting guides by endpoint testing and error handling

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
**Note:** The findings report can be exported in text format for easier readability and sharing. To export the report as a text file, use the following endpoint:

```
GET /api/run-prowler-generate-checks-report-fundings
```

This endpoint generates a plain text version of the compliance report, maintaining the structure and key findings while providing a lightweight, easily distributable format.


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
**Note:** The compliance report can be exported in text format for easier readability and sharing. To export the report as a text file, use the following endpoint:

```
GET /api/export-compliance-report
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

- HTML API documentation: http://localhost:8000/docs_page
- Interactive API documentation (Swagger UI): http://localhost:8000/docs
- Alternative API documentation (ReDoc): http://localhost:8000/redoc
- Prowler Documentation: https://docs.prowler.com/


## Running the Application


### ***Option A*** 
```bash
uvicorn main:app --reload --port 8000
```
**note** if use this approach you must comment out the line in main.py
```python 
# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
```
Access the API at http://localhost:8000
### ***Option B***

```bash
ptyhon main.py
```
**note** if use this approach you must check for line is not commented out in main.py 
```python 
 if __name__ == '__main__':
     import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
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

## some commands to check

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


### Workflow Configuration

The workflow configuration is located in `.github/workflows/docker-publish.yml`:

```yaml
name: Docker Build and Push

on:
  push:
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

The workflow generates the following tag for the image:
- `latest`: For the main branch

Note: Version tags (v*.*.*) have been removed from the automated workflow. Images are now only tagged with 'latest' when pushing to the main branch.

### Tag Generation Process

The workflow automatically handles version tagging through the following steps:

1. Version Management
   - Reads current version from `version.json`
   - Increments the version number
   - Updates `version.json` with new version
   - Commits the change with message "Bump version to [version] [skip ci]"

2. Docker Tag Creation
   - Uses docker/metadata-action to generate tags
   - Tags format: `v[number]` (e.g., v1, v2, v3)
   - Tags are applied only on pushes to main branch
   - Automated version incrementing ensures unique tags for each build

   Why Docker Tags Matter:
   - Version Control: Tags help track different versions of your container image, making it easy to roll back to previous versions if needed
   - Deployment Management: Different environments (dev, staging, prod) can use specific versions of your application
   - Reproducibility: Each build has a unique tag, ensuring you can always recreate the exact environment
   - Auditing: Tags help track which version is running in production and when changes were made
   - CI/CD Integration: Automated tagging simplifies continuous deployment by providing consistent versioning

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

## New Features and Updates : V5


### API Documentation Page 

The documentation page (`/docs`) has been enhanced with:

1. Interactive Features
   - Live API testing capability
   - Request/response examples
   - Real-time endpoint testing

2. Navigation
   - Quick links to all endpoints
   - Organized by category
   - Search functionality

3. Visual Improvements
   - Syntax highlighting for code examples
   - Clear endpoint descriptions
   - Status code indicators

### Compliance Report Enhancements

The compliance report page now includes:

1. Print Optimization
   - Print-friendly layout
   - Footer positioning for printed pages
   

2. Navigation
   - "Go Back" functionality
   - Quick links to documentation
   - Easy access to dashboard

3. Content Display
   - Better formatting for findings
   - Severity indicators
   - Collapsible sections

### Dashboard Updates

The main dashboard (`/`) features:

1. New UI Elements
   - Documentation access button
   - Status indicators
   - Loading animations

2. Improved Layout
   - Centered content design
   - Responsive grid system
   - Better spacing and alignment

### Brand Guidelines

When extending or modifying the application, maintain these branding elements:

1. Colors
   - Primary Blue: #0366d6
   - Secondary Gray: #586069
   - Background: #ffffff
   - Text: #24292e

2. Typography
   - Main Font: System default
   - Logo Font: Bold weight for "AJC"
   - Regular weight for "Security"

3. Layout
   - Centered content
   - Consistent padding (2rem)
   - Responsive breakpoints
   - Footer always visible

4. Assets
   - Heart emoji in attribution
   - GitHub icon in links
   - Document icons for navigation

### Future Enhancements

Planned features for future releases:

1. Authentication
   - User login system
   - Role-based access control
   - Session management

2. Reporting
   - Custom report templates
   - Export in multiple formats
   - Scheduled reports

3. Integration
   - Additional cloud providers
   - Third-party security tools
   - Custom compliance frameworks

4. AI-Powered Security Analysis
   - Intelligent threat detection and prioritization
   - Automated security recommendations based on findings
   - Machine learning models for anomaly detection
   - Natural language processing for security report generation
   - Predictive security risk assessment

5. UI/UX
   - Dark mode support
   - Custom theming options
   - Accessibility improvements

## Contact

For questions, support, or contributions, please contact:
- GitHub: [@ahmadjallab](https://github.com/ahmadjallab)
- Email: [contact@ajcsecurity.com](mailto:contact@ajcsecurity.com)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

 2025 AJC Security. All rights reserved.