from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI
#import gradio as gr
import sys
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


os.environ["OPENAI_API_KEY"] = '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'

def construct_index(directory_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 200
    chunk_size_limit = 1000

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk('index.json')

    return index

def chatbot(input_text):
    index = GPTSimpleVectorIndex.load_from_disk('index.json')

    # Check if the input_text is empty or too short
    if not input_text.strip():
        return "I'm sorry, but I need more information to assist you."

    response = index.query(input_text, response_mode="compact")

    # Check if the response is empty or too short (indicating a lack of context)
    if not response.response.strip():
        return "I'm not sure how to respond to that. Could you please provide more details?"

    # Check if the response does not end with the specified string
    if not response.response.strip().endswith("is not mentioned in the context information."):
        return response.response

    return "So sorry can't answer that question right now, please be more specific."

@app.route('/api/chatbot', methods=['POST'])
def chatbot_endpoint():
    try:
        # Get the input text from the JSON payload
        payload_data = request.get_json()
        input_text = payload_data.get('input_text')

        if not input_text:
            return jsonify({'error': 'Missing input_text in the payload'}), 400

        # Call your chatbot function with the input text
        response = chatbot(input_text)

        # Return the chatbot's response in the JSON format
        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'error': 'An error occurred while processing the request.'}), 500
if __name__ == '__main__':
    app.run(host='192.168.43.54', port=5000, debug=False)



#index = construct_index("docs")


    