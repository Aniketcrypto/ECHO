import os
import requests
import random
import json
import time
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# File paths
ACCOUNTS_FILE = "accounts.json"
PROXIES_FILE = "proxies.txt"
BANNER_URL = "https://raw.githubusercontent.com/Aniketcrypto/aniketcrypto/refs/heads/main/echo.json"

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Fetch and display the banner
def print_banner():
    try:
        response = requests.get(BANNER_URL)
        if response.status_code == 200:
            banner = response.text
            print(Fore.CYAN + banner)
        else:
            print(Fore.RED + "Failed to fetch banner. Please check the URL.")
    except Exception as e:
        print(Fore.RED + f"Error fetching banner: {e}")
    print(Style.RESET_ALL)

# Generate a random User-Agent
def generate_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.49 Safari/537.36",
    ]
    return random.choice(user_agents)

# Load accounts from JSON file
def load_accounts():
    try:
        with open(ACCOUNTS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save accounts to JSON file
def save_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        json.dump(accounts, file, indent=4)

# Load proxies from file
def load_proxies():
    try:
        with open(PROXIES_FILE, "r") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        return []

# Save proxies to file
def save_proxies(proxies):
    with open(PROXIES_FILE, "w") as file:
        for proxy in proxies:
            file.write(proxy + "\n")

# Add a new account
def add_account():
    account_name = input(Fore.CYAN + "Enter account name: ")
    auth_token = input(Fore.CYAN + "Enter auth token: ")

    accounts = load_accounts()
    accounts[account_name] = {"auth_token": auth_token}
    save_accounts(accounts)

    print(Fore.GREEN + f"Account '{account_name}' added successfully!")

# Add proxies
# Add proxies
def add_proxies():
    proxies = []
    accounts = load_accounts()
    num_accounts = len(accounts)

    print(Fore.CYAN + f"Add {num_accounts} proxies (one per account).")
    print(Fore.CYAN + "Enter all proxies in separate lines, then press 'Ctrl+D' to finish:")

    try:
        # Read proxies until EOF (Ctrl+D)
        while True:
            proxy = input()
            if proxy.strip():  # Ignore empty lines
                proxies.append(proxy.strip())
    except EOFError:
        pass  # Stop reading when 'Ctrl+D' is pressed

    # Validate if the number of proxies matches the number of accounts
    if len(proxies) != num_accounts:
        print(Fore.RED + f"Error: You must provide exactly {num_accounts} proxies.")
        return

    save_proxies(proxies)
    print(Fore.GREEN + "Proxies added successfully!")

# Perform check-in for an account
def perform_check_in(account_name, account_data):
    """Perform daily check-in for the given account."""
    url = "https://api.sayecho.xyz/daily-waves"
    headers = {
        "User-Agent": generate_random_user_agent(),
        "Authorization": account_data["auth_token"],
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Referer": "https://www.sayecho.xyz",
    }

    print(Fore.YELLOW + f"Performing check-in for account: {account_name}...")
    response = requests.post(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        earned_points = data.get("score", 0)  # Points earned from check-in
        print(Fore.GREEN + f"Check-in successful! Points earned: {earned_points}")

        # Fetch total points and rank
        fetch_account_info(account_name, account_data)
    else:
        print(Fore.RED + f"Check-in failed! Response: {response.text}")

# Fetch account info (total points, rank)
def fetch_account_info(account_name, account_data):
    """Fetch total points and rank for the given account."""
    url = "https://api.sayecho.xyz/me"
    headers = {
        "User-Agent": generate_random_user_agent(),
        "Authorization": account_data["auth_token"],
        "Content-Type": "application/json",
        "Accept": "*/*",
        "Referer": "https://www.sayecho.xyz",
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        total_points = data.get("score", 0)  # Total points
        rank = data.get("rank", "N/A")  # Rank
        print(Fore.BLUE + f"Total Points: {total_points}")
        print(Fore.MAGENTA + f"Rank: {rank}")
    else:
        print(Fore.RED + f"Failed to fetch account info! Response: {response.text}")

# Perform daily check-in for all accounts
def daily_check_in_all_accounts():
    """Perform daily check-in for all accounts."""
    accounts = load_accounts()
    if not accounts:
        print(Fore.RED + "No accounts found. Please add an account first.")
        return

    for account_name, account_data in accounts.items():
        perform_check_in(account_name, account_data)

# Main script
def main():
    clear_screen()
    print_banner()

    while True:
        print(Fore.CYAN + "\n--- Daily Check-In Script ---")
        print(Fore.YELLOW + "1. Add Account")
        print(Fore.YELLOW + "2. Add Proxies")
        print(Fore.YELLOW + "3. Perform Check-In (One Time)")
        print(Fore.YELLOW + "4. Start 24-Hour Check-In Loop")
        print(Fore.YELLOW + "5. Exit")

        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == "1":
            add_account()
        elif choice == "2":
            add_proxies()
        elif choice == "3":
            daily_check_in_all_accounts()
        elif choice == "4":
            print(Fore.GREEN + "Starting 24-hour check-in loop...")
            while True:
                daily_check_in_all_accounts()
                print(Fore.YELLOW + "Waiting 24 hours for the next check-in...")
                time.sleep(24 * 60 * 60)  # Wait for 24 hours
        elif choice == "5":
            print(Fore.GREEN + "Exiting script. Have a nice day!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
