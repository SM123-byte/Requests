from huggingface_hub import InferenceClient
from datetime import datetime
from config import HF_API_KEY

MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",
]

client = InferenceClient(api_key=HF_API_KEY)

print(f"Primary Models: {MODELS[0]}")
print("Type 'exit' to quit")

while True:
    prompt = input("Enter prompt: ").strip()

    if prompt.lower() in {"quit", "exit", "q"}:
        break

    if not prompt:
        continue

    print("Generating...")
    image = None
    used_model = None

    for model in MODELS:
        try:
            image = client.text_to_image(prompt=prompt, model=model)
            used_model = model
            break
        except Exception as e:
            print(f"Model failed: {model}")
            continue

    if image:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Generated_{timestamp}.png"
        image.save(filename)
        print(f"Saved: {filename}")
        print(f"Used model: {used_model}")
        image.show()
        print()
    else:
        print("Error: All models failed! Check your API key or model access.\n")

print("Goodbye!")