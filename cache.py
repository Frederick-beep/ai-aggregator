cache = {}

def get_cache(prompt):
    return cache.get(prompt)

def set_cache(prompt, result):
    cache[prompt] = result
