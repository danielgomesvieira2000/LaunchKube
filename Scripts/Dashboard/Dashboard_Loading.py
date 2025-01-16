import os

from PIL import Image, ImageTk, ImageSequence
import tkinter as tk

def show_loading(app, loadtext):
    app.clear_main_content()

    loading_frame = tk.Frame(app.main_content, bg="white")
    loading_frame.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame

    loading_label = tk.Label(
        loading_frame,
        text=loadtext,
        font=("Arial", 16, "bold"),
        bg="white",
        fg="#333333",
    )
    loading_label.pack(pady=20)

    gif_label = tk.Label(loading_frame, bg="white")
    gif_label.pack()

    current_file_path = os.path.abspath(__file__)
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
    gif_path = "media/spinner.gif"  # Replace with your GIF file path
    spinner_path = os.path.join(project_root, gif_path)
    gif = Image.open(spinner_path)
    frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]

    def animate(index):
        if gif_label.winfo_exists():
            frame = frames[index]
            gif_label.configure(image=frame)
            index = (index + 1) % len(frames)
            app.after(100, animate, index)
        else:
            return

    animate(0)
