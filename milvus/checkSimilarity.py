from pymilvus import Collection, connections
from sentence_transformers import SentenceTransformer
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access values from the configuration file
db_collection = config.get('Database', 'db_collection')
host = config.get('Database', 'db_host')
port = config.get('Database', 'db_port')

# Return a dictionary with the retrieved values

model = SentenceTransformer('all-MiniLM-L6-v2')  # Higher-dimension model optimized for semantics
def connect_to_milvus():
    try:
        connections.connect("default", host=host, port=port)
        print("Connected to Milvus successfully!")
    except Exception as e:
        print(f"Connection error: {e}")

def get_embedding(question):
    # Generate a context-rich embedding for the question
    embedding = model.encode(question)
    return embedding.tolist()

# Function to find the closest match in Milvus using cosine similarity
def find_closest_entries(embedding, limit=1):
    collection = Collection(db_collection)
    collection.load()
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    
    # Run the search with the provided embedding
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param=search_params,
        limit=limit,
        output_fields=["sample_prompt"]
    )
    
    # Check if we have results
    if results and results[0]:
        # Retrieve the top `top_k` matches' question text and similarity scores
        matches = []
        for hit in results[0]:  # Iterate over the top_k results
            sample_prompt = hit.entity.get("sample_prompt")
            template_id = hit.entity.get("template_id")
            similarity_score = hit.distance
            similarity_percentage = similarity_score * 100  # Convert cosine similarity to percentage
            matches.append({"sample_prompt": sample_prompt, "similarity": similarity_percentage, "template_id": template_id})
        
        return matches  # Return a list of results
    
    return []  # Return an empty list if no results


# Process a user question, compare with existing questions in Milvus, and get a Mistral response
def checkSimilarity(question):
    # Step 1: Generate embedding for the new question
    connect_to_milvus()
    embedding = get_embedding(question)

    # Step 2: Find the closest question in the database based on cosine similarity
    results = find_closest_entries(embedding, 5)
    
    for idx, result in enumerate(results):
        print(f"Rank {idx+1}:")
        print(f"Question: {result['sample_prompt']}")
        print(f"Similarity: {result['similarity']:.2f}%")
    if results  is not None:
        return results
    else:
        return "Not found" 