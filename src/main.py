'''
*
* Project: schema-alignment-bird
* main.py
*
* Author: Gianluca Farinaccio <gia.farinaccio@stud.uniroma3.it>
* Date: 25.03.2025
*
'''

import json
import time
import argparse
import os

import utils
import llm_adapter


# Create the parser
parser = argparse.ArgumentParser()

# Add arguments
parser.add_argument("-n","--name", type=str, help="name of your benchmark",required=True)

# Parse the arguments
args = parser.parse_args()

benchmark_name = args.name
os.makedirs(f'output_{benchmark_name}', exist_ok=True)


''' 
1st step - Reformat database schema

Extract only useful information about dbs schema from 'dev_table.json'.
Generate a new file that contains db schema information, more compact and more useful for LLM.
'''

with open('dataset/dev_tables.json') as f:
	data = json.load(f)

dbs_schema = {}

for db in data:
	schema = utils.format_db_schema(db)
	dbs_schema[db['db_id']] = schema

out = json.dumps(dbs_schema, indent=4)

with open('dataset/db_schema.json', 'w') as f:
	f.write(out)


'''
2nd step - Ground-Truth extraction from SQL queries 

Extract the ST's name from SQL queries contained in 'mini_dev_postgresql.json'
The extracted names will be the ground-truth. They will be compared to LLM response.

We create a JSON file that will be completely filled in the next step. 

...
<question-id> {
	"question" : None,
	"true": [None],
	"predicted": [None]
},
...

This JSON file contains a set of JSON object as above, where:
- <question-id> is the unique id of question.
	- "db_id" is the id of database that the query refers to
	- "question" is the natural language query.
	- "true" is the list of ST's names extracted from SQL query. It is our ground-truth.
	- "predicted" is the list of ST's names infered by LLM. (Filled in the next step)

'''

with open('dataset/db_schema.json', 'r') as f:
	db_schemas = json.load(f)

with open('dataset/mini_dev_postgresql.json', 'r') as f:
	dataset = json.load(f)

output = {}

for query in dataset:
	qid = query["question_id"]
	did = query["db_id"]

	# Extract the ST's names from SQL query
	extracted_tables = list(utils.extract_tables_from_sql_v2(query["SQL"]))
	extracted_tables = [s.lower() for s in extracted_tables]
	extracted_tables = set(extracted_tables)

	'''
	To avoid any mistakes, we make a check on extracted tables
	Any extracted tables name must also be contained in "tables" JSON object
	associated to that database_id. 
	This mechanism avoid to extract as table name some SQL keyword 
	in challenging SQl queries.
	'''
	db_tables = list(db_schemas[did]["tables"].keys())
	db_tables = [s.lower() for s in db_tables]
	db_tables = set(db_tables)

	ground_truth = extracted_tables & db_tables

	print(f"query: {qid} ----")
	print(f"extracted_tables: {extracted_tables}")
	print(f"db_tables: {db_tables}")
	print(f"ground_truth: {ground_truth}")		

	obj = {
		"db_id": did,
		"question" : query["question"],
		"true": list(ground_truth),
		"predicted" : [None]
	}

	output[qid] = obj


with open(f'output_{benchmark_name}/output_template.json', 'w') as f:
	f.write(json.dumps(output, indent = 4))



'''
3rd step - Use of LLM to infer the ST's names. 

Use of LLM to infer the ST's names based on natural language query and DB schema.
See "llm_adapter.py" for prompt-template.

The call to LLM is based on Groq API (Free), so to respect the rate-limits of 30 request/minute
we add a 2.2s sleep between each request.

The completed JSON in file will be saved in /output-{bench_name} dir.
It is updated every 30request, to avoid data loss in case of API crash.

'''

with open('dataset/db_schema.json', 'r') as f:
	db_schemas = json.load(f)


with open(f'output_{benchmark_name}/output_template.json', 'r') as f:
	queries = json.load(f)


output = {}
i = 1
for qid, obj in queries.items():

	prompt = utils.generate_prompt(obj["question"], db_schemas[obj["db_id"]])
	llm_response = list(llm_adapter.call_to_llm(prompt).split(","))

	llm_response = [s.lower() for s in llm_response]

	obj["predicted"] = llm_response
	output[qid] = obj
	print(f'{i}: question_id:{qid}')

	if(i%30 == 0):
		with open(f'output_{benchmark_name}/output_completed.json', 'w') as f:
			f.write(json.dumps(output, indent=4))
		print('-- partial saved')

	time.sleep(2.2)
	i+=1

print("done!")









