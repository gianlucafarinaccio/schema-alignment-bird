import json
import re

'''
Extract ST's names from a SQL query.
It returns a set that contains table's names.

Sometimes this function could make some mistakes for very challeging query.
To make sure that extracted tables are all table names, properly actions are required.
See "2nd step" in "main.py" for more information

'''
def extract_tables_from_sql_v2(sql_query):
    table_pattern = re.compile(r'\b(?:FROM|JOIN)\s+([`"\[]?[\w\.]+[`"\]]?)', re.IGNORECASE)
    tables = table_pattern.findall(sql_query)
    clean_tables = [table.strip('`"[]') for table in tables]
    return set(clean_tables)

'''
Reformat the database schemas contained in "dataset/dev_tables.json"
It returns a JSON that contains only relevant information about every DB schema.

'''
def format_db_schema(json_data):
    # Estrai i dati dal JSON in input
    table_names = json_data["table_names_original"]
    column_names = json_data["column_names_original"]
    column_types = json_data["column_types"]
    
    # Inizializza la struttura del risultato
    db_schema = {"tables": {}}

    # Itera sulle tabelle e assegna le colonne corrispondenti
    table_columns = {table: [] for table in table_names}
    
    # Popola le tabelle con i nomi delle colonne e i rispettivi tipi
    for (index, column) in enumerate(column_names):
        table_index = column[0]
        column_name = column[1]
        column_type = column_types[index]
        
        # Aggiungi il nome della colonna e il tipo alla tabella corrispondente
        table_columns[table_names[table_index]].append([column_name, column_type])
    
    # Aggiungi le tabelle al risultato
    db_schema["tables"] = table_columns
    
    return db_schema


def generate_prompt(nl_query, db_schema):

    prompt = f"""
Based on the following natural-language query:
{nl_query}

And based on the following relational database schema in JSON format:
{db_schema}

Identify only the source tables required to extract the information for the query.
Consider foreign keys and relationships if necessary.
Do not return column names, SQL queries, or additional explanations.

Format the output as a single comma-separated string with no spaces, like this: table1,table2,table3
    """

    return prompt


