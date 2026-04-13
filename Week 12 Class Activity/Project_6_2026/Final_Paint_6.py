import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import ImageGrab, Image, ImageTk
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
        tk.Label(self.tip, text=self.text, bg="#333", fg="white", padx=5, pady=2).pack()

    def hide(self, e):
        if self.tip:
            self.tip.destroy()

# ---------------- MAIN APP ----------------
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Paint Studio Pro")
        self.root.geometry("1150x750")

        # State Variables
        self.brush_color = "black"
        self.current_tool = "brush"
        self.history = []
        self.current_action = []
        self.image_refs = []  # Prevents garbage collection of loaded images
        
        # Selection, Movement & Shapes
        self.selection_box = None
        self.selected_items = []
        self.temp_item = None # For drawing dynamic lines/rectangles/ovals
        self.start_x = 0
        self.start_y = 0
        self.last_x = 0
        self.last_y = 0

        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        """Unified UI Structure"""
        self.header = tk.Frame(self.root, bg="#ffffff", height=60, relief="raised", bd=1)
        self.header.pack(side="top", fill="x")

        def add_btn(parent, txt, cmd, tip):
            b = tk.Button(parent, text=txt, command=cmd, relief="flat", overrelief="groove", padx=8, pady=5)
            b.pack(side="left", padx=1)
            ToolTip(b, tip)
            return b

        # Drawing Tools Group
        draw_group = tk.LabelFrame(self.header, text="Tools", bg="white", padx=5)
        draw_group.pack(side="left", padx=5, pady=2)
        add_btn(draw_group, "🖌", lambda: self.set_tool("brush"), "Brush")
        add_btn(draw_group, "✒", lambda: self.set_tool("pen"), "Pen")
        add_btn(draw_group, "🎨", lambda: self.set_tool("spray"), "Spray")
        add_btn(draw_group, "📏", lambda: self.set_tool("line"), "Line")
        add_btn(draw_group, "⬛", lambda: self.set_tool("rectangle"), "Rectangle")
        add_btn(draw_group, "⚪", lambda: self.set_tool("oval"), "Oval")
        add_btn(draw_group, "🧽", lambda: self.set_tool("eraser"), "Eraser")
        add_btn(draw_group, "🔲", lambda: self.set_tool("select"), "Select/Move")

        # Editing Group
        edit_group = tk.LabelFrame(self.header, text="Edit", bg="white", padx=5)
        edit_group.pack(side="left", padx=5, pady=2)
        add_btn(edit_group, "🌈", self.choose_color, "Color Picker")
        add_btn(edit_group, "↩", self.undo, "Undo")
        add_btn(edit_group, "🗑", self.clear_canvas, "Clear Canvas")
        add_btn(edit_group, "📋", self.copy_selection, "Copy Selection")
        add_btn(edit_group, "❌", self.delete_selection, "Delete Selection")

        # File Group
        file_group = tk.LabelFrame(self.header, text="Project", bg="white", padx=5)
        file_group.pack(side="left", padx=5, pady=2)
        add_btn(file_group, "📂", self.open_file, "Open File")
        add_btn(file_group, "💾", self.save_canvas, "Save Canvas")
        add_btn(file_group, "🔳", self.open_template, "Templates")

        # Brush Size
        size_group = tk.Frame(self.header, bg="white")
        size_group.pack(side="right", padx=15)
        tk.Label(size_group, text="Size", bg="white").pack()
        self.size_scale = tk.Scale(size_group, from_=1, to=40, orient="horizontal", bg="white", bd=0)
        self.size_scale.set(5)
        self.size_scale.pack()

        # Canvas
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-c>", lambda e: self.copy_selection())
        self.root.bind("<Delete>", lambda e: self.delete_selection())

    # ---------------- LOGIC: FILE & TOOLS ----------------
    def set_tool(self, tool):
        self.current_tool = tool
        self.root.config(cursor="cross")

    def clear_canvas(self):
        if messagebox.askyesno("Clear", "Are you sure you want to clear the entire canvas?"):
            self.canvas.delete("all")
            self.history = []
            self.image_refs = []
            self.selected_items = []

    def open_file(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not path: return

        choice = messagebox.askyesnocancel("Open Image", "Clear canvas before opening?\n\n'Yes' = New Project\n'No' = Add to current")
        if choice is None: return
        
        if choice:
            self.canvas.delete("all")
            self.history = []
            self.image_refs = []

        try:
            img = Image.open(path)
            img.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()))
            photo = ImageTk.PhotoImage(img)
            self.image_refs.append(photo)
            self.canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")

    def open_template(self):
        choice = messagebox.askquestion("Templates", "Choose a template:\nYes = Grid\nNo = Dots")
        self.canvas.delete("all")
        if choice == 'yes':
            for i in range(0, 1500, 40):
                self.canvas.create_line(i, 0, i, 1000, fill="#eee")
                self.canvas.create_line(0, i, 1500, i, fill="#eee")
        else:
            for x in range(20, 1500, 40):
                for y in range(20, 1000, 40):
                    self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="#bbb", outline="")

    def save_canvas(self):
        path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if path:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(path)
            messagebox.showinfo("Saved", "Image saved successfully!")

    # ---------------- LOGIC: DRAWING & SELECTION ----------------
    def on_press(self, e):
        self.start_x, self.start_y = e.x, e.y
        self.last_x, self.last_y = e.x, e.y
        self.current_action = []
        self.temp_item = None

        if self.current_tool == "select":
            if self.selection_box: self.canvas.delete(self.selection_box)
            self.selection_box = self.canvas.create_rectangle(e.x, e.y, e.x, e.y, outline="blue", dash=(4,2))

    def on_drag(self, e):
        size = self.size_scale.get()
        
        if self.current_tool == "brush":
            item = self.canvas.create_oval(e.x-size, e.y-size, e.x+size, e.y+size, fill=self.brush_color, outline="")
            self.current_action.append(item)

        elif self.current_tool == "pen":
            item = self.canvas.create_line(self.last_x, self.last_y, e.x, e.y, fill=self.brush_color, width=size, smooth=True)
            self.current_action.append(item)
            self.last_x, self.last_y = e.x, e.y

        elif self.current_tool == "spray":
            for _ in range(15):
                rx, ry = random.randint(-size*2, size*2), random.randint(-size*2, size*2)
                item = self.canvas.create_oval(e.x+rx, e.y+ry, e.x+rx+1, e.y+ry+1, fill=self.brush_color, outline="")
                self.current_action.append(item)

        elif self.current_tool == "eraser":
            item = self.canvas.create_oval(e.x-size, e.y-size, e.x+size, e.y+size, fill="white", outline="")
            self.current_action.append(item)
            
        elif self.current_tool in ["line", "rectangle", "oval"]:
            # Delete previous temporary shape while dragging
            if self.temp_item: self.canvas.delete(self.temp_item)
            
            if self.current_tool == "line":
                self.temp_item = self.canvas.create_line(self.start_x, self.start_y, e.x, e.y, fill=self.brush_color, width=size)
            elif self.current_tool == "rectangle":
                self.temp_item = self.canvas.create_rectangle(self.start_x, self.start_y, e.x, e.y, outline=self.brush_color, width=size)
            elif self.current_tool == "oval":
                self.temp_item = self.canvas.create_oval(self.start_x, self.start_y, e.x, e.y, outline=self.brush_color, width=size)

        elif self.current_tool == "select":
            self.canvas.coords(self.selection_box, self.start_x, self.start_y, e.x, e.y)

        elif self.current_tool == "move" and self.selected_items:
            dx, dy = e.x - self.last_x, e.y - self.last_y
            for item in self.selected_items:
                if item != self.selection_box: self.canvas.move(item, dx, dy)
            self.last_x, self.last_y = e.x, e.y

    def on_release(self, e):
        # Finalize Shape logic
        if self.current_tool in ["line", "rectangle", "oval"] and self.temp_item:
            self.current_action.append(self.temp_item)
            self.temp_item = None

        # Finalize Selection logic
        if self.current_tool == "select":
            bbox = self.canvas.coords(self.selection_box)
            self.selected_items = self.canvas.find_overlapping(*bbox)
            if len(self.selected_items) > 1: self.current_tool = "move"
        
        # Save History
        if self.current_action:
            self.history.append(self.current_action)

    # ---------------- ACTIONS ----------------
    def choose_color(self):
        c = colorchooser.askcolor(initialcolor=self.brush_color)[1]
        if c: self.brush_color = c

    def undo(self):
        if self.history:
            for item in self.history.pop():
                self.canvas.delete(item)

    def delete_selection(self):
        for item in self.selected_items:
            if item != self.selection_box: self.canvas.delete(item)
        self.selected_items = []
        if self.selection_box: self.canvas.delete(self.selection_box)
        self.set_tool("brush")

    def copy_selection(self):
        new_items = []
        for item in self.selected_items:
            if item == self.selection_box: continue
            
            coords = self.canvas.coords(item)
            t = self.canvas.type(item)

            if t == "oval":
                n = self.canvas.create_oval(*coords, fill=self.brush_color, outline="")
            elif t == "rectangle":
                n = self.canvas.create_rectangle(*coords, outline=self.brush_color)
            elif t == "line":
                n = self.canvas.create_line(*coords, fill=self.brush_color)
            else:
                continue

            self.canvas.move(n, 10, 10)
            new_items.append(n)

        if new_items:
            self.history.append(new_items)
            self.selected_items = new_items # Switch selection to newly copied items

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()