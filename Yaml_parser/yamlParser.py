import yaml
from typing import List, Dict, Any, Tuple


def load_yaml(yaml_file_path: str) -> Dict[str, Any]:
    with open(yaml_file_path, 'r') as yaml_file:
        return yaml.safe_load(yaml_file)


def load_validation_rules(file_path: str) -> Dict[str, List[str]]:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def process_yaml(yaml_file: str) -> None:
    try:
        # Extract model data
        model_file_path = "Yaml_parser/model.jsx"
        frontend_file_path = "Yaml_parser/ClassView.jsx"
        customization = yaml_file.get("customization", [])
        model_array = [ms["microservice"]["model"] for ms in customization]

        new_lines = [create_model_line(element) for elements in model_array for element in elements]
        new_cards = [
            add_info_card(element)
            for elements in model_array
            for element in elements
            if element.get("uiElement") == "infocard"
        ]

        # Update files
        modify_file(model_file_path, new_lines, "// @generation**")
        modify_file(frontend_file_path, new_cards, "{/*generate Info Card*/}")

        print("Files updated successfully.")

    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except ValueError as e:
        print(f"Validation error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def modify_file(file_path: str, content: List[str], marker: str) -> None:
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

        updated_lines = []
        marker_found = False

        for line in lines:
            updated_lines.append(line)
            if marker in line:
                updated_lines.extend(content)
                marker_found = True

        if not marker_found:
            raise ValueError(f"Marker '{marker}' not found in {file_path}. Please add the marker to the file.")

        with open(file_path, 'w') as file:
            file.writelines(updated_lines)

    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
        raise
    except Exception as e:
        print(f"An error occurred while modifying the file: {e}")
        raise


def create_model_line(element: Dict[str, Any]) -> str:
    model_field = element.get("modelField")
    field_type = element.get("type")

    if not model_field or not field_type:
        raise ValueError(f"Invalid element: {element}")

    return f"  {model_field}: {{ type: {field_type.capitalize()} }},\n"


def add_info_card(element: Dict[str, Any]) -> str:
    headline = element.get("friendlyName", "Default Headline")
    content_type = element.get("content")
    model_name = element.get("modelField")

    if not headline or not content_type or not model_name:
        raise ValueError(f"Invalid InfoCard element: {element}")

    base_card = f"<InfoCard headline='{headline}'"

    match content_type:
        case "url":
            # return f"{base_card} link={{customization.{model_name}}} >\n"
            return (
                f"{base_card} url={{customization?.{model_name}}} >\n"
                f"  <div>\n"
                f"    <h3 className=\"text-lg font-semibold mb-2\">Edit Link</h3>\n"
                f"    <input\n"
                f"      type=\"text\"\n"
                f"      value={{customization?.{model_name} || \"\"}}\n"
                f"      onChange={{(e) => handleCustomizationChange(\"{model_name}\", e.target.value)}}\n"
                f"      placeholder=\"Enter new Value\"\n"
                f"      className=\"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500\"\n"
                f"    />\n"
                f"  </div>\n"
                f"</InfoCard>\n"
            )
        case "text":
                        return (
                f"{base_card} info={{customization?.{model_name}}} >\n"
                f"  <div>\n"
                f"    <h3 className=\"text-lg font-semibold mb-2\">Edit Link</h3>\n"
                f"    <input\n"
                f"      type=\"text\"\n"
                f"      value={{customization?.{model_name} || \"\"}}\n"
                f"      onChange={{(e) => handleCustomizationChange(\"{model_name}\", e.target.value)}}\n"
                f"      placeholder=\"Enter new Value\"\n"
                f"      className=\"w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500\"\n"
                f"    />\n"
                f"  </div>\n"
                f"</InfoCard>\n"
            )
        case _:
            print(f"Warning: Unsupported content type '{content_type}' for InfoCard.")
            return ""


def validate_yaml(data: Dict[str, Any], rules: Dict[str, List[str]]) -> bool:

    valid_categories = set(rules["valid_categories"])
    valid_types = set(rules["valid_types"])
    valid_contents = set(rules["valid_contents"])
    valid_ui_elements = set(rules["valid_ui_elements"])
    required_microservice_keys = set(rules["required_microservice_keys"])
    required_model_keys = set(rules["required_model_keys"])

    if not isinstance(data, dict) or "customization" not in data:
        print("Error: Top-level key must be 'customization'.")
        return False

    customization = data["customization"]

    if not isinstance(customization, list):
        print("Error: 'customization' must be a list.")
        return False

    for item in customization:
        if not isinstance(item, dict) or "microservice" not in item:
            print("Error: Each item in 'customization' must be a dictionary with a 'microservice' key.")
            return False

        microservice = item["microservice"]

        if not isinstance(microservice, dict) or set(microservice.keys()) != required_microservice_keys:
            print(f"Error: 'microservice' must contain only {required_microservice_keys}. Found: {microservice.keys()}.")
            return False

        category = microservice["category"]
        if category not in valid_categories:
            print(f"Error: Invalid 'category' value: {category}. Must be one of {valid_categories}.")
            return False

        model = microservice["model"]
        if not isinstance(model, list):
            print("Error: 'model' must be a list.")
            return False

        for element in model:
            if not isinstance(element, dict) or set(element.keys()) != required_model_keys:
                print(f"Error: Each 'model' element must contain only {required_model_keys}. Found: {element.keys()}.")
                return False

            if element["type"] not in valid_types:
                print(f"Error: Invalid 'type' value: {element['type']}. Must be one of {valid_types}.")
                return False

            if element["content"] not in valid_contents:
                print(f"Error: Invalid 'content' value: {element['content']}. Must be one of {valid_contents}.")
                return False
            
            if element["uiElement"] not in valid_ui_elements:
                print(f"Error: Invalid 'content' value: {element['uiElement']}. Must be one of {valid_ui_elements}.")
                return False

    print("YAML data is valid.")
    return True
