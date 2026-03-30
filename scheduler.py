from key_pool import KeyPool
from config import OPENROUTER_KEYS, GROQ_KEYS, TOGETHER_KEYS
from providers import call_openrouter, call_groq, call_together

openrouter_pool = KeyPool([OPENROUTER_KEYS] if OPENROUTER_KEYS else [])
groq_pool = KeyPool(GROQ_KEYS)
together_pool = KeyPool(TOGETHER_KEYS)

async def smart_call(prompt):
    # 短问题优先 Groq
    if len(prompt) < 50 and groq_pool.get():
        try:
            return await call_groq(prompt, groq_pool.get())
        except:
            pass

    providers = [
        (call_openrouter, openrouter_pool),
        (call_groq, groq_pool),
        (call_together, together_pool)
    ]

    for fn, pool in providers:
        key = pool.get()
        if not key:
            continue
        try:
            return await fn(prompt, key)
        except:
            continue

    return {"error": "all providers failed"}
