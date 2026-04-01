import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime

# -------------------------------
# MAIN APPLICATION CLASS
# -------------------------------
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calendar Planner")
        self.root.geometry("800x600")

        # -------------------------------
        # DATA STORAGE
        # Stores events as:
        # {date: [(title, category)]}
        # -------------------------------
        self.events = {}

        # Category colors
        self.categories = {
            "Work": "#FF6B6B",
            "School": "#4D96FF",
            "Gym": "#6BCB77",
            "Personal": "#FFD93D"
        }

        # Current date
        now = datetime.now()
        self.year = now.year
        self.month = now.month

        # UI Setup
        self.create_widgets()
        self.draw_calendar()

    # -------------------------------
    # UI SETUP
    # -------------------------------
    def create_widgets(self):

        # Header (Month navigation)
        header = tk.Frame(self.root)
        header.pack(pady=10)

        tk.Button(header, text="<", command=self.prev_month).pack(side="left")
        self.month_label = tk.Label(header, text="", font=("Arial", 16))
        self.month_label.pack(side="left", padx=20)
        tk.Button(header, text=">", command=self.next_month).pack(side="left")

        # Calendar frame
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        # -------------------------------
        # EVENT INPUT SECTION
        # -------------------------------
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Date (YYYY-MM-DD):").grid(row=0, column=0)
        self.date_entry = tk.Entry(form)
        self.date_entry.grid(row=0, column=1)

        tk.Label(form, text="Event Title:").grid(row=1, column=0)
        self.title_entry = tk.Entry(form)
        self.title_entry.grid(row=1, column=1)

        tk.Label(form, text="Category:").grid(row=2, column=0)

        self.category_var = tk.StringVar(value="Work")
        ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=list(self.categories.keys()),
            state="readonly"
        ).grid(row=2, column=1)

        # Add event button
        tk.Button(form, text="Add Event", command=self.add_event, bg="#4CAF50", fg="white").grid(
            row=3, column=0, columnspan=2, pady=5
        )

        # -------------------------------
        # TEMPLATE SECTION
        # -------------------------------
        template_frame = tk.Frame(self.root)
        template_frame.pack(pady=10)

        tk.Label(template_frame, text="Schedule Templates:").pack()

        tk.Button(template_frame, text="Work Week Template", command=self.apply_work_template).pack(side="left", padx=5)
        tk.Button(template_frame, text="Student Template", command=self.apply_student_template).pack(side="left", padx=5)
        tk.Button(template_frame, text="Fitness Template", command=self.apply_fitness_template).pack(side="left", padx=5)

    # -------------------------------
    # DRAW CALENDAR
    # -------------------------------
    def draw_calendar(self):

        # Clear previous calendar
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.month_label.config(text=f"{calendar.month_name[self.month]} {self.year}")

        cal = calendar.monthcalendar(self.year, self.month)

        # Days of week header
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=("Arial", 10, "bold")).grid(row=0, column=col)

        # Fill calendar
        for row_idx, week in enumerate(cal, start=1):
            for col_idx, day in enumerate(week):
                if day == 0:
                    continue

                date_str = f"{self.year}-{self.month:02d}-{day:02d}"

                # Frame for each day
                frame = tk.Frame(self.calendar_frame, borderwidth=1, relief="solid", width=100, height=80)
                frame.grid(row=row_idx, column=col_idx, padx=2, pady=2)
                frame.grid_propagate(False)

                tk.Label(frame, text=str(day)).pack(anchor="nw")

                # Display events
                if date_str in self.events:
                    for title, category in self.events[date_str]:
                        tk.Label(
                            frame,
                            text=title,
                            bg=self.categories.get(category, "white"),
                            wraplength=80
                        ).pack(fill="x")

    # -------------------------------
    # ADD EVENT
    # -------------------------------
    def add_event(self):
        date = self.date_entry.get()
        title = self.title_entry.get()
        category = self.category_var.get()

        if not date or not title:
            messagebox.showwarning("Input Error", "Please fill all fields")
            return

        if date not in self.events:
            self.events[date] = []

        self.events[date].append((title, category))

        self.draw_calendar()

    # -------------------------------
    # TEMPLATE FUNCTIONS
    # -------------------------------
    def apply_work_template(self):
        """Adds a standard 9–5 work schedule for weekdays"""
        for day in range(1, 29):
            date = f"{self.year}-{self.month:02d}-{day:02d}"
            weekday = datetime(self.year, self.month, day).weekday()

            if weekday < 5:  # Monday-Friday
                self.events.setdefault(date, []).append(("Work 9-5", "Work"))

        self.draw_calendar()

    def apply_student_template(self):
        """Adds school + study schedule"""
        for day in range(1, 29):
            date = f"{self.year}-{self.month:02d}-{day:02d}"
            weekday = datetime(self.year, self.month, day).weekday()

            if weekday < 5:
                self.events.setdefault(date, []).append(("Classes", "School"))
                self.events.setdefault(date, []).append(("Study", "School"))

        self.draw_calendar()

    def apply_fitness_template(self):
        """Adds gym routine every other day"""
        for day in range(1, 29, 2):
            date = f"{self.year}-{self.month:02d}-{day:02d}"
            self.events.setdefault(date, []).append(("Workout", "Gym"))

        self.draw_calendar()

    # -------------------------------
    # MONTH NAVIGATION
    # -------------------------------
    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.draw_calendar()


# -------------------------------
# RUN APPLICATION
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()