import requests

# Define the base URL for the Ollama instance
OLLAMA_BASE_URL = "http://192.168.10.109:11434/api"  # Adjust port if necessary
MODEL_NAME = "llama3.2"

def ask_llama_for_clarification(user_request):
    # Prepare the prompt to guide Llama in generating a follow-up question
    prompt = (
        f"User request: '{user_request}'\n"
        "Please respond with a question that would help clarify or elaborate on the user's request."
    )
    
    # Define headers and payload for the Ollama API request
    headers = {"Content-Type": "application/json"}
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    
    # Send a request to the Ollama instance
    response = requests.post(f"{OLLAMA_BASE_URL}/generate", headers=headers, json=payload)
    
    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        # Extract the generated question from Llama's response
        clarification_question = result.get("response")
        return clarification_question
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

# Main function to interact with the user
if __name__ == "__main__":
    user_input = input("Enter your initial request: ")
    try:
        follow_up_question = ask_llama_for_clarification(user_input)
        print("Llama's follow-up question:", follow_up_question)
    except Exception as e:
        print("Error:", e)

