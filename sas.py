print("SAS — Smart Adaptive System activated.")

name = input("Enter your name: ")
print(f"SAS: Welcome, {name}.")

while True:
    user = input("You: ").lower()

    if user == "exit":
        print("SAS: Session terminated.")
        break

    elif "hello" in user or "hi" in user:
        print(f"SAS: Hello {name}. What do you need?")

    elif "your name" in user:
        print("SAS: I am SAS — Smart Adaptive System.")

    else:
        print("SAS: Still learning. Try something else.")
