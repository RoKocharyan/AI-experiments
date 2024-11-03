from db_connect import connect_to_milvus, check_version, ensure_collection_exists, find_closest_question
from embedding_util import get_embedding, query_mistral

# Initialize and setup Milvus
connect_to_milvus()
check_version()
ensure_collection_exists()

# Process a user question, compare with existing questions in Milvus, and get a Mistral response
def process_question(question):
    # Generate embedding for the new question using CodeBERT
    embedding = get_embedding(question)

    # Find the closest question in the database based on cosine similarity
    closest_question = find_closest_question(embedding)
    if closest_question:
        print(f"Closest match found: '{closest_question}'")
    else:
        print("No similar question found in the database.")
        return

    # Send the closest question to Mistral for a response
    response = query_mistral(closest_question)
    return response

# Example usage
if __name__ == "__main__":
    print("Enter your question (type 'exit' to quit):")
    while True:
        user_question = input("> ")
        if user_question.lower() == "exit":
            print("Exiting program.")
            break
        
        response = process_question(user_question)
        if response:
            print(f"Mistral response: {response}")
        else:
            print("Failed to get a response from Mistral.")