from dotenv import load_dotenv
import os
from data_embed import *
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
import textwrap


from flask import Flask, request, jsonify

# Un comment this line only while running first time
# create_vectordb() # Calling funtion to create and store vector DB

# API key for hugging face
load_dotenv()
APIKEY = os.getenv('HF_API_TOKEN')


# Reading the stored vector DB
vectordb = Chroma(persist_directory=persist_directory, 
                  embedding_function=hf)

retriever = vectordb.as_retriever()
retriever = vectordb.as_retriever(search_kwargs={"k": 3})

# Using hugging face with llama model for the chatbot

repo_id = "meta-llama/Llama-3.2-1B-Instruct"
llm=HuggingFaceEndpoint(repo_id=repo_id,
                        max_length=128, temperature=1,
                        token= APIKEY)

# Prompt template to get the desired output format

prompt_template = """
Answer the given question as a robot assistant for the Brainlox website. depending on the question answer related to the data given.
If you don't know the answer, just say "I cannot answer this question" and don't try to make up an answer. Answer only once.


Question: {question}
Answer:
"""

prompt = PromptTemplate(
    template=prompt_template, 
    input_variables=[
        'question'
    ]
)


qa_chain = RetrievalQA.from_chain_type(llm=prompt|llm, 
                                  chain_type="stuff",
                                  retriever=retriever,
            )

def process_llm_response(text, width=110):
    # Split the input text into lines based on newline characters
    lines = text.split('\n')

    # Wrap each line individually
    wrapped_lines = [textwrap.fill(line, width=width) for line in lines]

    # Join the wrapped lines back together using newline characters
    wrapped_text = '\n'.join(wrapped_lines)

    return wrapped_text


# Flask Restfull api

app = Flask(__name__)

# Test api by sending post request to url/chat with the input message.
@app.route('/chat', methods=['POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form

        print(user_input)

        res = qa_chain({"query": user_input['message']})
        res = process_llm_response(res['result'])

        return jsonify({'response': res})


if __name__ == '__main__':
    app.run(port=5000)