from huggingface_hub import InferenceClient
from PIL import Image, ImageEnhance, ImageFilter
from config import HF_API_KEY

MODELS = [
    "ByteDance/SDXL-Lightning",
    "stabilityai/stable-diffusion-xl-base-1.0",
    "stabilityai/sdxl-turbo",
    "runwayml/stable-diffusion-v1-5",
]

client = InferenceClient(api_key=HF_API_KEY)
print(f"Primary model: {MODELS[0]}")
print("Type 'quit' to exit\n")


def post_process_image(image, mode="default"):
    """Returns the processed PIL.Image with optional day/night adjustments."""
    if mode == "day":
        image = ImageEnhance.Brightness(image).enhance(1.3)
        image = ImageEnhance.Contrast(image).enhance(1.1)
        image = image.filter(ImageFilter.GaussianBlur(radius=1))
    elif mode == "night":
        image = ImageEnhance.Contrast(image).enhance(1.4)
        image = ImageEnhance.Brightness(image).enhance(0.9)
        image = image.filter(ImageFilter.GaussianBlur(radius=0.5))
    else:
        image = ImageEnhance.Brightness(image).enhance(1.2)
        image = ImageEnhance.Contrast(image).enhance(1.3)
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
    return image


def generate_image_from_text():
    while True:
        prompt = input("Enter prompt: ").strip()
        if prompt.lower() in ["quit", "exit", "q"]:
            break
        if not prompt:
            continue

        mode = input("Choose mode (default/day/night): ").strip().lower()
        if mode not in ["default", "day", "night"]:
            mode = "default"

        print("Generating...")
        image = None

        for model in MODELS:
            try:
                image = client.text_to_image(prompt, model=model)
                break
            except Exception:
                print(" Executing next...")
                continue

        if image:
            print("Applying post-processing effects...\n")
            processed_image = post_process_image(image, mode=mode)
            processed_image.show()
            print()

            try:
                save_option = input("Do you want to save the processed image? (yes/no): ").strip().lower()
                if save_option == 'yes':
                    file_name = input("Enter a name for the image file (without extension): ").strip()
                    processed_image.save(f"{file_name}.png")
                    print(f"Image saved as {file_name}.png\n")
                    print("-" * 80 + "\n")
            except Exception as e:
                print(f"An error occurred: {e}\n")
        else:
            print("Error: All models failed. Check your API key.\n")


def main():
    print("Welcome to the Post-Processing Magic Workshop!")
    print("This program generates an image from text and applies post-processing effects.")
    print("Type 'exit' to quit.\n")

    while True:
        try:
            generate_image_from_text()
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    main()