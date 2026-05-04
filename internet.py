import requests

def wiki_search(query):
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + query
        r = requests.get(url).json()
        return r.get("extract", "No info found.")
    except:
        return "Internet error."


def web_search(query):
    try:
        url = "https://api.duckduckgo.com/?q=" + query + "&format=json"
        r = requests.get(url).json()
        return r.get("AbstractText", "No clear result online.")
    except:
        return "Search failed."
