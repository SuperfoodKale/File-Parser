import os 
import sys
import argparse
import pathlib
import importlib.util
import time

#dynamically load all modular rules available to the rule engine 
def importFromDir(directory):
    if not pathlib.Path(directory).is_dir():
        print(f"Error: Rules directory '{directory}' not found")
        sys.exit()

    for py_file in pathlib.Path(directory).glob("*.py"):
        module_name = py_file.stem 
        try:
            spec = importlib.util.spec_from_file_location(module_name, py_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module_name] = module 
            globals()[module_name] = module
            RuleNames.append(module_name)
        except SyntaxError as e:
            print(f"Error: Syntax error in rule file '{py_file}': {e}")
            sys.exit()
        except Exception as e:
            print(f"Error: Failed to load rule file '{py_file}': {e}")
            sys.exit()

#load all rows from the input file into a nested list
def loadRows(filepath, noHeader=None):
    InputRows = []

    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    start_index = 0 if noHeader == 1 else 1

    for line in lines[start_index:]:
        if line.strip() == "":
            continue 
        row = line.split(",")
        InputRows.append(row)

    return InputRows
    
RuleNames = []
importFromDir("Rules")

#argument parsing 
parser = argparse.ArgumentParser()
parser.add_argument("Input", help="The input csv file to parse")
parser.add_argument("Rules", help="The rules for which to parse the input csv file")
parser.add_argument("-nh", action="count", help="Tells the file reader that the input file does not contain a header")
parser.add_argument("-v", "--verbose", action="count", help="Makes output more verbose by generating an additional output file detailing which rules each row of the failed output csv failed")
args = parser.parse_args()

InputRows = []
ParsedRules = [] 
Rules = []

#open rules file with error handling
try:
    with open(args.Rules, 'r') as f:
        Rules = f.readlines()
except FileNotFoundError as e:
    print(f"Error opening rules file: {e}")
    sys.exit()
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

#open input file with error handling
try: 
    InputRows = loadRows(args.Input, args.nh)
except FileNotFoundError as e:
    print(f"Error opening input file: {e}")
    sys.exit()
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

if not InputRows:
    print("Error: Input file contains no data rows")
    sys.exit()

#parse rules into names and arguments for each column
if Rules:
    for lineNum, line in enumerate(Rules, start=1):
        if not line.strip():
            ParsedRules.append([])
            continue
        columnRules = []
        for segment in line.rstrip().split(";"):
            segment = segment.strip()
            if not segment:
                continue
            if ":" not in segment:
                print(f"Error: Malformed rule on line {lineNum} (missing ':'): '{segment}'")
                sys.exit()
            Rule, _, Args = segment.partition(":")
            Rule = Rule.strip()
            if not Rule:
                print(f"Error: Empty rule name on line {lineNum}: '{segment}'")
                sys.exit()
            if Rule.lower() not in RuleNames:
                print(f"Error: Unknown rule '{Rule}' on line {lineNum} - not found in Rules/ directory")
                sys.exit()
            Args = [a.strip() for a in Args.split(",")]
            columnRules.append([Rule, Args])
        ParsedRules.append(columnRules)

#apply parsed rules for each column to every row and write to output file 
timestamp = str(int(time.time()))
passFileName = f"passed-{timestamp}.csv"
failFileName = f"failed-{timestamp}.csv"

try:
    with open(passFileName, "a") as passFile, open(failFileName, "a") as failFile:
        for rowID, row in enumerate(InputRows):
            if len(row) > len(ParsedRules):
                print(f"Error: Row {rowID + 1} has {len(row)} columns but only {len(ParsedRules)} rules are defined")
                sys.exit()
            failed = False
            for colID, value in enumerate(row):
                # skip columns with no rules defined
                if colID >= len(ParsedRules) or not ParsedRules[colID]:
                    continue
                for rule in ParsedRules[colID]:
                    ruleName = rule[0].lower()
                    ruleArgs = rule[1]
                    try:
                        result = getattr(globals()[ruleName], ruleName)(InputRows, rowID, colID, value, ruleArgs)
                    except Exception as e:
                        print(f"Error: Rule '{rule[0]}' failed on row {rowID + 1}, column {colID + 1} with value '{value}': {e}")
                        sys.exit()
                    if not result:
                        failFile.write(",".join(row) + "\n")
                        failed = True
                        break
                if failed:
                    break
            if not failed:
                passFile.write(",".join(row) + "\n")
except IOError as e:
    print(f"Error: Could not write to output files: {e}")
    sys.exit()