from pydantic import BaseModel
from typing import List
import requests
import json


# Define struct for sending chat
class ChatRequest(BaseModel):
    model: str
    messages: dict
    stream: bool

# Define struct for recieving chat
class ChatResponse(BaseModel):
    model: str
    created_at: str
    message: dict
    done: bool

# Struct for stream
class ChatStreamChunk(BaseModel):
    message: dict
    done: bool = False

def format_message(prompt: str) -> dict:
    """
    """
    message = {"messages": [{
        "role": "user",
        "content": prompt
    }]}
    return message

def ollama_call(prompt: str, model: str, stream: bool) -> dict:
    """
    """
    # Note: url and model are hard coded.
    url = "http://localhost:11434/api/generate"

    message = format_message(prompt=prompt)
    print(message)
    payload = ChatRequest(model=model, message=message, stream=stream)
    print(payload)

    # Send request

    # Recieve response/chunks
    # Print chunks

    # Return response (As message format?)

if __name__ == "__main__":
    # NOTE: url and model are hard coded.
    model = "gemma3:4b"

    prompt = "Hello gemma3!"

    ollama_call(prompt=prompt, model=model, stream=True)
    