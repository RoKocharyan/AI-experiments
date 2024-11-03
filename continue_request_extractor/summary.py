import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/api/chat', methods=['GET', 'POST'])
@app.route('/api/generate', methods=['GET', 'POST'])
def handle_request():
    # Capture request body
    request_body = request.get_data(as_text=True)

    try:
        # Parse the request body as JSON
        parsed_body = json.loads(request_body)

        # Process "content" field and save it to a separate file
        if "messages" in parsed_body:
            for message in parsed_body["messages"]:
                if "content" in message:
                    # Format the content to be more readable
                    content = message["prompt"].replace("\\r\\n", "\n").replace("\\n", "\n")

                    # Write the decoded content to a new file with UTF-8 encoding
                    with open('decoded_content.py', 'w', encoding='utf-8') as decoded_file:
                        decoded_file.write(content)

                    # Update the message content in the JSON for logging
                    message["content"] = content

        # Save the parsed JSON body to a summary log file in a pretty-printed format
        with open('summary.json', 'a', encoding='utf-8') as json_file:
            json.dump(parsed_body, json_file, indent=2)
            json_file.write('\n')  # Add a newline for each entry

    except json.JSONDecodeError:
        print("Invalid JSON received.")

    # Respond with a simple message
    return "Request received!"


if __name__ == '__main__':
    # Listen on port 5000
    app.run(host='0.0.0.0', port=5000)
