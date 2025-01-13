from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from milvus.checkSimilarity import checkSimilarity 
from file_operations import *
from ollama.ollama_api import *
import json
import httpx
import asyncio
import requests 

import configparser

config = configparser.ConfigParser()
config.read('config.ini')

OLLAMA_BASE_URL = config.get('Ollama', 'host')
MODEL_NAME = config.get('Ollama', 'model')

app = FastAPI()

# Thread-safe messages storage
MESSAGES = []
LOCK = asyncio.Lock()
iteration = 0

# Add CORS Middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body model validation
class ChatRequest(BaseModel):
    message: str

def add_message(role: str, content: str):
    MESSAGES.append({"role": role, "content": content}) 

async def stream_ollama_response(messages):
    headers = {
        "Content-Type": "application/json",
        "Accept": "text/event-stream",
    }
    body = {
        "model": MODEL_NAME,
        "messages": messages
    }
    response_message = ""  # Variable to store the assistant's response content
    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", OLLAMA_BASE_URL + "chat", headers=headers, json=body) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if line:
                        # Parse the line as JSON and extract the "content"
                        try:
                            data = json.loads(line)
                            content = data.get("message", "").get("content" , "")
                            # print(content + "")
                            response_message += content
                        except json.JSONDecodeError:
                            # Handle cases where the line is not valid JSON
                            pass
                        # Stream the data to the client
                        yield f"data: {line}\n\n"
                
                # Once the response is fully received, add to MESSAGES
                if response_message:
                    async with LOCK:  # Ensure thread safety
                        MESSAGES.append({"role": "assistant", "content": response_message})
                        

        except httpx.RequestError as exc:
            yield f"data: Error connecting to Ollama API: {exc}\n\n"
        except httpx.HTTPStatusError as exc:
            yield f"data: HTTP error: {exc.response.status_code} {exc.response.text}\n\n"

def ask_llama_for_clarification(user_request):
    # Prepare the prompt to guide Llama in generating a follow-up question
    prompt = (
        f"User request: '{user_request}'\n"
        "Please respond with a question that would help clarify or elaborate on the user's request. do not go in technical stuff"
    )
    add_message("user", prompt)

def summarizeConversation():
    prompt = (
        f"this is user conversation'{MESSAGES}'\n"
        "Please respond with a short user request description."
    )
    return ollama_generate(prompt, "llama3.2")



ITERATIONS = 0
# to run 
# uvicorn AiAssistant:app --host 0.0.0.0 --port 8000
# v1
@app.post("/chat")
async def chat(request: ChatRequest):
    global ITERATIONS
    async with LOCK:
        # Add the user's message
        add_message("user", request.message)
        if ITERATIONS  > 1 :
            summ = summarizeConversation()
            print(summ)
            result = checkSimilarity(summ)
            
            
        ITERATIONS = ITERATIONS + 1 
    # Stream the response from the Ollama API
    # print(MESSAGES)

    return StreamingResponse(stream_ollama_response(MESSAGES), media_type="text/event-stream")
#v2
# @app.post("/chat")
# async def chat(request: ChatRequest):
#     async with LOCK:
#         # Add the user's message
#         modifyModel(request.message)
#         #print(mmm)
#         #add_message("user", mmm)
        
#     # Stream the response from the Ollama API
#     return StreamingResponse(stream_ollama_response(MESSAGES), media_type="text/event-stream")

# to run 
# uvicorn AiAssistant:app --host 0.0.0.0 --port 8000

# if __name__ == "__main__":
#     print("type 'exit' to quit")
#     while True:
#         request = input(">>>")
#         if request == "exit":
#             print("Exiting...")
#             break
#         add_message("user", request)
#         stream_ollama_response(MESSAGES)
