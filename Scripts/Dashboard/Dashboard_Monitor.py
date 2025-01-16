import tkinter as tk
from tkinter import ttk

def show_monitor(app):
    app.clear_main_content()

    home_frame = tk.Frame(app.main_content, bg="white")
    home_frame.pack(fill=tk.X, pady=20, padx=20, anchor="w")

    # Credits
    project_label = tk.Label(
        home_frame,
        text="Monitor Screen",
        font=("Arial", 12),
        bg="white",
        fg="#333333",
    )
    project_label.pack(side=tk.LEFT, padx=(0, 10))
