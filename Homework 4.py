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
    stocks = []
    while True:
        stock = input("Enter a symbol: ").upper()
        if stock != '' and stock not in stocks:
            stocks.append(stock)
        else:
            if stock == '':
                watchlist_name = input("Enter a name for watchlist: ")
                watchlist = os.path.join('../watchlists/', watchlist_name + '.watchlist')
                break
    with open(watchlist, 'w') as file:
        for stock in stocks:
            file.write(stock.strip())


def edit_list():
    read_directory()
    edited = input("Enter a list to edit: ")




def delete_list():
    watchlists = read_directory()
    if watchlists:
        choice = int(input("Enter a watchlist number: "))
        chosen_file = watchlists[choice - 1]
        if os.path.exists(chosen_file):
            answer = input("Are you sure you want to delete this watchlist? (Y/N) ").lower()
            if answer == 'y':
                os.remove(chosen_file)
                print(f"{chosen_file} has been deleted.")
            else:
                print("This file will not be deleted.")
        else:
            print(f"{chosen_file} does not exist.")


options = {"1": track, "2": add_list, "3": edit_list, "4": delete_list}


def main():
    while True:
        display_menu()
        choice = (input("Enter your selection: "))
        if choice == "1":
            read_list()
            # not sure how to make the chosen watchlist be the one that gets tracked
            watchlist = "AMZN AAPL GOOG FB".split()
            options[choice](watchlist)
        elif choice in "2":
            options[choice]()
        elif choice in "3":
            options[choice]()
        elif choice in "4":
            options[choice]()
        elif choice == '5':
            print("Goodbye!")
            sleep(1)
            sys.exit()
        else:
            print("Enter a valid selection")


if __name__ == "__main__":
    main()