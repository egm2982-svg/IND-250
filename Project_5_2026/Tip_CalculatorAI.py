import tkinter as tk
from tkinter import ttk, messagebox

class TipCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tip Calculator")
        self.root.geometry("400x350")

        # -------------------------------
        # VARIABLES (Tkinter Variables)
        # -------------------------------
        self.bill_amount = tk.StringVar()
        self.tip_percentage = tk.StringVar(value="15%")
        self.num_people = tk.IntVar(value=1)

        self.tip_amount = tk.StringVar()
        self.total_amount = tk.StringVar()
        self.per_person = tk.StringVar()

        # Build UI
        self.create_widgets()

        # Trace changes (AUTO CALCULATE)
        self.bill_amount.trace_add("write", self.calculate)
        self.tip_percentage.trace_add("write", self.calculate)
        self.num_people.trace_add("write", self.calculate)

    def create_widgets(self):
        """Create and place all widgets"""

        # -------------------------------
        # BILL INPUT
        # -------------------------------
        tk.Label(self.root, text="Enter Bill Amount ($):").pack(pady=5)
        tk.Entry(self.root, textvariable=self.bill_amount).pack()

        # -------------------------------
        # TIP SELECTION (Dropdown)
        # -------------------------------
        tk.Label(self.root, text="Select Tip Percentage:").pack(pady=5)
        tip_menu = ttk.Combobox(
            self.root,
            textvariable=self.tip_percentage,
            values=["10%", "15%", "20%"],
            state="readonly"
        )
        tip_menu.pack()

        # -------------------------------
        # NUMBER OF PEOPLE
        # -------------------------------
        tk.Label(self.root, text="Number of Diners:").pack(pady=5)
        people_spinbox = tk.Spinbox(
            self.root,
            from_=1,
            to=6,
            textvariable=self.num_people,
            width=5
        )
        people_spinbox.pack()

        # -------------------------------
        # RESULTS DISPLAY
        # -------------------------------
        tk.Label(self.root, text="Tip Amount:").pack(pady=5)
        tk.Label(self.root, textvariable=self.tip_amount, fg="green").pack()

        tk.Label(self.root, text="Total Bill (with Tip):").pack(pady=5)
        tk.Label(self.root, textvariable=self.total_amount, fg="blue").pack()

        tk.Label(self.root, text="Amount Per Person:").pack(pady=5)
        tk.Label(self.root, textvariable=self.per_person, fg="purple").pack()

        # -------------------------------
        # EXIT BUTTON
        # -------------------------------
        tk.Button(self.root, text="Exit", command=self.root.quit, bg="red", fg="white").pack(pady=20)

    def calculate(self, *args):
        """Automatically calculate tip, total, and split"""

        try:
            # Get bill amount and convert to float
            bill = float(self.bill_amount.get())

            # Extract tip percentage (remove % symbol)
            tip_percent = int(self.tip_percentage.get().replace("%", "")) / 100

            # Number of people
            people = self.num_people.get()

            # -------------------------------
            # CALCULATIONS
            # -------------------------------
            tip = bill * tip_percent
            total = bill + tip
            per_person = total / people

            # -------------------------------
            # UPDATE DISPLAY
            # -------------------------------
            self.tip_amount.set(f"${tip:.2f}")
            self.total_amount.set(f"${total:.2f}")
            self.per_person.set(f"${per_person:.2f}")

        except ValueError:
            # Handles non-numeric input
            self.tip_amount.set("Invalid input")
            self.total_amount.set("Invalid input")
            self.per_person.set("Invalid input")


# -------------------------------
# MAIN PROGRAM
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TipCalculatorApp(root)
    root.mainloop()