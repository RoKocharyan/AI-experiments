import os
import subprocess
import requests
import re

def list_functions(directory="functions"):
    return [f for f in os.listdir(directory) if f.endswith(".py")]

def execute_file(file_path):
    try:
        subprocess.run(["python", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {file_path}: {e}")

def generate_new_function():
    # Step 2: Get user prompt for the function
    user_prompt = input("Describe the function you need (e.g., 'I need a function to calculate area of a rectangle'): ")
    
    # Add instruction to Ollama prompt for correct response format
    ollama_prompt = f"{user_prompt}\n\nYour response should consist of and name for the file that i should create and Python code containing only utf-8 charecters,starting from a new line no other description. The Python code should include a main function to allow CLI interaction and that function shloud be called only one time, no infinite loops. and only python code shloud be in code brackets name of the file should be outside without any brackets,"
    
    # Step 3: Call the Ollama API with TinyLlama model
    try:
        response = requests.post(
            "http://192.168.10.109:11434/api/generate",
            json={"model": "llama3.2", "prompt": ollama_prompt,"stream": False}
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract response text (which includes filename and code)
        response_text = result.get("response")
        #print(response_text)
        # Use regex to find filename and code within triple backticks (```...```)
        match = re.search(r"([a-zA-Z0-9_]+\.py)\s*```(?:python)?\s*(.*?)```", response_text, re.DOTALL)
        if match:
            filename, code = match.groups()
            file_path = os.path.join("functions", filename)
            
            # Save the code to a new Python file in the functions directory
            with open(file_path, "w") as f:
                f.write(code.strip())
            print(f"New function '{filename}' has been created.")
        else:
            print("Failed to parse the function filename and code. Please try again.")

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")

def main():
    functions_dir = "functions"
    functions = list_functions(functions_dir)

    while True:
        print("\nSelect an option:")
        for i, func in enumerate(functions, 1):
            print(f"{i}. {func}")
        print(f"{len(functions) + 1}. Generate new function")
        print("0. Exit")

        try:
            choice = int(input("Enter your choice: "))
            if choice == 0:
                print("Exiting...")
                break
            elif 1 <= choice <= len(functions):
                selected_function = functions[choice - 1]
                file_path = os.path.join(functions_dir, selected_function)
                print(f"\nRunning {selected_function}...\n")
                execute_file(file_path)
            elif choice == len(functions) + 1:
                generate_new_function()
                functions = list_functions(functions_dir)  # Refresh the menu with the new function
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main()
