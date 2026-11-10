import sapphire.models

environment = {
    "USERNAME": "User"
}

while True:
    prompt = input("User: ")
    print("Sapphire:", sapphire.models.zero(prompt, environment))