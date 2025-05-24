import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import shutil
import os

def pick_file():
    filepath = filedialog.askopenfilename(filetypes=[("Valve Map Files", "*.vmf")])
    if not filepath:
        return
    file_var.set(filepath)
    backup_name = os.path.basename(filepath) + ".bak"
    backup_entry_var.set(backup_name)
    mode_dropdown.config(state="readonly")

def on_mode_select(event=None):
    backup_check.config(state="normal")
    clusterify_btn.config(state="normal")
    backup_entry.config(state="normal")

def run_clusterify():
    filepath = file_var.get()
    if not filepath:
        return
    try:
        if backup_var.get():
            backup_path = os.path.join(os.path.dirname(filepath), backup_entry_var.get())
            shutil.copyfile(filepath, backup_path)

        with open(filepath, "r") as file:
            lines = file.readlines()

        modified_lines = []
        lightmode_count = 0
        mode_num = mode_var.get().split(" - ")[0] if " - " in mode_var.get() else mode_var.get()

        for line in lines:
            if '"_lightmode"' in line:
                continue
            modified_lines.append(line)
            if '"_lightHDR"' in line:
                modified_lines.append(f'\t\t"_lightmode" "{mode_num}"\n')
                lightmode_count += 1

        with open(filepath, "w") as file:
            file.writelines(modified_lines)

        msg = f"File updated successfully.\n{lightmode_count} light(s) modified."
        if backup_var.get():
            msg += f"\nBackup saved as '{backup_entry_var.get()}'."
        messagebox.showinfo("Success", msg)
    except Exception as e:
        messagebox.showerror("Error", str(e))

def open_github(event=None):
    webbrowser.open("https://github.com/dk865/clusterifier")

def open_website(event=None):
    webbrowser.open("https://dk865.github.io")

def show_help():
    help_text = (
        "Light Modes Explained:\n\n"
        "Static:\n"
        " - No dynamic or specular lighting.\n"
        " - Produces direct and bounced static lightmaps.\n\n"
        "Specular:\n"
        " - Static lighting with added specular reflections.\n"
        " - Produces direct and bounced static lightmaps.\n\n"
        "Static Bounce:\n"
        " - Dynamic direct and specular lighting.\n"
        " - Only bounced lighting is static.\n\n"
        "Fully Dynamic:\n"
        " - Dynamic direct and specular lighting.\n"
        " - No static lightmaps at all.\n"
    )
    messagebox.showinfo("Light Mode Help", help_text)

root = tk.Tk()
root.title("CLUSTERIFIER")
root.geometry("500x420")
root.resizable(False, False)

title_label = tk.Label(root, text="CLUSTERIFIER", font=("Helvetica", 22, "bold"), cursor="hand2")
title_label.pack(pady=(15, 10))
title_label.bind("<Button-1>", open_website)

file_frame = tk.Frame(root)
file_frame.pack(pady=10)
file_var = tk.StringVar()
file_btn = tk.Button(file_frame, text="Choose VMF File", command=pick_file, width=30, font=("Helvetica", 10))
file_btn.pack()

mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)
tk.Label(mode_frame, text="Lighting Mode:").grid(row=0, column=0, padx=(0, 10))
mode_var = tk.StringVar()
mode_dropdown = ttk.Combobox(mode_frame, textvariable=mode_var, values=[
    "Static",
    "Specular",
    "Static Bounce",
    "Fully Dynamic"
], width=35, state="disabled")
mode_dropdown.grid(row=0, column=1)
mode_dropdown.bind("<<ComboboxSelected>>", on_mode_select)
help_button = tk.Button(mode_frame, text="?", width=2, command=show_help)
help_button.grid(row=0, column=2, padx=(5, 0))

backup_frame = tk.Frame(root)
backup_frame.pack(pady=10)
backup_var = tk.BooleanVar()
backup_check = tk.Checkbutton(backup_frame, text="Create backup", variable=backup_var, state="disabled")
backup_check.grid(row=0, column=0, sticky="w")

backup_entry_var = tk.StringVar()
backup_entry = tk.Entry(backup_frame, textvariable=backup_entry_var, width=40, state="disabled")
backup_entry.grid(row=0, column=1, padx=(10, 0))

clusterify_btn = tk.Button(root, text="Clusterify!", command=run_clusterify, state="disabled", width=30, font=("Helvetica", 10, "bold"))
clusterify_btn.pack(pady=(20, 10))

footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", pady=10)
footer = tk.Label(footer_frame, text="Made by dk865", font=("Helvetica", 9, "italic"), cursor="hand2", fg="#555")
footer.pack(side="right")
footer2 = tk.Label(footer_frame, text="Source Code (GitHub)", font=("Helvetica", 9, "italic"), cursor="hand2", fg="#555")
footer2.pack(side="right")
footer.bind("<Button-1>", open_website)
footer2.bind("<Button-1>", open_github)

root.mainloop()
