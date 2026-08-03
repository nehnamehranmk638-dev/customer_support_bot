# conversation.py — handles history and token trimming

import tiktoken
from config import MODEL, MAX_HISTORY_TOKENS, SYSTEM_PROMPT

def count_tokens(messages):
    """Count total tokens in a list of messages"""
    encoder = tiktoken.encoding_for_model(MODEL)
    total = sum(
        len(encoder.encode(m["content"])) + 4
        for m in messages
    ) + 2
    return total

def trim_history(history):
    """
    Trim conversation history to stay within token budget.
    Always keeps most recent messages.
    System prompt is handled separately — never trimmed.
    """
    while count_tokens(history) > MAX_HISTORY_TOKENS and len(history) > 2:
        # Remove oldest user+assistant pair (first 2 messages)
        history.pop(0)
        history.pop(0)
    
    return history

def build_messages(history):
    """Build the full messages list with system prompt prepended"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + history