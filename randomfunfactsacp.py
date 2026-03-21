import requests

j_url = "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
t_url = "https://uselessfacts.jsph.pl/api/v2/facts/today?language=en"

def get_facts(url):
    response = requests.get(url)
    if response.status_code == 200:
        fact_data = response.json()
        print(f"Did you know? {fact_data['text']}")
    else:
        print("Did you know? We just failed to fetch fact!")

print("Please choose the topic：")
print("1. Random fact")
print("2. Today's fact")

choice = input("Please enter 1 or 2：")

if choice == "1":
    selected_url = j_url
elif choice == "2":
    selected_url = t_url
else:
    print("Invalid input")
    
while True:
    user_input = input("Press enter to get new facts, or press 'q' to quit.")
    if user_input.lower() == "q":
        break
    get_facts(selected_url)