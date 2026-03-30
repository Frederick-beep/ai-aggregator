import os

OPENROUTER_KEYS = os.getenv("OPENROUTER_KEYS", "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")
GROQ_KEYS = os.getenv("GROQ_KEYS", "").split(",")
TOGETHER_KEYS = os.getenv("TOGETHER_KEYS", "").split(",")
Google_KEYS = os.getenv("Google_KEYS", "AIzaSyAIRi940QpfoxN27DjNLEy9Hy1ONkUWCaM")
DeepSeek_KEYS = os.getenv("DeepSeek_KEYS", "sk-cd8b2a27fe634588a99ee317b98496f2")

TIMEOUT = 15
