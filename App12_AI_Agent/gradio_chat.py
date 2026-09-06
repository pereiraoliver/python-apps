import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gradio as gr
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Load environment variables and retrieve the OpenAI API key.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Tool that returns today's date in the India/Kolkata timezone.
def get_date():
    """Get the current date."""
    print("I was called")
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")


# Initialize the language model that will power the chatbot.
llm = ChatOpenAI(model="gpt-5.6-luna", api_key=OPENAI_API_KEY, use_responses_api=True)
# Define the agent's behavior and provide instructions for using the date tool.
system_prompt = """
You are a helpful witty assistant.
Answer all user queries in short and simple (less than 50 words).
If the user is asking about today's date, use get_date tool.
"""
# Create the LangChain agent and give it access to the date tool.
agent = create_agent(model=llm, tools=[get_date], system_prompt=system_prompt)


# Handle each chat message by converting the conversation history
# into LangChain's expected message format and invoking the agent.
def chat(message, history):
    # Convert Gradio's history format into LangChain's message format.
    messages = [
        {"role": item["role"], "content": item["content"][0]["text"]}
        for item in history
    ]
    # Add the current user message to the conversation.
    messages.append({"role": "user", "content": message})
    # Run the agent with the complete conversation.
    response = agent.invoke({"messages": messages})
    # Return the agent's latest response to Gradio.
    return response["messages"][-1].content


# Build the Gradio chatbot interface and connect it to the chat function.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    gr.ChatInterface(fn=chat)
# Start the Gradio application.
demo.launch()
