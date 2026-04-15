import tkinter as tk #Import the tools and exe needed for the project
from tkinter import ttk

class TipCalculatorApp: #The Machine - Userface titles and options
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Tip App")
        self.root.geometry("420x520")
        self.root.configure(bg="#eaf4ff")  # soft mobile background

        # -------------------------------
        # VARIABLES
        # -------------------------------
        self.bill_amount = tk.StringVar()
        self.tip_percentage = tk.StringVar(value="18%")
        self.num_people = tk.IntVar(value=1)
        self.state = tk.StringVar(value="Virginia")
        self.service_type = tk.StringVar(value="Dine-In")

        self.tip_amount = tk.StringVar()
        self.tax_amount = tk.StringVar()
        self.total_amount = tk.StringVar()
        self.per_person = tk.StringVar()
        self.tip_advice = tk.StringVar()

        # -------------------------------
        # ALL 50 STATES TAX RATES (approx avg) - pulled from ChatGPT, possibly not accurate
        # -------------------------------
        self.tax_rates = {
            "Alabama": 0.04, "Alaska": 0.00, "Arizona": 0.056,
            "Arkansas": 0.065, "California": 0.0725, "Colorado": 0.029,
            "Connecticut": 0.0635, "Delaware": 0.00, "Florida": 0.06,
            "Georgia": 0.04, "Hawaii": 0.04, "Idaho": 0.06,
            "Illinois": 0.0625, "Indiana": 0.07, "Iowa": 0.06,
            "Kansas": 0.065, "Kentucky": 0.06, "Louisiana": 0.0445,
            "Maine": 0.055, "Maryland": 0.06, "Massachusetts": 0.0625,
            "Michigan": 0.06, "Minnesota": 0.06875, "Mississippi": 0.07,
            "Missouri": 0.04225, "Montana": 0.00, "Nebraska": 0.055,
            "Nevada": 0.0685, "New Hampshire": 0.00, "New Jersey": 0.06625,
            "New Mexico": 0.05125, "New York": 0.04, "North Carolina": 0.0475,
            "North Dakota": 0.05, "Ohio": 0.0575, "Oklahoma": 0.045,
            "Oregon": 0.00, "Pennsylvania": 0.06, "Rhode Island": 0.07,
            "South Carolina": 0.06, "South Dakota": 0.045,
            "Tennessee": 0.07, "Texas": 0.0625, "Utah": 0.061,
            "Vermont": 0.06, "Virginia": 0.053, "Washington": 0.065,
            "West Virginia": 0.06, "Wisconsin": 0.05, "Wyoming": 0.04,
            "District of Columbia": 0.06
        }

        self.create_widgets()

        # Auto update - Pulling the state tax 
        for var in [self.bill_amount, self.tip_percentage, self.state, self.num_people]:
            var.trace_add("write", self.calculate)

    # -------------------------------
    # UI (MOBILE STYLE) - Asked CHAT GPT to update the userface style
    # -------------------------------
    def create_widgets(self): #This has all the fonts, colors, graphics and columns

        container = tk.Frame(self.root, bg="#eaf4ff") #text box, color
        container.pack(fill="both", expand=True, padx=15, pady=10) #Size and information

        # TITLE
        tk.Label(
            container,
            text="💸 Smart Tip",
            font=("Segoe UI", 18, "bold"),
            bg="#eaf4ff"
        ).pack(pady=10)

        # INPUT CARD
        card = tk.Frame(container, bg="white", bd=0, relief="flat")
        card.pack(fill="x", pady=10)

        def styled_label(text):
            return tk.Label(card, text=text, bg="white", font=("Segoe UI", 10))

        def styled_entry(var):
            return tk.Entry(card, textvariable=var, font=("Segoe UI", 11), bd=1)

        # Bill
        styled_label("Bill Amount").grid(row=0, column=0, pady=8, padx=10, sticky="w")
        styled_entry(self.bill_amount).grid(row=0, column=1, padx=10)

        # Tip % - Information, not calculation
        styled_label("Tip %").grid(row=1, column=0, pady=8, padx=10, sticky="w")
        ttk.Combobox(
            card,
            textvariable=self.tip_percentage,
            values=["10%", "15%", "18%", "20%", "25%"],
            state="readonly"
        ).grid(row=1, column=1)

        # People
        styled_label("People").grid(row=2, column=0, pady=8, padx=10, sticky="w")
        tk.Spinbox(card, from_=1, to=10, textvariable=self.num_people).grid(row=2, column=1)

        # State
        styled_label("State").grid(row=3, column=0, pady=8, padx=10, sticky="w")
        ttk.Combobox(
            card,
            textvariable=self.state,
            values=list(self.tax_rates.keys()),
            state="readonly"
        ).grid(row=3, column=1)

        # Service type
        styled_label("Service").grid(row=4, column=0, pady=8, padx=10, sticky="w")
        ttk.Combobox(
            card,
            textvariable=self.service_type,
            values=["Dine-In", "Takeout", "Delivery"],
            state="readonly"
        ).grid(row=4, column=1)

        # RESULTS CARD
        result = tk.Frame(container, bg="#dff6ff")
        result.pack(fill="x", pady=10)

        def result_label(text, var):
            tk.Label(result, text=text, bg="#dff6ff").pack(anchor="w", padx=10)
            tk.Label(result, textvariable=var, font=("Segoe UI", 12, "bold"), bg="#dff6ff").pack(anchor="w", padx=10)

        result_label("Tax", self.tax_amount)
        result_label("Tip", self.tip_amount)
        result_label("Total", self.total_amount)
        result_label("Per Person", self.per_person)

        # ADVICE CARD
        advice = tk.Frame(container, bg="#fff4cc")
        advice.pack(fill="x", pady=10)

        tk.Label(advice, text="💡 Tip Advice", bg="#fff4cc", font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10)
        tk.Label(advice, textvariable=self.tip_advice, wraplength=350, bg="#fff4cc").pack(anchor="w", padx=10)

        ttk.Button(container, text="Exit", command=self.root.quit).pack(pady=10)

    # -------------------------------
    # CALCULATIONS
    # -------------------------------
    def calculate(self, *args): #Calcuation for the ouptut of the text boxes above ^
        try:
            bill = float(self.bill_amount.get())
            tip_percent = int(self.tip_percentage.get().replace("%", "")) / 100
            people = self.num_people.get()
            state = self.state.get()
            service = self.service_type.get()

            tax_rate = self.tax_rates[state]
            tax = bill * tax_rate
            tip = bill * tip_percent
            total = bill + tax + tip
            per_person = total / people

            self.tax_amount.set(f"${tax:.2f}")
            self.tip_amount.set(f"${tip:.2f}")
            self.total_amount.set(f"${total:.2f}")
            self.per_person.set(f"${per_person:.2f}")

            # Etiquette logic
            if service == "Dine-In":
                advice = "18–22% is standard for full service."
            elif service == "Delivery":
                advice = "15–20% depending on distance and conditions."
            else:
                advice = "10–12% is acceptable for takeout."

            if tax_rate > 0.065:
                advice += " Higher-tax state → tipping slightly more is common."

            self.tip_advice.set(advice)

        except:
            self.tax_amount.set("—")
            self.tip_amount.set("—")
            self.total_amount.set("—")
            self.per_person.set("—")
            self.tip_advice.set("Enter valid inputs.")
            

# RUN
if __name__ == "__main__":
    root = tk.Tk()
    app = TipCalculatorApp(root)
    root.mainloop()