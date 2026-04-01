import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
import ttkbootstrap as tb
import calendar
from datetime import datetime, timedelta

class ModernCalendar:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Calendar Planner")
        self.root.geometry("1000x720")

        # -------------------------------
        # DATA
        # -------------------------------
        self.events = {}
        self.selected_date = None

        self.categories = {
            "Work": "#ff6b6b",
            "School": "#4d96ff",
            "Gym": "#6bcb77",
            "Goals": "#ffd93d"
        }

        self.category_visibility = {k: tk.IntVar(value=1) for k in self.categories}

        now = datetime.now()
        self.year, self.month = now.year, now.month
        self.view_mode = tk.StringVar(value="Month")

        # Monthly themes (color + emoji "graphics")
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
    # UI
    # -------------------------------
    def create_widgets(self):

        # Header
        header = tk.Frame(self.root)
        header.pack(pady=10)

        tk.Button(header, text="<", command=self.prev_month).pack(side="left")
        self.title_label = tk.Label(header, font=("Arial", 18, "bold"))
        self.title_label.pack(side="left", padx=20)
        tk.Button(header, text=">", command=self.next_month).pack(side="left")

        ttk.Combobox(
            header,
            textvariable=self.view_mode,
            values=["Month", "Week"],
            state="readonly"
        ).pack(side="left", padx=10)

        # Category filters
        filter_frame = tk.Frame(self.root)
        filter_frame.pack()

        for cat in self.categories:
            tk.Checkbutton(
                filter_frame,
                text=cat,
                variable=self.category_visibility[cat],
                command=self.draw_calendar
            ).pack(side="left")

        # Event input
        form = tk.Frame(self.root)
        form.pack(pady=10)

        tk.Label(form, text="Selected Date:").grid(row=0, column=0)
        self.date_label = tk.Label(form, text="None")
        self.date_label.grid(row=0, column=1)

        tk.Label(form, text="Event:").grid(row=1, column=0)
        self.title_entry = tk.Entry(form)
        self.title_entry.grid(row=1, column=1)

        tk.Label(form, text="Category:").grid(row=2, column=0)
        self.cat_var = tk.StringVar(value="Work")
        ttk.Combobox(form, textvariable=self.cat_var, values=list(self.categories)).grid(row=2, column=1)

        tk.Button(form, text="Add Event", command=self.add_event).grid(row=3, column=0, columnspan=2)

        # Countdown
        self.countdown_label = tk.Label(self.root, font=("Arial", 10, "italic"))
        self.countdown_label.pack()

        # Calendar frame
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

    # -------------------------------
    # EVENT LOGIC
    # -------------------------------
    def add_event(self):
        if not self.selected_date:
            messagebox.showwarning("Error", "Select a date by clicking a calendar cell")
            return

        title = self.title_entry.get()
        cat = self.cat_var.get()

        self.events.setdefault(self.selected_date, []).append((title, cat))
        self.update_countdown()
        self.draw_calendar()

    def select_date(self, date):
        self.selected_date = date
        self.date_label.config(text=date)

    def update_countdown(self):
        today = datetime.now()
        upcoming = []

        for d in self.events:
            dt = datetime.strptime(d, "%Y-%m-%d")
            if dt >= today:
                upcoming.append((dt, self.events[d][0][0]))

        if upcoming:
            nearest = min(upcoming, key=lambda x: x[0])
            days = (nearest[0] - today).days
            self.countdown_label.config(text=f"Next Event: {nearest[1]} in {days} days")

    # -------------------------------
    # DRAW CALENDAR
    # -------------------------------
    def draw_calendar(self):
        for w in self.calendar_frame.winfo_children():
            w.destroy()

        emoji = self.month_themes[self.month][1]
        self.title_label.config(text=f"{emoji} {calendar.month_name[self.month]} {self.year} {emoji}")

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

                frame = tk.Frame(self.calendar_frame, width=130, height=100, bg="white", bd=1, relief="ridge")
                frame.grid(row=r, column=c, padx=4, pady=4)
                frame.grid_propagate(False)

                # Clickable date
                tk.Button(
                    frame,
                    text=str(day),
                    command=lambda d=date_str: self.select_date(d),
                    bg="white",
                    bd=0
                ).pack(anchor="nw")

                # Events
                if date_str in self.events:
                    for title, cat in self.events[date_str]:
                        if self.category_visibility[cat].get():
                            tk.Label(
                                frame,
                                text=title,
                                bg=self.categories[cat],
                                fg="black",
                                wraplength=110
                            ).pack(fill="x", pady=1)

    def draw_week(self):
        if not self.selected_date:
            start = datetime(self.year, self.month, 1)
        else:
            start = datetime.strptime(self.selected_date, "%Y-%m-%d")

        week = [start + timedelta(days=i) for i in range(7)]

        for i, day in enumerate(week):
            date_str = day.strftime("%Y-%m-%d")

            frame = tk.Frame(self.calendar_frame, width=140, height=300, bg="white", bd=1, relief="ridge")
            frame.grid(row=0, column=i, padx=4, pady=4)
            frame.grid_propagate(False)

            tk.Label(frame, text=day.strftime("%a\n%d"), font=("Arial", 10, "bold")).pack()

            if date_str in self.events:
                for title, cat in self.events[date_str]:
                    if self.category_visibility[cat].get():
                        tk.Label(frame, text=title, bg=self.categories[cat]).pack(fill="x")

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
        color, _ = self.month_themes[self.month]
        self.root.configure(bg=color)


# -------------------------------
# RUN
# -------------------------------
if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = ModernCalendar(root)
    root.mainloop()