import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar #Import was different - re-wrote prompt to get a better look
from datetime import datetime, timedelta

# -------------------------------
# MAIN APPLICATION CLASS
# -------------------------------
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calendar Planner")
        self.root.geometry("900x650")

        # -------------------------------
        # DATA STORAGE
        # -------------------------------
        self.events = {}  # {date: [(title, category)]}

        # Categories + colors
        self.categories = {
            "Work": "red",
            "School": "blue",
            "Gym": "green",
            "Personal": "gold",
            "Goals": "purple"
        }

        self.category_visibility = {
            k: tk.IntVar(value=1) for k in self.categories
        }

        # Current date
        now = datetime.now()
        self.year, self.month = now.year, now.month

        self.view_mode = tk.StringVar(value="Month")

        self.create_widgets()

    # -------------------------------
    # UI SETUP
    # -------------------------------
    def create_widgets(self):

        # -------------------------------
        # VIEW TOGGLE
        # -------------------------------
        ttk.Combobox(
            self.root,
            textvariable=self.view_mode,
            values=["Month", "Week"],
            state="readonly"
        ).pack(pady=5)

        # -------------------------------
        # CATEGORY FILTERS
        # -------------------------------
        filter_frame = tk.Frame(self.root)
        filter_frame.pack()

        for cat in self.categories:
            tk.Checkbutton(
                filter_frame,
                text=cat,
                variable=self.category_visibility[cat],
                command=self.refresh_calendar
            ).pack(side="left")

        # -------------------------------
        # TKCALENDAR WIDGET
        # -------------------------------
        self.cal = Calendar(
            self.root,
            selectmode="day",
            year=self.year,
            month=self.month,
            date_pattern="yyyy-mm-dd"
        )
        self.cal.pack(pady=10)

        # -------------------------------
        # EVENT INPUT
        # -------------------------------
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Selected Date:").grid(row=0, column=0)
        self.date_label = tk.Label(form, text="")
        self.date_label.grid(row=0, column=1)

        tk.Label(form, text="Event:").grid(row=1, column=0)
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

        tk.Button(form, text="Add Event", command=self.add_event).grid(row=3, column=0, columnspan=2)

        # Countdown label
        self.countdown_label = tk.Label(self.root, fg="red")
        self.countdown_label.pack()

        # -------------------------------
        # TEMPLATE BUTTONS
        # -------------------------------
        template_frame = tk.Frame(self.root)
        template_frame.pack(pady=10)

        tk.Button(template_frame, text="Work Week", command=self.apply_work_template).pack(side="left")
        tk.Button(template_frame, text="Student", command=self.apply_student_template).pack(side="left")
        tk.Button(template_frame, text="Fitness", command=self.apply_fitness_template).pack(side="left")

        # -------------------------------
        # WEEK VIEW DISPLAY
        # -------------------------------
        self.week_frame = tk.Frame(self.root)
        self.week_frame.pack()

        # Bind date selection
        self.cal.bind("<<CalendarSelected>>", self.update_selected_date)

    # -------------------------------
    # EVENT HANDLING
    # -------------------------------
    def update_selected_date(self, event):
        date = self.cal.get_date()
        self.date_label.config(text=date)
        self.refresh_week_view()

    def add_event(self):
        date = self.cal.get_date()
        title = self.title_entry.get()
        cat = self.category_var.get()

        if not title:
            messagebox.showwarning("Error", "Enter an event title")
            return

        self.events.setdefault(date, []).append((title, cat))

        # Highlight date in calendar
        self.cal.calevent_create(date, title, tags=cat)
        self.cal.tag_config(cat, background=self.categories[cat])

        self.update_countdown()
        self.refresh_week_view()

    def update_countdown(self):
        today = datetime.now()
        future = []

        for d in self.events:
            dt = datetime.strptime(d, "%Y-%m-%d")
            if dt >= today:
                future.append((dt, self.events[d][0][0]))

        if future:
            nearest = min(future, key=lambda x: x[0])
            days = (nearest[0] - today).days
            self.countdown_label.config(text=f"Next: {nearest[1]} in {days} days")

    # -------------------------------
    # WEEK VIEW
    # -------------------------------
    def refresh_week_view(self):
        for w in self.week_frame.winfo_children():
            w.destroy()

        if self.view_mode.get() != "Week":
            return

        selected = datetime.strptime(self.cal.get_date(), "%Y-%m-%d")
        week = [selected + timedelta(days=i) for i in range(7)]

        for i, day in enumerate(week):
            frame = tk.Frame(self.week_frame, width=120, height=150, bd=1, relief="solid")
            frame.grid(row=0, column=i)
            frame.grid_propagate(False)

            tk.Label(frame, text=day.strftime("%a\n%d")).pack()

            date_str = day.strftime("%Y-%m-%d")

            if date_str in self.events:
                for title, cat in self.events[date_str]:
                    if self.category_visibility[cat].get():
                        tk.Label(frame, text=title, bg=self.categories[cat]).pack(fill="x")

    def refresh_calendar(self):
        """Refresh calendar filtering"""
        self.cal.calevent_remove("all")

        for date in self.events:
            for title, cat in self.events[date]:
                if self.category_visibility[cat].get():
                    self.cal.calevent_create(date, title, tags=cat)
                    self.cal.tag_config(cat, background=self.categories[cat])

        self.refresh_week_view()

    # -------------------------------
    # TEMPLATE FUNCTIONS
    # -------------------------------
    def apply_work_template(self):
        for i in range(1, 29):
            date = f"{self.year}-{self.month:02d}-{i:02d}"
            if datetime(self.year, self.month, i).weekday() < 5:
                self.events.setdefault(date, []).append(("Work 9-5", "Work"))
        self.refresh_calendar()

    def apply_student_template(self):
        for i in range(1, 29):
            date = f"{self.year}-{self.month:02d}-{i:02d}"
            if datetime(self.year, self.month, i).weekday() < 5:
                self.events.setdefault(date, []).append(("Classes", "School"))
        self.refresh_calendar()

    def apply_fitness_template(self):
        for i in range(1, 29, 2):
            date = f"{self.year}-{self.month:02d}-{i:02d}"
            self.events.setdefault(date, []).append(("Workout", "Gym"))
        self.refresh_calendar()


# -------------------------------
# RUN APPLICATION
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()