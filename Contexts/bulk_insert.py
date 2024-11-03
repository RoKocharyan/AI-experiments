from db_connection import connect_to_milvus, ensure_collection_exists, insert_embedding
from embedding_util import get_embedding

# Connect to Milvus and ensure the collection exists
connect_to_milvus()
ensure_collection_exists()

# List of questions to be added to Milvus
questions = [
    "How can I improve my English speaking and pronunciation skills?",
    "How do I create recurring events in a calendar component?",
    "What’s the best way to practice English writing?",
    "Can you help me troubleshoot an SQL syntax error?",
    "How can I fetch data from an API in JavaScript?",
    "How do I handle user authentication in a web app?",
    "Can you give me feedback on my paraphrasing?",
    "What are the steps to implement a multi-step form in React?",
    "How do I style components using Tailwind CSS?",
    "Can you help me set up Google OAuth 2.0 for my project?",
    "What’s the best way to validate email and password fields?",
    "How can I optimize a function in Python?",
    "How do I translate my app using react-i18next?",
    "How can I create a chatbot with OpenAI’s API?",
    "How do I implement CAPTCHA verification in my form?",
    "Can you explain how to use the React Context API?",
    "How can I improve the styling of my website’s components?",
    "How do I handle form validation in JavaScript?",
    "What’s the most effective way to organize my project files?",
    "How do I make a fetch request to display deleted users only?",
    "How can I set up and connect to a Firebase database?",
    "Can you suggest improvements to my resume?",
    "How do I manage user roles and permissions in my app?",
    "How do I integrate a calendar view in my React app?",
    "What are some strategies to improve TOEFL scores?",
    "Can you help me understand WebRTC for video calls?",
    "How do I handle pagination in a table component?",
    "How can I manage a multi-language app in React?",
    "How do I design a responsive layout in HTML/CSS?",
    "What are the best practices for error handling in JavaScript?",
    "How do I fetch images from an API in a mobile app?",
    "Can you help me plan a TOEFL preparation schedule?",
    "How do I implement form validation in Swift?",
    "How can I improve my vocabulary for academic writing?",
    "How do I add a map component in a chat app?",
    "What’s the best way to optimize SQL queries?",
    "How do I troubleshoot failed backups in Rubrik?",
    "How can I add audio and video call functionality to my app?",
    "How do I manage event scheduling with recurring options?",
    "What are some basic CSS styling techniques for beginners?",
    "How can I use Firebase for user authentication in a web app?",
    "How do I upload files to AWS S3 from my app?",
    "How can I pass data between components in React?",
    "How do I manage user accounts in my admin dashboard?",
    "Can you give me feedback on my English essay?",
    "How do I handle form submission in a multi-step registration?",
    "How can I implement a custom theme for my website?",
    "How do I add a search filter in a table component?",
    "What’s the best way to debug JavaScript errors?",
    "Can you help me plan a website layout for a business?"
]

# Function to bulk insert questions into Milvus
def bulk_insert_questions():
    for question in questions:
        embedding = get_embedding(question)  # Generate embedding
        insert_embedding(embedding, question)  # Insert into Milvus
        print(f"Inserted question: '{question}' into Milvus with embedding.")

# Run the bulk insertion
if __name__ == "__main__":
    bulk_insert_questions()
    print("All questions have been successfully inserted into Milvus.")