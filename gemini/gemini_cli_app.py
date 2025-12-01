import os
import textwrap
import google.generativeai as genai
from dotenv import load_dotenv

# ---------------------------------------------------
# 1. Load API key from .env and configure Gemini
# ---------------------------------------------------
load_dotenv()  # loads variables from .env into environment

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please add it to .env file.")

genai.configure(api_key=API_KEY)

# Choose a model (you can also use "gemini-1.5-pro" if enabled)
MODEL_NAME = "models/gemini-2.5-flash"
model = genai.GenerativeModel(MODEL_NAME)


# ---------------------------------------------------
# 2. Helper function to print outputs nicely
# ---------------------------------------------------
def pretty_print(text: str):
    """Wrap and print long text nicely in terminal."""
    print("\n" + "-" * 60)
    print(textwrap.fill(text, width=80))
    print("-" * 60 + "\n")


# ---------------------------------------------------
# 3. Core feature: Send any prompt to Gemini
# ---------------------------------------------------
def simple_prompt_mode():
    print("\n[ Simple Prompt Mode ]")
    user_prompt = input("Type your prompt: ")

    if not user_prompt.strip():
        print("Empty prompt. Returning to main menu.\n")
        return

    print("\nSending request to Gemini...\n")
    response = model.generate_content(user_prompt)

    pretty_print("Gemini response:\n\n" + response.text)


# ---------------------------------------------------
# 4. Extra feature: Summarization Mode
# ---------------------------------------------------
def summarization_mode():
    print("\n[ Summarization Mode ]")
    print("Paste a paragraph / text to summarize.")
    print("When you are done, press Enter, then Ctrl+D (Linux/Mac) or Ctrl+Z + Enter (Windows).")
    print("-" * 60)

    print("Enter text below:\n")

    # Read multi-line input from user
    try:
        user_text = ""
        while True:
            line = input()
            user_text += line + "\n"
    except EOFError:
        pass  # user finished input

    if not user_text.strip():
        print("No text entered. Returning to main menu.\n")
        return

    prompt = (
        "Summarize the following text in 3–5 bullet points, "
        "keeping the key ideas clear and simple:\n\n" + user_text
    )

    print("\nSending summarization request to Gemini...\n")
    response = model.generate_content(prompt)

    pretty_print("Summary:\n\n" + response.text)


# ---------------------------------------------------
# 5. (Optional) Chat mode – simple history
# ---------------------------------------------------
def chat_mode():
    print("\n[ Chat Mode ]")
    print("Type messages to chat with Gemini.")
    print("Type 'exit' to return to the main menu.")
    print("-" * 60)

    chat = model.start_chat(history=[])

    while True:
        user_msg = input("You: ")
        if user_msg.lower().strip() in ("exit", "quit"):
            print("Exiting chat mode...\n")
            break

        response = chat.send_message(user_msg)
        pretty_print("Gemini: " + response.text)


# ---------------------------------------------------
# 6. Main menu loop
# ---------------------------------------------------
def main():
    while True:
        print("==========================================")
        print("   Gemini CLI App")
        print("==========================================")
        print("1. Simple Prompt")
        print("2. Summarization (Extra Feature)")
        print("3. Chat Mode (Optional, extra)")
        print("4. Exit")
        print("==========================================")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            simple_prompt_mode()
        elif choice == "2":
            summarization_mode()
        elif choice == "3":
            chat_mode()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, 3, or 4.\n")


if __name__ == "__main__":
    main()
