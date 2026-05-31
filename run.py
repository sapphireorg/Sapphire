import sapphire.models

prompt = "What countries are in Asia?"

while True:
    prompt = input("User: ")
    print("Sapphire:", sapphire.models.zero(prompt))