import requests
import json
import re

# Your OpenAI API key
API_KEY = "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"

# OpenAI API endpoint for chat completions
API_URL = "https://api.openai.com/v1/chat/completions"

def generate_3d_shape(user_input):
    """
    Sends a request to OpenAI to generate a 3D shape based on user input.

    :param user_input: A description of the desired 3D shape.
    :return: JSON response containing points and order or guidelines for improvement.
    """
    # Prepare the request payload
    payload = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "user",
                "content": (
                    f"You are a 3D shape generator assistant. The user wants to generate a 3D shape based "
                    f"on the following description: {user_input}. If the description is sufficient, generate "
                    f"the shape in this JSON format: {{ \"points\": [(x1, y1, z1), (x2, y2, z2), ...], \"order\": "
                    f"[[index1, index2, index3, ...], ...] }}. If the input is too vague or invalid, provide clear, "
                    f"actionable guidelines to describe a valid 3D shape. if the input is sufficient, only return the json file, do not return any other feedback"
                )
            }
        ],
        "temperature": 0.7
    }

    # Set up headers for authentication and content type
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }

    # Send the POST request to the OpenAI API
    response = requests.post(API_URL, headers=headers, json=payload)

    # Handle the response
    if response.status_code == 200:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        return content
    else:
        return f"Error: {response.status_code} - {response.text}"
    
def extract_json_from_response(response):
    # Use regular expression to find the JSON part of the response
    json_pattern = r'```json\n(.*?)\n```'
    match = re.search(json_pattern, response, re.DOTALL)  # re.DOTALL allows '.' to match newlines
    
    if match:
        # Extract the JSON string from the response
        json_data = match.group(1)
        # Parse the JSON string into a Python dictionary
        return json_data
    else:
        print("No JSON found in the response")

def main():
    """
    Main function to handle user input and generate 3D shapes.
    """
    print("Welcome to the 3D Shape Generator!")
    user_input = input("Enter a description of a 3D shape (e.g., '3D octagonal prism'): ")

    result = generate_3d_shape(user_input)

    try:
        shape_data = json.loads(result)
        if "points" in shape_data and "order" in shape_data:
            with open("generated_3d_shape.json", "w") as f:
                json.dump(shape_data, f, indent=4)
            #print("extracted points are here", extract_points_and_order(shape_data))
            print("\n3D shape generated successfully! Saved to 'generated_3d_shape.json'.")
        else:
            print("\nThe response contains guidelines or an unexpected format:")
            print(result)
    except json.JSONDecodeError:
        # Print guidelines or plain text if the result is not JSON
        print("\nThe response from OpenAI:")
        print(result)

def extract_points_and_order(json_data):
    # Parse the JSON if it's in string format
    data = json.loads(json_data) if isinstance(json_data, str) else json_data
    
    # Extract the "points" and "order" from the nested structure
    points = data['choices'][0]['message']['content'].split('"points": ')[1].split('"order": ')[0].strip().strip(',').strip()
    order = data['choices'][0]['message']['content'].split('"order": ')[1].split('}')[0].strip().strip(',')
    
    # Convert the string representation of points and order into actual lists
    points_list = json.loads(f"[{points}]")
    order_list = json.loads(f"[{order}]")
    
    return points_list, order_list

if __name__ == "__main__":
    main()
