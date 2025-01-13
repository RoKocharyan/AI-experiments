from file_operations.file_operations import *
from ollama.ollama_api import ollama_generate
from Yaml_parser.yamlParser import *

if __name__ == "__main__":
    prompt = read_file_content("Yaml_parser/yaml prompt gen prompt.md")
    user_requsst = "new field to save url displayed as infoCard that will hold onboarding link"
    # user_requsst = "new text field in account whit a table view to hold image of creator called avatar"
    prompt = prompt.replace("@request", user_requsst)
    
    answer = ollama_generate(prompt, "llama3.2")
    # print(answer)
    code = extractCode(answer, "yml")
    # print(code)
    overwrite_file(code, "Yaml_parser/example.yaml")

    validation_rules = load_validation_rules("Yaml_parser/validation_rules.yaml")
    example = load_yaml("Yaml_parser/example.yaml")
    if not validate_yaml(example, validation_rules):
        print("YAML validation failed.")
    else:  
        process_yaml(example)