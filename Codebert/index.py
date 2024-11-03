from pymilvus import connections, Collection

# Step 1: Connect to Milvus
connections.connect("default", host="localhost", port="19530")
print("Connected to Milvus successfully!")

# Step 2: Load the collection
collection = Collection("CodebertDB")

# Step 3: Define and create the index
index_params = {
    "index_type": "HNSW",
    "metric_type": "COSINE",
    "params": {
        "M": 16,
        "efConstruction": 200
    }
}

# Create the HNSW index on the embedding field
collection.create_index(
  field_name="embedding",
  index_params=index_params,
  index_name="Embedding"
)

collection.load()
print("HNSW index created successfully on 'embedding' field.")