from pydantic import BaseModel
from typing import List, Optional, Union
import requests
import json
import os


# Define struct for request
class ChatRequest(BaseModel):
    model: str
    messages: Union[dict, str]
    stream: bool

# Define struct for response
class ChatResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool

# Struct for stream enabled
class GenStreamChunk(BaseModel):
    response: str = ""
    done: bool = False

def compile_messages(
        question: str, 
        response: Optional[str], 
        stored_messages: Optional[dict]) -> dict:
    if stored_messages:
        pass
    elif response:
        conversation = \
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                },
                {
                    "role": "assistant",
                    "content": response
                }
            ]
        }
    else:
        conversation = \
            {
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            }
    return conversation

def save_messages(messages: dict) -> None:
    if not os.isdir("./saved_messages"):
        os.mkdir("./saved_messages")

    with open("./saved_messages/conversation1.json", "w") as f:
        messages = json.dumps(messages)
        f.write(messages)

def load_messages() -> dict:
    with open("./saved_messages/conversation1.json", "r") as f:
        messages = f.read()
        messages = json.loads(messages)
        return messages

# Ollama call
def ollama_call(messages: dict, model: str, stream: bool) -> str:
    url = "http://localhost:11434/api/chat"
    payload = ChatRequest(model=model, messages=messages, stream=stream)

    # Send post
    response = requests.post(url=url, json=payload.model_dump(), stream=stream)
    response.raise_for_status() # Check for HTTP status code

    if stream:
        full_response = ""
        for line in response.iter_lines():
            if line:
                chunk = GenStreamChunk(**json.loads(line))
                print(chunk.response, end="", flush=True) # Print after each chunk
                full_response += chunk.response
        print()
        return full_response
    else:
        # Parse data
        data = ChatResponse(**response.json())
        return data.response


if __name__ == "__main__":
    model = "gemma3:4b"
    run = True # For CLI testing
    print("Type `quit` to end session.")
    while run:
        prompt = input(f"Enter prompt for {model}\n> ")

        if prompt == "quit":
            run = False
        else:
            data = ollama_call(messages=prompt, model=model, stream=True)
            print(f"{model}: {data}")

            if not os.path.isfile("./saved_messages/conversation1.json"):
                messages = compile_messages(question=prompt, response=data)
                save_messages(messages)
            else:
                previous_conversation = load_messages()
                messages = compile_messages(
                    question=prompt, 
                    response=data,
                    stored_messages=previous_conversation)
                save_messages(messages)
