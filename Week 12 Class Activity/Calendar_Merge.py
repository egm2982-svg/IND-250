import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime, timedelta

# -------------------------------
# MAIN APPLICATION CLASS
# -------------------------------
class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Calendar Planner")
        self.root.geometry("950x650")

        # -------------------------------
        # DATA STORAGE
        # -------------------------------
        self.events = {}
        self.selected_date = None

        # Category colors
        self.categories = {
            "Work": "#FF6B6B",
            "School": "#4D96FF",
            "Gym": "#6BCB77",
            "Personal": "#FFD93D",
            "Goals": "#B983FF"
        }

        # Category visibility (multi-select)
        self.category_visibility = {
            k: tk.IntVar(value=1) for k in self.categories
        }

        # Current date
        now = datetime.now()
        self.year = now.year
        self.month = now.month

        # View toggle
        self.view_mode = tk.StringVar(value="Month")

        # Month themes (color + emoji)
        self.month_themes = {
            1: ("#e3f2fd", "❄️"),
            2: ("#fce4ec", "💖"),
            3: ("#e8f5e9", "🌸"),
            4: ("#fff3e0", "🌼"),
            5: ("#e0f7fa", "🌷"),
            6: ("#ede7f6", "☀️"),
            7: ("#fffde7", "🌻"),
            8: ("#f3e5f5", "🌺"),
            9: ("#e1f5fe", "🍂"),
            10: ("#fbe9e7", "🎃"),
            11: ("#e8eaf6", "🍁"),
            12: ("#f1f8e9", "🎄"),
        }

        self.create_widgets()
        self.update_theme()
        self.draw_calendar()

    # -------------------------------
    # UI SETUP
    # -------------------------------
    def create_widgets(self):

        # HEADER
        header = tk.Frame(self.root)
        header.pack(pady=10)

        tk.Button(header, text="<", command=self.prev_month).pack(side="left")

        self.month_label = tk.Label(header, font=("Arial", 16))
        self.month_label.pack(side="left", padx=20)

        tk.Button(header, text=">", command=self.next_month).pack(side="left")

        ttk.Combobox(
            header,
            textvariable=self.view_mode,
            values=["Month", "Week"],
            state="readonly"
        ).pack(side="left", padx=10)

        # CATEGORY FILTERS
        filter_frame = tk.Frame(self.root)
        filter_frame.pack()

        for cat in self.categories:
            tk.Checkbutton(
                filter_frame,
                text=cat,
                variable=self.category_visibility[cat],
                command=self.draw_calendar
            ).pack(side="left")

        # -------------------------------
        # EVENT INPUT SECTION
        # -------------------------------
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Selected Date:").grid(row=0, column=0)
        self.date_label = tk.Label(form, text="None")
        self.date_label.grid(row=0, column=1)

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

        tk.Button(form, text="Add Event", command=self.add_event, bg="#4CAF50", fg="white").grid(
            row=3, column=0, columnspan=2, pady=5
        )

        # Countdown
        self.countdown_label = tk.Label(self.root, fg="red")
        self.countdown_label.pack()

        # TEMPLATE SECTION (kept from your original)
        template_frame = tk.Frame(self.root)
        template_frame.pack(pady=10)

        tk.Label(template_frame, text="Schedule Templates:").pack()

        tk.Button(template_frame, text="Work Week", command=self.apply_work_template).pack(side="left", padx=5)
        tk.Button(template_frame, text="Student", command=self.apply_student_template).pack(side="left", padx=5)
        tk.Button(template_frame, text="Fitness", command=self.apply_fitness_template).pack(side="left", padx=5)

        # Calendar frame
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

    # -------------------------------
    # EVENT HANDLING
    # -------------------------------
    def add_event(self):
        if not self.selected_date:
            messagebox.showwarning("Error", "Click a date on the calendar")
            return

        title = self.title_entry.get()
        category = self.category_var.get()

        self.events.setdefault(self.selected_date, []).append((title, category))

        self.update_countdown()
        self.draw_calendar()

    def select_date(self, date):
        self.selected_date = date
        self.date_label.config(text=date)

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
    # DRAW CALENDAR
    # -------------------------------
    def draw_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        emoji = self.month_themes[self.month][1]
        self.month_label.config(text=f"{emoji} {calendar.month_name[self.month]} {self.year}")

        if self.view_mode.get() == "Month":
            self.draw_month()
        else:
            self.draw_week()

    def draw_month(self):
        cal = calendar.monthcalendar(self.year, self.month)

        for r, week in enumerate(cal):
            for c, day in enumerate(week):
                if day == 0:
                    continue

                date_str = f"{self.year}-{self.month:02d}-{day:02d}"

                frame = tk.Frame(self.calendar_frame, width=120, height=90, bg="white", bd=1, relief="ridge")
                frame.grid(row=r, column=c, padx=3, pady=3)
                frame.grid_propagate(False)

                tk.Button(
                    frame,
                    text=str(day),
                    command=lambda d=date_str: self.select_date(d),
                    bd=0,
                    bg="white"
                ).pack(anchor="nw")

                if date_str in self.events:
                    for title, cat in self.events[date_str]:
                        if self.category_visibility[cat].get():
                            tk.Label(
                                frame,
                                text=title,
                                bg=self.categories[cat],
                                wraplength=100
                            ).pack(fill="x", pady=1)

    def draw_week(self):
        start = datetime(self.year, self.month, 1) if not self.selected_date else datetime.strptime(self.selected_date, "%Y-%m-%d")

        week = [start + timedelta(days=i) for i in range(7)]

        for i, day in enumerate(week):
            date_str = day.strftime("%Y-%m-%d")

            frame = tk.Frame(self.calendar_frame, width=130, height=250, bg="white", bd=1)
            frame.grid(row=0, column=i, padx=3, pady=3)
            frame.grid_propagate(False)

            tk.Label(frame, text=day.strftime("%a\n%d")).pack()

            if date_str in self.events:
                for title, cat in self.events[date_str]:
                    if self.category_visibility[cat].get():
                        tk.Label(frame, text=title, bg=self.categories[cat]).pack(fill="x")

    # -------------------------------
    # TEMPLATE FUNCTIONS
    # -------------------------------
    def apply_work_template(self):
        for day in range(1, 29):
            date = f"{self.year}-{self.month:02d}-{day:02d}"
            if datetime(self.year, self.month, day).weekday() < 5:
                self.events.setdefault(date, []).append(("Work 9-5", "Work"))
        self.draw_calendar()

    def apply_student_template(self):
        for day in range(1, 29):
            date = f"{self.year}-{self.month:02d}-{day:02d}"
            if datetime(self.year, self.month, day).weekday() < 5:
                self.events.setdefault(date, []).append(("Classes", "School"))
        self.draw_calendar()

    def apply_fitness_template(self):
        for day in range(1, 29, 2):
            date = f"{self.year}-{self.month:02d}-{day:02d}"
            self.events.setdefault(date, []).append(("Workout", "Gym"))
        self.draw_calendar()

    # -------------------------------
    # NAVIGATION
    # -------------------------------
    def prev_month(self):
        self.month -= 1
        if self.month == 0:
            self.month = 12
            self.year -= 1
        self.update_theme()
        self.draw_calendar()

    def next_month(self):
        self.month += 1
        if self.month == 13:
            self.month = 1
            self.year += 1
        self.update_theme()
        self.draw_calendar()

    # -------------------------------
    # THEME
    # -------------------------------
    def update_theme(self):
        color = self.month_themes[self.month][0]
        self.root.configure(bg=color)


# -------------------------------
# RUN APPLICATION
# -------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()