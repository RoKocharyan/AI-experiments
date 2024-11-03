from sentence_transformers import SentenceTransformer
import requests

# Load a more semantically powerful model for sentence embedding
model = SentenceTransformer('all-MiniLM-L6-v2')  # Higher-dimension model optimized for semantics

def get_embedding(question):
    # Generate a context-rich embedding for the question
    embedding = model.encode(question)
    return embedding.tolist() 

# Function to query Mistral model for a response
def query_mistral(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        result = response.json()
        
        # Extract response text (which includes filename and code)
        response_text = result.get("response")
        return response_text
  
    except requests.exceptions.RequestException as e:
        print(f"Error calling Mistral API: {e}")
