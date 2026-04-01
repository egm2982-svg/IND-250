#import tkinter as tk #pulling in the extenension tkinter which will generate the userface graphics
#from tkinter import
#def 
   # root = tk.TK() #establishes the tkinter needs to be activated; root is the variable
# Widgets will now be added - Autocompletion will allow us to pull in the code - Use AI to explain the actions in the library 
#label = tk.Label(root, text='GeeksForGeeks.org!') label.pack()
#root,title("") #button=tk.Button(root, text="Stop", width=25, command=root.destroy) button.pack() #root.mainloop #command is what the action is uppon use of the button
#entry1.grid(row-0, column1) - use to create a command entry #resize must be called in order to move pixels to match window size
#fixed for resize is an option to avoid any odd auto formats
#var1=tk.IntVar() #var2=tk.Intvar() -> #tk.checkbutton(root, text='male',variable=var1).grid(row-0, sticky=tk.w) *sticky will move if possible* W signifies west*
#Checkbutton needs a variable to pull and push information to - txtt with A and B can be used as .pack(anchor) to creat options
#lb=tk.Listbox(root) #lb.insert(#value)
#canvas can draw mathematical equations - use for formulas
#see notes from Week 12
#root.mainloop() #checking and waiting for input END
# -------------------------------
# IMPORTS
# -------------------------------
import tkinter as tk  # Core GUI library
from tkinter import ttk
import ttkbootstrap as tb  # Modern styling (BONUS)

# -------------------------------
# CLASS-BASED APPLICATION
# -------------------------------
class TipCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Tip Calculator")
        self.root.geometry("450x400")

        # -------------------------------
        # VARIABLES (store input/output)
        # -------------------------------
        self.bill_var = tk.StringVar()
        self.tip_var = tk.StringVar(value="15%")
        self.people_var = tk.IntVar(value=1)

        # Extra widgets
        self.round_var = tk.IntVar()  # checkbox (round up option)

        self.tip_result = tk.StringVar()
        self.total_result = tk.StringVar()
        self.per_person_result = tk.StringVar()

        # Build UI
        self.create_widgets()

        # AUTO UPDATE (no button needed)
        self.bill_var.trace_add("write", self.calculate)
        self.tip_var.trace_add("write", self.calculate)
        self.people_var.trace_add("write", self.calculate)
        self.round_var.trace_add("write", self.calculate)

    # -------------------------------
    # UI CREATION FUNCTION
    # -------------------------------
    def create_widgets(self):

        # Label
        tk.Label(self.root, text="Enter Bill Amount ($):").grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Entry (user input)
        entry1 = tk.Entry(self.root, textvariable=self.bill_var)
        entry1.grid(row=0, column=1)

        # -------------------------------
        # TIP DROPDOWN (Combobox)
        # -------------------------------
        tk.Label(self.root, text="Tip Percentage:").grid(row=1, column=0, sticky="w")

        tip_menu = ttk.Combobox(
            self.root,
            textvariable=self.tip_var,
            values=["10%", "15%", "20%"],
            state="readonly"
        )
        tip_menu.grid(row=1, column=1)

        # -------------------------------
        # NUMBER OF PEOPLE (Spinbox)
        # -------------------------------
        tk.Label(self.root, text="Number of Diners:").grid(row=2, column=0, sticky="w")

        spin = tk.Spinbox(self.root, from_=1, to=6, textvariable=self.people_var)
        spin.grid(row=2, column=1)

        # -------------------------------
        # CHECKBOX (From your notes)
        # -------------------------------
        tk.Checkbutton(
            self.root,
            text="Round Up Per Person",
            variable=self.round_var
        ).grid(row=3, column=0, columnspan=2, sticky="w")

        # -------------------------------
        # LISTBOX (From your notes)
        # Shows quick tip suggestions
        # -------------------------------
        tk.Label(self.root, text="Tip Suggestions:").grid(row=4, column=0, sticky="w")

        self.listbox = tk.Listbox(self.root, height=3)
        self.listbox.insert(1, "Good Service (15%)")
        self.listbox.insert(2, "Great Service (20%)")
        self.listbox.insert(3, "Excellent (25%)")
        self.listbox.grid(row=4, column=1)

        # -------------------------------
        # OUTPUT LABELS
        # -------------------------------
        tk.Label(self.root, text="Tip Amount:").grid(row=5, column=0, sticky="w")
        tk.Label(self.root, textvariable=self.tip_result).grid(row=5, column=1)

        tk.Label(self.root, text="Total Bill:").grid(row=6, column=0, sticky="w")
        tk.Label(self.root, textvariable=self.total_result).grid(row=6, column=1)

        tk.Label(self.root, text="Per Person:").grid(row=7, column=0, sticky="w")
        tk.Label(self.root, textvariable=self.per_person_result).grid(row=7, column=1)

        # -------------------------------
        # EXIT BUTTON
        # command defines action when clicked
        # -------------------------------
        tk.Button(self.root, text="Exit", command=self.root.destroy, bg="red", fg="white").grid(
            row=8, column=0, columnspan=2, pady=10
        )

    # -------------------------------
    # CALCULATION FUNCTION
    # -------------------------------
    def calculate(self, *args):
        try:
            # Convert bill input to float
            bill = float(self.bill_var.get())

            # Convert tip percentage
            tip_percent = int(self.tip_var.get().replace("%", "")) / 100

            # Number of people
            people = self.people_var.get()

            # -------------------------------
            # CALCULATIONS
            # -------------------------------
            tip = bill * tip_percent
            total = bill + tip
            per_person = total / people

            # OPTIONAL ROUNDING (checkbox)
            if self.round_var.get() == 1:
                per_person = round(per_person)

            # -------------------------------
            # DISPLAY RESULTS
            # -------------------------------
            self.tip_result.set(f"${tip:.2f}")
            self.total_result.set(f"${total:.2f}")
            self.per_person_result.set(f"${per_person:.2f}")

        except ValueError:
            # Handles non-numeric input
            self.tip_result.set("Invalid")
            self.total_result.set("Invalid")
            self.per_person_result.set("Invalid")


# -------------------------------
# MAIN PROGRAM
# -------------------------------
if __name__ == "__main__":
    root = tb.Window(themename="cosmo")  # ttkbootstrap theme
    app = TipCalculatorApp(root)
    root.mainloop()