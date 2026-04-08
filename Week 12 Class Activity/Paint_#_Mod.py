import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox
from PIL import Image, ImageTk, ImageGrab
import numpy as np

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Paint App")
        self.root.geometry("1000x700")

        # ---------------- STATE ----------------
        self.tool = "pen"
        self.color = "black"
        self.size = 5
        self.history = []
        self.start_x = None
        self.start_y = None
        self.image_on_canvas = None

        # ---------------- MENU ----------------
        menu = tk.Menu(root)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="New", command=self.clear_canvas)
        file_menu.add_command(label="Open Image", command=self.open_image)
        file_menu.add_command(label="Save", command=self.save_canvas)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.quit)

        menu.add_cascade(label="File", menu=file_menu)
        root.config(menu=menu)

        # ---------------- TOOLBAR ----------------
        toolbar = tk.Frame(root, bg="#eeeeee")
        toolbar.pack(fill="x")

        tools = ["pen", "rectangle", "circle", "line", "arrow", "star"]
        for t in tools:
            tk.Button(toolbar, text=t.capitalize(),
                      command=lambda x=t: self.set_tool(x)).pack(side="left", padx=3, pady=5)

        tk.Button(toolbar, text="Color", command=self.choose_color).pack(side="left", padx=5)
        tk.Button(toolbar, text="Undo", command=self.undo).pack(side="left", padx=5)

        # Brush/Shape Size Slider
        self.size_slider = tk.Scale(toolbar, from_=1, to=30,
                                    orient="horizontal", label="Size")
        self.size_slider.set(self.size)
        self.size_slider.pack(side="left", padx=10)

        # ---------------- CANVAS ----------------
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Mouse bindings
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonPress-1>", self.start_shape)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    # ---------------- TOOL CONTROL ----------------
    def set_tool(self, tool):
        self.tool = tool

    def choose_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.color = c

    # ---------------- DRAWING ----------------
    def draw(self, event):
        if self.tool == "pen":
            size = self.size_slider.get()
            item = self.canvas.create_oval(
                event.x - size, event.y - size,
                event.x + size, event.y + size,
                fill=self.color, outline=self.color
            )
            self.history.append(item)

    def start_shape(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def end_shape(self, event):
        if self.start_x is None:
            return

        size = self.size_slider.get()

        if self.tool == "rectangle":
            item = self.canvas.create_rectangle(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.color, width=size
            )

        elif self.tool == "circle":
            item = self.canvas.create_oval(
                self.start_x, self.start_y, event.x, event.y,
                outline=self.color, width=size
            )

        elif self.tool == "line":
            item = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.color, width=size
            )

        elif self.tool == "arrow":
            item = self.canvas.create_line(
                self.start_x, self.start_y, event.x, event.y,
                fill=self.color, width=size, arrow=tk.LAST
            )

        elif self.tool == "star":
            item = self.draw_star(self.start_x, self.start_y, event.x, event.y, size)

        else:
            self.start_x = None
            return

        self.history.append(item)
        self.start_x = None

    def draw_star(self, x1, y1, x2, y2, width):
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        r = abs(x2 - x1) // 2
        points = []

        for i in range(10):
            angle = i * 36
            radius = r if i % 2 == 0 else r // 2
            px = cx + int(radius * np.cos(np.radians(angle)))
            py = cy + int(radius * np.sin(np.radians(angle)))
            points.extend([px, py])

        return self.canvas.create_polygon(points, outline=self.color, fill="", width=width)

    # ---------------- FILE FUNCTIONS ----------------
    def clear_canvas(self):
        self.canvas.delete("all")
        self.history.clear()

    def undo(self):
        if self.history:
            self.canvas.delete(self.history.pop())

    def open_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
        )
        if not file_path:
            return

        img = Image.open(file_path)
        img = img.resize((800, 600))
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG files", "*.png")]
        )
        if not file_path:
            return

        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()

        ImageGrab.grab().crop((x, y, x1, y1)).save(file_path)
        messagebox.showinfo("Saved", "Image saved successfully!")

# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()