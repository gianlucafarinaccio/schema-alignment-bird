import utils
import llm_adapter
import json
import time


# REFORMAT DATABASE SCHEMA ------------------

# with open('dev_tables.json') as f:
# 	data = json.load(f)

# dbs_schema = {}

# for db in data:
# 	schema = utils.format_db_schema(db)
# 	dbs_schema[db['db_id']] = schema

# out = json.dumps(dbs_schema, indent=4)

# with open('db_schema.json', 'w') as f:
# 	f.write(out)


# CALL TO LLM ------------------

# with open('db_schema.json', 'r') as f:
# 	db_schemas = json.load(f)


# with open('mini_dev_postgresql.json', 'r') as f:
# 	queries = json.load(f)

# output = {}
# i=1
# for obj in queries:

# 	prompt = utils.generate_prompt(obj["question"], db_schemas[obj["db_id"]])
# 	llm_response = llm_adapter.call_to_llm(prompt).split(",")

# 	current = {
# 		"question" : obj["question"],
# 		"true" : list(utils.extract_tables_from_sql_v2(obj["SQL"])),
# 		"predicted": llm_response
# 	}

# 	output[obj["question_id"]] = current
# 	print(f'{i}: question_id:{obj["question_id"]}')
# 	time.sleep(3)
# 	i+=1


# print("done!")

# with open("response_v3_sql_dan.json", 'w') as f:
# 	f.write(json.dumps(output))


# GROUND TRUTH CHECK ------------------

with open('db_schema.json', 'r') as f:
	db_schemas = json.load(f)

with open('mini_dev_postgresql.json', 'r') as f:
	dataset = json.load(f)

with open('response.json', 'r') as f:
	response = json.load(f)


for obj in dataset:
	qid = obj["question_id"]
	did = obj["db_id"]

	real_tables = list(db_schemas[did]["tables"].keys())
	real_tables = [s.lower() for s in real_tables]
	real_tables = set(real_tables)

	tables = response[str(qid)]["true"]
	tables = [s.lower() for s in tables]

	checked_tables = set(tables) & real_tables

	response[str(qid)]["true"] = list(checked_tables)

	predicted_tables = response[str(qid)]["predicted"]
	predicted_tables = [x.lower() for x in predicted_tables]
	response[str(qid)]["predicted"] = predicted_tables
	response[str(qid)]["db_id"] = did 

with open('response_t.json', 'w') as f:
	f.write(json.dumps(response))









