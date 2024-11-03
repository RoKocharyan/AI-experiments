from pymilvus import Collection
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')  # Higher-dimension model optimized for semantics

def get_embedding(question):
    # Generate a context-rich embedding for the question
    embedding = model.encode(question)
    return embedding.tolist()

# Function to find the closest match in Milvus using cosine similarity
def find_closest_question(embedding, top_k=1):
    collection = Collection("ContextDB")
    search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    
    # Run the search with the provided embedding
    results = collection.search(
        data=[embedding],
        anns_field="embedding",
        param=search_params,
        limit=top_k,
        output_fields=["context"]
    )
    
    # Check if we have results
    if results and results[0]:
        # Retrieve the closest match's question text and similarity score
        closest_match = results[0][0].entity.get("context")
        similarity_score = results[0][0].distance
        similarity_percentage = similarity_score * 100  # Convert cosine similarity to percentage
        
        # Print or handle the similarity and context text
        # if similarity_percentage > 10:
        #     return "Please give me more details"
        # else:
        return closest_match, similarity_percentage
    return None, None

# Process a user question, compare with existing questions in Milvus, and get a Mistral response
def process_question(question):
    # Step 1: Generate embedding for the new question
    embedding = get_embedding(question)

    # Step 2: Find the closest question in the database based on cosine similarity
    closest_match, similarity_percentage = find_closest_question(embedding)
    
    if closest_match and similarity_percentage is not None:
        return f"Closest match: '{closest_match}' with {similarity_percentage:.2f}% similarity"
    else:
        return "Not found"