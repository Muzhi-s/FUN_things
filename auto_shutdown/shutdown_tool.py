import os
import tkinter as tk
from tkinter import messagebox, ttk

class ShutdownTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Shutdown Tool")
        self.root.geometry("350x200")
        self.root.resizable(False, False)
        
        # 使用 ttk 样式
        style = ttk.Style()
        style.configure("TButton", font=("Arial", 12), padding=5)
        style.configure("TLabel", font=("Arial", 10))
        style.configure("TEntry", font=("Arial", 12))
        
        # 输入框和标签
        self.label_minutes = ttk.Label(root, text="Enter shutdown time (minutes):")
        self.label_minutes.pack(pady=10)

        self.entry_minutes = ttk.Entry(root, width=10)
        self.entry_minutes.pack(pady=5)

        # 设置关机和取消关机按钮
        self.button_set = ttk.Button(root, text="Set Shutdown", command=self.schedule_shutdown)
        self.button_set.pack(pady=5)

        self.button_cancel = ttk.Button(root, text="Cancel Shutdown", command=self.cancel_shutdown)
        self.button_cancel.pack(pady=5)
    
    def schedule_shutdown(self):
        try:
            minutes = int(self.entry_minutes.get())
            if minutes < 0:
                raise ValueError("Time must be non-negative.")
            seconds = minutes * 60
            os.system(f"shutdown /s /f /t {seconds}")
            messagebox.showinfo("Success", f"System will shut down in {minutes} minute(s).")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of minutes.")
    
    def cancel_shutdown(self):
        os.system("shutdown /a")
        messagebox.showinfo("Canceled", "Scheduled shutdown has been canceled.")

def main():
    root = tk.Tk()
    app = ShutdownTool(root)
    root.mainloop()

if __name__ == "__main__":
    main()
