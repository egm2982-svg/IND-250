import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import ImageGrab

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Paint App")
        self.root.geometry("900x650")

        self.brush_color = "black"
        self.brush_size = 5

        # Store strokes for undo
        self.history = []

        # -------- MENU BAR --------
        menu_bar = tk.Menu(root)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", command=self.clear_canvas)
        file_menu.add_command(label="Open Template", command=self.open_template)
        file_menu.add_command(label="Save", command=self.save_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        menu_bar.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu_bar)

        # -------- TOOLBAR --------
        top_frame = tk.Frame(root, bg="#eeeeee", height=50)
        top_frame.pack(fill="x")

        tk.Button(top_frame, text="Color", command=self.choose_color).pack(side="left", padx=5)
        tk.Button(top_frame, text="Undo", command=self.undo).pack(side="left", padx=5)
        tk.Button(top_frame, text="Clear", command=self.clear_canvas).pack(side="left", padx=5)

        self.size_slider = tk.Scale(top_frame, from_=1, to=20,
                                   orient="horizontal", label="Brush Size")
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side="left", padx=5)

        # -------- CANVAS --------
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        self.canvas.bind("<B1-Motion>", self.paint)

    # -------- DRAWING --------
    def paint(self, event):
        size = self.size_slider.get()
        x1, y1 = event.x - size, event.y - size
        x2, y2 = event.x + size, event.y + size

        item = self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=self.brush_color,
            outline=self.brush_color
        )

        self.history.append(item)

    # -------- TOOLS --------
    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color

    def undo(self):
        if self.history:
            last_item = self.history.pop()
            self.canvas.delete(last_item)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.history.clear()

    # -------- SAVE FUNCTION --------
    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )

        if not file_path:
            return

        # Get canvas position on screen
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
        messagebox.showinfo("Saved", "Image saved successfully!")

    # -------- TEMPLATES --------
    def open_template(self):
        self.clear_canvas()

        choice = messagebox.askquestion(
            "Templates",
            "Choose a template:\nYes = Grid\nNo = Dots"
        )

        if choice == "yes":
            self.draw_grid()
        else:
            self.draw_dots()

    def draw_grid(self):
        for i in range(0, 900, 40):
            self.canvas.create_line([(i, 0), (i, 650)], fill="#ddd")
        for i in range(0, 650, 40):
            self.canvas.create_line([(0, i), (900, i)], fill="#ddd")

    def draw_dots(self):
        for x in range(20, 900, 40):
            for y in range(20, 650, 40):
                self.canvas.create_oval(x-2, y-2, x+2, y+2, fill="#bbb")

# -------- RUN APP --------
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()