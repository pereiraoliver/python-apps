import os
from datetime import datetime
from zoneinfo import ZoneInfo

import gradio as gr
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

# Load environment variables.
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# Return today's date in the India/Kolkata timezone.
def get_date():
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")


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
# Create the agent with access to the date tool.
agent = create_agent(
    model=llm,
    tools=[get_date],
    system_prompt=system_prompt,
)


# Handle messages from the Gradio chat interface.
def chat(message, history):
    # Convert Gradio history into LangChain's message format.
    messages = [
        {
            "role": item["role"],
            "content": item["content"][0]["text"],
        }
        for item in history
    ]
    # Add the current user message.
    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )
    # Send the conversation to the agent.
    response = agent.invoke({"messages": messages})
    # Return the agent's final response to Gradio.
    return response["messages"][-1].content


# Build the Gradio interface.
with gr.Blocks() as demo:
    gr.Markdown("# AI Chatbot")
    # Connect the chat UI to the chat() function.
    gr.ChatInterface(fn=chat)
# Start the application.
demo.launch()
