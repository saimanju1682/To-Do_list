import tkinter as tk
from tkinter import ttk
import sqlite3
from datetime import datetime

conn = sqlite3.connect("todolist.db")
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT,
        priority INTEGER,
        due_date DATE
    )
''')
conn.commit()

def add_task():
    task = task_entry.get()
    priority = priority_var.get()
    due_date = due_date_entry.get()
    
    if task:
        cursor.execute("INSERT INTO tasks (task, priority, due_date) VALUES (?, ?, ?)",
                       (task, priority, due_date))
        conn.commit()
        task_entry.delete(0, tk.END)
        due_date_entry.delete(0, tk.END)
        refresh_list()

def delete_task():
    selected_item = task_tree.selection()
    if selected_item:
        task_id = task_tree.item(selected_item, "values")[0]
        cursor.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
        refresh_list()

def refresh_list():
    for row in task_tree.get_children():
        task_tree.delete(row)
    
    cursor.execute("SELECT * FROM tasks ORDER BY priority DESC, due_date ASC")
    tasks = cursor.fetchall()
    
    for task in tasks:
        task_tree.insert("", "end", values=(task[0], task[1], task[2], task[3]))

root = tk.Tk()
root.title("To-Do List Application")
root.configure(bg="blue")

task_label = tk.Label(root, text="Task:")
task_label.pack()
task_entry = tk.Entry(root)
task_entry.pack()

priority_label = tk.Label(root, text="Priority:")
priority_label.pack()
priority_var = tk.IntVar()
priority_entry = ttk.Combobox(root, textvariable=priority_var, values=[1, 2, 3, 4, 5])
priority_entry.pack()

due_date_label = tk.Label(root, text="Due Date (DD-MM-YYYY):")
due_date_label.pack()
due_date_entry = tk.Entry(root)
due_date_entry.pack()

add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack()

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack()

task_tree = ttk.Treeview(root, columns=("ID", "Task", "Priority", "Due Date"), show="headings")
task_tree.heading("ID", text="ID")
task_tree.heading("Task", text="Task")
task_tree.heading("Priority", text="Priority")
task_tree.heading("Due Date", text="Due Date")
task_tree.pack()
refresh_list()

root.mainloop()

conn.close()
