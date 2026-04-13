import tkinter as tk
from tkinter import colorchooser, filedialog
from PIL import ImageGrab
import random

# ---------------- TOOLTIP ----------------
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tip = None
        widget.bind("<Enter>", self.show)
        widget.bind("<Leave>", self.hide)

    def show(self, e):
        self.tip = tk.Toplevel(self.widget)
        self.tip.wm_overrideredirect(True)
        self.tip.geometry(f"+{e.x_root+10}+{e.y_root+10}")
        tk.Label(self.tip, text=self.text, bg="#333", fg="white").pack()

    def hide(self, e):
        if self.tip:
            self.tip.destroy()

# ---------------- APP ----------------
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Paint Studio Pro")
        self.root.geometry("1100x750")

        self.brush_color = "black"
        self.current_tool = "brush"
        self.history = []
        self.current_action = []

        # Selection
        self.selection_box = None
        self.selected_items = []
        self.move_start = None

        # ---------------- MENU TOGGLE ----------------
        self.toolbar_visible = True
        tk.Button(root, text="☰ Menu", command=self.toggle_toolbar).pack(fill="x")

        # ---------------- TOOLBAR ----------------
        self.toolbar = tk.Frame(root, bg="#90caf9", height=80)
        self.toolbar.pack(fill="x")

        def btn(txt, cmd, tip):
            b = tk.Button(self.toolbar, text=txt, command=cmd, padx=8, pady=8)
            ToolTip(b, tip)
            return b

        btn("🖌", lambda: self.set_tool("brush"), "Brush").pack(side="left")
        btn("✒", lambda: self.set_tool("pen"), "Pen").pack(side="left")
        btn("🎨", lambda: self.set_tool("spray"), "Spray").pack(side="left")
        btn("📏", lambda: self.set_tool("line"), "Line").pack(side="left")
        btn("⬛", lambda: self.set_tool("rectangle"), "Rectangle").pack(side="left")
        btn("⚪", lambda: self.set_tool("oval"), "Oval").pack(side="left")
        btn("🧽", lambda: self.set_tool("eraser"), "Eraser").pack(side="left")
        btn("🔲", lambda: self.set_tool("select"), "Select").pack(side="left")

        btn("📋", self.copy_selection, "Copy").pack(side="left")
        btn("❌", self.delete_selection, "Delete").pack(side="left")

        btn("🎨", self.choose_color, "Color").pack(side="left")
        btn("↩", self.undo, "Undo").pack(side="left")

        self.size = tk.Scale(self.toolbar, from_=1, to=20, orient="horizontal")
        self.size.pack(side="right")

        # ---------------- CANVAS ----------------
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_draw)

        # Shortcuts
        root.bind("<Control-z>", lambda e: self.undo())
        root.bind("<Control-c>", lambda e: self.copy_selection())
        root.bind("<Delete>", lambda e: self.delete_selection())

    # ---------------- TOOLBAR ----------------
    def toggle_toolbar(self):
        if self.toolbar_visible:
            self.toolbar.pack_forget()
        else:
            self.toolbar.pack(fill="x")
        self.toolbar_visible = not self.toolbar_visible

    def set_tool(self, tool):
        self.current_tool = tool

    # ---------------- DRAW ----------------
    def start_draw(self, e):
        self.start_x, self.start_y = e.x, e.y
        self.last_x, self.last_y = e.x, e.y
        self.current_action = []

        if self.current_tool == "select":
            if self.selection_box:
                self.canvas.delete(self.selection_box)
            self.selection_box = self.canvas.create_rectangle(
                e.x, e.y, e.x, e.y, outline="blue", dash=(4,2)
            )

    def draw(self, e):
        size = self.size.get()

        if self.current_tool == "brush":
            i = self.canvas.create_oval(e.x-size,e.y-size,e.x+size,e.y+size,
                                        fill=self.brush_color)
            self.current_action.append(i)

        elif self.current_tool == "pen":
            i = self.canvas.create_line(self.last_x,self.last_y,e.x,e.y,
                                        fill=self.brush_color,width=size,smooth=True)
            self.current_action.append(i)
            self.last_x,self.last_y = e.x,e.y

        elif self.current_tool == "spray":
            for _ in range(15):
                x = e.x + random.randint(-size*2,size*2)
                y = e.y + random.randint(-size*2,size*2)
                i = self.canvas.create_oval(x,y,x+1,y+1,fill=self.brush_color)
                self.current_action.append(i)

        elif self.current_tool == "eraser":
            i = self.canvas.create_oval(e.x-size,e.y-size,e.x+size,e.y+size,
                                        fill="white")
            self.current_action.append(i)

        elif self.current_tool == "select":
            self.canvas.coords(self.selection_box,
                               self.start_x,self.start_y,e.x,e.y)

        elif self.current_tool == "move" and self.selected_items:
            dx = e.x - self.start_x
            dy = e.y - self.start_y
            for item in self.selected_items:
                self.canvas.move(item, dx, dy)
            self.start_x, self.start_y = e.x, e.y

    def end_draw(self, e):
        if self.current_tool == "select":
            x1,y1,x2,y2 = self.canvas.coords(self.selection_box)

            # FIXED: better selection detection
            self.selected_items = self.canvas.find_overlapping(x1,y1,x2,y2)

            # Switch to move mode automatically
            if self.selected_items:
                self.current_tool = "move"
            return

        if self.current_action:
            self.history.append(self.current_action)

    # ---------------- SELECTION ACTIONS ----------------
    def copy_selection(self):
        new_items=[]
        for item in self.selected_items:
            coords=self.canvas.coords(item)
            t=self.canvas.type(item)

            if t=="oval":
                n=self.canvas.create_oval(*coords,fill=self.brush_color)
            elif t=="rectangle":
                n=self.canvas.create_rectangle(*coords,outline=self.brush_color)
            elif t=="line":
                n=self.canvas.create_line(*coords,fill=self.brush_color)
            else:
                continue

            self.canvas.move(n,10,10)
            new_items.append(n)

        if new_items:
            self.history.append(new_items)

    def delete_selection(self):
        for i in self.selected_items:
            self.canvas.delete(i)
        self.selected_items=[]

    # ---------------- UTIL ----------------
    def undo(self):
        if self.history:
            for i in self.history.pop():
                self.canvas.delete(i)

    def choose_color(self):
        c=colorchooser.askcolor()[1]
        if c:
            self.brush_color=c

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()