# AI Chatbot Using Rasa

This is a simple AI chatbot built using the Rasa framework. It can respond to greetings, tell the current time, and is being extended to handle math operations and weather queries.

## Features
- Greeting & farewell handling
- Tells current time using custom actions
- Intent classification & entity extraction (NLU)
- Modular and scalable design

## Upcoming Features
- Arithmetic operation handling
- Weather forecasting (API)
- User memory for name recall

## Tech Stack
- Python
- Rasa NLU/Core
- YAML for training data
- Custom Actions (Python)

## How to Run
```bash
rasa train
rasa run actions
rasa shell
