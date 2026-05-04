from brain import think

print("SAS-AI starting...")

while True:
    user = input("You: ")
    response = think(user)

    if response == "__EXIT__":
        print("SAS-AI: Shutting down... 👋")
        break

    print("SAS-AI:", response)
