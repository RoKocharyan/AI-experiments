import re
import difflib

def extractCode(payload):
    match = re.search(r"```(?:javascript)?\s*(.*?)```", payload, re.DOTALL)
    #if match:
        #print (match.groups())
    return match.group(1)

def overwrite_file(text, filename):
    with open(filename, 'w') as file:
        file.write(text)

def read_file_content(file_path):
    """
    Reads the content of a file and returns it as a string.

    :param file_path: Path to the file to be read.
    :return: Content of the file as a string.
    """
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Error: The file at '{file_path}' was not found."
    except Exception as e:
        return f"An error occurred: {e}"
    
def find_differences(model1, model2):
    """
    Compares two models (as strings) and identifies the different field.

    :param model1: First model as a string.
    :param model2: Second model as a string.
    :return: The field that differs as a string.
    """
    model1_lines = set(model1.splitlines())
    model2_lines = set(model2.splitlines())
    
    # Find lines that are in model1 but not in model2, and vice versa
    diff1 = model1_lines - model2_lines
    diff2 = model2_lines - model1_lines

    # Combine differences and return
    differences = diff1.union(diff2)
    return "\n".join(differences)

