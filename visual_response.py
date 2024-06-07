import os, re, requests, anthropic
from IPython import display # type: ignore
from base64 import b64decode

STABILITY_API_KEY = "sk-39zhSls9WskEQ7OSffJDjmpzdVe8RVZgYc0H4J439q76LRNa"

ANTHROPIC_API_KEY = "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"

MODEL_NAME = "claude-3-opus-20240229"

CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def gen_image(prompt, height = 1024, width = 1024, num_samples = 1):
    engine_id = "stable-diffusion-v1-6"
    api_host = "https://api.stability.ai"

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization":f"Bearer {STABILITY_API_KEY}"
        },
        json = {
            "text_prompts": [
                {
                    "text": prompt,
                }
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": num_samples,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception("Not a 200 Response!") + str(response.text)

    data = response.json()
    return data["artifacts"][0]["base64"]