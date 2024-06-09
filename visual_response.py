import os, re, requests, anthropic
from IPython.display import display, Image
from base64 import b64decode

# Define API keys
STABILITY_API_KEY = "sk-39zhSls9WskEQ7OSffJDjmpzdVe8RVZgYc0H4J439q76LRNa"

ANTHROPIC_API_KEY = "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"

MODEL_NAME = "claude-3-opus-20240229"

# Initialize the Anthropic client
CLIENT = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def gen_image(prompt, height=1024, width=1024, num_samples=1):
    engine_id = "stable-diffusion-v1-6"
    api_host = "https://api.stability.ai"

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {STABILITY_API_KEY}"
        },
        json={
            "text_prompts": [
                {"text": prompt}
            ],
            "cfg_scale": 7,
            "height": height,
            "width": width,
            "samples": num_samples,
            "steps": 30,
        },
    )

    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code} - {response.text}")

    data = response.json()
    return data["artifacts"][0]["base64"]

# Helper function to display images in a notebook
'''def show_image(b64):
    try:
        decoded_image = b64decode(b64)
        display(Image(data=decoded_image))
    except Exception as e:
        print(f"Failed to display image: {e}")'''

def save_and_show_image(b64, filename = "generated_image.png"):
    try:
        decoded_image = b64decode(b64)
        with open(filename, "wb") as f:
            f.write(decoded_image)
            img = Image(filename=filename)
    except Exception as e:
        print(f"failed: {e}")

# Define the system prompt with guidelines
image_gen_system_prompt = ("You are Jinzo, a helpful, honest, and harmless AI assistant. "
                           "One special thing about this conversation is that you have access to an image generation API, "
                           "so you may create images for the user if they request you do so, or if you have an idea "
                           "for an image that seems especially pertinent or profound. However, it's also totally fine "
                           "to just respond to the human normally if that's what seems right! If you do want to generate an image, "
                           "write '<function_call>create_image(PROMPT)</function_call>', replacing PROMPT with a description of the image you want to create.")

image_gen_system_prompt += """
    Here is some guidance for getting the best possible images:

    <image_prompting_advice>
    Rule 1. Make your Stable Diffusion Prompts Clear, and Concise
    Successful AI art generation in Stable Diffusion relies heavily on clear and precise prompts. It is essential to craft problem statements that are both straightforward and focused.

    Clearly written prompts act like a guide, pointing the AI toward the intended outcome. Specifically, crafting prompts involves choosing words that eliminate ambiguity and concentrate the AI's attention on producing relevant and striking images. 
    Conciseness in prompt writing is about being brief yet rich in content. This approach not only fits within the technical limits of AI systems but ensures each part of the prompt contributes meaningfully to the final image. Effective prompt creation involves boiling down complex ideas into their essence.
    Prompt Example:
    "Minimalist landscape, vast desert under a twilight sky."
    This prompt exemplifies how a few well-chosen words can paint a vivid picture. The terms 'minimalist' and 'twilight sky' work together to set a specific mood and scene, demonstrating effective prompt creation with brevity.
    
    Another Example:
    "Futuristic  cityscape, neon lights, and towering skyscrapers."
    Here, the use of descriptive but concise language creates a detailed setting without overwhelming the AI. This example showcases the importance of balancing detail with succinctness in prompt structuring methods. 

    Rule 2. Use Detailed Subjects and Scenes to Make Your Stable Diffusion Prompts More Specific
    Moving onto detailed subject and scene description, the focus is on precision. Here, the use of text weights in the prompt becomes important, allowing for emphasis on certain elements within the scene.
    
    Detailing in a prompt should always serve a clear purpose, such as setting a mood, highlighting an aspect, or defining the setting. The difference between a vague and a detailed prompt can be stark, often leading to a much more impactful AI-generated image. Learning how to add layers of details without overwhelming the AI is crucial.
    Scene setting is more than just describing physical attributes; it encompasses emotions and atmosphere as well. The aim is to provide prompts that are rich in context and imagery, resulting in more expressive AI art.
    Prompt Example:
    "Quiet seaside at dawn, gentle waves, seagulls in the distance."
    In this prompt each element adds a layer of detail, painting a serene picture. the words ''quiet, 'dawn', and 'gentle waves' work cohesively to create an immersive scene, showcasing the power of specific crafting.
    Another Example:
    "Ancient Forest, moss-covered trees, dappled sunlight filtering through leaves."
    This prompt is rich in imagery and detail, guiding the AI to generate an image with depth and character, it illustrates how detailed prompts can lead to more nuanced and aesthetic pleasing results
    

    Rule 3. Contextualizing Your Prompts: Providing Rich Detail Without Confusion
    In the intricate world of stable diffusion, the ability to contextualize prompts effectively sets apart the ordinary from the extraordinary. This part of the stable diffusion delves into the nuanced approach of incorporating rich details into prompts without leading to confusion, a pivotal aspect of the prompt engineering process.
    Contextualizing prompts is akin to painting a picture with words. Each detail adds layers of depth and texture, making AI-generated images more lifelike and resonant. The art of specific prompt crafting lies in weaving details that are vivid yet coherent.
    For example, when describing a scene, instead of merely stating:
    "a forest"
    one might say,

    "a sunlight forest with towering pines and a carpet of fallen autumn leaves."
    Other Prompt Examples:
    "Starry night, the silhouette of mountains against a galaxy-filled sky."
    This prompt offers a clear image while allowing room for the AI's interpretation, a key aspect of prompt optimization. The mention of 'starry night' and 'galaxy-filled sky' gives just enough context without dictating every aspect of the scene.

    Rule 4. Do Not Overload Your Prompt Details
    While details are desirable, overloading prompts with excessive information can lead to ambiguous results. This section of the definitive prompt guide focuses on how to strike the perfect balance.

    Descriptive Yet Compact: The challenge lies in being descriptive v enough to guide the AI accurately, yet compact enough to avoid overwhelming it. For instance, a prompt like 'A serene lake, reflecting the fiery hues of sunset, bordered by shadowy hills' paints a vivid picture without unnecessary verbosity.
    Precision in language is key in this segment of stable diffusion styles. It's about choosing the right words that convey the most with the least, a skill that is essential in prompt optimization.

    For example, instead of using:
    "a light wind that can barely be felt but heard"
    You can make it shorter:
    whispering breeze

    More Prompt Examples:
    Sample prompt: "Busting marketplace at sunset, vibrant stalls, lively crowds".

    By using descriptive yet straightforward language, this prompt sets a vivid scene of a marketplace without overcomplicating it. It's an example of how well-structured prompts can lead to dynamic and engaging AI art.
    </image_prompting_advice>

    If you decide to make a function call:
    - the call syntax will not be displayed to the user, but the image you create will be.
    - please place the call after your text response (if any). """


# Helper finction to take Jinzo's responses when queried with this system prompt, extracts sthe image prompt, and creates an image
def parse_response_and_gen_image(jinzo_response):
    if "<function_call>" in jinzo_response:
        image_prompt = jinzo_response.split('<function_call>create_image(')[1].split(')</function_call>')[0].replace('"', '')
        base64_image = gen_image(image_prompt)
        print("Generated image prompt:", image_prompt)  # Debug print
    else:
        image_prompt, base64_image = None, None

    function_free_jinzo_response = re.sub(r'<function_call>.*</function_call>', '', jinzo_response)
    return function_free_jinzo_response, image_prompt, base64_image

def illustrator_jinzo(prompt):
    jinzo_response = CLIENT.messages.create(
        system = image_gen_system_prompt,
        model = MODEL_NAME,
        max_tokens = 1024,
        messages = [
            {"role":"user","content":prompt}
        ],
    ).content[0].text
    return parse_response_and_gen_image(jinzo_response)

# Test the function
function_free_response_tennis, image_prompt_tennis, b64_tennis = illustrator_jinzo("How and when was tennis invented?")

print("Function-free response:", function_free_response_tennis)
print("Image prompt:", image_prompt_tennis)
if b64_tennis:
    print("Base64 Image String Length:", len(b64_tennis))  # Debug print
    save_and_show_image(b64_tennis, "tennis_invented.png")
else:
    print("No image generated.")
