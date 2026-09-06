import os
from datetime import datetime
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

load_dotenv()


def get_date():
    """Get today's date in India."""
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")


llm = ChatOpenAI(
    model="gpt-5.6-luna",
    api_key=os.getenv("OPENAI_API_KEY"),
    use_responses_api=True,
)

agent = create_agent(
    model=llm,
    tools=[get_date],
    system_prompt="You are a helpful assistant.",
)

query = input("Enter a query: ")

response = agent.invoke({"messages": [{"role": "user", "content": query}]})

print(response["messages"][-1].content[0]["text"])
