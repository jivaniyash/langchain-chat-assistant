import sys
import os
# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing necessary libraries
import chainlit as cl
from langchain_experimental.llms.ollama_functions import OllamaFunctions
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import SystemMessage
# from ..utils import functions
from utils.functions import get_current_weather, get_random_joke
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize the AI model
llm = OllamaFunctions(model="llama3.1", # change model name here
                    format="json", 
                    temperature=0.1)

# Define tools (functions) that can be called by the AI model
import json
with open('./utils/tools.json', 'r') as fp:
    tools = json.load(fp)

llm = llm.bind_tools(tools=tools)

with open ('./utils/systemPrompt.md', 'r') as fp:
    lines = fp.readlines()
    systemPrompt = ''.join(lines)

# Create the prompt template for the AI model
prompt = ChatPromptTemplate.from_messages([
    SystemMessage(content=systemPrompt),
    ("human", "{input}"),
])


# Function to process user queries
def process_query(query):
    """
    Processes user queries by invoking the AI model and calling appropriate functions.

    Args:
    query (str): The user's input query

    Returns:
    str: The response to the user's query
    """
    logging.info(f"Processing query: {query}")
    formatted_prompt = prompt.format_messages(input=query)
    logging.debug(f"Formatted prompt: {formatted_prompt}")
    result = llm.invoke(formatted_prompt)
    logging.info(f"Model result: {result}")

    if result.tool_calls:
        for tool_call in result.tool_calls:
            function_name = tool_call['name']
            args = tool_call['args']
            logging.info(f"Function call: {function_name}, Args: {args}")

            if function_name == "get_current_weather":
                return get_current_weather(**args)
            elif function_name == "get_random_joke":
                return get_random_joke()

    return result.content

# Chainlit event handler for chat start


@cl.on_chat_start
async def start():
    """
    Initializes the chat session.
    """
    logging.info("Chat started")
    cl.user_session.set("model", llm)

# Chainlit event handler for incoming messages


@cl.on_message
async def main(message: cl.Message):
    """
    Handles incoming user messages, processes them, and sends responses.

    Args:
    message (cl.Message): The incoming user message
    """
    logging.info(f"Received message: {message.content}")
    try:
        response = await cl.make_async(process_query)(message.content)
        logging.info(f"Response: {response}")
        await cl.Message(content=response).send()
    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(f"Error: {error_message}")
        await cl.Message(content=error_message).send()