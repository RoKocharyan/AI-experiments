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
def find_closest_question(embedding, top_k=1):
    collection = Collection(db_collection)
    collection.load()
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    
    # Run the search with the provided embedding
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["sample_prompt"]
    )
    
    # Check if we have results
    if results and results[0]:
        # Retrieve the closest match's question text and similarity score
        closest_match = results[0][0].entity.get("sample_prompt")
        similarity_score = results[0][0].distance
        similarity_percentage = similarity_score * 100  # Convert cosine similarity to percentage
        
        # Print or handle the similarity and context text
        # if similarity_percentage > 10:
        #     return "Please give me more details"
        # else:
        return closest_match, similarity_percentage
    return None, None

# Process a user question, compare with existing questions in Milvus, and get a Mistral response
def checkSimilarity(question):
    # Step 1: Generate embedding for the new question
    connect_to_milvus()
    embedding = get_embedding(question)

    # Step 2: Find the closest question in the database based on cosine similarity
    closest_match, similarity_percentage = find_closest_question(embedding)
    
    if closest_match and similarity_percentage is not None:
        return closest_match, similarity_percentage
    else:
        return "Not found" 