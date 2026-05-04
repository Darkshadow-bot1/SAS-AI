import requests
import json
import os

CACHE_FILE = "dict_cache.json"

# load local cache
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)
else:
    cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

def get_meaning(word):
    word = word.lower().strip()

    # 1. check local cache first
    if word in cache:
        return cache[word] + " (from memory)"

    # 2. fetch from internet dictionary API
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        res = requests.get(url, timeout=5).json()

        meaning = res[0]["meanings"][0]["definitions"][0]["definition"]

        # store in cache
        cache[word] = meaning
        save_cache()

        return meaning + " (from internet)"
    
    except:
        return "No definition found."
