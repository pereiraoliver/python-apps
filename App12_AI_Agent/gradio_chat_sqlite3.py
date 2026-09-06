import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import gradio as gr
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver

# Define the project directory so the database is stored alongside the application.
BASE_DIR = Path(__file__).resolve().parent
# Load environment variables and retrieve the OpenAI API key.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Tool that returns today's date in the India/Kolkata timezone.
def get_date():
    """Get the current date"""
    print("I was called")
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")


# Create a SQLite database connection that will be used to persist
# the agent's conversation state between messages.
conn = sqlite3.connect(BASE_DIR / "chatbot_memory.db", check_same_thread=False)
checkpointer = SqliteSaver(conn)
# Initialize the language model that will power the chatbot.
llm = ChatOpenAI(model="gpt-5.6-luna", api_key=OPENAI_API_KEY, use_responses_api=True)
# Define the agent's behavior and instructions for using the date tool.
system_prompt = """
You are a helpful witty assistant.
Answer all user queries in short and simple (less than 50 words).
If the user is asking about today's date, use get_date tool .
"""
# Create the agent with the language model, available tools,
# system instructions, and persistent conversation memory.
agent = create_agent(
    model=llm, tools=[get_date], system_prompt=system_prompt, checkpointer=checkpointer
)


# Handle each chat message by identifying the conversation thread,
# invoking the agent, and returning its latest response.
def chat(message, history, thread_id):
    # Use the thread ID to tell LangGraph which conversation
    # should be loaded from the SQLite checkpointer.
    config = {"configurable": {"thread_id": thread_id}}
    # Send the current user message to the agent.
    response = agent.invoke(
        {"messages": [{"role": "user", "content": message}]}, config
    )
    # Return the agent's latest response to Gradio.
    last_response = response["messages"][-1].content
    return last_response


# Build the Gradio chatbot interface and create a unique
# conversation ID for each new chat session.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # Store a unique ID that allows the agent to maintain
    # memory for this particular conversation.
    thread_id = gr.State(lambda: str(uuid.uuid4()))
    gr.ChatInterface(fn=chat, additional_inputs=[thread_id])
# Start the Gradio application.
demo.launch()
