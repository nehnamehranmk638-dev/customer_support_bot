# conversation.py — handles history and token trimming

from config import MAX_HISTORY_TOKENS, SYSTEM_PROMPT

def count_tokens(messages):
    """
    Rough token count — works for any model including Ollama.
    Approximation: 1 token ≈ 4 characters (good enough for trimming)
    """
    total = 0
    for m in messages:
        total += len(m["content"]) // 4 + 4  # 4 overhead per message
    return total + 2

def trim_history(history):
    """
    Trim conversation history to stay within token budget.
    Always keeps most recent messages.
    System prompt is handled separately — never trimmed.
    """
    while count_tokens(history) > MAX_HISTORY_TOKENS and len(history) > 2:
        # Remove oldest user+assistant pair
        history.pop(0)
        history.pop(0)
    
    return history

def build_messages(history):
    """Build the full messages list with system prompt prepended"""
    return [
        {"role": "system", "content": SYSTEM_PROMPT}
    ] + history