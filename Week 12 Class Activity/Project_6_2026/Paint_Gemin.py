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

# ---------------- APP ----------------
class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎨 Paint Studio Pro")
        self.root.geometry("1200x800")
        
        # State Variables
        self.brush_color = "black"
        self.current_tool = "brush"
        self.history = []
        self.current_action = []
        self.image_layers = [] # To keep references to loaded images
        self.selection_box = None
        self.selected_items = []

        self.setup_ui()
        self.setup_bindings()

    def setup_ui(self):
        """Clean Header and Canvas Layout"""
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill="both", expand=True)

        # 1. Header Toolbar
        self.toolbar = tk.Frame(self.main_frame, bg="#ffffff", height=55, relief="raised", bd=1)
        self.toolbar.pack(side="top", fill="x")

        # --- TOOL GROUP ---
        tool_frame = tk.Frame(self.toolbar, bg="#ffffff")
        tool_frame.pack(side="left", padx=10)

        tools = [
            ("🖌 Brush", "brush", "Draw with brush"),
            ("✒ Pen", "pen", "Fine lines"),
            ("🎨 Spray", "spray", "Airbrush"),
            ("🧽 Eraser", "eraser", "Erase paths"),
            ("🔲 Select", "select", "Select area"),
        ]

        for text, tool_id, tip in tools:
            btn = tk.Button(tool_frame, text=text, command=lambda t=tool_id: self.set_tool(t), 
                            relief="flat", overrelief="groove", padx=8)
            btn.pack(side="left", padx=2, pady=10)
            ToolTip(btn, tip)

        # --- ACTION GROUP ---
        action_frame = tk.Frame(self.toolbar, bg="#ffffff")
        action_frame.pack(side="left", padx=20)

        actions = [
            ("🎨 Color", self.choose_color, "Select Color"),
            ("↩ Undo", self.undo, "Undo (Ctrl+Z)"),
            ("🗑 Clear", self.clear_canvas, "Clear Canvas"),
            ("📂 Open", self.open_file, "Open Image"),
            ("💾 Save", self.save_canvas, "Save PNG"),
        ]

        for text, cmd, tip in actions:
            btn = tk.Button(action_frame, text=text, command=cmd, relief="flat", overrelief="groove", padx=8)
            btn.pack(side="left", padx=2)
            ToolTip(btn, tip)

        # --- SETTINGS GROUP ---
        self.size_scale = tk.Scale(self.toolbar, from_=1, to=50, orient="horizontal", bg="white", highlightthickness=0)
        self.size_scale.set(5)
        self.size_scale.pack(side="right", padx=20)
        tk.Label(self.toolbar, text="Size:", bg="white").pack(side="right")

        # 2. Canvas
        self.canvas = tk.Canvas(self.main_frame, bg="white", highlightthickness=0, cursor="cross")
        self.canvas.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_bindings(self):
        self.canvas.bind("<Button-1>", self.on_press)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
        self.root.bind("<Control-z>", lambda e: self.undo())

    # --- CANVAS ACTIONS ---
    def clear_canvas(self):
        """Wipe all items and reset state."""
        if messagebox.askyesno("Clear", "Are you sure you want to clear the entire canvas?"):
            self.canvas.delete("all")
            self.history = []
            self.image_layers = []
            self.selected_items = []

    def open_file(self):
        """Open an image with the option to clear the canvas first."""
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if not path:
            return

        # NEW OPTION: Ask to clear or overlay
        choice = messagebox.askyesnocancel("Open Image", "Clear canvas before opening?\n\n'Yes' = New Project\n'No' = Add to current")
        
        if choice is None: # User cancelled
            return
        
        if choice: # Clear canvas
            self.canvas.delete("all")
            self.history = []
            self.image_layers = []

        try:
            img = Image.open(path)
            # Resize image if it's larger than the canvas
            img.thumbnail((self.canvas.winfo_width(), self.canvas.winfo_height()))
            
            photo = ImageTk.PhotoImage(img)
            self.image_layers.append(photo) # Keep reference
            self.canvas.create_image(0, 0, anchor="nw", image=photo)
        except Exception as e:
            messagebox.showerror("Error", f"Could not load image: {e}")

    # --- DRAWING LOGIC ---
    def set_tool(self, tool):
        self.current_tool = tool

    def choose_color(self):
        _, hex_color = colorchooser.askcolor(initialcolor=self.brush_color)
        if hex_color: self.brush_color = hex_color

    def undo(self):
        if self.history:
            for item in self.history.pop():
                self.canvas.delete(item)

    def on_press(self, e):
        self.last_x, self.last_y = e.x, e.y
        self.start_x, self.start_y = e.x, e.y
        self.current_action = []

        if self.current_tool == "select":
            if self.selection_box: self.canvas.delete(self.selection_box)
            self.selection_box = self.canvas.create_rectangle(e.x, e.y, e.x, e.y, outline="blue", dash=(4,4))

    def on_drag(self, e):
        size = self.size_scale.get()
        
        if self.current_tool == "brush":
            item = self.canvas.create_oval(e.x-size, e.y-size, e.x+size, e.y+size, fill=self.brush_color, outline="")
            self.current_action.append(item)

        elif self.current_tool == "pen":
            item = self.canvas.create_line(self.last_x, self.last_y, e.x, e.y, 
                                          fill=self.brush_color, width=size, capstyle="round", smooth=True)
            self.current_action.append(item)
            self.last_x, self.last_y = e.x, e.y

        elif self.current_tool == "spray":
            for _ in range(8):
                sx, sy = e.x + random.randint(-size*2, size*2), e.y + random.randint(-size*2, size*2)
                item = self.canvas.create_oval(sx, sy, sx+1, sy+1, fill=self.brush_color, outline="")
                self.current_action.append(item)

        elif self.current_tool == "eraser":
            item = self.canvas.create_oval(e.x-size, e.y-size, e.x+size, e.y+size, fill="white", outline="")
            self.current_action.append(item)

        elif self.current_tool == "select":
            self.canvas.coords(self.selection_box, self.start_x, self.start_y, e.x, e.y)

    def on_release(self, e):
        if self.current_action:
            self.history.append(self.current_action)

    def save_canvas(self):
        path = filedialog.asksaveasfilename(defaultextension=".png")
        if path:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x, y, x1, y1)).save(path)
            messagebox.showinfo("Success", "Saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()