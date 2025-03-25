import json
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("-n","--name", type=str, help="name of your benchmark",required=True)

# Parse the arguments
args = parser.parse_args()

benchmark_name = args.name

with open(f'output_{benchmark_name}/output_completed.json', 'r') as f:
	results = json.load(f)


out = {}

for key,value in results.items():

	l = value["predicted"] 
	l = [s.lower() for s in l]

	value["predicted"] = l
	out[key] = value

with open(f'output_{benchmark_name}/output_completed_adjusted.json', 'w') as f:
	f.write(json.dumps(out, indent = 4))

print("done!")