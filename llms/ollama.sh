ollama pull codellama:7b
ollama pull codellama:13b
ollama pull codellama:34b
ollama pull codellama:70b


ollama run mistral:instruct --verbose "Please process $(cat prompt.txt)"