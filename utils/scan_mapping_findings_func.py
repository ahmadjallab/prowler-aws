import json
import os

def map_findings_to_pillars(findings):
    """
    Maps Prowler findings to AWS Well-Architected Framework Security Pillars.

    :param findings: List of parsed findings.
    :return: Dictionary categorized by WAF Security Pillar.
    """
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the JSON file
    json_path = os.path.join(current_dir, '..', 'compliance_filecheck', 'RequirementIDs_for_corresponding_checks_pillar_sec01_sec03.json')
    
    try: 
        with open(json_path, 'r') as f:
            SECURITY_PILLAR_MAPPING = json.load(f)
    except FileNotFoundError as e:
        print(f"Error: The file was not found at {json_path}. {e}")
        return []
        
    mapped_findings = {"SEC01": [], "SEC02": [], "SEC03": []}
    
    for finding in findings:
        for pillar, checks in SECURITY_PILLAR_MAPPING.items():
            if finding["check_id"] in checks:
                # Add finding to the appropriate pillar
                mapped_findings[pillar[:5]].append(finding)
    
    return mapped_findings