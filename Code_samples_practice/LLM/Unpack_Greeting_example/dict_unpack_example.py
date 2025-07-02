import json

# Dictionary to unpack
person = {"name": "Aravind", "age": 25, "Greet": "How are you"}

# Updated greet function that returns a dictionary
def greet(name, age, Greet):
    message = f"Good morning {name}, You are {age} old, {Greet}"
    print(message)
    return {
        "message": message
    }

# Call the function and capture the return value
output = greet(**person)

# Save output to a JSON file
with open("greeting_output.json", "w") as f:
    json.dump(output, f, indent=4)
