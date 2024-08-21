# Langchain - Gen AI - Assistant using OLLAMA

---
## Steps

### 1. Install Ollama 
```sh
curl -fsSL https://ollama.com/install.sh | sh
ollama serve
```

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
pip install langchain-ollama langchain chainlit langchain_experimental
``` 

### 4. Clone Git Repo
```sh
git clone https://github.com/jivaniyash/langchain-chat-assistant.git
```

### 5. Download Model (if not exists inside model directory)
```sh
ollama pull llama3.1
```
If you want to use any other model, locate it from [ollama](https://ollama.com/search?c=tools). Make sure you change the model name in `./app/main-ollama.py`


### 6. Run the script
```sh
chainlit run ./app/main_ollama.py
```

### 7. Uninstall Ollama Packages

Remove the ollama service:
```sh
sudo systemctl stop ollama
sudo systemctl disable ollama
sudo rm /etc/systemd/system/ollama.service
```
Remove the ollama binary from your bin directory (either /usr/local/bin, /usr/bin, or /bin):
```sh
sudo rm $(which ollama)
```
Remove the downloaded models and Ollama service user and group:
```sh
sudo rm -r /usr/share/ollama
sudo userdel ollama
sudo groupdel ollama
```

