import requests
import re
import random
from config import HF_API_KEY


MODEL = "sentence-transformers/all-MiniLM-L6-v2"
API = f"https://router.huggingface.co/hf-inference/models/{MODEL}/pipeline/sentence-similarity"
HEAD = {"Authorization": f"Bearer {HF_API_KEY}"}

TH = 0.05  
DEMOS = [
    "I love this product, it works perfectly.",
    "This is the worst experience I've had.",
    "The meeting was okay, nothing special.",
    "I am very happy with the results.",
    "The app keeps crashing and it's frustrating.",
    "It was an average day overall."
]

TOK = lambda s: " | ".join(s.split())
bar = lambda s: "█" * int(s * 10) + "░" * (10 - int(s * 10))

clean = lambda t: [
    w for w in (re.sub(r"[^a-z0-9']+", "", x.lower()) for x in t.split()) if w
]

# I added new reference sentences to show what each would be
REFERENCE_SENTENCES = {
    "POSITIVE": "I am very happy and satisfied with this.",
    "NEGATIVE": "I am very unhappy and disappointed with this.",
    "NEUTRAL": "It is okay and acceptable, nothing special."
}


def hf_similarity(source, sentences):
    """
    Call the sentence-similarity pipeline:
    inputs: { "source_sentence": str, "sentences": [str, ...] }
    returns: list of floats (similarities) in the same order as 'sentences'
    """
    r = requests.post(
        API,
        headers=HEAD,
        json={"inputs": {"source_sentence": source, "sentences": sentences}},
        timeout=30
    )
    if not r.ok:
        raise RuntimeError(r.text)

    data = r.json()

    if isinstance(data, dict) and "error" in data:
        raise RuntimeError(data["error"])

    if not isinstance(data, list) or not data:
        raise RuntimeError(f"Unexpected response: {data}")

    # Expect a list of floats
    return [float(x) for x in data]


def hf_sentiment(text):
    """
    Build a pseudo-sentiment on top of sentence similarity.
    We compare the input to POSITIVE / NEGATIVE / NEUTRAL reference sentences
    and pick the label with the highest similarity.
    """
    labels = list(REFERENCE_SENTENCES.keys())
    reference_texts = [REFERENCE_SENTENCES[l] for l in labels]

    sims = hf_similarity(text, reference_texts)

    scores = {label: sim for label, sim in zip(labels, sims)}
    return scores


def map_label(scores):
    best_label = max(scores, key=scores.get)
    best_score = scores[best_label]

    if best_score < TH:
        return "NEUTRAL (LOW CONFIDENCE)", best_score

    return best_label, best_score


def show_result(text, scores):
    label, score = map_label(scores)
    print("\n🎯 Sentiment Result (via similarity)")
    print(f"Text: {text}")
    print(f"Label: {label}")
    print(f"Confidence (similarity to that label): {round(score * 100, 1)}% [{bar(score)}]")

    print("\nSimilarities to reference sentences:")
    for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        print(f" - {k:<10} {round(v * 100, 1)}%")


def show_flow(text):
    tokens = TOK(text)
    words = clean(text)
    print("\n🔁 FLOW")
    print("\n1) Input text")
    print(f" {text}")
    print("\n2) Split into tokens")
    print(f" {tokens}")
    print("\n3) Meaningful words")
    print(" ", ", ".join(words) if words else "None")
    print("\n4) Under the hood")
    print("   - We send your sentence to a sentence-similarity model.")
    print("   - It measures how close your text is to 3 reference sentences:")
    for label, ref in REFERENCE_SENTENCES.items():
        print(f"     * {label}: {ref}")
    print("   - The label whose reference sentence is most similar becomes your sentiment.")


def run(text):
    scores = hf_sentiment(text)
    show_result(text, scores)
    show_flow(text)


def main():
    print("Type a sentence to classify as positive, negative, or neutral (via similarity).")
    print("Type 'exit' anytime to quit.\n")

    while True:
        text = input("Text: ").strip()
        if text.lower() == "exit":
            break
        if not text:
            continue

        try:
            run(text)

            print("\n--- RANDOM DEMOS ---")
            for i, demo in enumerate(random.sample(DEMOS, 2), 1):
                print(f"\nDemo {i}:")
                run(demo)

            print("\n(Next round → Text or 'exit')\n")
        except Exception as e:
            print(f"\n⚠️ Oops! {e}\n")


if __name__ == "__main__":
    main()