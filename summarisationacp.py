import requests
from config import HF_API_KEY
from colorama import Fore, Style, init

init(autoreset=True)


DEFAULT_MODEL = "google/pegasus-xsum"

def build_api_url(model_name: str) -> str:
    return f"https://router.huggingface.co/hf-inference/models/{model_name}"

def query(payload, model_name=DEFAULT_MODEL):
    api_url = build_api_url(model_name)
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    response = requests.post(api_url, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except Exception as e:
        print(Fore.RED + f"❌ Request failed: {e}")
        print(Fore.RED + f"Response text: {response.text}")
        return None
    return response.json()

def summarize_text(text, min_length, max_length, model_name=DEFAULT_MODEL):
    payload = {
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length
        }
    }

    print(Fore.BLUE + Style.BRIGHT +
          f"\n✨ Performing AI summarization using model: {model_name}")
    result = query(payload, model_name=model_name)
    if result is None:
        return None

    
    if isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + "❌ Unexpected summarization response format:", result)
        return None


if __name__ == "__main__":
    print(Fore.YELLOW + Style.BRIGHT + "👋 Hi there! What's your name?")
    user_name = input("Your name: ").strip()
    if not user_name:
        user_name = "User"

    print(Fore.GREEN +
          f"Welcome, {user_name}! Let's give your text some AI magic ✨.")

    print(Fore.YELLOW + Style.BRIGHT +
          "\nPlease enter the text you want to summarize (paste multi-line text and press Enter, then Ctrl+D/Ctrl+Z if needed):")
    user_text = input("> ").strip()

    if not user_text:
        print(Fore.RED + "❌ No text provided. Exiting.")
    else:
        print(Fore.YELLOW +
              "\nEnter the model name you want to use "
              "(e.g., facebook/bart-large-cnn or leave blank for default Pegasus):")
        model_choice = input("Model name (leave blank for default): ").strip()
        if not model_choice:
            model_choice = DEFAULT_MODEL

        
        print(Fore.YELLOW + "\nChoose your summarization style:")
        print("1. Standard Summary (shorter, more concise)")
        print("2. Enhanced Summary (longer, more detailed)")
        print("3. Custom Length (you choose min/max tokens)")
        style_choice = input("Enter 1, 2 or 3: ").strip()

        if style_choice == "2":
            min_length = 80
            max_length = 200
            print(Fore.WHITE + "Enhancing summarization process... ✨")
        elif style_choice == "3":
            print(Fore.YELLOW +
                  "\nEnter your desired minimum summary length (approx. token count):")
            try:
                min_length = int(input("Min length: ").strip())
            except ValueError:
                min_length = 50
                print(Fore.RED +
                      "Invalid input. Using default min_length = 50.")

            print(Fore.YELLOW +
                  "Enter your desired maximum summary length (must be > min):")
            try:
                max_length = int(input("Max length: ").strip())
                if max_length <= min_length:
                    raise ValueError
            except ValueError:
                max_length = max(150, min_length + 50)
                print(Fore.RED +
                      f"Invalid input. Using default max_length = {max_length}.")
            print(Fore.BLUE +
                  f"Using custom summarization settings (min={min_length}, max={max_length})... 🛠️")
        else:
            min_length = 50
            max_length = 150
            print(Fore.BLUE + "Using standard summarization settings... ✅")

        summary = summarize_text(
            user_text,
            min_length=min_length,
            max_length=max_length,
            model_name=model_choice
        )

        if summary:
            print(Fore.GREEN + Style.BRIGHT +
                  f"\n🧠 AI Summarizer Output for {user_name}:")
            print(Fore.GREEN + summary)
        else:
            print(Fore.RED + "❌ Failed to generate summary.")