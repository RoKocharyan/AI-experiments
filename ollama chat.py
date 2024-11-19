import requests
import json
#from milvus.checkSimilarity import process_question 
from extractCode import extractCode, overwrite_file
# Define the base URL for the Ollama instance
OLLAMA_BASE_URL = "http://192.168.10.109:11434/api/"  # Adjust port if necessary
MODEL_NAME = "llama3.2"
MESSAGES = []


def addMessage(role, content):
    message = { "role" : role, "content" : content }
    MESSAGES.append(message)
    return

def chat():
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "messages": MESSAGES
        
    }
    response_text = ""
    try:
        with requests.post(OLLAMA_BASE_URL + "chat/", headers=headers, json=data, stream=True) as response:
            response.raise_for_status()  # Check for request errors

            # Process each chunk in the streaming response
            for line in response.iter_lines():
                if line:
                    # Decode JSON and parse the line
                    message = json.loads(line.decode('utf-8'))

                    # Check if 'done' is True to stop the loop
                    if message.get("done"):
                        break

                    # Print the content immediately if it exists
                    if "message" in message and "content" in message["message"]:
                        word = message["message"]["content"]
                        response_text += word  # Append each word with a space
                        print(word, end='', flush=True)
                        
        addMessage("asistant", response_text)
    except requests.exceptions.RequestException as e:
        return e
    return 
def askQuestion(question):
    prompt = question
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_BASE_URL}generate/", headers=headers, json=data)
    
    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        # Extract the generated question from Llama's response
        clarification_question = result.get("response")
        #print(clarification_question)
        return clarification_question
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    

def summarizeConversation():
    prompt = (
        f"this is user conversation'{MESSAGES}'\n"
        "Please respond with a short user request description."
    )
    headers = {"Content-Type": "application/json"}
    data = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_BASE_URL}generate/", headers=headers, json=data)
    
    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        # Extract the generated question from Llama's response
        clarification_question = result.get("response")
        print(clarification_question)
        return clarification_question
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")
    return

def ask_llama_for_clarification(user_request):
    # Prepare the prompt to guide Llama in generating a follow-up question
    prompt = (
        f"User request: '{user_request}'\n"
        "Please respond with a question that would help clarify or elaborate on the user's request."
    )
    addMessage("user", prompt)
# Main function to interact with the user
if __name__ == "__main__":
    print("type 'exit' to quit")
    iteration = 0
    while True:
        request = input(">>>")
        if request == "exit":
            print("Exiting...")
            break
        response = askQuestion(request)
        code = extractCode(response)
        overwrite_file(code, "model.jsx")
        # if iteration < 4 :
        #     ask_llama_for_clarification(request)
        # else:
        #     summ = summarizeConversation()
        #     print(summ)
            
        #     # addMessage("user", request)
        # iteration += iteration + 1
        # chat()
        # print()


