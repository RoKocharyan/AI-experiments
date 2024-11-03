from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
from embedding_util import query_mistral

# Connect to Milvus
def connect_to_milvus():
    try:
        connections.connect("default", host="localhost", port="19530")
        print("Connected to Milvus successfully!")
    except Exception as e:
        print(f"Connection error: {e}")

# Check Milvus server version
def check_version():
    try:
        version = utility.get_server_version()
        print(f"Milvus server version: {version}")
    except Exception as e:
        print(f"Error fetching server version: {e}")

# Ensure collection exists
def ensure_collection_exists():
    collection_name = "ContextDB"
    if collection_name not in utility.list_collections():
        print(f"Collection '{collection_name}' does not exist. Creating the collection.")
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=384),  # Updated to 384 dimensions
            FieldSchema(name="context", dtype=DataType.VARCHAR, max_length=512)
        ]
        schema = CollectionSchema(fields, description="Context collection")
        collection = Collection(collection_name, schema=schema)
        print(f"Collection '{collection_name}' created successfully.")
    else:
        print(f"Collection '{collection_name}' already exists. Skipping creation.")

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
        if similarity_percentage < 70:
            additional_prompt = "Please give more detailed information about your question"
            mistral_response = query_mistral(additional_prompt)
            print(f"{similarity_percentage:.2f}%")
            return mistral_response or additional_prompt
        
        # If similarity is above 70%, generate a response based on the closest match
        return f"Closest match: '{closest_match}' with {similarity_percentage:.2f}% similarity"
    
    return "No similar question found in the database."

# Insert embedding and text into Milvus
def insert_embedding(embedding, context_text):
    collection = Collection("ContextDB")
    data = [[embedding], [context_text]]
    collection.insert(data)
    collection.flush()  # Ensure data is written
    print("Embedding and context text inserted successfully.")