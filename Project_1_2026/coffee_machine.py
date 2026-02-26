import time
from vending_machine import VendingMachine

class CoffeeVendingMachine(VendingMachine):
    def __init__(self, item_name, item_price, stock):
        super().__init__(item_name, item_price, stock)
        
        # Default values (strong black coffee)
        self.strength = 3 
        self.cream = 0
        self.sugar = 0
# Reset Balance ^ (Maybe change default?)
    # ✅ Helper method (keeps code clean) <- AI Reset balance, this creates the need for money < makes sure the balance is lower than the price, price is named to be set value in  Test
    def _has_sufficient_funds(self):
        if self.balance < self.item_price:
            print("Please insert enough money first.")
            return False
        return True
# Print prompts the user for the first command ^ Below prompts the cream setting
    def set_cream(self, count):
        if not self._has_sufficient_funds():
            return
     #If sets the numeric options for Number of Cream and requires answer   
        if 0 <= count <= 2:
            self.cream = count
        else:
            print("Cream must be between 0 and 2.")
#Else prompts the user to enter a valid input based on required coung in line 24
    def set_sugar(self, count):
        if not self._has_sufficient_funds():
            return
#def = defines the set sugar; if not is prompting not enough money; return keeps the vending machine working but send it back to the start
        if 0 <= count <= 2:
            self.sugar = count
        else:
            print("Sugar must be between 0 and 2.")
#If is another action; count determines how many are possible 
    def set_strength(self, count):
        if not self._has_sufficient_funds():
            return
#def = defined; is the set strength, need a default to work off of; same clause as above to keep the vending machine working
        if 1 <= count <= 3:
            self.strength = count
        else:
            print("Strength must be between 1 and 3.")
#If causing the choice, but requiring some value to move forward 
    def purchase(self):
        if super().purchase():
            print("Brewing...", end="")
            for _ in range(6):
                print(".", end='', flush=True)
                time.sleep(0.3)
#Def = defined; Purchase, this funciton is post defaults and customization; it is the function machine for the acutal coffee and post monetary intake
            print(f"\n☕ Coffee ready!")
            print(f"Strength: {self.strength}, Cream: {self.cream}, Sugar: {self.sugar}")

            # ✅ Reset defaults AFTER purchase
            self.strength = 3
            self.cream = 0
            self.sugar = 0
# -> ^ Reset above for next use; below is the else for lack of monetary value
        else:
            print("Unable to purchase, please come back later!")
# Menu for options listed below
    def menu(self):
        while True:
            print("\n----------------------------")
            print(f"Balance: ${self.balance:.2f}")
            print(f"Price: ${self.item_price:.2f}")
            print(f"Strength: {self.strength} | Cream: {self.cream} | Sugar: {self.sugar}")
            print("----------------------------")

            print("U-Brewit Coffee Dispenser")
            print("1. Add Funds")
            print("2. Set Strength")
            print("3. Set Cream")
            print("4. Set Sugar")
            print("5. Brew Coffee")
            print("6. Refund")
            print("7. Quit")

            try:
                option = int(input("Enter Selection: "))
            except ValueError:
                print("Invalid input.")
                continue

            if option == 1:
                money = float(input("Enter money: $"))
                self.insert_money(money)

            elif option == 2:
                strength = int(input("Enter strength (1-3): "))
                self.set_strength(strength)

            elif option == 3:
                cream = int(input("Enter cream (0-2): "))
                self.set_cream(cream)

            elif option == 4:
                sugar = int(input("Enter sugar (0-2): "))
                self.set_sugar(sugar)

            elif option == 5:
                self.purchase()

            elif option == 6:
                self.refund()

            elif option == 7:
                print("Goodbye!")
                break
