import os
import pandas_datareader as pdr
import sys
from time import sleep, time
import yfinance as yf

def display_menu():
    print("""
StockTracker Menu
1. Track watchlist
2. Add watchlist
3. Edit watchlist
4. Delete watchlist
5. Exit
    """)


def read_directory():
    if not os.path.exists("../watchlists/"):
        print("No saved watchlists")
        os.mkdir("../watchlists")
    else:
        files = sorted(os.listdir("../watchlists"))
        if not files:
            print("No available watchlists")
        else:
            print("Available watchlists:")
            print("-" * 21)
            for number, name in enumerate(files, 1):
                if name.endswith('watchlist'):
                    name = name.replace('.watchlist', '')
                    print(f"{number} - {name}")
            return files


def read_list():
    watchlists = read_directory()
    if watchlists:
        choice = int(input("Enter a watchlist number: "))
        chosen_file = watchlists[choice - 1]
        return open(f"../watchlists/{chosen_file}", "r").read().split()
    else:
        return "Select add a list from the menu..."


def track(watchlist):
    start_time = time()
    prompt = ''
    while True:
        for symbol in watchlist:
            try:
                print(f'{symbol:8}{pdr.get_quote_yahoo(symbol)["price"].values[0]}')
                sleep(1)
                if time() - start_time >= 10:
                    start_time = time()
                    prompt = input("To continue press enter, any key to quit: ")
            except:
                print(f"{symbol} not found")
        print(f"Elapsed time: {time() - start_time}")
        if prompt.isalpha():
            break


def add_list():
    while True:
        new_list = input(print("Enter a symbol: ")).upper()
        if new_list == '':
            name = input(print("Enter a name for watchlist: "))


def edit_list():
    print("Enter a list to add")


def delete_list():
    print("Enter a list to delete: ")


options = {"1": track, "2": add_list, "3": edit_list, "4": delete_list}


def main():
    while True:
        display_menu()
        choice = (input("Enter your selection: "))
        if choice == "1":
            read_list()
            watchlist = "AMZN AAPL GOOG FB".split()
            options[choice](watchlist)
        elif choice in "234":
            options[choice]()
        elif choice == '5':
            print("Goodbye!")
            sleep(1)
            sys.exit()
        else:
            print("Enter a valid selection")


if __name__ == "__main__":
    main()