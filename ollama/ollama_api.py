import os
import configparser
import requests
import httpx
import json
import asyncio
import requests
from dotenv import load_dotenv

load_dotenv(override=True)


OLLAMA_BASE_URL = os.getenv("OLLAMA_HOST")


def ollama_create_model(prompt, new_model_name, base):
    headers = {"Content-Type": "application/json"}
    # Correctly formatting the "modelfile" with supported commands
    modelfile_content = f"FROM {base}\nSYSTEM \"{prompt}\""  # Ensure SYSTEM uses valid quotes
    
    # Debug: Print the modelfile content
    print("Generated modelfile content:")
    print(modelfile_content)
    
    data = {
        "name": new_model_name,  # Corrected syntax for model name
        "modelfile": modelfile_content  # Passing the generated modelfile
    }
    
    # Make POST request to Ollama API to create the model
    response = requests.post(f"{OLLAMA_BASE_URL}/api/create", headers=headers, json=data)
    print(OLLAMA_BASE_URL + 'create')
    
    # Debug: Print the raw response content
    print("Raw response content:")
    print(response.text)
    
    # Handle response
    if response.status_code == 200:
        try:
            result = response.json()
            # Extract and return a meaningful result, e.g., model ID or success message
            print("Model created successfully:", result)
            return result
        except requests.exceptions.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            raise Exception(f"Invalid JSON response: {response.text}")
    else:
        # Handle errors with detailed feedback
        error_message = f"Error {response.status_code}: {response.text}"
        print(error_message)
        raise Exception(error_message)

def ollama_generate(prompt, model):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_BASE_URL}/api/generate/", headers=headers, json=data)
    
    # Check for successful response
    if response.status_code == 200:
        result = response.json()
        # Extract the generated question from Llama's response
        answer = result.get("response")
        # print(clarification_question)
        return answer
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

def ollama_chat(messages, model):
    headers = {"Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": messages
        
    }
    response_text = ""
    try:
        with requests.post(OLLAMA_BASE_URL + "/api/chat/", headers=headers, json=data, stream=True) as response:
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
                        
        return("asistant", response_text)
    except requests.exceptions.RequestException as e:
        return e
    
async def ollama_chat_stream(messages, model):
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    body = {
        "model": model,
        "messages": messages
    }
    response_message = ""  # Variable to store the assistant's response content
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", OLLAMA_BASE_URL + "/api/chat", headers=headers, json=body) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        # Parse the line as JSON and extract the "content"
                        try:
                            data = json.loads(line)
                            content = data.get("message", "").get("content" , "")
                            print(content)
                            response_message += content
                        except json.JSONDecodeError:
                            # Handle cases where the line is not valid JSON
                            pass
                        # Stream the data to the client
                        yield f"data: {line}\n\n"
                
                # Once the response is fully received, add to MESSAGES
                if response_message:
                    async with LOCK:  # Ensure thread safety
                        messages.append({"role": "assistant", "content": response_message})
                        

        except httpx.RequestError as exc:
            yield f"data: Error connecting to Ollama API: {exc}\n\n"
        except httpx.HTTPStatusError as exc:
            yield f"data: HTTP error: {exc.response.status_code} {exc.response.text}\n\n"
