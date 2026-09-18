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

# Get the project directory for storing the database.
BASE_DIR = Path(__file__).resolve().parent
# Load environment variables.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Return today's date in the India/Kolkata timezone.
def get_date():
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")


# Connect to SQLite for persistent conversation memory.
conn = sqlite3.connect(
    BASE_DIR / "chatbot_memory.db",
    check_same_thread=False,
)
checkpointer = SqliteSaver(conn)
# Initialize the language model.
llm = ChatOpenAI(
    model="gpt-5.6-luna",
    api_key=OPENAI_API_KEY,
    use_responses_api=True,
)
# Define the agent's behavior.
system_prompt = """
You are a helpful witty assistant.
Answer all user queries in short and simple (less than 50 words).
If the user is asking about today's date, use get_date tool.
"""
# Create the agent with the date tool and persistent memory.
agent = create_agent(
    model=llm,
    tools=[get_date],
    system_prompt=system_prompt,
    checkpointer=checkpointer,
)


# Handle messages from the Gradio chat interface.
def chat(message, history, thread_id):
    # Identify which conversation memory the agent should use.
    config = {"configurable": {"thread_id": thread_id}}
    # Send the user's message to the agent.
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": message,
                }
            ]
        },
        config,
    )
    # Return the agent's final response to Gradio.
    return response["messages"][-1].content


# Build the Gradio interface.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # Create a unique ID for this conversation.
    thread_id = gr.State(lambda: str(uuid.uuid4()))
    # Connect the chat UI to the chat() function.
    gr.ChatInterface(
        fn=chat,
        additional_inputs=[thread_id],
    )
# Start the application.
demo.launch()
