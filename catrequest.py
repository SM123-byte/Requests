import requests
from colorama import Fore, init

init(autoreset=True)

def get_cat_fact():
    url = "https://catfact.ninja/fact"
    response= requests.get(url)

    if response.status_code == 200:
        print(f"{Fore.CYAN}\nFull JSON Response: {response.json()}")

        cat_data= response.json()
        return f"{Fore.GREEN}{cat_data['fact']}-{cat_data['length']}"
    
    else:
        return "Failed to retrieve fact!"
    
def main():

    print(f"{Fore.RED}\n Welcome to Random Fact Generator For Cats!\n")
    
    while True:
        user= input(f"{Fore.YELLOW}Please enter to get a new fact or type 'q'/ 'exit' to quit.").strip().lower()

        if user in ("q", "exit"):
            print(f"{Fore.MAGENTA}Goodbye!👋\n")
            break
        cat = get_cat_fact()
        print("\n", cat, "\n")

if __name__ == "__main__":
    main()