import time
from vending_machine import VendingMachine

class CoffeeVendingMachine(VendingMachine):
    def __init__(self, item_name, item_price, stock):
        super().__init__(item_name, item_price, stock)
        
        # Default values (strong black coffee)
        self.strength = 3 
        self.cream = 0
        self.sugar = 0

    # ✅ Helper method (keeps code clean)
    def _has_sufficient_funds(self):
        if self.balance < self.item_price:
            print("Please insert enough money first.")
            return False
        return True

    def set_cream(self, count):
        if not self._has_sufficient_funds():
            return
        
        if 0 <= count <= 2:
            self.cream = count
        else:
            print("Cream must be between 0 and 2.")

    def set_sugar(self, count):
        if not self._has_sufficient_funds():
            return
        
        if 0 <= count <= 2:
            self.sugar = count
        else:
            print("Sugar must be between 0 and 2.")

    def set_strength(self, count):
        if not self._has_sufficient_funds():
            return
        
        if 1 <= count <= 3:
            self.strength = count
        else:
            print("Strength must be between 1 and 3.")

    def purchase(self):
        if super().purchase():
            print("Brewing...", end="")
            for _ in range(6):
                print(".", end='', flush=True)
                time.sleep(0.3)

            print(f"\n☕ Coffee ready!")
            print(f"Strength: {self.strength}, Cream: {self.cream}, Sugar: {self.sugar}")

            # ✅ Reset defaults AFTER purchase
            self.strength = 3
            self.cream = 0
            self.sugar = 0

        else:
            print("Unable to purchase, please come back later!")

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
