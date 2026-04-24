import os 
import sys
import argparse
import pathlib
import importlib.util
import time

def importFromDir(directory):
    for py_file in pathlib.Path(directory).glob("*.py"):
        module_name = py_file.stem 
        RuleNames.append(module_name)
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module 
        globals()[module_name] = module

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

parser = argparse.ArgumentParser()
parser.add_argument("Input", help="The input csv file to parse")
parser.add_argument("Rules", help="The rules for which to parse the input csv file")
parser.add_argument("-nh", action="count", help="Tells the file reader that the input file does not contain a header")
parser.add_argument("-v", "--verbose", action="count", help="Makes output more verbose by generating an additional output file detailing which rules each row of the failed output csv failed")
args = parser.parse_args()

InputRows = []
Rules = []
ParsedRules = [] 

try:
	with open(args.Rules, 'r') as f:
		Rules = f.readlines()
except FileNotFoundError as e:
    print(f"Error opening rules file: {e}")
    sys.exit()
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

try: 
    InputRows = loadRows(args.Input, args.nh)
except FileNotFoundError as e:
    print(f"Error opening rules file: {e}")
    sys.exit()
except Exception as e:
    print(f"Error: {e}")
    sys.exit()

if Rules:
    for line in Rules:
        if not line.strip():
            ParsedRules.append(["",""])
        Rule, Args = line.rstrip().split(":")
        Args = Args.split(",")
        ParsedRules.append([Rule,Args])

for rowID, row in enumerate(InputRows): 
    failed = False
    timestamp =str(int(time.time()))
    passFileName = str("passed-" + timestamp +".csv")
    failFileName = str("failed-" + timestamp +".csv")
    passFile = open(passFileName, "a")
    failFile = open(failFileName, "a")
    for colID, value in enumerate(row): 
        ruleName = ParsedRules[colID][0].lower()
        ruleArgs = ParsedRules[colID][1]
        if not getattr(globals()[ruleName], ruleName)(InputRows,rowID,colID,value,ruleArgs):
            failFile.write(",".join(row) + "\n")
            failed = True
            break
    if not failed:
        passFile.write(",".join(row) + "\n")
    
        
        
            