import re
from typing import List, Dict, Any, Tuple
import yaml


def extractCode(payload, language=None):
    # Remove curly braces around the language
    language_pattern = rf"{language}" if language else ""
    # Construct the regex pattern without curly braces
    pattern = rf"```{language_pattern}\s*(.*?)```"
    
    match = re.search(pattern, payload, re.DOTALL)
    if match:
        return match.group(1).strip()  # Optional: Remove leading/trailing whitespace
    return None

def overwrite_file(content, filename):
    with open(filename, 'w') as file:
        file.write(content)

def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at '{file_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"
    
def find_differences(model1, model2):

    model1_lines = set(model1.splitlines())
    model2_lines = set(model2.splitlines())
    
    # Find lines that are in model1 but not in model2, and vice versa
    diff1 = model1_lines - model2_lines
    diff2 = model2_lines - model1_lines

    # Combine differences and return
    differences = diff1.union(diff2)
    return "\n".join(differences)

def load_yaml(yaml_file_path: str) -> Dict[str, Any]:
    with open(yaml_file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)