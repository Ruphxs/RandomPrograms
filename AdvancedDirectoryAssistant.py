import os
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox, ttk
import datetime
from sys import platform
import webbrowser
files = ['file1.txt', 'file2.txt', 'file3.txt']
def update_color(label, color_index=0):
    # Define a list of colors to cycle through (rainbow colors)
    colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet']
    # Update the label's text color
    label.config(fg=colors[color_index])
    # Move to the next color in the list
    color_index = (color_index + 1) % len(colors)
    # Schedule the update_color function to be called after 500ms
    label.after(500, update_color, label, color_index)
def get_file_details(directory):
    """Return a list of tuples containing file details."""
    file_details = []
    for file_name in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, file_name)):
            file_size = os.path.getsize(os.path.join(directory, file_name))
            file_mtime = datetime.datetime.fromtimestamp(
                os.path.getmtime(os.path.join(directory, file_name))
            ).strftime('%Y-%m-%d %I:%M:%S %p')
            file_details.append((file_name, file_size, file_mtime))
    return file_details

def apply_filter():
    directory = directory_label.cget("text")
    if not directory:
        messagebox.showwarning("Warning", "Please select a directory first.")
        return
    
    # Get the list of file details
    file_details = get_file_details(directory)
    
    # Decide the key for sorting based on the selected filter
    selected_filter = filter_var.get()
    if selected_filter == 'Sort by Name':
        file_details.sort(key=lambda x: x[0].lower())
    elif selected_filter == 'Sort by Size':
        file_details.sort(key=lambda x: x[1])
    
    # Clear the Treeview
    for item in file_list.get_children():
        file_list.delete(item)
    
    # Insert the sorted files back into the Treeview
    for file_name, file_size, file_mtime in file_details:
        file_list.insert('', 'end', values=(file_name, file_size, file_mtime))
# Initialize Tkinter
root = tk.Tk()
root.title("Enhanced File Manager GUI")
root.geometry("800x600")  # Increased size for additional features

from tkinter import ttk
color_scheme = {
    "background": "#23272A",
    "text": "#ffffff",
    "button": "#2C2F33",
    "button_text": "#ffffff",
    "frame": "#2C2F33",
    "tree": "#99AAB5",
}
# Initialize the style
style = ttk.Style()
style.theme_use('alt')
# Pick a theme that is available on your system
# This is optional; themes depend on the operating system
# style.theme_use('default')  # You can replace 'default' with 'clam', 'alt', 'classic', 'vista', 'xpnative'

# Customize the Treeview colors
style.configure("Treeview",
                background="#0FF8FD",  # Light yellow background
                foreground="#000000",  # Blue text
                rowheight=25,
                fieldbackground="#000000")  # Light yellow field background

# Change selected color
style.map('Treeview', background=[('selected', '#000099')])  # Darker blue selected background

filter_var = tk.StringVar()

filter_combobox = ttk.Combobox(root, textvariable=filter_var)
filter_combobox['values'] = ('Sort by Name', 'Sort by Size')  # Add other filter types here
filter_combobox.current(0)  # Set the default value
filter_combobox.pack()

apply_button = tk.Button(root, text="Apply Filter", command=apply_filter)
apply_button.pack()
# Customize the Treeview Heading (Column Header)
style.configure("Treeview.Heading",
                background="#3c3f41",
                foreground="#ffffff",
                relief="flat")

# Apply the style for every label, button, etc.
style.configure("TLabel", background=color_scheme["background"], foreground=color_scheme["text"])
style.configure("TButton", background=color_scheme["button"], foreground=color_scheme["button_text"])

# Use the style for a specific button if needed
# style.configure("Accent.TButton", background="#E1C699")

# Now, when you create a button, you can specify the style:
# ttk.Button(toolbar, text="Browse", command=browse_directory, style="Accent.TButton").pack(side=tk.LEFT, padx=2, pady=2)


# Set a colorful theme
color_scheme = {
    "background": "#23272A",
    "text": "#ffffff",
    "button": "#2C2F33",
    "button_text": "#ffffff",
    "frame": "#2C2F33",
    "tree": "#99AAB5",
}

# Function handlers
def browse_directory():
    dirname = filedialog.askdirectory(parent=root)
    if dirname:
        directory_label.config(text=dirname)
        refresh_file_list()

def refresh_file_list():
    # Clearing the Treeview
    for item in file_list.get_children():
        file_list.delete(item)
    # Filling the Treeview with new directory content
    directory = directory_label.cget("text")
    if directory:
        for file_name in os.listdir(directory):
            if os.path.isfile(os.path.join(directory, file_name)):
                file_size = os.path.getsize(os.path.join(directory, file_name))
                file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(directory, file_name))).strftime('%Y-%m-%d %I:%M:%S %p')
                file_list.insert('', 'end', values=(file_name, str(file_size), file_mtime))

def confirm_delete():
    confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete selected file(s)?")
    if confirm:
        delete_selected_files()

def delete_selected_files():
    selected_items = file_list.selection()
    directory = directory_label.cget("text")
    for item_id in selected_items:
        file_name = file_list.set(item_id, 'Name')
        file_path = os.path.join(directory, file_name)
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                file_list.delete(item_id)
        except OSError as e:
            messagebox.showerror("Error", f"Error deleting file {file_name}: {e}")

def rename_file_request():
    selected_items = file_list.selection()
    if not selected_items:
        messagebox.showinfo("Rename", "Please select a file to rename.")
        return
    rename_file(selected_items[0])

def rename_file(item_id):
    directory = directory_label.cget("text")
    original_file_name = file_list.set(item_id, 'Name')
    original_file_path = os.path.join(directory, original_file_name)
    new_file_name = simpledialog.askstring("Rename", "Enter new file name:", initialvalue=original_file_name)
    if not new_file_name:
        return
    new_file_path = os.path.join(directory, new_file_name)
    try:
        os.rename(original_file_path, new_file_path)
    except OSError as e:
        messagebox.showerror("Error", f"Error renaming file: {e}")
    else:
        refresh_file_list()

def view_properties(item_id):
    directory = directory_label.cget("text")
    file_name = file_list.set(item_id, 'Name')
    file_path = os.path.join(directory, file_name)
    file_size = os.path.getsize(file_path)
    file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %I:%M:%S %p')
    messagebox.showinfo("Properties", f"File: {file_name}\nSize: {file_size} bytes\nLast Modified: {file_mtime}")

def search_in_directory():
    search_query = simpledialog.askstring("Search", "Enter search term:")
    if search_query:
        for item in file_list.get_children():
            file_name = file_list.set(item, 'Name')
            if search_query.lower() not in file_name.lower():
                file_list.detach(item)
            else:
                file_list.reattach(item, '', 'end')

def open_file():
    selected_items = file_list.selection()
    if selected_items:  # Assuming we only open the first selected
        item_id = selected_items[0]
        file_name = file_list.set(item_id, 'Name')
        file_path = os.path.join(directory_label.cget("text"), file_name)
        if platform == "win32":  # Windows
            os.startfile(file_path)
        elif platform == "darwin":  # MacOS
            subprocess.Popen(["open", file_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", file_path])

# New Features Implementation
def copy_file():
    selected_items = file_list.selection()
    if not selected_items:
        messagebox.showinfo("Copy", "Please select a file to copy.")
        return
    directory = directory_label.cget("text")
    destination = filedialog.askdirectory(parent=root)
    for item_id in selected_items:
        file_name = file_list.set(item_id, 'Name')
        file_path = os.path.join(directory, file_name)
        shutil.copy(file_path, destination)

def move_file():
    selected_items = file_list.selection()
    if not selected_items:
        messagebox.showinfo("Move", "Please select a file to move.")
        return
    directory = directory_label.cget("text")
    destination = filedialog.askdirectory(parent=root)
    for item_id in selected_items:
        file_name = file_list.set(item_id, 'Name')
        file_path = os.path.join(directory, file_name)
        shutil.move(file_path, destination)
        refresh_file_list()

def create_directory():
    directory = directory_label.cget("text")
    if not directory:
        messagebox.showinfo("New Directory", "Please select a directory where the new folder will be created.")
        return
    new_dir_name = simpledialog.askstring("New Directory", "Enter name for new directory:")
    if new_dir_name:
        new_dir_path = os.path.join(directory, new_dir_name)
        try:
            os.makedirs(new_dir_path)
        except OSError as e:
            messagebox.showerror("Error", f"Error creating directory: {e}")
        else:
            refresh_file_list()

def open_with_default():
    selected_items = file_list.selection()
    if not selected_items:
        messagebox.showinfo("Open", "Please select a file to open.")
        return
    directory = directory_label.cget("text")
    for item_id in selected_items:
        file_name = file_list.set(item_id, 'Name')
        file_path = os.path.join(directory, file_name)
        if platform == "win32":  # Windows
            os.startfile(file_path)
        elif platform == "darwin":  # MacOS
            subprocess.Popen(["open", file_path])
        else:  # Linux
            subprocess.Popen(["xdg-open", file_path])

def open_email():
    # This will attempt to open the default mail client.
    # The actual mailto: URL should contain an email address.
    webbrowser.open('mailto:colbyruphxs1@gmail.com')

def open_phone():
    # For opening a phone number, this functionality will work if the user's device supports it.
    # Replace 'your_phone_number' with your actual phone number.
    webbrowser.open('tel:19023712577')

def open_github():
    # Replace 'your_github_username' with your actual GitHub username.
    webbrowser.open('https://github.com/Ruphxs')
    
    
    
    # Get the list of file details
    file_details = get_file_details(directory)
    
    # Decide the key for sorting based on the selected filter
    selected_filter = filter_var.get()
    if selected_filter == 'Sort by Name':
        file_details.sort(key=lambda x: x[0].lower())
    elif selected_filter == 'Sort by Size':
        file_details.sort(key=lambda x: x[1])
    
    # Clear the Treeview
    for item in file_list.get_children():
        file_list.delete(item)
    
    # Insert the sorted files back into the Treeview
    for file_name, file_size, file_mtime in file_details:
        file_list.insert('', 'end', values=(file_name, file_size, file_mtime))
# Create Menu and Toolbar
top_frame = tk.Frame(root, bg='white')
top_frame.pack(side=tk.TOP, fill=tk.X)

menu_bar = tk.Menu(top_frame)
root.config(menu=menu_bar)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Copy", command=copy_file)
file_menu.add_command(label="Move", command=move_file)
file_menu.add_command(label="Delete", command=confirm_delete)
file_menu.add_command(label="Create Directory", command=create_directory)
file_menu.add_command(label="Refresh", command=refresh_file_list)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
right_text = tk.Label(top_frame, text="Made By Colby Niedzielski", bg='white', fg='black')
right_text.pack(side='right', padx=10, pady=5)
update_color(right_text)
# Toolbar Frame
toolbar = tk.Frame(root, bg=color_scheme["button"])
toolbar.pack(side=tk.TOP, fill=tk.X)

# Add Toolbar buttons
browse_button = tk.Button(toolbar, text="Browse", command=browse_directory, bg=color_scheme["button"], fg=color_scheme["button_text"])
browse_button.pack(side=tk.LEFT, padx=2, pady=2)

rename_button = tk.Button(toolbar, text="Rename", command=rename_file_request, bg=color_scheme["button"], fg=color_scheme["button_text"])
rename_button.pack(side=tk.LEFT, padx=2, pady=2)

delete_button = tk.Button(toolbar, text="Delete", command=confirm_delete, bg=color_scheme["button"], fg=color_scheme["button_text"])
delete_button.pack(side=tk.LEFT, padx=2, pady=2)

search_button = tk.Button(toolbar, text="Search", command=search_in_directory, bg=color_scheme["button"], fg=color_scheme["button_text"])
search_button.pack(side=tk.LEFT, padx=2, pady=2)

open_button = tk.Button(toolbar, text="Open", command=open_file, bg=color_scheme["button"], fg=color_scheme["button_text"])
open_button.pack(side=tk.LEFT, padx=2, pady=2)

copy_button = tk.Button(toolbar, text="Copy", command=copy_file, bg=color_scheme["button"], fg=color_scheme["button_text"])
copy_button.pack(side=tk.LEFT, padx=2, pady=2)

move_button = tk.Button(toolbar, text="Move", command=move_file, bg=color_scheme["button"], fg=color_scheme["button_text"])
move_button.pack(side=tk.LEFT, padx=2, pady=2)

create_dir_button = tk.Button(toolbar, text="New Dir", command=create_directory, bg=color_scheme["button"], fg=color_scheme["button_text"])
create_dir_button.pack(side=tk.LEFT, padx=2, pady=2)

open_with_default_button = tk.Button(toolbar, text="Open With", command=open_with_default, bg=color_scheme["button"], fg=color_scheme["button_text"])
open_with_default_button.pack(side=tk.LEFT, padx=2, pady=2)

# File List Panel
file_list_frame = tk.Frame(root, bg=color_scheme["frame"])
file_list_frame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Creating Treeview Widget
file_list = ttk.Treeview(file_list_frame, columns=("Name", "Size", "Last Modified"), show="headings")
file_list.heading("Name", text="Name")
file_list.heading("Size", text="Size")
file_list.heading("Last Modified", text="Last Modified")
file_list.column("Name", stretch=tk.YES)
file_list.column("Size", stretch=tk.NO)
file_list.column("Last Modified", stretch=tk.NO)
file_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

# Scrollbar for the Treeview
scrollbar = ttk.Scrollbar(file_list_frame, orient="vertical", command=file_list.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
file_list.configure(yscrollcommand=scrollbar.set)

# Directory label
directory_label = tk.Label(root, text="No Directory Selected", bg=color_scheme["background"], fg=color_scheme["text"], anchor='w')
directory_label.pack(fill=tk.X, padx=5, pady=2)

links_panel = tk.Frame(root, bg='white')
links_panel.pack(side=tk.TOP, fill=tk.X)

# Email Button
email_button = tk.Button(links_panel, text="Email Me", command=open_email)
email_button.pack(side=tk.LEFT, padx=2, pady=2)

# Phone Button
phone_button = tk.Button(links_panel, text="Call Me", command=open_phone)
phone_button.pack(side=tk.LEFT, padx=2, pady=2)

# GitHub Button
github_button = tk.Button(links_panel, text="GitHub", command=open_github)
github_button.pack(side=tk.LEFT, padx=2, pady=2)




root.mainloop()
