import tkinter as tk
from tkinter import messagebox, ttk
import json
import os
from datetime import datetime

FILE_NAME = "tasks_advanced.json"

def load_tasks():
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []
    return []

def save_tasks(tasks):
    try:
        with open(FILE_NAME, "w") as f:
            json.dump(tasks, f, indent=4)
    except Exception as e:
        messagebox.showerror("File Error", f"Could not save tasks:\n{e}")

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📝 Advanced To-Do List")
        self.root.geometry("500x600")
        self.root.configure(bg="#1e1e1e")

        self.tasks = load_tasks()

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", background="#1e1e1e", foreground="white", font=("Segoe UI", 11))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TCombobox", fieldbackground="#333", background="#333", foreground="white")

        input_frame = tk.Frame(self.root, bg="#1e1e1e")
        input_frame.pack(pady=10)

        self.task_entry = tk.Entry(input_frame, width=30, font=("Segoe UI", 12), bg="#333", fg="white", insertbackground="white")
        self.task_entry.grid(row=0, column=0, padx=5, pady=5)

        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], width=10, state="readonly")
        self.priority_menu.grid(row=0, column=1, padx=5)

        self.due_entry = tk.Entry(input_frame, width=15, font=("Segoe UI", 10), bg="#333", fg="white", insertbackground="white")
        self.due_entry.grid(row=0, column=2, padx=5)
        self.due_entry.insert(0, "YYYY-MM-DD")

        self.add_btn = tk.Button(self.root, text="➕ Add Task", command=self.add_task, bg="#28a745", fg="white", font=("Segoe UI", 11))
        self.add_btn.pack(pady=10)

        self.task_listbox = tk.Listbox(self.root, width=65, height=20, font=("Segoe UI", 11), bg="#2e2e2e", fg="white", selectbackground="#444")
        self.task_listbox.pack(padx=10, pady=10)

        self.complete_btn = tk.Button(self.root, text="✅ Mark Complete", command=self.mark_complete, bg="#007bff", fg="white", font=("Segoe UI", 10))
        self.complete_btn.pack(pady=5)

        self.delete_btn = tk.Button(self.root, text="🗑️ Delete Task", command=self.delete_task, bg="#dc3545", fg="white", font=("Segoe UI", 10))
        self.delete_btn.pack(pady=5)

        self.load_to_listbox()

    def add_task(self):
        task = self.task_entry.get().strip()
        priority = self.priority_var.get()
        due_date = self.due_entry.get().strip()

        if not task:
            messagebox.showwarning("⚠️ Error", "Task description is required.")
            return

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("❌ Invalid Date", "Use format YYYY-MM-DD.")
                return

        self.tasks.append({
            "task": task,
            "priority": priority,
            "due": due_date,
            "done": False
        })
        save_tasks(self.tasks)

        self.task_entry.delete(0, tk.END)
        self.due_entry.delete(0, tk.END)
        self.due_entry.insert(0, "YYYY-MM-DD")
        self.load_to_listbox()

    def load_to_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "✅" if task["done"] else "❌"
            display = f"{task['task']} [{task['priority']}] (Due: {task['due']}) {status}"
            self.task_listbox.insert(tk.END, display)

    def mark_complete(self):
        index = self.task_listbox.curselection()
        if index:
            i = index[0]
            if i < len(self.tasks):
                self.tasks[i]["done"] = True
                save_tasks(self.tasks)
                self.load_to_listbox()
        else:
            messagebox.showinfo("ℹ️ No Selection", "Select a task to mark complete.")

    def delete_task(self):
        index = self.task_listbox.curselection()
        if index:
            i = index[0]
            if i < len(self.tasks):
                task_name = self.tasks[i]["task"]
                del self.tasks[i]
                save_tasks(self.tasks)
                self.load_to_listbox()
                messagebox.showinfo("🗑️ Deleted", f"Task '{task_name}' was deleted.")
        else:
            messagebox.showinfo("ℹ️ No Selection", "Select a task to delete.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
