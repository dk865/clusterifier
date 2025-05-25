import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import shutil
import os
import zipfile

def pick_file():
    filepath = filedialog.askopenfilename(filetypes=[("Valve Map Files", "*.vmf")])
    if not filepath:
        return
    file_var.set(filepath)
    backup_entry_var.set("")
    mode_dropdown.config(state="readonly")
    backup_check.config(state="normal")
    convert_check.config(state="normal")
    clusterify_btn.config(state="normal")
    backup_entry.config(state="disabled")
    save_backup_btn.config(state="disabled")
    backup_var.set(False)

def pick_folder():
    folder = filedialog.askdirectory()
    if folder:
        batch_dir_var.set(folder)
        mode_dropdown.config(state="readonly")
        backup_check.config(state="normal")
        backup_var.set(False)
        convert_check.config(state="normal")
        clusterify_btn.config(state="normal")
        backup_entry_var.set("")
        backup_entry.config(state="disabled")
        save_backup_btn.config(state="disabled")

def update_backup_controls():
    is_single_mode = notebook.index(notebook.select()) == 0
    is_batch_mode = notebook.index(notebook.select()) == 1
    backup_enabled = backup_var.get()

    if is_single_mode:
        backup_check.config(state="normal")
    elif is_batch_mode:
        backup_check.config(state="normal")
    else:
        backup_check.config(state="disabled")
        backup_var.set(False)
        backup_enabled = False

    if backup_enabled:
        backup_entry.config(state="normal")
        save_backup_btn.config(state="normal")
        if not backup_entry_var.get():
            if is_single_mode:
                original_file = file_var.get()
                if original_file:
                    backup_entry_var.set(original_file + ".bak")
            elif is_batch_mode:
                folder = batch_dir_var.get()
                if folder:
                    backup_entry_var.set(os.path.join(folder, "vmf_backups.zip"))
    else:
        backup_entry_var.set("")
        backup_entry.config(state="disabled")
        save_backup_btn.config(state="disabled")

def on_backup_toggle():
    update_backup_controls()

def on_save_backup():
    is_single_mode = notebook.index(notebook.select()) == 0
    is_batch_mode = notebook.index(notebook.select()) == 1

    if is_single_mode:
        original_file = file_var.get()
        if original_file:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".bak",
                filetypes=[("Backup Files", "*.bak")],
                initialfile=os.path.basename(original_file) + ".bak",
                title="Choose backup file location"
            )
            if save_path:
                backup_entry_var.set(save_path)
            else:
                backup_var.set(False)
                backup_entry_var.set("")
    elif is_batch_mode:
        folder = batch_dir_var.get()
        if folder:
            save_path = filedialog.asksaveasfilename(
                defaultextension=".zip",
                filetypes=[("ZIP files", "*.zip")],
                initialfile="vmf_backups.zip",
                title="Save backup zip file as"
            )
            if save_path:
                backup_entry_var.set(save_path)
            else:
                backup_var.set(False)
                backup_entry_var.set("")
    update_backup_controls()

def on_tab_change(event=None):
    update_backup_controls()

def get_all_vmf_files(directory):
    vmf_files = []
    for root_dir, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".vmf"):
                vmf_files.append(os.path.join(root_dir, file))
    return vmf_files

def run_clusterify():
    is_batch = notebook.index(notebook.select()) == 1

    if is_batch:
        folder = batch_dir_var.get()
        if not folder:
            messagebox.showwarning("No folder selected", "Please select a batch folder first.")
            return
        filepaths = get_all_vmf_files(folder)
        if not filepaths:
            messagebox.showwarning("No VMF files found", "No .vmf files found in the selected folder.")
            return
    else:
        filepath = file_var.get()
        if not filepath:
            messagebox.showwarning("No file selected", "Please select a VMF file first.")
            return
        filepaths = [filepath]

    try:
        if backup_var.get():
            backup_path = backup_entry_var.get()
            if not backup_path:
                messagebox.showwarning("No backup path", "Please specify a backup file location.")
                return

            if is_batch:
                with zipfile.ZipFile(backup_path, 'w') as zipf:
                    for f in filepaths:
                        bak = f + ".bak"
                        shutil.copyfile(f, bak)
                        arcname = os.path.relpath(f, folder)
                        zipf.write(bak, arcname)
                        os.remove(bak)
            else:
                shutil.copyfile(filepaths[0], backup_path)

        total_lights = 0
        mode_map = {
            "Static": "0",
            "Specular": "1",
            "Static Bounce": "2",
            "Fully Dynamic": "3"
        }
        selected_mode = mode_var.get()
        mode_num = mode_map.get(selected_mode, "0")

        for filepath in filepaths:
            with open(filepath, "r") as file:
                lines = file.readlines()

            modified_lines = []
            lightmode_count = 0
            inside_entity = False
            current_entity = []

            for line in lines:
                stripped = line.strip()
                if stripped == "entity":
                    inside_entity = True
                    current_entity = [line]
                    continue
                if inside_entity:
                    current_entity.append(line)
                    if stripped == "}":
                        inside_entity = False
                        class_index = next((i for i, l in enumerate(current_entity) if '"classname"' in l), None)
                        lightmode_index = next((i for i, l in enumerate(current_entity) if '"_lightHDR"' in l), None)

                        if class_index is not None and lightmode_index is not None:
                            classname = current_entity[class_index]
                            if convert_var.get():
                                if '"classname" "light"' in classname:
                                    current_entity[class_index] = '\t\t"classname" "light_rt"\n'
                                elif '"classname" "light_spot"' in classname:
                                    current_entity[class_index] = '\t\t"classname" "light_rt_spot"\n'

                            current_entity.insert(lightmode_index + 1, f'\t\t"_lightmode" "{mode_num}"\n')
                            lightmode_count += 1

                            if convert_var.get() and ('"light_rt"' in current_entity[class_index] or '"light_rt_spot"' in current_entity[class_index]):
                                if not any('_rt_radius' in l for l in current_entity):
                                    current_entity.insert(-2, '\t\t"_rt_radius" "256"\n')
                                if not any('_rt_fifty_percent_scale' in l for l in current_entity):
                                    current_entity.insert(-2, '\t\t"_rt_fifty_percent_scale" "0.5"\n')

                        modified_lines.extend(current_entity)
                    continue
                modified_lines.append(line)

            with open(filepath, "w") as file:
                file.writelines(modified_lines)

            total_lights += lightmode_count

        msg = f"{len(filepaths)} file(s) updated.\nTotal lights modified: {total_lights}."
        if backup_var.get():
            msg += f"\nBackup saved as '{os.path.basename(backup_entry_var.get())}'."
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
        " - Standard Source engine baked lighting\n"
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

def show_convert_help():
    messagebox.showinfo("Convert to light_rt Help",
        " - light_rt and light_rt_spot are new entities included with the Portal 2 Community Edition clustered beta.\n"
        " - These new entities are almost completely identical to the old ones.\n"
        " - It is recommended to only use these entities."
    )

root = tk.Tk()
root.title("CLUSTERIFIER")
root.geometry("540x500")
root.resizable(False, False)

file_var = tk.StringVar()
mode_var = tk.StringVar()
backup_var = tk.BooleanVar()
backup_entry_var = tk.StringVar()
convert_var = tk.BooleanVar(value=False)
batch_dir_var = tk.StringVar()

title_label = tk.Label(root, text="CLUSTERIFIER", font=("Helvetica", 22, "bold"), cursor="hand2")
title_label.pack(pady=(15, 10))
title_label.bind("<Button-1>", open_website)

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill='both')

single_tab = tk.Frame(notebook)
batch_tab = tk.Frame(notebook)
notebook.add(single_tab, text="Single File")
notebook.add(batch_tab, text="Batch Folder")

file_frame = tk.Frame(single_tab)
file_frame.pack(pady=10)
file_entry = tk.Entry(file_frame, textvariable=file_var, width=48)
file_entry.grid(row=0, column=0, padx=(10, 5))
browse_btn = tk.Button(file_frame, text="Browse", command=pick_file)
browse_btn.grid(row=0, column=1)

batch_frame = tk.Frame(batch_tab)
batch_frame.pack(pady=10)
batch_dir_entry = tk.Entry(batch_frame, textvariable=batch_dir_var, width=48)
batch_dir_entry.grid(row=0, column=0, padx=(10, 5))
batch_browse_btn = tk.Button(batch_frame, text="Browse", command=pick_folder)
batch_browse_btn.grid(row=0, column=1)

mode_frame = tk.Frame(root)
mode_frame.pack(pady=10)
tk.Label(mode_frame, text="Lighting Mode:").grid(row=0, column=0, padx=(0, 10))
mode_dropdown = ttk.Combobox(mode_frame, textvariable=mode_var, values=[
    "Static",
    "Specular",
    "Static Bounce",
    "Fully Dynamic"
], width=35, state="disabled")
mode_dropdown.grid(row=0, column=1)
help_button = tk.Button(mode_frame, text="?", width=2, command=show_help)
help_button.grid(row=0, column=2, padx=(5, 0))

convert_frame = tk.Frame(root)
convert_frame.pack()
convert_check = tk.Checkbutton(convert_frame, text="Convert lights to light_rt/light_rt_spot", variable=convert_var, state="disabled")
convert_check.grid(row=0, column=0)
convert_help_btn = tk.Button(convert_frame, text="?", width=2, command=show_convert_help)
convert_help_btn.grid(row=0, column=1, padx=(5, 0))

backup_frame = tk.Frame(root)
backup_frame.pack(pady=10)
backup_check = tk.Checkbutton(backup_frame, text="Create backup", variable=backup_var, state="disabled", command=on_backup_toggle)
backup_check.grid(row=0, column=0, sticky="w")
backup_entry = tk.Entry(backup_frame, textvariable=backup_entry_var, width=40, state="disabled")
backup_entry.grid(row=0, column=1, padx=(10, 0))
save_backup_btn = tk.Button(backup_frame, text="Save As", state="disabled", command=on_save_backup)
save_backup_btn.grid(row=0, column=2, padx=(5, 10))

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

notebook.bind("<<NotebookTabChanged>>", on_tab_change)

root.mainloop()
