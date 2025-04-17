import os
from dotenv import load_dotenv
from src.api_handler import OpenAIAPIRequestHandler
from src.db_handler import DBHandler
from src.chat_utils import chat, create_cache_for_session


# Load config
load_dotenv()
API_KEY = os.getenv("API_KEY", "")
BASE_URL = os.getenv("BASE_URL", None)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "27012"))
DB_NAME = os.getenv("DB_NAME", "terminal-chatbot")

# Create objects
llm_api_request_handler = OpenAIAPIRequestHandler(API_KEY, BASE_URL)
database_handler = DBHandler(DB_HOST, DB_PORT, DB_NAME)

# Command loop
current_session_id, current_session_name = None, None

while True:

    command = input("> ")
    command_words = command.strip().split(" ")

    if len(command_words) == 2 and command_words[0] == "new_chat":
        new_session_id = database_handler.start_new_session(command_words[1])
        if new_session_id is not None:
            current_session_id = new_session_id
            current_session_name = command_words[1]

            # Start chat
            chat(
                new_session_id,
                llm_api_request_handler,
                database_handler
            )
        else:
            print("FAILED TO CREATE NEW SESSION")

    elif len(command_words) == 2 and command_words[0] == "go_chat":
        session_name = command_words[1]
        all_session = database_handler.get_sessions()

        # Check if session exists
        found_session = None
        for session in all_session:
            if session[1] == session_name:
                found_session = session
                break
        if found_session is None:
            print(f"NO SESSION NAMED {session_name}")
            continue

        # Start chat
        chat(
            found_session[0],
            llm_api_request_handler,
            database_handler,
            create_cache_for_session(
                database_handler.get_session_chats(found_session[0]))
        )

    elif len(command_words) == 1 and command_words[0] == "list_sessions":
        all_sessions = database_handler.get_all_sessions()

        print("{:^50} {:^30} {:^30}".format("SESSION NAME", "CREATED DATE", "UPDATED DATE"))
        for session in all_sessions:
            print("{:^50} {:^30} {:^30}".format(
                session["session_name"], session["create_date"], session["last_update_date"]))

    elif len(command_words) == 1 and command_words[0] == "help":
        print("SUPPORTED COMMANDS ARE FOLLOWING:")
        print("1. Create a new session:\n\tnew_chat <session_name>")
        print("2. Attach to existing session:\n\tgo_chat <session_name>")
        print("3. List all existing sessions:\n\tlist_sessions")
        print("4. Help to use Terminal-Chat:\n\thelp")
        print("5. Exit back to main menu form session:\n\texit")
        print("6. Show history of current session:\n\tshow")
    else:
        print("NO VALID COMMAND")




