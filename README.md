# ShopEase Customer Support Bot

A CLI customer support chatbot for ShopEase, a fictional Indian 
e-commerce platform. Built with Python and the OpenAI API.

## Features
- Strict persona — always responds as "Nena" from ShopEase support
- Topic guardrails — politely refuses non-ShopEase questions
- Streaming responses — word by word output like ChatGPT
- Smart history trimming — never exceeds token limits
- Conversation logging — every session saved to chat_logs.json
- Token usage display — see context size after every reply

## Project structure
customer-support-bot/
├── bot.py           ← main entry point
├── config.py        ← all settings and system prompt
├── conversation.py  ← history management and token trimming
├── logger.py        ← JSON conversation logging
├── chat_logs.json   ← auto-generated conversation logs
└── .env             ← API key (not in repo)

## How to run
1. Clone this repo
2. Install dependencies: pip install openai python-dotenv tiktoken
3. Create .env with your OPENAI_API_KEY
4. Run: python bot.py

## Tech used
Python, OpenAI API, tiktoken