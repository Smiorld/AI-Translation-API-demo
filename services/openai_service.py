import os
from openai import OpenAI
from cache import get_cached_translation, set_cached_translation

client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.getenv("OPENAI_API_KEY"),
                )


def translate_and_proofread(text, target="English"):
    cache_key = f"{text}_{target}"
    cached = get_cached_translation(cache_key)
    if cached:
        return cached

    # Step 1: translation
    try:
        translation = client.chat.completions.create(
            model="minimax/minimax-m2:free",
            messages=[{"role": "user", "content": f"Translate this to {target} without any further explanation: {text}"}]
        ).choices[0].message.content.strip() # type: ignore

        # Step 2: proofread
        proofread = client.chat.completions.create(
            model="microsoft/mai-ds-r1:free",
            messages=[{"role": "user", "content": f"Proofread this translation, answer only with the proofreaded text: {translation}"}]
        ).choices[0].message.content.strip() # type: ignore
    except Exception as e:
        print(f"Error: {e}")
        return {"translated": "", "proofread": ""}

    result = {"translated": translation, "proofread": proofread}
    set_cached_translation(cache_key, result)
    return result