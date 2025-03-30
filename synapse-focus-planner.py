import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import time
import threading
from datetime import datetime
import os

DATA_FILE = "planner_data.json"

# Load or create planner data
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w') as f:
        json.dump({}, f)

with open(DATA_FILE, 'r') as f:
    planner_data = json.load(f)

# Save planner data
def save_data():
    with open(DATA_FILE, 'w') as f:
        json.dump(planner_data, f, indent=4)

# ----------------- MAIN APP -------------------

class SynapsePlanner(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🧠 Synapse Focus Planner")
        self.geometry("800x600")
        self.configure(bg="#1e1e2f")

        self.current_date = datetime.now().strftime("%Y-%m-%d")
        self.build_ui()

    def build_ui(self):
        self.build_header()
        self.build_daily_tasks()
        self.build_pomodoro()
        self.build_goal_section()

    def build_header(self):
        tk.Label(self, text=f"Today: {self.current_date}", font=("Helvetica", 16),
                 fg="white", bg="#1e1e2f").pack(pady=10)

    def build_daily_tasks(self):
        self.task_frame = tk.Frame(self, bg="#1e1e2f")
        self.task_frame.pack(pady=10)

        self.task_listbox = tk.Listbox(self.task_frame, width=50, font=("Arial", 12),
                                       bg="#2e2e3f", fg="white", selectbackground="orange")
        self.task_listbox.pack(side=tk.LEFT, padx=10)

        scrollbar = tk.Scrollbar(self.task_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        self.load_tasks()

        tk.Button(self, text="➕ Add Task", command=self.add_task).pack(pady=5)
        tk.Button(self, text="✅ Complete Task", command=self.complete_task).pack(pady=5)

    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        tasks = planner_data.get(self.current_date, {}).get("tasks", [])
        for task in tasks:
            self.task_listbox.insert(tk.END, f"☐ {task}")

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task:")
        if task:
            planner_data.setdefault(self.current_date, {}).setdefault("tasks", []).append(task)
            save_data()
            self.load_tasks()

    def complete_task(self):
        selection = self.task_listbox.curselection()
        if selection:
            index = selection[0]
            task_text = self.task_listbox.get(index)
            self.task_listbox.delete(index)
            self.task_listbox.insert(index, task_text.replace("☐", "☑"))
            planner_data[self.current_date]["tasks"][index] = task_text.replace("☐", "☑")
            save_data()

    def build_pomodoro(self):
        self.timer_frame = tk.Frame(self, bg="#1e1e2f")
        self.timer_frame.pack(pady=15)

        self.timer_label = tk.Label(self.timer_frame, text="25:00", font=("Courier", 24),
                                    fg="white", bg="#1e1e2f")
        self.timer_label.pack()

        tk.Button(self.timer_frame, text="▶ Start Pomodoro", command=self.start_pomodoro).pack()

    def start_pomodoro(self):
        self.countdown(25 * 60)

    def countdown(self, remaining):
        if remaining >= 0:
            mins, secs = divmod(remaining, 60)
            time_str = f"{mins:02}:{secs:02}"
            self.timer_label.config(text=time_str)
            self.after(1000, self.countdown, remaining - 1)
        else:
            messagebox.showinfo("Pomodoro Finished!", "Take a break!")

    def build_goal_section(self):
        self.goal_frame = tk.Frame(self, bg="#1e1e2f")
        self.goal_frame.pack(pady=10)

        tk.Label(self.goal_frame, text="🎯 Goals", font=("Helvetica", 14), fg="white", bg="#1e1e2f").pack()
        tk.Button(self.goal_frame, text="Add Goal", command=self.add_goal).pack()

        self.goal_listbox = tk.Listbox(self.goal_frame, width=50, font=("Arial", 12),
                                       bg="#2e2e3f", fg="white")
        self.goal_listbox.pack()
        self.load_goals()

    def load_goals(self):
        self.goal_listbox.delete(0, tk.END)
        goals = planner_data.get("goals", [])
        for goal in goals:
            self.goal_listbox.insert(tk.END, f"🎯 {goal}")

    def add_goal(self):
        goal = simpledialog.askstring("New Goal", "Enter goal:")
        if goal:
            planner_data.setdefault("goals", []).append(goal)
            save_data()
            self.load_goals()

# ------------------ RUN APP -------------------

if __name__ == "__main__":
    app = SynapsePlanner()
    app.mainloop()
