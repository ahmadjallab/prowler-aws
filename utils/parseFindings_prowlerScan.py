import json
import os

def parse_prowler_scan(file_name='prowler_scan.asff.json'):
    """
    Parses the Prowler scan JSON file and extracts findings.

    :param file_name: Name of the Prowler JSON output file.
    :return: List of parsed findings IF file not found return empty list.
    """
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the results file
    file_path = os.path.join(current_dir, '..', 'results', file_name)
    
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return []
        
    findings = []
    for finding in data:
        findings.append({
                "check_id": finding.get("GeneratorId").replace("prowler-", ""),
                "title": finding.get("Title"),
                "description": finding.get("Description"),
                "severity": finding.get("Severity", {}).get("Label"),
                "status": finding.get("Compliance", {}).get("Status"),
                "resource_id": finding.get("Resources", [{}])[0].get("Id"),
                "related_requirements": finding.get("Compliance", {}).get("RelatedRequirements", []),
                "remediation_text": finding.get("Remediation", {}).get("Recommendation", {}).get("Text"),
                "remediation_url": finding.get("Remediation", {}).get("Recommendation", {}).get("Url"),
            })
    
    return findings