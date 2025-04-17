import os
from src.api_handler import OpenAIAPIRequestHandler
from src.chat_cache import ChatCache
from src.db_handler import DBHandler


def chat(
    session_id: str,
    llm_api: OpenAIAPIRequestHandler,
    db_handler: DBHandler,
    chat_cache: ChatCache = None
):

    model = os.getenv("MODEL", "")
    system_prompt = os.getenv("SYSTEM_ROLE", None)
    memory_top_k = int(os.getenv("MEMORY_TOP_K", "3"))

    if chat_cache is None:
        chat_cache = ChatCache(memory_top_k)

    while True:

        message = input("USER: ")
        message_words = message.strip().split(" ")

        if len(message_words) == 1 and message_words[0] == "exit":
            return
        elif len(message_words) == 1 and message_words[0] == "clear":
            os.system("clear")
        elif len(message_words) == 1 and message_words[0] == "show":
            session_chats = db_handler.get_session_chats(session_id)
            print("-"*20 + " START HISTORY " + "-"*20 + "\n")
            for chat_dict in session_chats:
                print(f"USER: {chat_dict['request']}\nCHAT-BOT: {chat_dict['response']}\n")
            print("-" * 20 + " END HISTORY " + "-" * 20 + "\n")
        else:
            try:
                response = llm_api.send_request(
                    chat_cache.get_cache() + message,
                    model,
                    system_prompt)
                print(response)
                response_text = response.choices[0].message.content
                print(f"\nCHAT-BOT: {response_text}\n")
                chat_cache.insert((message, response_text))
                db_handler.update_session(session_id, message, response_text)
            except:
                print("CHECK YOUR INTERNET CONNECTION OR YOUR QUOTA")


def create_cache_for_session(session_chats):

    memory_top_k = int(os.getenv("MEMORY_TOP_K", "3"))
    chat_cache = ChatCache(memory_top_k)

    if len(session_chats) <= 3:
        for chat_dict in session_chats:
            chat_cache.insert((chat_dict["request"], chat_dict["response"]))
    else:
        for chat_dict in session_chats[-3:]:
            chat_cache.insert((chat_dict["request"], chat_dict["response"]))

    return chat_cache
