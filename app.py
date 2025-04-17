import os
from dotenv import load_dotenv
from src.api_handler import OpenAIAPIRequestHandler
from src.chat_cache import ChatCache

load_dotenv()
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", None)
MODEL = os.getenv("MODEL", "")
SYSTEM_ROLE = os.getenv("SYSTEM_ROLE", None)
MEMORY_TOP_K = int(os.getenv("MEMORY_TOP_K", "3"))

llm_api_request_handler = OpenAIAPIRequestHandler(API_KEY, BASE_URL)
chat_cache = ChatCache()

while True:

    message = input("> ")

    try:
        response = llm_api_request_handler.send_request(
            chat_cache.get_cache() + message,
            MODEL,
            system_role=SYSTEM_ROLE)

        response_text = response.choices[0].message.content
        print(f"\n{response_text}\n")

        chat_cache.insert((message, response_text))
    except:
        print("CHECK YOUR INTERNET CONNECTION OR YOUR QUOTA")
