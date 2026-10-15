
import tkinter as tk
from tkinter import messagebox
import os
from PIL import Image, ImageTk

# Main Window
root = tk.Tk()
root.title("Photo Slideshow Album")
root.geometry("500x550")
root.configure(bg="white")

# List of image paths
image_paths = [
    r"C:\Users\HP\Pictures\Screenshots\image1.png",
    r"C:\Users\HP\Pictures\Screenshots\image2.png",
    r"C:\Users\HP\Pictures\Screenshots\image3.png",
    r"C:\Users\HP\Pictures\Screenshots\image4.png",
    r"C:\Users\HP\Pictures\Screenshots\image5.png"
]

images = []
image_size = (400, 350)

# Load images
for path in image_paths:
    if os.path.exists(path):
        try:
            img = Image.open(path)
            img = img.resize(image_size)
            images.append(img)
        except (OSError, ValueError):
            print(f"Unable to load image: {path}")

# Convert PIL images into Tkinter-compatible images
final_images = []

for img in images:
    photo = ImageTk.PhotoImage(img)
    final_images.append(photo)

# Current image index and slideshow state
current_index = 0
is_playing = False
after_id = None

# Label widget to display photos
image_label = tk.Label(root, bg="white")
image_label.pack(pady=20)

# Image counter
counter_label = tk.Label(
    root, text="", font=("Arial", 10), bg="white"
)
counter_label.pack()

# Display selected image
def show_image():
    if not final_images:
        image_label.config(
            image="",
            text="No images found. Check image paths.",
            font=("Arial", 12)
        )
        counter_label.config(text="0 images")
        return

    image_label.config(image=final_images[current_index])
    image_label.image = final_images[current_index]
    counter_label.config(
        text=f"Image {current_index + 1} of {len(final_images)}"
    )

# Show next image
def next_image():
    global current_index

    if final_images:
        current_index = (current_index + 1) % len(final_images)
        show_image()

# Show previous image
def previous_image():
    global current_index

    if final_images:
        current_index = (current_index - 1) % len(final_images)
        show_image()

# Automatically change images
def slideshow():
    global current_index, after_id

    if is_playing and final_images:
        next_image()
        after_id = root.after(2000, slideshow)

# Play or pause slideshow
def toggle_slideshow():
    global is_playing, after_id

    if not final_images:
        messagebox.showwarning(
            "No Images", "Please check your image paths."
        )
        return

    if is_playing:
        is_playing = False

        if after_id is not None:
            root.after_cancel(after_id)
            after_id = None

        play_button.config(text="Play Slideshow")
    else:
        is_playing = True
        play_button.config(text="Pause Slideshow")
        after_id = root.after(2000, slideshow)

# Navigation buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(pady=10)

previous_button = tk.Button(
    button_frame,
    text="Previous",
    command=previous_image
)
previous_button.pack(side=tk.LEFT, padx=5)

play_button = tk.Button(
    button_frame,
    text="Play Slideshow",
    command=toggle_slideshow,
    bg="black",
    fg="yellow",
    font=("Arial", 12)
)
play_button.pack(side=tk.LEFT, padx=5)

next_button = tk.Button(
    button_frame,
    text="Next",
    command=next_image
)
next_button.pack(side=tk.LEFT, padx=5)

# Display first image
show_image()

root.mainloop()
