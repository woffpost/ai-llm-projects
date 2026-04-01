# Caption Generator

Batch Instagram caption generator for Soviet 1:43 diecast models.

## How it works
Reads a list of models from `models.txt`, generates captions for each using Anthropic API, saves results to `captions.txt`.

## Stack
- Python
- Anthropic API
- asyncio (parallel requests)

## Setup
```bash
pip install anthropic python-dotenv
```
Create `.env` file:
```
ANTHROPIC_API_KEY=your_key_here
```