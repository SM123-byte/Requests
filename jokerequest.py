import requests
from colorama import Fore, init

init(autoreset=True)

def get_random_joke():
    url = "https://official-joke-api.appspot.com/random_joke"
    response= requests.get(url)

    if response.status_code == 200:
        print(f"{Fore.CYAN}\nFull JSON Response: {response.json()}")

        joke_data= response.json()
        return f"{Fore.GREEN}{joke_data['setup']}-{joke_data['punchline']}"
    
    else:
        return "Failed to retrieve joke!"
    
def main():

    print(f"{Fore.RED}\n Welcome to Random Joke Generator!\n")
    
    while True:
        user= input(f"{Fore.YELLOW}Please enter to get a new joke or type 'q'/ 'exit' to quit.").strip().lower()

        if user in ("q", "exit"):
            print(f"{Fore.MAGENTA}Goodbye!👋\n")
            break
        joke = get_random_joke()
        print("\n", joke, "\n")

if __name__ == "__main__":
    main()