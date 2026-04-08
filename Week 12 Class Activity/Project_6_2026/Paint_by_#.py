import tkinter as tk
from tkinter import filedialog, colorchooser, messagebox, simpledialog
from PIL import Image, ImageTk
import numpy as np
import cv2

# ================= MAIN MENU =================
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Creative Art Suite")
        self.root.geometry("400x300")

        tk.Label(root, text="Enter Your Name:", font=("Arial", 12)).pack(pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        tk.Button(root, text="Scratch Pad", width=20, command=self.open_scratch).pack(pady=10)
        tk.Button(root, text="Color By Number", width=20, command=self.open_color_by_number).pack(pady=10)

    def open_scratch(self):
        ScratchPad(tk.Toplevel(self.root), self.name_entry.get())

    def open_color_by_number(self):
        ColorByNumber(tk.Toplevel(self.root), self.name_entry.get())


# ================= SCRATCH PAD =================
class ScratchPad:
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"{user}'s Scratch Pad")

        self.canvas = tk.Canvas(root, bg="white", width=800, height=600)
        self.canvas.pack()

        self.tool = "brush"
        self.color = "black"
        self.size = 5
        self.history = []

        toolbar = tk.Frame(root)
        toolbar.pack(fill="x")

        tools = ["brush", "rectangle", "circle", "line", "arrow", "star"]
        for t in tools:
            tk.Button(toolbar, text=t, command=lambda x=t: self.set_tool(x)).pack(side="left")

        tk.Button(toolbar, text="Color", command=self.choose_color).pack(side="left")
        tk.Button(toolbar, text="Undo", command=self.undo).pack(side="left")
        tk.Button(toolbar, text="Save", command=self.save).pack(side="left")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.start_x = None
        self.start_y = None

        self.canvas.bind("<ButtonPress-1>", self.start_shape)
        self.canvas.bind("<ButtonRelease-1>", self.end_shape)

    def set_tool(self, tool):
        self.tool = tool

    def choose_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.color = c

    def draw(self, e):
        if self.tool == "brush":
            item = self.canvas.create_oval(
                e.x-self.size, e.y-self.size,
                e.x+self.size, e.y+self.size,
                fill=self.color, outline=self.color
            )
            self.history.append(item)

    def start_shape(self, e):
        self.start_x, self.start_y = e.x, e.y

    def end_shape(self, e):
        if not self.start_x:
            return

        if self.tool == "rectangle":
            item = self.canvas.create_rectangle(self.start_x, self.start_y, e.x, e.y, outline=self.color)
        elif self.tool == "circle":
            item = self.canvas.create_oval(self.start_x, self.start_y, e.x, e.y, outline=self.color)
        elif self.tool == "line":
            item = self.canvas.create_line(self.start_x, self.start_y, e.x, e.y, fill=self.color)
        elif self.tool == "arrow":
            item = self.canvas.create_line(self.start_x, self.start_y, e.x, e.y, fill=self.color, arrow=tk.LAST)
        elif self.tool == "star":
            item = self.draw_star(self.start_x, self.start_y, e.x, e.y)

        else:
            return

        self.history.append(item)
        self.start_x = None

    def draw_star(self, x1, y1, x2, y2):
        cx, cy = (x1+x2)//2, (y1+y2)//2
        r = abs(x2-x1)//2
        points = []
        for i in range(10):
            angle = i * 36
            radius = r if i % 2 == 0 else r//2
            px = cx + int(radius * np.cos(np.radians(angle)))
            py = cy + int(radius * np.sin(np.radians(angle)))
            points.extend([px, py])
        return self.canvas.create_polygon(points, outline=self.color, fill="")

    def undo(self):
        if self.history:
            self.canvas.delete(self.history.pop())

    def save(self):
        file = filedialog.asksaveasfilename(defaultextension=".png")
        if file:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x1 = x + self.canvas.winfo_width()
            y1 = y + self.canvas.winfo_height()
            ImageGrab.grab().crop((x,y,x1,y1)).save(file)


# ================= COLOR BY NUMBER =================
class ColorByNumber:
    def __init__(self, root, user):
        self.root = root
        self.root.title(f"{user}'s Color By Number")

        tk.Button(root, text="Open Image", command=self.load_image).pack()
        tk.Button(root, text="Save Progress", command=self.save).pack()

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.image = None
        self.segmented = None
        self.colors = []

        self.canvas.bind("<Button-1>", self.fill_color)

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        img = cv2.imread(path)
        img = cv2.resize(img, (400,400))

        # Reduce colors (k-means)
        Z = img.reshape((-1,3))
        Z = np.float32(Z)

        K = 6
        _, label, center = cv2.kmeans(Z, K, None,
                                     (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0),
                                     10, cv2.KMEANS_RANDOM_CENTERS)

        center = np.uint8(center)
        self.segmented = center[label.flatten()].reshape(img.shape)

        self.colors = center

        self.display_image(self.segmented)

    def display_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image = ImageTk.PhotoImage(Image.fromarray(img_rgb))
        self.canvas.create_image(0,0, anchor="nw", image=self.image)

    def fill_color(self, event):
        if self.segmented is None:
            return

        x, y = event.x, event.y
        if x >= 400 or y >= 400:
            return

        region_color = self.segmented[y, x]

        new_color = colorchooser.askcolor()[0]
        if not new_color:
            return

        mask = (self.segmented == region_color).all(axis=2)
        self.segmented[mask] = new_color[::-1]

        self.display_image(self.segmented)

    def save(self):
        file = filedialog.asksaveasfilename(defaultextension=".png")
        if file and self.segmented is not None:
            cv2.imwrite(file, self.segmented)


# ================= RUN =================
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()