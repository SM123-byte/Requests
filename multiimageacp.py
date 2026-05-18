
import os
import base64
import requests
from typing import Tuple, Optional

from config import HF_API_KEY

API_URL = "https://router.huggingface.co/v1/chat/completions"
HEADERS = {"Authorization": f"Bearer {HF_API_KEY}", "Content-Type": "application/json"}

MODELS = [
    "Qwen/Qwen3-VL-8B-Instruct:together",
    "Qwen/Qwen3-VL-32B-Instruct:together",
    "Qwen/Qwen2.5-VL-32B-Instruct:together",
    "Qwen/Qwen2-VL-7B-Instruct:together",
]

# Converts raw image bytes to data URL

def data_url(b: bytes) -> str:
    return "data:image/jpeg;base64," + base64.b64encode(b).decode("utf-8")


def extract_err(r: requests.Response) -> str:
    try:
        j = r.json()
        return j.get("error", {}).get("message") or str(j)
    except Exception:
        return (r.text or "").strip() or r.reason or "Request failed."

# Sends single image to API

def query_caption(image_bytes: bytes) -> Tuple[Optional[str], Optional[str]]:
    base = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Give a short, clear caption for this image.",
                    },
                    {"type": "image_url", "image_url": {"url": data_url(image_bytes)}},
                ],
            }
        ],
        "max_tokens": 60,
        "temperature": 0.2,
    }

    last_err: Optional[str] = None

    for model in MODELS:
        try:
            r = requests.post(
                API_URL,
                headers=HEADERS,
                json={**base, "model": model},
                timeout=120,
            )
        except requests.RequestException as e:
            last_err = f"Request failed for model {model}: {e}"
            continue

        if r.status_code != 200:
            last_err = f"Model {model} error: {extract_err(r)}"
            continue

        try:
            d = r.json()
        except Exception:
            last_err = f"Model {model} returned non-JSON response."
            continue

        cap = (
            d.get("choices", [{}])[0]
            .get("message", {})
            .get("content", "")
            .strip()
        )
        if cap:
            return cap, None

        last_err = f"Model {model} returned an empty caption."

    return None, last_err or "No caption found."

# Asks user for a valid image path or folder type 

def main() -> None:
    raw_path = (
        input("Enter an images folder or a single image file (Enter for 'images'): ")
        .strip()
        or "images"
    )

    if os.path.isdir(raw_path):
        folder_path = raw_path
        image_files = sorted(
            f
            for f in os.listdir(folder_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
            and os.path.isfile(os.path.join(folder_path, f))

            # Conditional case for whether it's a directory or a regular file
        )
        if not image_files:
            print(f"No valid image files found in '{folder_path}'. Exiting.")
            return
        image_paths = [os.path.join(folder_path, f) for f in image_files]

    elif os.path.isfile(raw_path):
        # Single image file
        image_paths = [raw_path]
    else:
        print(f"Path '{raw_path}' does not exist. Exiting.")
        return

    print(f"Found {len(image_paths)} image(s).\n")

    captions: list[tuple[str, str]] = []

    for idx, img_path in enumerate(image_paths, start=1):
        img_name = os.path.basename(img_path)
        print(f"[{idx}/{len(image_paths)}] Processing: {img_path}")

        try:
            with open(img_path, "rb") as img_file:
                image_bytes = img_file.read()
        except Exception as e:
            print(f"Could not load image '{img_name}'. Error: {e}")
            continue

        cap, err = query_caption(image_bytes)
        if err:
            print(f"[API Error] {err} for '{img_name}'")
            continue

        print(f"Caption: {cap}")
        captions.append((img_name, cap))

    if captions:
        # If a directory was given, it puts summary there; if a single file, use its directory
        base_folder = (
            raw_path if os.path.isdir(raw_path) else os.path.dirname(raw_path) or "."
        )
        summary_file = os.path.join(base_folder, "captions_summary.txt")
        try:
            with open(summary_file, "w", encoding="utf-8") as sf:
                for img_name, caption in captions:
                    sf.write(f"{img_name}: {caption}\n")
        except Exception as e:
            print(f"\nCould not write summary file. Error: {e}")
            return

        print(f"\nAll captions saved to: {summary_file}")
    else:
        print(
            "\nNo captions were generated. Please check for errors or try different images."
        )

   

if __name__ == "__main__":
    main()