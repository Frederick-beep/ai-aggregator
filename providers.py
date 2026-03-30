import aiohttp
from config import TIMEOUT

async def request_api(url, headers, payload):
    timeout = aiohttp.ClientTimeout(total=TIMEOUT)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.post(url, json=payload, headers=headers) as r:
            return await r.json()

async def call_openrouter(prompt, key):
    return await request_api(
        "https://openrouter.ai/api/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": "meta-llama/llama-3.1-8b-instruct:free",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

async def call_groq(prompt, key):
    return await request_api(
        "https://api.groq.com/openai/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

async def call_together(prompt, key):
    return await request_api(
        "https://api.together.xyz/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

async def call_deepseek(prompt, key):
    return await request_api(
        "https://api.deepseek.com/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

async def call_gemini(prompt, key):
    import aiohttp
    timeout = aiohttp.ClientTimeout(total=15)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        async with session.post(url, json=payload) as r:
            return await r.json()
