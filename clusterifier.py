import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser

def pick_file():
    filepath = filedialog.askopenfilename(filetypes=[("Valve Map Files (P2:CE ONLY)", "*.vmf")])
    if not filepath:
        return
    try:
        with open(filepath, "r") as file:
            lines = file.readlines()
        modified_lines = []
        for line in lines:
            if '"_lightmode"' in line:
                continue
            modified_lines.append(line)
            if '"_lightHDR"' in line:
                mode_num = mode_var.get().split(" - ")[0]
                modified_lines.append(f'\t\t"_lightmode" "{mode_num}"\n')
        with open(filepath, "w") as file:
            file.writelines(modified_lines)
        messagebox.showinfo("Success", "File updated successfully.")
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
root.geometry("500x360")
root.resizable(False, False)

title_label = tk.Label(root, text="CLUSTERIFIER", font=("Helvetica", 22, "bold"), cursor="hand2")
title_label.pack(pady=(15, 10))
title_label.bind("<Button-1>", open_website)

frame = tk.Frame(root)
frame.pack(pady=10)

mode_label = tk.Label(frame, text="Lighting Mode:")
mode_label.grid(row=0, column=0, padx=(0, 10))

mode_var = tk.StringVar(value="Static")
mode_options = [
    "Static",
    "Specular",
    "Static Bounce",
    "Fully Dynamic"
]
mode_dropdown = ttk.Combobox(frame, textvariable=mode_var, values=mode_options, width=35, state="readonly")
mode_dropdown.grid(row=0, column=1)

help_button = tk.Button(frame, text="?", width=2, command=show_help)
help_button.grid(row=0, column=2, padx=(5, 0))

btn_pick = tk.Button(root, text="Pick VMF File", command=pick_file, width=30, font=("Helvetica", 10, "bold"))
btn_pick.pack(pady=(20, 10))



footer_frame = tk.Frame(root)
footer_frame.pack(side="bottom", pady=10)
footer = tk.Label(footer_frame, text="Made by dk865", font=("Helvetica", 9, "italic"), cursor="hand2", fg="#555")
footer.pack(side="right")
footer2 = tk.Label(footer_frame, text="Source Code (GitHub)", font=("Helvetica", 9, "italic"), cursor="hand2", fg="#555")
footer2.pack(side="right")
footer.bind("<Button-1>", open_website)
footer2.bind("<Button-1>", open_github)


root.mainloop()
