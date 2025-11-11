translation_cache = {}

# could be using redis, but let's keep it simple for demo.
def get_cached_translation(key):
    return translation_cache.get(key)

def set_cached_translation(key, value):
    translation_cache[key] = value
