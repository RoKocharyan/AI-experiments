import requests
from transformers import AutoTokenizer, AutoModel
import torch

# Load CodeBERT for embedding generation
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModel.from_pretrained("microsoft/codebert-base")

def get_embedding(question):
    # Tokenize and generate embeddings using CodeBERT
    inputs = tokenizer(question, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
        embedding = outputs.last_hidden_state[:, 0, :].squeeze().tolist()  # Use the [CLS] token
    return embedding

# Function to query Mistral model for a response using subprocess
def query_mistral(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt,"stream": False}
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract response text (which includes filename and code)
        response_text = result.get("response")
        return response_text
  
    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama API: {e}")



    #     def query_mistral(prompt):
    # try:
    #     result = subprocess.run(
    #         ["ollama", "run", "mistral"],
    #         input=prompt, 
    #         capture_output=True,
    #         text=True,
    #         encoding='utf-8', 
    #         check=True
    #     )
    #     return result.stdout.strip()
    # except subprocess.CalledProcessError as e:
    #     print(f"Error querying Mistral model: {e.stderr.strip()}")
    #     return None
    # except UnicodeDecodeError as e:
    #     print(f"Encoding error: {e}")
    #     return None
    # except Exception as e:
    #     print(f"Unexpected error querying Mistral: {e}")
    #     return None
