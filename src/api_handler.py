from openai import OpenAI
from google import genai


class OpenAIAPIRequestHandler:

    def __init__(self, api_key: str, base_url: str = None):

        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key,
        )

    def send_request(self, message: str, model: str, system_role: str = None):

        if len(model) == 0:
            raise Exception("NO VALID MODEL")

        request_messages = []
        if system_role is not None:
            request_messages.append(
                {
                    "role": "system",
                    "content": system_role
                }
            )

        request_messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        )

        completion = self.client.chat.completions.create(
            extra_headers={},
            extra_body={},
            model=model,
            messages=request_messages
        )

        # print(completion)
        # print(completion.choices[0].message.content)

        return completion
