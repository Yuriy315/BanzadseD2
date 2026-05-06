import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Предопределённые задачи с типами
TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть лекцию", "type": "учёба"},
    {"name": "Погулять на улице", "type": "отдых"},
]

HISTORY_FILE = "tasks.json"

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.history = self.load_history()
        self.current_filter = None

        # Виджеты
        self.task_label = tk.Label(root, text="Ваша задача появится здесь", font=("Arial", 14))
        self.task_label.pack(pady=10)

        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        self.filter_var = tk.StringVar(value="все")
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        ttk.OptionMenu(filter_frame, self.filter_var, "все", "все", "учёба", "спорт", "работа", "отдых",
                       command=self.apply_filter).pack(side=tk.LEFT)

        self.history_listbox = tk.Listbox(root, width=50, height=10)
        self.history_listbox.pack(pady=10)
        self.update_history_list()

    def generate_task(self):
        filtered_tasks = [t for t in TASKS if not self.current_filter or t["type"] == self.current_filter]
        if not filtered_tasks:
            messagebox.showwarning("Нет задач", "Нет задач выбранного типа.")
            return
        task = random.choice(filtered_tasks)
        self.task_label.config(text=task["name"])
        self.history.append(task)
        self.save_history()
        self.update_history_list()

    def apply_filter(self, value):
        self.current_filter = None if value == "все" else value

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def update_history_list(self):
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            self.history_listbox.insert(tk.END, f"{task['name']} ({task['type']})")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()