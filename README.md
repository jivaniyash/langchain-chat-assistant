# Langchain - Gen AI - Assistant using OpenAI

![](https://github.com/jivaniyash/langchain-chat-assistant/blob/main/images/image.jpg)
---
## Steps

### 1. Configure OpenAI API Key
Create an API key from [openai.com](https://platform.openai.com/api-keys)

### 2. Create & Activate Virtual Env
Open a new terminal
```sh
sudo apt install python3.11-venv
python3 -m venv .venv
source ./.venv/bin/activate
python3 -m pip install --upgrade pip
```

### 3. Install Packages
```sh
pip install chainlit langchain_openai langchain
``` 

### 4. Clone Git Repo
```sh
git clone https://github.com/jivaniyash/langchain-chat-assistant.git
```

### 5. Run the script
```sh
chainlit run ./app/main_openai.py -w
```
`-w` flag to enable auto-reloading

Please follow instructions if you want to run local LLM from [README-ollama.md](https://github.com/jivaniyash/langchain-chat-assistant/blob/main/README-ollama.md)