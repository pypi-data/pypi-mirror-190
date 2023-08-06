import yaml

def load_yaml(yaml_filepath): 
    with open(yaml_filepath, 'r') as f:
        cfg = yaml.full_load(f)
    return cfg