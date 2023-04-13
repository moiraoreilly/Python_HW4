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
        return open(f"../watchlists/{chosen_file}", "r").read().split(), chosen_file
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
            file.write(stock.strip() + ' ')
    print(f"{watchlist_name} has been added.")
    file.close()


def edit_list():
    read_directory()
    edited = input("Enter a list to edit: ")
    watchlist = os.path.join('../watchlists/', edited + '.watchlist')

    while True:
        add = input(f"Would you like to add or delete? (A/D/Enter to stop) ").lower()
        if add == 'a':
            file = open(watchlist, 'a+')
            symbol = input(f"Please enter a symbol to add to {edited}: ").upper()
            if symbol not in watchlist:
                file.write(symbol + " ")
        elif add == 'd':
            file = open(watchlist, 'r')
            data = file.read().split()
            i = 1
            for stock in data:
                print(f"{i} - {stock}")
                i += 1
            deleted = input("Enter number of stock to delete: ")


            # make a dict to be able to put in number of which stock to delete
        elif add == '':
            break
        else:
            print("Please enter A, D, or press enter to stop")


def delete_list():
    watchlists = read_directory()
    if watchlists:
        choice = (input("Enter a watchlist: "))
        watchlist = os.path.join('../watchlists/', choice + '.watchlist')
        if os.path.exists(watchlist):
            answer = input("Are you sure you want to delete this watchlist? (Y/N) ").lower()
            if answer == 'y':
                os.remove(watchlist)
                print(f"{choice} has been deleted.")
            else:
                print("This file will not be deleted.")
        else:
            print(f"{choice} does not exist.")


def main():
    options = {"1": track, "2": add_list, "3": edit_list, "4": delete_list}
    while True:
        display_menu()
        choice = (input("Enter your selection: "))
        if choice == "1":
            watchlist = read_list()[0]
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