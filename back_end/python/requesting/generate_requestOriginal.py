from pydantic import BaseModel
import requests
import json

# Define struct for request
class GenRequest(BaseModel):
    model: str
    prompt: str
    stream: bool

# Define struct for response
class GenResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool

# Struct for stream enabled
class GenStreamChunk(BaseModel):
    response: str = ""
    done: bool = False

def ollama_call(prompt: str, model: str, stream: bool) -> str:
    """
    Sends a prompt to the Ollama API and returns a generated response.

    Args:
        prompt (str): A text to be send to the Ollama model.
        model (str): Name of Ollama model requesting a response from.

    Returns:
        str: The reponse to the user's prompt.

    Raises:
        requests.excpetions.HTTPErorr: If the API request returns an HTTP error code.
    """
    # NOTE: url and model are hard coded.
    url = "http://localhost:11434/api/generate"
    payload = GenRequest(model=model, prompt=prompt, stream=stream)

    # Send post
    response = requests.post(url=url, json=payload.model_dump(), stream=stream)
    response.raise_for_status() # Check for HTTP status code

    if stream:
        full_response = ""
        # Iterate through recieved data
        for line in response.iter_lines():
            if line:
                chunk = GenStreamChunk(**json.loads(line)) # Unpack JSON to pydantic struct
                print(chunk.response, end="", flush=True) # Print after each chunk
                full_response += chunk.response
        print() # New line
        return full_response
    else:
        # Parse data
        data = GenResponse(**response.json())# Unpack JSON to pydantic struct
        return data.response
    

if __name__ == "__main__":
    # NOTE: url and model are hard coded.
    model = "gemma3:4b"
    run = True # For CLI testing
    print("Type `quit` to end session.")
    while run:
        prompt = input(f"Enter prompt for {model}\n> ")

        if prompt == "quit":
            run = False
        else:
            data = ollama_call(prompt=prompt, model=model, stream=True)
            print(f"Full response from {model}:\n{data}\n")
