import os
from AVClient import AVClient
import google.generativeai as genai

#  Replace with your actual API key
genai.configure(api_key=os.environ.get("API_KEY_GEMINI"))

# Setup Model (choose a model, e.g., gemini-pro)
model = genai.GenerativeModel('gemini-2.0-flash-exp')


# Function to Interact with Gemini
def process_with_gemini(system_prompt, user_prompt):
    """Sends a prompt to Gemini and returns the response."""

    chat = model.start_chat(
        history=[],
    )

    # send system prompt first
    chat.send_message(system_prompt)

    # then user prompt
    response = chat.send_message(user_prompt)

    return response.text


if __name__ == "__main__":

    avClient = AVClient(os.environ.get("API_KEY_AV"))
    #res = avClient.get_global_quote("MSFT")
    #res = avClient.get_income_statement("MSFT")
    res = avClient.get_overview("MSFT")
    desc=res["Description"]
    print(str(res).replace("'","\""))
    print(desc)



    # system_prompt = """You are a helpful and creative writing assistant. You will receive instructions from the user.
    # Follow the instructions, pay attention to details. Give a conversational and clear output."""
    #
    # user_prompt = "Please write a short story about a cat who goes on an adventure in a magical forest."
    #
    # try:
    #     gemini_response = process_with_gemini(system_prompt, user_prompt)
    #     print("Gemini's Response:\n")
    #     print(gemini_response)
    #
    # except Exception as e:
    #     print(f"Error during Gemini API call: {e}")
