import tkinter as tk
from tkinter import ttk
import requests

root = tk.Tk()
root.title("User Management App")

name_var = tk.StringVar()
age_var = tk.StringVar()
address_var = tk.StringVar()

def add_user():
    data = {
        "name": name_var.get(),
        "age": age_var.get(),
        "address": address_var.get(),
    }
    response = requests.post("http://127.0.0.1:5000/api/add_user", json=data)
    print(response.json())
    load_data()

def load_data():
    tree.delete(*tree.get_children())
    response = requests.get("http://127.0.0.1:5000/api/get_users")
    users = response.json()
    for user in users:
        tree.insert("", "end", values=(user["name"], user["age"], user["address"]))

def delete_user():
    selected_item = tree.selection()
    if selected_item:
        user_name = tree.item(selected_item, "values")[0]
        response = requests.delete(f"http://127.0.0.1:5000/api/delete_user/{user_name}")
        print(response.json())
        load_data()

def update_user():
    selected_item = tree.selection()
    if selected_item:
        user_name = tree.item(selected_item, "values")[0]
        data = {
            "age": age_var.get(),
            "address": address_var.get(),
        }
        response = requests.put(f"http://127.0.0.1:5000/api/update_user/{user_name}", json=data)
        print(response.json())
        load_data()

# Labels
tk.Label(root, text="Name:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(root, text="Age:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(root, text="Address:").grid(row=2, column=0, padx=5, pady=5)

# Entry widgets
tk.Entry(root, textvariable=name_var).grid(row=0, column=1, padx=5, pady=5)
tk.Entry(root, textvariable=age_var).grid(row=1, column=1, padx=5, pady=5)
tk.Entry(root, textvariable=address_var).grid(row=2, column=1, padx=5, pady=5)

# Buttons
tk.Button(root, text="Add User", command=add_user).grid(row=3, column=0, columnspan=2, pady=10)
tk.Button(root, text="Load Data", command=load_data).grid(row=4, column=0, columnspan=2, pady=10)
tk.Button(root, text="Delete User", command=delete_user).grid(row=5, column=0, columnspan=2, pady=10)
tk.Button(root, text="Update User", command=update_user).grid(row=6, column=0, columnspan=2, pady=10)

# Treeview
tree = ttk.Treeview(root, columns=("Name", "Age", "Address"), show="headings")
tree.heading("Name", text="Name")
tree.heading("Age", text="Age")
tree.heading("Address", text="Address")
tree.grid(row=7, column=0, columnspan=2, pady=10)

root.mainloop()
