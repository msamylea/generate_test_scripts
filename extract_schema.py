import json

def extract_schema(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
    schema = {}
    for key, value in data.items():
        if isinstance(value, dict):
            schema[key] = extract_schema_from_dict(value)
        elif isinstance(value, list):
            schema[key] = extract_schema_from_list(value)
        else:
            schema[key] = type(value).__name__
    return schema

seen_schemas = {}

def extract_schema_from_dict(d):
    schema = {}
    for key, value in d.items():
        if isinstance(value, dict):
            schema[key] = extract_schema_from_dict(value)
        elif isinstance(value, list):
            schema[key] = extract_schema_from_list(value)
        else:
            schema[key] = type(value).__name__

    schema_str = json.dumps(schema, sort_keys=True)
    if schema_str in seen_schemas:
        return seen_schemas[schema_str]
    else:
        seen_schemas[schema_str] = schema
        return schema

def extract_schema_from_list(lst):
    if not lst:
        return 'empty list'
    if isinstance(lst[0], dict):
        schemas = [extract_schema_from_dict(item) for item in lst]
    elif isinstance(lst[0], list):
        schemas = [extract_schema_from_list(item) for item in lst]
    else:
        return type(lst[0]).__name__

    merged_schema = {}
    for schema in schemas:
        merged_schema.update(schema)
    schema_str = json.dumps(merged_schema, sort_keys=True)
    if schema_str in seen_schemas:
        return seen_schemas[schema_str]
    else:
        seen_schemas[schema_str] = merged_schema
        return merged_schema
def main():
    json_file = "C:/Code/fl_doh_parse/dialog-skill.json"  # replace with your JSON file
    schema = extract_schema(json_file)
    with open('schema.txt', 'w') as f:
        json.dump(schema, f, indent=4)

if __name__ == '__main__':
    main()