from uuid import uuid4
import datetime
import pymongo


class DBHandler:

    def __init__(self, host: str, port: int, db_name: str):
        self.client = pymongo.MongoClient(host, port)
        self.database = self.client.get_database(db_name)

    def start_new_session(self, name: str) -> [int | None]:

        if name is None:
            print("SELECT NAME FOR SESSION")
            return None

        new_session_id = str(uuid4())
        self.database["sessions"].insert_one(
            {
                "id": new_session_id,
                "session_name": name,
                "create_date": str(datetime.datetime.now()),
                "last_update_date": str(datetime.datetime.now()),
                "chats": []
            }
        )

        return new_session_id

    def update_session(self, session_id, prompt, response):

        self.database["sessions"].update_one(
            {"id": session_id},
            {
                "$set": {
                    "last_update_date": str(datetime.datetime.now())
                },
                "$push": {
                    "chats": {
                        "request": prompt,
                        "response": response,
                        "chat_date": str(datetime.datetime.now())
                    }
                }
            }
        )

    def get_sessions(self) -> list[tuple[str, str]]:

        sessions_list = list(self.database["sessions"].find())
        sessions_info = [(session["id"], session["session_name"]) for session in sessions_list]

        return sessions_info

    def get_all_sessions(self) -> list[tuple[str, str]]:

        sessions_list = list(self.database["sessions"].find())

        return sessions_list

    def get_session_chats(self, session_id) -> list[dict]:

        session = self.database["sessions"].find_one({"id": session_id})
        return session["chats"]
