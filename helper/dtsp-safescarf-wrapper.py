#/usr/bin/python3

import json
import os
import logging
import argparse

#SOURCE_FILE = 'dtsp-scanresults.json'
SAFESCARF_FORMAT = {
  "test": 0,
  "thread_id": 0,
  "found_by": [],
  "url": "",
  "tags": [],
  "push_to_jira": "false",
  "sla_start_date": "",
  "sla_expiration_date": "",
  "findings" : []
}


def check_source_file(source_file):
    return True if os.path.isfile(source_file) else False

def read_source_file(source_file):
    result = None
    if check_source_file(source_file):
        try:
            with open(source_file, 'r') as f:
                result = json.loads(f.read())
        except:
            logging.error("File {} cannot be read. Check that it is in the correct JSON format".format(str(source_file)))
    else:
        logging.error("File {} cannot be found.".format(str(source_file)))
    return result

# Helper functions for the following parse_data() function:
def iter_vulns(element):
    severity = element.get("severity", "")
    if(severity == "negligible" or severity == "unknown"):
        severity = "info"
    finding = {
        "title": element.get("description", ""),
        "description": element.get("description", ""),
        "severity": severity.capitalize(),
        "numerical_severity": "{}".format(element.get("severity_index", "")),
        "cve": element.get("cve", ""),
    }
    return finding

def iter_components(component, result_list, finding):
    finding_by_artefact = {}
    finding_by_artefact = finding
    finding_by_artefact["component_name"] = component.get("name", "")
    finding_by_artefact["component_version"] = component.get("version", "")
    result_list["findings"].append(finding_by_artefact.copy())

# Function to extract Data to the test itself
def parse_data(input):

    # General Test data
    PARSED_DATA = SAFESCARF_FORMAT

    # TODO: ASK "is the dtsp scan always with grype or could there be other engines?"
    if (input.get("engine_name", "") == "grype"):
        PARSED_DATA["found_by"] = "Anchore Grype"
    else:
        logging.error("Engine unknown, for now only grype is supported.")
        # exit 1 noch hinzufügen? Testen mit "echo $ ?" ob das schon im logging.error passiert

    PARSED_DATA["tags"] = input.get("tags", [])
    PARSED_DATA["sla_start_date"] = input.get("started_at", "")[:10]
    PARSED_DATA["sla_expiration_date"] = input.get("finished_at", "")[:10]

    # Each individual Vulnerability
    for element in input.get("vulnerabilities", []):
        finding = iter_vulns(element)
        # Artifacts for each individual vulnerability
        for component in element.get("artifacts", []):
            iter_components(component, PARSED_DATA, finding)
    return PARSED_DATA

# Read command line arguments like filename
def parse_arguments():
    parser = argparse.ArgumentParser(description='Process inputfile')
    parser.add_argument('file', type=str, help='Specify input Filename to process as argument when calling the script. If file is not in same directory, input path and filename')
    parser.add_argument('-d', '--destination', type=str, default='parsed_scanresults.json', help='Specify destination filename for the parsed data (optional)')

    return parser.parse_args()


def main():
    args = parse_arguments()
    try:
        json_file_contents = read_source_file(args.file)
    except:
        logging.error("Please provide an inputfile within the current directory or the full Path to the input file")

    parsed_data = parse_data(json_file_contents)
    # Debug
    # print(parsed_data)

    # Write Formatted Data to new file
    with open(args.destination, 'w') as f:
        json.dump(parsed_data, f, indent=2)

if __name__ == "__main__":
    main()
