import os 
import sys
import argparse
import pathlib
import importlib.util


def import_from_dir(directory):
    for py_file in pathlib.Path(directory).glob("*.py"):
        module_name = py_file.stem 
        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[module_name] = module 
        globals()[module_name] = module

import_from_dir("Rules")

parser = argparse.ArgumentParser()
parser.add_argument("Input", help="The input csv file to parse")
parser.add_argument("Rules", help="The rules for which to parse the input csv file")
parser.add_argument("-v", "--verbose", action="count", help="Makes output more verbose by generating an additional output file detailing which rules each row of the failed output csv failed")
args = parser.parse_args()

print(args)
InputFile = args.Input
Rules = []
ParsedRules = [] 

try:
	with open(args.Rules, 'r') as f:
		Rules = f.readlines()
except FileNotFoundError as e:
	print(f"Error opening rules file: {e}")
except Exception as e:
	print(f"Error: {e}")

if Rules:
	for line in Rules:
		Rule, Args = line.rstrip().split(":")
		Args = Args.split(",")
		ParsedRules.append([Rule,Args])

print(ParsedRules)
