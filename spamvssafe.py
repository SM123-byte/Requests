# Sorry for late response; really busy throughout the week!

import requests
from config import HF_API_KEY  

# API key variables

MODEL_ID = "facebook/bart-large-mnli"
API_URL = f"https://router.huggingface.co/hf-inference/models/{MODEL_ID}"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}"}

# Two labels given
LABELS = ["Spam", "Safe"]


def ask_hf(message: str):
    """Send the message to Hugging Face and get predictions back."""
    payload = {
        "inputs": message,
        "parameters": {"candidate_labels": LABELS}
    }

    response = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    if not response.ok:
        raise RuntimeError(f"HF error {response.status_code}: {response.text}")

    return response.json()  

def best_label(preds: list):
    """Pick the label with the highest score."""
    best = max(preds, key=lambda x: x["score"])
    return best["label"], best["score"]


def bar(score: float) -> str:
    """Make a small bar showing confidence (0–100%)."""
    pct = int(score * 100)
    blocks = pct // 10          
    return "█" * blocks + "░" * (10 - blocks)


def show_result(message: str, preds: list):
    """Print a simple, clear result to the terminal."""
    label, score = best_label(preds)

    print("\n" + "=" * 60)
    print("AI Spam Message Classifier")
    print("=" * 60)
    print("Message:", message)
    print(f"Result: {label}")
    print(f"Confidence: {round(score * 100, 1)}% [{bar(score)}]")

    print("\nAll labels:")
    for p in sorted(preds, key=lambda x: x["score"], reverse=True):
        print(f"- {p['label']:<5} {round(p['score'] * 100, 1)}% [{bar(p['score'])}]")
    print("=" * 60)


def main():
    print("Welcome to the AI Spam Detector!")
    print("I will classify your message as 'Spam' or 'Safe'.")
    print("Type 'exit' to quit.\n")

    while True:
        message = input("Message: ").strip()

        if message.lower() == "exit":
            print("Goodbye! Stay safe online.")
            break

        if not message:
            print("Please type a non-empty message.\n")
            continue

        try:
            preds = ask_hf(message)

            
            if isinstance(preds, list) and preds and "label" in preds[0]:
                show_result(message, preds)
            else:
                print("Unexpected API reply:", preds)

        except Exception as e:
            print("\nSomething went wrong.")
            print("Reason:", e)
            print("Tip: Check your HF_API_KEY and internet.\n")


if __name__ == "__main__":
    main()