# from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

# # Connect to Milvus
# def connect_to_milvus():
#     try:
#         connections.connect("default", host="localhost", port="19530")
#         print("Connected to Milvus successfully!")
#     except Exception as e:
#         print(f"Connection error: {e}")

# # Check Milvus server version
# def check_version():
#     try:
#         version = utility.get_server_version()
#         print(f"Milvus server version: {version}")
#     except Exception as e:
#         print(f"Error fetching server version: {e}")

# # Ensure collection exists
# def ensure_collection_exists():
#     collection_name = "CodebertDB"
#     if collection_name not in utility.list_collections():
#         print(f"Collection '{collection_name}' does not exist. Creating the collection.")
#         fields = [
#             FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
#             FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),  # Set to CodeBERT's dimension
#             FieldSchema(name="context", dtype=DataType.VARCHAR, max_length=512)
#         ]
#         schema = CollectionSchema(fields, description="Context collection")
#         collection = Collection(collection_name, schema=schema)
#         print(f"Collection '{collection_name}' created successfully.")
#     else:
#         print(f"Collection '{collection_name}' already exists. Skipping creation.")

# # Function to find the closest match in Milvus using cosine similarity
# def find_closest_question(embedding, top_k=1):
#     collection = Collection("CodebertDB")
#     search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}
    
#     # Run the search with the provided embedding
#     results = collection.search(
#         data=[embedding],
#         anns_field="embedding",
#         param=search_params,
#         limit=top_k,
#         output_fields=["context"]
#     )
    
#     # Check if we have results
#     if results and results[0]:
#         # Retrieve the closest match's question text
#         closest_match = results[0][0].entity.get("context")
#         print(results)
#         return closest_match
#     return None

# # Insert embedding and text into Milvus
# def insert_embedding(embedding, context_text):
#     collection = Collection("CodebertDB")
#     data = [[embedding], [context_text]]
#     collection.insert(data)
#     collection.flush()  # Ensure data is written
#     print("Embedding and context text inserted successfully.")


from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility

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
    collection_name = "CodebertDB"
    if collection_name not in utility.list_collections():
        print(f"Collection '{collection_name}' does not exist. Creating the collection.")
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768),  # Set to CodeBERT's dimension
            FieldSchema(name="context", dtype=DataType.VARCHAR, max_length=512)
        ]
        schema = CollectionSchema(fields, description="Context collection")
        collection = Collection(collection_name, schema=schema)
        print(f"Collection '{collection_name}' created successfully.")
    else:
        print(f"Collection '{collection_name}' already exists. Skipping creation.")

def find_closest_question(embedding, top_k=5):
    ensure_collection_exists()  # Ensure the collection exists before searching
    collection = Collection("CodebertDB")
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
    matches = []
    if results and results[0]:
        print("Top 5 Similar Questions:")
        for i, result in enumerate(results[0]):
            # Retrieve the match's question text and similarity score
            match_text = result.entity.get("context")
            similarity_score = result.distance
            similarity_percentage = (1 - similarity_score) * 100  # Convert cosine similarity to percentage
            
            print(f"{i+1}. Question: {match_text}")
            print(f"   Similarity: {similarity_percentage:.2f}%")
            
            # Append to matches list for possible further processing
            matches.append((match_text, similarity_percentage))
        
    return matches

# Insert embedding and text into Milvus
def insert_embedding(embedding, context_text):
    collection = Collection("CodebertDB")
    data = [[embedding], [context_text]]
    collection.insert(data)
    collection.flush()  # Ensure data is written
    print("Embedding and context text inserted successfully.")