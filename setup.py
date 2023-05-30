import sys
import os

# Check if API Key is provided
def set_API_key():
    if os.path.exists(os.path.join(os.getcwd(),'.env')):
        return
    else:
        _input = input("Wprowadz klucz API do OpenAI:")
        with open('.env', 'w') as file:
            file.write('API_KEY = ' + _input)

