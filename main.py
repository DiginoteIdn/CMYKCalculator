#CMYKCalculator
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def rgb_to_cmyk(r, g, b):
    if r == 255 and g == 255 and b == 255:
        return 0, 0, 0, 0
    elif r == 0 and g == 0 and b == 0:
        return 0, 0, 0, 1

    c = 1 - r / 255.0
    m = 1 - g / 255.0
    y = 1 - b / 255.0
    k = min(c, m, y)

    if k == 1:
        c = 0
        m = 0
        y = 0
    else:
        c = (c - k) / (1 - k)
        m = (m - k) / (1 - k)
        y = (y - k) / (1 - k)

    return c, m, y, k


def calculate_cmyk_percentage(image_path, progress_var):
    image = Image.open(image_path).convert('RGB')
    np_image = np.array(image)

    total_pixels = np_image.shape[0] * np_image.shape[1]

    c_total = 0
    m_total = 0
    y_total = 0
    k_total = 0

    for idx, pixel in enumerate(np_image.reshape(-1, 3)):
        r, g, b = pixel
        c, m, y, k = rgb_to_cmyk(r, g, b)
        c_total += c
        m_total += m
        y_total += y
        k_total += k

        if idx % 1000 == 0:
            progress_var.set((idx / total_pixels) * 100)
            root.update_idletasks()

    cyan_percentage = (c_total / total_pixels) * 100
    magenta_percentage = (m_total / total_pixels) * 100
    yellow_percentage = (y_total / total_pixels) * 100
    black_percentage = (k_total / total_pixels) * 100

    return cyan_percentage, magenta_percentage, yellow_percentage, black_percentage


def open_file():
    file_path = filedialog.askopenfilename(
        title="Select an image file",
        filetypes=(("Image files", "*.jpg;*.jpeg;*.png"), ("All files", "*.*"))
    )
    if file_path:
        progress_var.set(0)
        cyan_percentage, magenta_percentage, yellow_percentage, black_percentage = calculate_cmyk_percentage(file_path,
                                                                                                             progress_var)

        result_text.set(
            f"CMYK Percentages:\nCyan: {cyan_percentage:.2f}%\nMagenta: {magenta_percentage:.2f}%\nYellow: {yellow_percentage:.2f}%\nBlack: {black_percentage:.2f}%")

        img = Image.open(file_path)
        img.thumbnail((600, 400))
        img = ImageTk.PhotoImage(img)

        img_label.config(image=img)
        img_label.image = img

        plot_chart([cyan_percentage, magenta_percentage, yellow_percentage, black_percentage])


def plot_chart(percentages):
    fig, ax = plt.subplots()
    labels = ['Cyan', 'Magenta', 'Yellow', 'Black']
    colors = ['#00FFFF', '#FF00FF', '#FFFF00', '#000000']

    # Remove any negative values which are not possible for percentages
    percentages = [max(0, p) for p in percentages]

    # Plot the bar chart
    ax.bar(labels, percentages, color=colors)
    ax.set_ylabel('Percentage')
    ax.set_title('CMYK Color Percentages')

    # Set the Y-axis limit to always show 0% to 100%
    ax.set_ylim(0, 100)

    # Clear the previous plot
    for widget in chart_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


root = tk.Tk()
root.title("CMYK Percentage Calculator by Diginote")

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, variable=progress_var, maximum=100)
progress_bar.pack(pady=10, padx=10, fill='x')

open_button = tk.Button(root, text="Open Image File", command=open_file)
open_button.pack(pady=10)

result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, justify="left")
result_label.pack(pady=20)

img_label = tk.Label(root)
img_label.pack()

chart_frame = tk.Frame(root)
chart_frame.pack()

root.mainloop()
