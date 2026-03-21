import requests

url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"

def get_random_fact():
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Did you know? {fact_data}['text']")
    else:
        print("Failed to fetch fact")
    
while True:
    
    user = input("Press Enter to get a new fact or press 'q' to quit:")
    
    if user.lower() == 'q':
        break
    
    get_random_fact()