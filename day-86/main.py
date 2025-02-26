import requests


words = requests.get("https://random-word-api.herokuapp.com/word?number=80").json()

text = ""

for word in words: 
    text = text + " " + word

print(text)