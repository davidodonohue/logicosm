import datetime
import math
import random
import os
import sys
import readchar
import random

accounts = []
prizes = []
investments = ["FOOD", "HOUSE", "CLOTH"]
skills = ["ADDITION"]
threshold = 100 # when to unlock next skill
combo = 0       # increases chance of receiving reward
combo_increment = 5
base_chance = 10
max_chance = 60         


if not os.path.exists("accounts"):
    os.mkdir("accounts")
#path = os.path.dirname(os.path.abspath(__file__))

path = os.path.abspath("accounts")

password = "abc"




#nowdate = datetime.datetime.strptime(nowstring, "%Y-%m-%d %H:%M:%S.%f")

def hash(password):
    key = "1"*len(password)
    encrypted_int = [ord(a)^ord(b) for a,b in zip(password, key)]
    encrypted_string = "".join([str(a) for a in encrypted_int])
    return encrypted_string

def save():
    file = open(os.path.join(path,current_account.name + ".acc"), "w")
    file.write(str(current_account.password) + "\n")
    file.write(str(current_account.balance) + "\n")
    for asset in current_account.portfolio:
        file.write("i," + asset + "," + str(current_account.portfolio[asset]) + "\n")
    for skill in current_account.expertise:
        file.write("e," + skill + "," + str(current_account.expertise[skill]) + "\n")
    file.close()

class account:
    def __init__(self, input, pas, bal):
        self.name = input
        self.password = pas
        self.balance = bal
        self.portfolio = {}
        self.expertise = {}
	
    def add(self, amount):
        self.balance += amount
        save()
    
    def subtract(self, amount):
        self.balance -= amount
        save()
		
    def buy(self, ticker, number):
        price = calcPrice(ticker,0) * number
        if self.balance >= price:
            self.subtract(price)
            self.portfolio[ticker] += number
            save()
            refresh(3.1, "Successfully purchased " + str(number) + " " + ticker)
        else:
            refresh(3.1, "Sorry, you don't have enough money :(")
    
    def sell(self, ticker, number):
        printAcc()
        owned = self.portfolio[ticker]
        if owned >= number:
            self.subtract(number * calcPrice(ticker,0))
            self.portfolio[ticker] -= number
            save()
            refresh(3.2, "Successfully sold " + number + " " + ticker)
        else:
            refresh(3.2, "You don't own that many :(")
            
    def experience(self, skill, xp):
        self.expertise[skill] += xp

def calcPrice(tick, history):
    today = datetime.datetime.now()
    difference = today - datetime.datetime(2000,1,1)
    num = difference.days - history
    return {
        investments[0] : (num % 2) + 50,
        investments[1] : (num % 3) + 48,
        investments[2] : int(round(math.sin(num)* 6 + 50))}[tick]

def read_accounts():
    global accounts
    accounts = []
    for filename in os.listdir(path):
        if filename.endswith(".acc"):
            name = os.path.split(filename)[1].split(".")[0]
            file = open(os.path.join(path, filename), "r")
            pw = file.readline().rstrip()
            accounts.append((name,pw)) # new addition
            file.close()    

# clear the terminal
def clear():
    os.system('cls||clear')

# print the information associated with the current account
def print_balance():
    print ("\n" + current_account.name + "'s balance: \t$" + str(current_account.balance))

def print_portfolio():
    print ("\n" + current_account.name + "'s portfolio:")
    for asset in current_account.portfolio:
        print (asset + ":\t\t\t" + str(current_account.portfolio[asset]))

# load a selected account as the current account
def load_account(name):
    global current_account
    filename = os.path.join(path, name) + ".acc"
    file = open(filename, "r")
    current_account = account(name, file.readline().rstrip(), int(file.readline()))
    for asset in investments:
        current_account.portfolio[asset] = 0
    for line in file:
        lst = line.split(",")
        if lst[0] == 'i':
            t = lst[1]
            if t in investments:
                current_account.portfolio[t] = int(lst[2])
        elif lst[0] == 'e':
            s = lst[1]
            current_account.expertise[s] = int(lst[2])
    refresh(0.1, "Successfully logged in!")


def createAcc():
    name = input("Please enter a name for the new account:")
    if any(x.lower() == name.lower() for x in accounts):
        refresh(0, "An account already exists with that name!")
    else:
        pw = hash(input("Please enter a password for this account:"))
        global current_account
        current_account = account(name, pw, 0)
        for asset in investments:
            current_account.portfolio[asset] = 0
        save()
        refresh(0.1, "Successfully created account!")

def printInvestments():
    print ("\nToday's investment prices:")
    for asset in investments:
        print (asset + ":\t\t\t" + str(calcPrice(asset,0)))

def quit():
    save()
    clear()
    sys.exit()
    
def select_account():
    if len(accounts) > 0:
        print ("\nWhich account would you like to access? Or press 'n' to create a new account")
        for index,(name,truepw) in enumerate(accounts):
            print(str(index + 1) + ": " + name)
        n = input("")
        if n == "n":
            createAcc()
        elif str.isdigit(n):
            if int(n)-1 <= len(accounts):
                pw = hash(input("Please enter your password:"))
                if pw == truepw:
                    load_account(name)
                else:
                    refresh(0, "Incorrect password!")
            refresh(0, "That account does not exist!")
        elif n.lower() in (name.lower() for (name,pw) in accounts):
            acc = [(x,y) for x,y in accounts if x.lower() == n.lower()]
            pw = hash(input("Please enter your password:"))
            if pw == acc[0][1]:
                load_account(acc[0][0])
            else:
                refresh(0, "Incorrect password!")
        else:
            refresh(0, "I didn't understand what you wrote :(")
    else:
        print("\nNo accounts detected!")
        createAcc()

def printHistory(days):
    for asset in investments:
        print (asset + " prices: ")
        for i in range(-1*days,-1):
            print (str(calcPrice(asset,i)), end=", ")
        print(str(calcPrice(asset,0)))
        
def read_prizes():
    global prizes
    file = open(os.path.join(path,"prizes.config"), "r")
    for line in file:
        info = line.split(",")
        prizes.append((info[0],info[1].rstrip()))

def refresh(state, status):
    clear()
    print(status)
    interface(state)

def interface(state):
    if state == 0:          # account not selected
        read_accounts()
        select_account()
    elif state == 0.1:           # account selected, main screen
        print_balance()
        print("\n1:\tLearning path\n2:\tPrize shop\n3:\tExchange market\n4:\tAchievements\n5:\tAdd money\n\nOr press 'q' to save and quit\n")
        inp = input("")
        if inp == '1':
            refresh(1, "Learning path")
        elif inp == '2':
            refresh(2,"Prize shop")
        elif inp == '3':
            refresh(3, "Exchange market")
        elif inp == '4':
            refresh(4, "Acievements have not yet been built")
        elif inp == '5':
            pw = input("Please enter the password to access this feature:")
            if pw != password:
                refresh(0.1, "Sorry! That password was not correct!")
            else:
                num = input("How much would you like to add?\n")
                current_account.add(int(num))
                refresh(0.1, "Successfully added $" + num + "!")
        elif inp == 'q':
            quit()
        else:
            refresh(0.1, "I don't know what that means!")
    elif state == 1:          # Learning path
        learn()
    elif state == 2:          #prizes
        for index, (prize, price) in enumerate(prizes):
            print(str(index+1) + ":\t" + prize + " for $" + price)
        print_balance()
        t = input("\nWhich prize would you like to buy? Or, press 'q' to return to the main menu\n")
        if t == 'q':
            refresh(0.1, "Welcome!")
        elif t.isdigit() and int(t)-1 < len(prizes):
            price = int(prizes[int(t)-1][1])
            if current_account.balance >= price:
                current_account.subtract(price)
                refresh(2, "Successfully bought " + prizes[int(t)-1][0])
            else:
                refresh(2, "You can't afford that prize!")
        else:
            refresh(2, "That isn't an input I recognise :(")
                    
    elif state == 3:       # Exchange market
        printInvestments()
        print_balance()
        print_portfolio()
        inp = input("Press 'b' to buy, 's' to sell, 'h' to check the history of prices, or 'q' to return to the main screen\n")
        if inp == 'b':
            refresh(3.1, "Exchange market: buying")
        elif inp == 's':
            refresh(3.2, "Exchange market: selling")
        elif inp == "h":
            refresh(3.3, "Exchange market: history")
        elif inp == "q":
            refresh(0.1, "Welcome!")
        else:
            refresh(3, "I don't know what you want to do :(")
    elif state == 3.1:      #Exchange: buying
        printInvestments()
        print_balance()
        inp = input("What would you like to buy? Or press 'e' to return to the main exchange market, or 'q' to return to the main menu\n")
        if inp == 'e':
            refresh(3, "Exchange market")
        elif inp == 'q':
            refresh(0.1, "Welcome!")
        elif inp.isdigit() and int(inp) < len(investments):
            n = input("How much " + investments[int(imp)] + " would you like to buy?\n")
            current_account.buy(inp, int(n))
        elif inp.upper() in investments:
            n = input("How much " + inp.upper() + " would you like to buy?\n")
            current_account.buy(inp.upper(), int(n))
        else:
            refresh(3.1, "I don't know what that is :(")
    elif state == 3.2:       #Exchange: selling
        printInvestments()
        print_portfolio()
        inp = input("What would you like to sell? Or press 'e' to return to the main exchange market, or 'q' to return to the main menu\n")
        if inp == 'e':
            refresh(3, "Exchange market")
        elif inp == 'q':
            refresh(0.1, "Welcome!")
        elif inp.isdigit() and int(inp) <= len(investments):
            n = input("How much " + investments[int(inp)] + " would you like to sell?\n")
            current_account.sell(inp, int(n))
        elif inp.upper() in investments:
            n = input("How much " + inp.upper() + " would you like to sell?\n")
            current_account.sell(inp.upper(), int(n))
        else:
            refresh(3.2, "I don't know what that is :(")
    elif state == 3.3:      #price history
        l = input("Select a number of days to look back on, press 'e' to go back to the exchange market, or press 'q' to go back to the main menu\n")
        if l == 'q':
            refresh(0.1, "Welcome!")
        elif l == 'e':
            refresh(3, "Exchange market")
        else:
            if str.isdigit(l):
                printHistory(int(l))
            else:
                refresh(3.3, "Please enter a number!")
        inp = input("Press 'e' to return to the exchange market, 'q' to return to the main menu, or 'h' to check the history again:")
        if inp == 'e':
            refresh(3, "Exchange market")
        elif inp == 'q':
            refresh(0.1, "Welcome!")
        elif inp == 'h':
            refresh(3.3, "Exchange: price history")
        else:
            refresh(3.3, "I don't know what that means :(")
    elif state == 4:        #Acievements
        next = input("Achievements are not yet available. Press any key to return to the main menu.")
        refresh(0.1, "Welcome!")

def reward_amount(selection):   
    global combo
    roll = random.randint(0,100) + min(combo, max_chance - base_chance)
    if roll > (100 - base_chance):
        return int(selection)
    else:
        return 0
    

def try_again(selection, true_ans):
    global combo
    combo = 0
    next = input("The correct answer is " + str(true_ans) + ". Press any key to try again, or 'q' to return to the main menu\n")
    if next == 'q':
        refresh(0.1, "Welcome!")
    else:
        journey(selection)

def learn():        # Main screen for learning path
    print("Choose a path, or press 'q' to return to the main menu")
    for index, skill in enumerate(skills):
        if skill == "ADDITION":
            print(str(index+1) + ": " + skill)
        elif current_account.expertise[skills[index-1]] >= threshold:
            print(str(index+1) + ": " + skill)
    selection = input("")
    if selection == 'q':
        refresh(0.1, "Welcome!")
    elif selection.isdigit and current_account.expertise[skills[index-1]] >= threshold:
        journey(selection)

def journey(selection):
    while True:
        clear()
        if selection == '1':    # Addition
            fst = random.randint(0,9)
            snd = random.randint(0,9)
            ans = input(str(fst) + " + " + str(snd) + " = ")
            if int(ans) == (fst + snd):
                success(selection)
            else:
                try_again(selection, fst+snd)
        else:
            refresh(0.1, "Welcome!")

def success(selection):
    global combo
    combo += combo_increment
    reward = reward_amount(selection)
    current_account.expertise[skills[int(selection)-1]] += 1
    if current_account.expertise[skills[int(selection)-1]] == 100 and len(skills) > int(selection) + 1:
        print("CONGRATULATIONS! You have unlocked the next skill!")
    if reward > 0:
        current_account.add(reward)
        save()
        next = input("Correct! You have been given $" + str(reward) + " for your hard work. Press any key for another question, or 'q' to return to the main menu\n")
        if next == 'q':
            refresh(0.1, "Welcome!")
        else:
            journey(selection)            
    else:
        next = input("Correct! Press any key for another question, or 'q' to return to the main menu\n")
        if next == 'q':
            refresh(0.1, "Welcome!")
        else:
            journey(selection) 


read_prizes()
refresh(0, "Welcome!")