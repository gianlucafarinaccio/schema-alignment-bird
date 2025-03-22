import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML
import json
import re

def extract_tables_from_sql(sql_query):
    """
    Estrae le tabelle da una query SQL in modo robusto usando sqlparse.
    """
    # parsed = sqlparse.parse(sql_query)
    # tables = set()

    # for stmt in parsed:
    #     for token in stmt.tokens:
    #         if token.ttype is None and token.get_real_name():  # Controlla se è un identificatore (tabella)
    #             tables.add(token.get_real_name())

    # return tables

    parsed = sqlparse.parse(sql_query)
    tables = set()
    
    for stmt in parsed:
        from_seen = False
        for token in stmt.tokens:
            if from_seen:
                if isinstance(token, IdentifierList):
                    for identifier in token.get_identifiers():
                        tables.add(identifier.get_real_name())
                elif isinstance(token, Identifier):
                    tables.add(token.get_real_name())
                elif token.ttype in (Keyword, DML):  # Fine della clausola FROM o inizio di una nuova istruzione
                    break
            
            if token.ttype in (Keyword, DML) and token.value.upper() in ('FROM', 'JOIN'):
                from_seen = True
    
    return tables

def extract_tables_from_sql_v2(sql_query):
    table_pattern = re.compile(r'\b(?:FROM|JOIN)\s+([`"\[]?[\w\.]+[`"\]]?)', re.IGNORECASE)
    tables = table_pattern.findall(sql_query)
    clean_tables = [table.strip('`"[]') for table in tables]
    return set(clean_tables)



def format_db_schema(json_data):
    # Estrai i dati dal JSON in input
    table_names = json_data["table_names"]
    column_names = json_data["column_names"]
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

#     prompt = f"""
# Based on this natural-language query:
# {nl_query}, 

# and based on this relational database schema information in JSON format: 
# {db_schema}

# Give me the source table to extract the information required in the query above.
# I want a clear output that contains only the source tables.
# Use the following output format "table-name-1, table-name-2, ... "
#     """

    prompt = f"""
Based on the following natural-language query:
{nl_query}

And based on the following relational database schema in JSON format:
{db_schema}

Identify only the source tables required to extract the information for the query.
Consider foreign keys and relationships if necessary.
Do not return column names, SQL queries, or additional explanations.

Format the output as a single comma-separated string with no spaces, like this: utable1,table2,table3
    """



    return prompt


