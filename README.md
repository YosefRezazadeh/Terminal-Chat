# Terminal-Chat
A simple chat bot under terminal

## Installation
You can easily install it with following command
```bash
pip install requirements.txt
```

Then you should set your `API_KEY` environment variable, you can set it manually or put it in `.env` file.
There are another environment variables that can be set:

- `BASE_URL`: If you are using API from other providers you can set it
- `MODEL`: Your desired LLM
- `SYSTEM_ROLE`: Message will be considered for system role
- `MEMORY_TOP_K`: In this project chat memory is simply created by added last k-messages to current prompt. Default value of k is 3, but you can adjust it.

## Run
We use MongoDB to store messages between user and LLM API. We used MongoDB using Docker, but you can install it on your device. MongoDB container will be started with following error:

```bash
docker run --name mongodb -p 27017:27017 -v ~/mongo/data:/data/db -d mongodb/mongodb-community-server:latest
```

Run following command to run

``` bash
python app.py
```

## How to use
Terminal-Chat currently supports following commands:

```bash
> help
SUPPORTED COMMANDS ARE FOLLOWING:
1. Create a new session:
        new_chat <session_name>
2. Attach to existing session:
        go_chat <session_name>
3. List all existing sessions:
        list_sessions
4. Help to use Terminal-Chat:
        help
5. Exit back to main menu form session:
        exit
6. Show history of current session:
        show

```

