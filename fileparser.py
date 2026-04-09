import os 
import argparse 

parser = argparse.ArgumentParser()
parser.add_argument("Input", help="The input csv file to parse")
parser.add_argument("Rules", help="The rules for which to parse the input csv file")
parser.add_argument("-v", "--verbose", action="count", help="Makes output more verbose by generating an additional output file detailing which rules each row of the failed output csv failed")

args = parser.parse_args()

print(args)