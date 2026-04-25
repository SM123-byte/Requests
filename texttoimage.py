import requests

from huggingface_hub import InferenceClient
from datetime import datetime
from PIL import Image
from config import HF_API_KEY

MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",
]

client = InferenceClient(api_key= HF_API_KEY)

print(f"Primary Models: {MODELS[0]}")
print("Type 'exit' to quit")

while True:
    prompt = input("Enter prompt: ").strip()

    if prompt.lower() in ["quit", "exit", "q"]:
        break
    if not prompt:
        continue
    print("Generating...")
    image = None

    for model in MODELS:
        try:
            image = client.text_to_image(prompt, model=model)
            break
        except Exception:
            print("Executing...")
            continue
    
    if image:
        timestamp= datetime.now().strftime("%Y%m%d_%H%M%S")
        filename= f"Generated_{timestamp}.png"

        image.save(filename)
        print(f"saved: {filename}")
        image.show()
        print()
    
    else:
        print("Error: All Models Failed! Check your API Key!\n")

print("Goodbye!")