import yaml

def process_yaml_and_update_model(yaml_file_path, model_file_path, marker):
    """
    Reads a YAML file, processes each element of the model array, 
    and updates a model.jsx file by adding new lines after a specific marker.

    :param yaml_file_path: Path to the YAML file.
    :param model_file_path: Path to the model.jsx file to be updated.
    :param marker: The line in the model.jsx file after which new lines will be added.
    """
    try:
        # Step 1: Read and parse the YAML file
        with open(yaml_file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
        
        # Extract the model array
        model_array = yaml_data.get('customization', {}).get('model', [])
        if not model_array:
            raise ValueError("No 'model' array found in the YAML file.")

        # Step 2: Read the model.jsx file
        with open(model_file_path, 'r') as model_file:
            lines = model_file.readlines()

        # Step 3: Prepare new lines to add
        new_lines = []
        for element in model_array:
            model_field = element.get('modelField', 'unknownField')
            field_type = element.get('type', 'string')
            # Generate the new line to add to the schema
            new_lines.append(f"  {model_field}: {{ type: {field_type.capitalize()} }},\n")

        # Step 4: Insert new lines after the marker
        updated_lines = []
        marker_found = False

        for line in lines:
            updated_lines.append(line)
            if marker in line:
                updated_lines.extend(new_lines)  # Add the new lines after the marker
                marker_found = True

        if not marker_found:
            raise ValueError(f"Marker '{marker}' not found in the file.")

        # Step 5: Write the updated content back to the model.jsx file
        with open(model_file_path, 'w') as model_file:
            model_file.writelines(updated_lines)

        print("Model file updated successfully.")

    except FileNotFoundError as e:
        print(f"Error: File not found. {e}")
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def addInfoCard (headline, name, type, payload):
    newCard = "<InfoCard headline='User count' info={users.length} />" 
    match type:
        case "url":
            return "zero"
        case "img":
            return "one"
        case "text":
            return "two"
        case _:
            return "unknown"

if __name__ == "__main__":
    file_path = "model.jsx"
    marker = "// @generation**"
    process_yaml_and_update_model("example.yaml","model.jsx",marker)