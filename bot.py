# bot.py — main entry point

from openai import OpenAI
from dotenv import load_dotenv
import os

from config import MODEL, MAX_RESPONSE_TOKENS, TEMPERATURE, COMPANY_NAME
from conversation import trim_history, build_messages, count_tokens
from logger import save_message, save_session_divider

load_dotenv()
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

# Conversation history — grows during the session
history = []

def get_response(user_message):
    """Send message, get streaming response, return full reply"""
    
    # Add user message to history
    history.append({"role": "user", "content": user_message})
    
    # Trim if needed
    trimmed = trim_history(history.copy())
    
    # Build full messages with system prompt
    messages = build_messages(trimmed)
    
    # Stream the response
    print(f"\n\033[94mNena:\033[0m ", end="", flush=True)
    full_reply = ""
    total_tokens = 0

    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=MAX_RESPONSE_TOKENS,
        temperature=TEMPERATURE,
        stream=True
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            print(delta.content, end="", flush=True)
            full_reply += delta.content

    print("\n")

    # Add reply to history
    history.append({"role": "assistant", "content": full_reply})

    # Log both messages
    save_message("user", user_message)
    save_message("assistant", full_reply)

    # Show token usage
    token_count = count_tokens(messages)
    print(f"\033[90m[Tokens in context: {token_count}]\033[0m\n")

    return full_reply

def print_welcome():
    print("\033[92m" + "=" * 55 + "\033[0m")
    print(f"\033[92m  Welcome to {COMPANY_NAME} Customer Support\033[0m")
    print("\033[92m" + "=" * 55 + "\033[0m")
    print("  Hi! I'm Nena. How can I help you today?")
    print("  (Type 'quit' to exit, 'clear' to reset chat)\n")

def main():
    save_session_divider()
    print_welcome()

    while True:
        try:
            user_input = input("\033[93mYou:\033[0m ").strip()
        except KeyboardInterrupt:
            print("\n\nSession ended. Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            print("\nNena: Thank you for contacting ShopEase support. Have a great day!")
            break

        if user_input.lower() == "clear":
            history.clear()
            print("\n\033[90m[Conversation cleared]\033[0m\n")
            continue

        get_response(user_input)

if __name__ == "__main__":
    main()