import argparse

from .json_schema import read_json_schema
from .csv_data import prepare_csv_data, output_csv

parser = argparse.ArgumentParser(description='Convert JSON to CSV.')
parser.add_argument('input', type=argparse.FileType('r'), help='input JSON file')
parser.add_argument('output', type=argparse.FileType('w'), help='output CSV file')
parser.add_argument('-c',
                    '--columns',
                    help='columns to output (separated by comma)',
                    default='name,type,enum,description')
parser.add_argument('-k', '--key', help='key to start from', default='properties')
args = parser.parse_args()

data: dict = read_json_schema(args.input.name)
columns: list = args.columns.split(',')

csvData = prepare_csv_data(data, args.key, columns)
output_csv(columns, csvData, args.output)
