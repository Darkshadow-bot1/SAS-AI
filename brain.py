import time
import requests
import json
import os

memory = {
    "name": None,
    "started": False
}

last_answer = None

CACHE_FILE = "dict_cache.json"

if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r") as f:
        dict_cache = json.load(f)
else:
    dict_cache = {}

def save_cache():
    with open(CACHE_FILE, "w") as f:
        json.dump(dict_cache, f)

def get_meaning(word):
    word = word.lower().strip()

    if word in dict_cache:
        return dict_cache[word] + " (memory)"

    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        r = requests.get(url, timeout=8)
        data = r.json()

        meaning = data[0]["meanings"][0]["definitions"][0]["definition"]

        dict_cache[word] = meaning
        save_cache()

        return meaning + " (internet)"
    except:
        return "I couldn't find a definition for that."

def wiki_search(query):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{query}"
        r = requests.get(url, timeout=10)

        if r.status_code == 200:
            data = r.json()
            return data.get("extract")

        return None
    except:
        return None

def web_search(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        r = requests.get(url, timeout=10)
        data = r.json()

        return data.get("AbstractText") or None
    except:
        return None

def calculator(expr):
    global last_answer

    try:
        expr = expr.lower()

        expr = expr.replace("calculate", "")
        expr = expr.replace("what is", "")
        expr = expr.replace("×", "*").replace("÷", "/")
        expr = expr.replace("x", "*")

        expr = expr.strip()

        if expr == "":
            return "Give me a math expression."

        if expr[0] in ["+", "-", "*", "/"] and last_answer is not None:
            expr = str(last_answer) + expr

        result = eval(expr, {"__builtins__": None}, {})

        last_answer = result

        return f"{expr} = {result}"

    except:
        return "I couldn't calculate that."

def get_greeting():
    hour = int(time.strftime("%H"))

    if 5 <= hour < 12:
        return "Good morning ☀️"
    elif 12 <= hour < 18:
        return "Good afternoon 🌤"
    elif 18 <= hour < 22:
        return "Good evening 🌙"
    else:
        return "Working late huh 🌌"

def intro():
    return "Yo 👋 I'm SAS-AI. Your smart adoptive system is online. What should I call you?"

def help_menu():
    return (
        "Commands:\n"
        "hello / hi / hey\n"
        "my name is ...\n"
        "time\n"
        "date\n"
        "what is ...\n"
        "who is ...\n"
        "search ...\n"
        "define ...\n"
        "meaning of ...\n"
        "calculate ...\n"
        "help\n"
        "exit"
    )

def think(user_input):
    text = user_input.lower().strip()

    if text in ["exit", "quit", "stop", "bye"]:
        return "__EXIT__"

    if not memory["started"]:
        memory["started"] = True
        return intro()

    if memory["name"] is None and "my name is" not in text:
        memory["name"] = user_input.strip()
        return f"Nice to meet you {memory['name']} 😎"

    if "my name is" in text:
        name = text.replace("my name is", "").strip()
        memory["name"] = name
        return f"Got it. I’ll remember you as {name}."

    if text in ["hello", "hi", "hey"]:
        greet = get_greeting()
        return f"{greet} {memory['name']} 👋" if memory["name"] else f"{greet} 👋"

    if "time" in text:
        return "Current time: " + time.strftime("%H:%M:%S")

    if "date" in text:
        return "Today's date: " + time.strftime("%Y-%m-%d")

    if any(x in text for x in ["calculate", "×", "÷", "*", "/", "+", "-"]):
        return calculator(text)

    if "what is" in text:
        query = text.replace("what is", "").strip()

        result = wiki_search(query)
        if result:
            return result

        result = web_search(query)
        return result or "I couldn't find info right now."

    if "who is" in text:
        query = text.replace("who is", "").strip()

        result = wiki_search(query)
        if result:
            return result

        result = web_search(query)
        return result or "I couldn't find info right now."

    if "search" in text:
        query = text.replace("search", "").strip()
        return web_search(query) or "No results found."

    if "define" in text:
        query = text.replace("define", "").strip()
        return get_meaning(query)

    if "meaning of" in text:
        query = text.replace("meaning of", "").strip()
        return get_meaning(query)

    if "help" in text:
        return help_menu()

    return "I'm still learning that one... but I'm improving step by step."
