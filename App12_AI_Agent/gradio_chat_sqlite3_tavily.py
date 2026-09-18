import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import gradio as gr
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver

# Load environment variables and find the project directory.
BASE_DIR = Path(__file__).resolve().parent
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")


# Return today's date in the India/Kolkata timezone.
def get_date():
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")


# Tool for up-to-date web searches.
search_tool = TavilySearchResults()
# SQLite stores conversation state for the agent.
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
# Tell the agent how to behave and when to use its tools.
system_prompt = """
You are a helpful witty assistant.
Answer all user queries in short and simple (less than 50 words).
If the user is explicitly asking about today's date, use get_date tool.
Use the search_tool for answering questions that require up-to-date information.
"""
# Create the agent with tools and persistent memory.
agent = create_agent(
    model=llm,
    tools=[get_date, search_tool],
    system_prompt=system_prompt,
    checkpointer=checkpointer,
)


# Handle a message from the Gradio chat interface.
def chat(message, history, thread_id):
    # Tell LangGraph which conversation's memory to use.
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
    # Return the agent's final message to Gradio.
    return response["messages"][-1].content


# Build the Gradio interface.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # Give each chat session a unique conversation ID.
    thread_id = gr.State(lambda: str(uuid.uuid4()))
    # Connect the chat UI to our chat() function.
    gr.ChatInterface(
        fn=chat,
        additional_inputs=[thread_id],
    )
# Start the application.
demo.launch()
