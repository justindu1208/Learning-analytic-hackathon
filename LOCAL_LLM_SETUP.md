# Local LLMs with Ollama. Quick Start Guide

Ollama lets you run open-source language models (like Llama 3, Mistral, etc.) locally on your laptop. No API keys or internet is required.

## 1. Install Ollama
- Click on https://ollama.com/download and download the Ollama installer
- Open the installer and follow the on-screen steps
- After installation, open your terminal and verify:
  ```bash
  ollama --version
  ```
  You should see something like:
  ```
  ollama version 0.1.x
  ```
- If you get “command not found” or similar, re-run the installer.
  

## 2. Pick a model from the library
- Browse the full model list here: https://ollama.com/library
- You must pull a model before you can chat or run code. For example, you can pull these models:
  ```bash
  ollama pull llama3.2:3b       # Small, fast, good for most use-cases (2 GB)
  ollama pull mistral:7b        # Higher quality, needs more memory (4.4 GB)
  ollama pull nomic-embed-text  # For embeddings / RAG tasks
  ```
- To see the list of models you installed, run in the terminal:
  ```bash
  ollama list
  ```
- To delete a model, run:
  ```bash
  ollama rm llama3.2:3b #remove llama3.2:3b model
  ```
## 3. Python Setup

- We recommend creating a clean Python environment for your project. (If you’re new to this, see the separate [Setup/SETUP_ENVIRONMENT.md](Setup/SETUP_ENVIRONMENT.md) guide in this repo.)
- Run this command in the terminal to see if the ollama Python package is installed already:
```bash
pip show ollama
```
- If it's not installed, run this command to install the package:
```bash
pip install ollama
```

## 4. Activate Ollama

Ollama runs as a local service that serves models to your terminal and Python scripts.

- **On macOS / Linux:**
Open a new terminal window and start the Ollama service manually:
```bash
ollama serve
```
Leave this window open — it’s your local LLM server.

- **On Windows:**
  Simply open the Ollama desktop app, which automatically starts the local service in the background.
  You can also run the same command in the terminal only if the app is closed.


## 5. Chat with Ollama in the Terminal

- Open a new tab in the terminal and run:
```bash
ollama run llama3.2:3b #or model that you pulled
```
- You'll be able to start chatting with the model and see:
```python-repl
>>>
```
- You can also give the model a role:
```bash
ollama run llama3.2:3b -r 
>>> /set system "You are a helpful data assistant."
```
- To stop the session, press **Ctrl + d**

## 6. Chat with Ollama from Python

Here is a simple example on how to use Ollama within your Python code:

```python
# file: demo_ollama.py
from ollama import Client

client = Client(host='http://localhost:11434')

# Store the user prompt in a variable
user_prompt = "Explain local LLMs in one short paragraph."

response = client.chat(
    model='llama3.2:3b',
    messages=[
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": user_prompt}
    ]
)

print(response['message']['content'])
```

- Run your file. For example, in the terminal run:
```bash
python demo_ollama.py
```

## 7. Tool Calling Example

The model can call your own Python functions (tools). It is a powerful way to integrate LLM into your code. Here’s a simple example:

```python
# demo_tools_llama32.py
from ollama import Client

client = Client(host='http://localhost:11434')

def get_weather(city: str):
    # Dummy implementation – replace with a real API call if you want
    return {"city": city, "summary": "Light rain", "temp_c": 13}

tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get current weather for a city",
        "parameters": {
            "type": "object",
            "properties": {"city": {"type": "string"}},
            "required": ["city"]
        }
    }
}]

messages = [{"role": "user", "content": "Do I need an umbrella in London today?"}]

resp = client.chat(model="llama3.2:3b", messages=messages, tools=tools)
tool_calls = (resp.get("message") or {}).get("tool_calls") or []

if tool_calls:
    # include the assistant message that requested the tool(s)
    messages.append(resp["message"])

    # execute requested tools and append results (no 'id' in Ollama; use tool_name)
    for call in tool_calls:
        fn = call["function"]["name"]
        args = call["function"].get("arguments", {}) or {}

        if fn == "get_weather":
            result = get_weather(args.get("city", ""))
        else:
            result = {"error": f"unknown tool {fn}"}

        messages.append({
            "role": "tool",
            "tool_name": fn,
            "content": str(result),
        })

    final = client.chat(model="llama3.2:3b", messages=messages)
    print(final["message"]["content"])
else:
    print(resp["message"]["content"])
```

- Run your file. For example, in the terminal run:
```bash
python demo_tools.py
```
- You can find more information on tooling here: https://ollama.com/blog/tool-support

## Use Streamlit + Ollama to create chatbots:
We recommend using Streamlit (Python library) to create a simple frontend for a chatbot powered by Ollama models.
- Install Streamlit (inside of your Python environment if you're using one):
```bash
pip install streamlit
```
- Example of Python code using Streamlit (frontend) and Ollama (LLM) to build a simple chatbot:

```python
#file: app.py
import streamlit as st
from ollama import Client

st.set_page_config(page_title="Local Chatbot", page_icon="🤖")
st.title("🤖 Local Chatbot")

# Connect to local Ollama
client = Client(host="http://localhost:11434")
MODEL = "llama3.2:3b"  # pull this first: ollama pull llama3.2:3b

# Chat state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"system","content":"You are a concise helpful assistant."}]

# Display history
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# User input
if prompt := st.chat_input("Ask me anything…"):
    st.session_state.messages.append({"role":"user","content":prompt})
    with st.chat_message("user"): st.markdown(prompt)

    # Call local model
    resp = client.chat(model=MODEL, messages=st.session_state.messages, options={"temperature":0.2})
    reply = resp["message"]["content"]

    st.session_state.messages.append({"role":"assistant","content":reply})
    with st.chat_message("assistant"): st.markdown(reply)

```
- In the terminal run:
```bash
streamlit run app.py
```
This will open a new tab in your default web browser showing your local chatbot interface, connected to your Ollama model running.
  
