import os 
import argparse 
import pathlib

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