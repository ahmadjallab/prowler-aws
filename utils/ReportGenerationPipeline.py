import json
import os
from .parseFindings_prowlerScan import parse_prowler_scan 
from .scan_mapping_findings_func import map_findings_to_pillars

def export_text_report_just_for_findings(findings, output_file="finding_report.txt"):
    """
    Generates a text file report from the parsed findings.

    :param findings: List of parsed findings.
    :param output_file: Path to the output text file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the results file
    file_path = os.path.join(current_dir, '..', 'output','compliance', output_file)
    with open(file_path, 'w', encoding='utf-8') as report:
        report.write("=== AWS Security Compliance Report ===\n\n")
        
        for idx, finding in enumerate(findings, start=1):
            report.write(f"Finding {idx}:\n")
            report.write(f"  Check ID: {finding['check_id']}\n")
            report.write(f"  Title: {finding['title']}\n")
            report.write(f"  Description: {finding['description']}\n")
            report.write(f"  Severity: {finding['severity']}\n")
            report.write(f"  Status: {finding['status']}\n")
            report.write(f"  Resource ID: {finding['resource_id']}\n")
            report.write(f"  Related Requirements: {', '.join(finding['related_requirements'])}\n")
            report.write(f"  Remediation: {finding['remediation_text']}\n")
            if finding['remediation_url']:
                report.write(f"  More Info: {finding['remediation_url']}\n")
            report.write("\n")  # Add a blank line between findings
    
  
def export_report_to_text(report_content, output_file="compliance_report.txt"):
    """
    Exports a given string report to a text file.

    :param report_content: The content of the report as a string.
    :param output_file: Path to the output text file.
    """
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the results file
    file_path = os.path.join(current_dir, '..', 'output','compliance', output_file)
    try:
        with open(file_path, 'w', encoding='utf-8') as report_file:
            report_file.write(report_content)
        print(f"Report successfully exported to {output_file}")
    except Exception as e:
        print(f"An error occurred while exporting the report: {e}")

def generate_compliance_report(mapped_findings):
    """
    Generates a compliance report based on mapped findings.

    :param mapped_findings: Findings categorized by WAF Security Pillar.
    :return: A human-readable string report.
    """
    report = []
    for pillar, findings in mapped_findings.items():
        report.append(f"\n=== {pillar} Compliance Report ===")
        if not findings:
            report.append("No findings for this pillar.")
            continue
        
        for finding in findings:
            report.append(f"- Check ID: {finding['check_id']}")
            report.append(f"  Title: {finding['title']}")
            report.append(f"  Description: {finding['description']}")
            report.append(f"  Severity: {finding['severity']}")
            report.append(f"  Status: {finding['status']}")
            report.append(f"  Resource ID: {finding['resource_id']}")
            report.append(f"  Remediation: {finding['remediation_text']}")
            if finding['remediation_url']:
                report.append(f"  Remediation Details: {finding['remediation_url']}")
    
    return "\n".join(report)

def generate_compliance_report_pipeline():
    # Step 1: Parse Prowler scan results
    #prowler_file = "prowler_output.json"
    findings = parse_prowler_scan()
    # Step 2: Map findings to WAF Security Pillar
    mapped_findings = map_findings_to_pillars(findings)
    # Step 3: Generate and print compliance report
    compliance_report = generate_compliance_report(mapped_findings)

   
    export_text_report_just_for_findings(findings, 'finding_report.txt')
        
    export_report_to_text(compliance_report, 'compliance_report.txt')
    #print(compliance_report)
    return compliance_report #string for now

