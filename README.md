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
Run following command to run

``` bash
python app.py
```