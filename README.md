# 🤖 AI Aggregator API

Multi-model scheduling API with caching and streaming support.

## Features

- ✅ **Auto-scheduling** - Smart routing to available providers
- ✅ **Key pooling** - Random key selection from multiple keys
- ✅ **Caching** - Reduce API calls with simple cache
- ✅ **Web UI** - Built-in chat interface
- ✅ **Streaming** - Real-time streaming responses

## Providers

- OpenRouter (Llama 3.1 8B)
- Groq (Llama3 70B)
- Together AI (Mixtral 8x7B)

## Setup

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```
OPENROUTER_KEYS=your_openrouter_keys
GROQ_KEYS=your_groq_keys
TOGETHER_KEYS=your_together_keys
```

Or set keys directly in `config.py`.

## Run

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /` - Web UI
- `POST /chat` - Send prompt, get JSON response
- `POST /stream` - Stream response

## Example

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello!"}'
```
