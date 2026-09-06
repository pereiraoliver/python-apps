import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

model = init_chat_model(
    model="gpt-5.6-luna", model_provider="openai", api_key=OPENAI_API_KEY
)

response = model.invoke(
    "Give a one line answer for - Why did the chicken cross the road?"
)

print(response)
