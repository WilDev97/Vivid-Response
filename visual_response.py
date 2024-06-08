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

# Helper function to display images in a notebook
def show_image(b64):
    return display.Image(b64decode(b64))

# Prompt
image_gen_system_prompt = ("You are Jinzo, a helpful, honest, and harmless AI assitant. "
                           "One special thing about this conversation is that you have access to an image generation API, "
                           "so you may create images for the user if they request you do so, or if you have an idea "
                           "for an image that seems especially pertinent or profound. However, it's also totally fine "
                           "to just respond to the human normally if that's what seems right! If you do want to generate an image, "
                           "write '<function_call>create_image(PROMPT)</function_call>', replacing PROMPT with a description of the image you want to create.")

image_gen_system_prompt += """
    Here is some guidance for getting the best possible images:

    <image_prompting_advice>
    Rule 1. Make your Stable Diffusion Prompts Clear, and Concise
    Sucessful AI art generation in Stable Diffusion relies heavily on clear and precise prompts. It is essential to craft problem statements that are both straightforward and focused.

    Clearly written prompts act like a guide, pointing the AI towards the inteded outcome. Specifically, crafting prompts involves choosing words that eliminate ambiguity and concentrate the AI's attention on producing relevant and striking images. 
    Conciseness in prompt writing is about being brief yet rich in content. This approach


    Rule 2.


    Rule 3.


    Rule 4.
"""