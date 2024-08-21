import sys
import os
# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importing necessary libraries
import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage
from langchain_core.messages import AIMessage, HumanMessage
from utils.functions import get_current_weather, get_random_joke
import logging

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Chainlit event handler for chat start
@cl.on_chat_start
async def on_chat_start():
    """
    Initializes the chat session.
    """
    # Initialize the AI model
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.environ['OPEN_AI_API_KEY'],
        streaming=True)

    with open ('./utils/systemPrompt.md', 'r') as fp:
        lines = fp.readlines()
        systemPrompt = ''.join(lines)

    prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content=systemPrompt),
            ("placeholder", "{chat_history}"),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ]
    )
    tools = [get_random_joke, get_current_weather]

    # Construct the Tools agent
    agent = create_tool_calling_agent(llm, tools, prompt)

    # Create an agent executor by passing in the agent and tools
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    logging.info("Chat started")
    cl.user_session.set("agent_executor", agent_executor)
    cl.user_session.set("chat_history", [])

# Chainlit event handler for incoming messages
@cl.on_message
async def on_message(message: cl.Message):
    """
    Handles incoming user messages, processes them, and sends responses.

    Args:
    message (cl.Message): The incoming user message
    """
    logging.info(f"Received message: {message.content}")
    
    agent_executor: AgentExecutor = cl.user_session.get("agent_executor")
    chat_history: list = cl.user_session.get("chat_history")

    try:
        # Use AgentExecutor to process the message
        result = agent_executor.invoke({"input": message.content, "chat_history": chat_history})
        
        ai_message = result['output'] # parse the ai message
        # Send the response back to the user
        await cl.Message(content=ai_message).send()

        # Append the new user message to chat history
        chat_history.append(HumanMessage(content=message.content))

        # Append the AI's response to the chat history
        chat_history.append(AIMessage(content=ai_message))

        # Update the chat history in the user session
        cl.user_session.set("chat_history", chat_history)

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        logging.error(f"Error: {error_message}")
        await cl.Message(content=error_message).send()

@cl.on_chat_end
def on_chat_end():
    """
    Creates a log file when user gets disconnected or starts a new chat session.
    """
    from datetime import datetime

    now = datetime.now()
    log_filename = f"chat_log_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"

    # Define the log file path
    log_file_path = os.path.join('./logs', log_filename)

    # Ensure the logs directory exists
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    chat_history: list = cl.user_session.get("chat_history")
    # Write chat history to the log file
    with open(log_file_path, 'w') as log_file:
        for message in chat_history:
            if isinstance(message, HumanMessage):
                log_file.write(f"User: {message.content}\n")
            elif isinstance(message, AIMessage):
                log_file.write(f"AI: {message.content}\n")
            else:
                log_file.write(f"Unknown: {message.content}\n")

    logging.info(f"Chat log written to {log_file_path}")