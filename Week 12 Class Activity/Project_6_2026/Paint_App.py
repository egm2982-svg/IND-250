import tkinter as tk
from tkinter import colorchooser

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint App")
        self.root.geometry("800x600")

        # Default values
        self.brush_color = "black"
        self.brush_size = 5

        # ----------- UI FRAME -----------
        top_frame = tk.Frame(root, bg="#f0f0f0", height=50)
        top_frame.pack(fill="x")

        # Color Button
        color_btn = tk.Button(top_frame, text="Color", command=self.choose_color)
        color_btn.pack(side="left", padx=5, pady=5)

        # Brush Size Slider
        self.size_slider = tk.Scale(top_frame, from_=1, to=20,
                                     orient="horizontal", label="Brush Size")
        self.size_slider.set(self.brush_size)
        self.size_slider.pack(side="left", padx=5)

        # Clear Button
        clear_btn = tk.Button(top_frame, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side="left", padx=5)

        # ----------- CANVAS -----------
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill="both", expand=True)

        # Mouse Events
        self.canvas.bind("<B1-Motion>", self.paint)

    # ----------- FUNCTIONS -----------

    def choose_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.brush_color = color

    def paint(self, event):
        x1 = event.x - self.size_slider.get()
        y1 = event.y - self.size_slider.get()
        x2 = event.x + self.size_slider.get()
        y2 = event.y + self.size_slider.get()

        self.canvas.create_oval(
            x1, y1, x2, y2,
            fill=self.brush_color,
            outline=self.brush_color
        )

    def clear_canvas(self):
        self.canvas.delete("all")


# ----------- RUN APP -----------
if __name__ == "__main__":
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()