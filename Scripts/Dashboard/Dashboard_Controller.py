import threading
import time
import customtkinter as ctk
from PIL import Image
from Scripts.Dashboard.Dashboard_Deploy import show_deploy
from Scripts.Dashboard.Dashboard_Home import show_home
from Scripts.Dashboard.Dashboard_Loading import show_loading
from Scripts.Dashboard.Dashboard_Monitor import show_monitor
from Scripts.Dashboard.Dashboard_Settings import show_settings


class DashboardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Launchkube")
        self.geometry("1000x600")
        self.configure(bg="#F5F5F5")
        self.resizable(width=False, height=False)
        self.iconbitmap('media/icon/launchkube_icon.ico')

        # Sidebar
        self.sidebar = ctk.CTkFrame(self, corner_radius=0, width=200, fg_color="#2C3E50")
        self.sidebar.pack(side=ctk.LEFT, fill=ctk.Y)

        launchkube_banner = ctk.CTkImage(light_image=Image.open('media/launchkube_banner.png'),
                                          dark_image=Image.open('media/launchkube_banner.png'),
                                          size=(200, 110))

        banner = ctk.CTkLabel(self.sidebar, text="", image=launchkube_banner)
        banner.pack(pady=10)

        self.buttons = {
            "Home": self.show_home,
            "Monitor": self.show_monitor,
            "Deploy": self.show_deploy,
            "Settings": self.show_settings,
        }

        for idx, (label, command) in enumerate(self.buttons.items()):
            btn = ctk.CTkButton(
                self.sidebar,
                text=label,
                fg_color="#34495E",
                text_color="white",
                font=("Arial", 12),
                corner_radius=5,
                command=command,
            )
            if label == "Settings":
                btn.pack(side=ctk.BOTTOM, fill=ctk.X, pady=10, padx=10)
            else:
                btn.pack(fill=ctk.X, pady=(10 if idx == 0 else 5, 0), padx=10)

        # Main Content Area
        self.main_content = ctk.CTkFrame(self, corner_radius=10, fg_color="white")
        self.main_content.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True)

        self.current_project_var = ctk.StringVar()

        self.show_home()

    def clear_main_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def update_content(self, message):
        self.clear_main_content()
        content_label = ctk.CTkLabel(
            self.main_content,
            text=message,
            font=("Arial", 16),
            text_color="#333333",
        )
        content_label.pack(expand=True)

    def show_home(self):
        show_loading(self, "Loading...")
        self.after(7, lambda: show_home(self))

    def show_monitor(self):
        show_loading(self, "Loading...")
        self.after(7, lambda: show_monitor(self))

    def show_deploy(self):
        show_loading(self, "Loading...")
        self.after(7, lambda: show_deploy(self))

    def show_settings(self):
        def load_settings():
            time.sleep(5)
            self.after(0, lambda: show_settings(self))

        show_loading(self, "Loading Settings...")
        threading.Thread(target=load_settings, daemon=True).start()

def dashboard_open():
    ctk.set_appearance_mode("dark")  # Modes: "dark", "light", "system"
    ctk.set_default_color_theme("blue")
    app = DashboardApp()
    app.mainloop()
