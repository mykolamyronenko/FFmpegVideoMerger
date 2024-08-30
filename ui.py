import customtkinter as ctk
from tkinter import filedialog
from CTkMessagebox import CTkMessagebox
import threading
from video_processing import VideoProcessor
from utils import change_theme
import os
class VideoConverterUI:
    def __init__(self):
        self.app = ctk.CTk()
        self.processor = VideoProcessor(self)
        self.init_ui()

    def init_ui(self):
        change_theme()
        self.app.title("Concatenation")
        self.app.geometry("400x300")
        self.files = []
        self.output = ''
        self.converted_files = []
        self.title = ctk.CTkLabel(self.app, text="Choose files to merge", font=("cursive", 20), text_color="#0070ff")
        self.title.pack(padx=10, pady=10)
        choose_files_button = ctk.CTkButton(self.app, text='Choose Files', command=self.choose_files, width=200)
        choose_files_button.pack(padx=10, pady=10)
        save_to_button = ctk.CTkButton(self.app, text='Save Output To', command=self.save_to, width=200)
        save_to_button.pack(padx=10, pady=10)
        merge_button = ctk.CTkButton(self.app, text='Merge Files', command=self.start_merge, width=200)
        merge_button.pack(padx=10, pady=10)
        self.progress = ctk.CTkLabel(self.app, text="")
        self.progress.pack(padx=10, pady=10)
        self.progress_bar = ctk.CTkProgressBar(self.app, width=300, mode='determinate')
        self.progress_bar.pack(padx=10, pady=10)

    def choose_files(self):
        self.files = list(filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4;*.ts;*.avi;*.mkv;*.flv")]))
        print(self.files)

    def save_to(self):
        self.output = filedialog.asksaveasfilename(defaultextension=".mp4")
        print(self.output)

    def start_merge(self):
        if not self.files or not self.output:
            self.progress_bar.set(1)
            CTkMessagebox(title="Warning", message="Please choose files and output location first.", icon="warning")
            return
        confirm = CTkMessagebox(title="Confirmation", message=f"Are you sure you want to merge the following files? : {', '.join(os.path.basename(file) for file in self.files)}\nThe merged file will be saved as:\n{self.output}", icon="question", option_1="Yes", option_2="No")

        if confirm.get() == "Yes":
            threading.Thread(target=self.processor.start_merge).start()
            self.title.configure(text="")
        else:
            self.files = []
            self.output = ''
            self.title.configure(text="Choose files to merge")

    def run(self):
        self.app.mainloop()
