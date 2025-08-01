import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# ----------------------------
# Tamil Mappings
# ----------------------------
tamil_vowels = {
    "a": ("அ", ""), "aa": ("ஆ", "ா"),
    "i": ("இ", "ி"), "ii": ("ஈ", "ீ"),
    "u": ("உ", "ு"), "uu": ("ஊ", "ூ"),
    "e": ("எ", "ெ"), "ee": ("ஏ", "ே"),
    "ai": ("ஐ", "ை"),
    "o": ("ஒ", "ொ"), "oo": ("ஓ", "ோ"),
    "au": ("ஔ", "ௌ"),
    "; (க்)": ("◌் (புள்ளி)", ""),  # Mei Pulli
    "sri": "ஸ்ரீ", "ohm": "ஓம்"
}

tamil_consonants = {
    "k": "க", "ng": "ங", "c": "ச", "nj": "ஞ",
    "d": "ட", "N": "ண", "th": "த", "nh": "ந",
    "p": "ப", "m": "ம", "b": "ப",
    "y": "ய", "r": "ர", "l": "ல",
    "v": "வ", "zh": "ழ", "L": "ள",
    "R": "ற", "n": "ன",
    "j": "ஜ", "sh": "ஷ", "s": "ஸ", "h": "ஹ",
    "ksh": "க்ஷ",
}

exceptions = {"sri": "ஸ்ரீ", "om": "ஓம்"}
tamil_consonants_ordered = list(tamil_consonants.keys())
grantha_keys = {"j", "sh", "s", "h", "ksh"}

# ----------------------------
# Transliteration Logic
# ----------------------------
def transliterate_word(word):
    if word in exceptions:
        return exceptions[word]

    i, result = 0, []
    while i < len(word):
        match = None

        # Mei Pulli check
        for c_key in sorted(tamil_consonants.keys(), key=len, reverse=True):
            if word[i:].startswith(c_key + ";"):
                result.append(tamil_consonants[c_key] + "்")
                i += len(c_key) + 1
                status_var.set(f"Pulli applied: {tamil_consonants[c_key]}் (Mei form)")
                match = True
                break
        if match:
            continue

        # Vowel attachment
        for v_key in sorted(tamil_vowels.keys(), key=len, reverse=True):
            if word[i:].startswith(v_key.replace(" (க்)", "")):
                if result and result[-1] in tamil_consonants.values():
                    cons = result.pop()
                    result.append(cons + tamil_vowels[v_key][1])
                else:
                    result.append(tamil_vowels[v_key][0])
                i += len(v_key.replace(" (க்)", ""))
                status_var.set("")
                match = True
                break
        if match:
            continue

        # Consonant check
        for c_key in sorted(tamil_consonants.keys(), key=len, reverse=True):
            if word[i:].startswith(c_key):
                result.append(tamil_consonants[c_key])
                i += len(c_key)
                status_var.set("")
                match = True
                break

        if not match:
            result.append(word[i])
            i += 1
            status_var.set("")

    return "".join(result)

def convert_text(text):
    if not tamil_mode[0]:
        return text
    return " ".join(transliterate_word(w) for w in text.split())

# ----------------------------
# GUI Functions
# ----------------------------
def on_text_change(event=None):
    input_text = input_box.get("1.0", tk.END).strip()
    output_text = convert_text(input_text)
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, output_text)
    output_box.config(state="disabled")

def toggle_mode(event=None):
    tamil_mode[0] = not tamil_mode[0]
    if tamil_mode[0]:
        mode_button.config(text="Tamil Mode", bg="green", fg="white")
        status_var.set("Mode: Tamil")
    else:
        mode_button.config(text="English Mode", bg="gray", fg="white")
        status_var.set("Mode: English")
    on_text_change()

def copy_to_clipboard(event=None):
    output_text = output_box.get("1.0", tk.END).strip()
    if output_text:
        root.clipboard_clear()
        root.clipboard_append(output_text)
        messagebox.showinfo("Copied", "Tamil text copied to clipboard!")

def save_to_file(event=None):
    output_text = output_box.get("1.0", tk.END).strip()
    if not output_text:
        messagebox.showwarning("Empty", "No Tamil text to save!")
        return
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        messagebox.showinfo("Saved", f"File saved: {file_path}")

def clear_output(event=None):
    output_box.config(state="normal")
    output_box.delete("1.0", tk.END)
    output_box.config(state="disabled")
    status_var.set("Output cleared")

# ----------------------------
# Build Consonant Grid (8x3)
# ----------------------------
def create_consonant_grid(parent):
    row_colors = ["#e6ffe6", "#f0fff0", "#fff9e6"]
    row, col = 0, 0
    for idx, key in enumerate(tamil_consonants_ordered):
        value = tamil_consonants[key]
        fg_color = "darkred" if key in grantha_keys else "darkgreen"
        bg_color = row_colors[row]
        text = f"{key}\n{value}"
        lbl = tk.Label(
            parent, text=text,
            font=("Arial", 10), width=8, height=2,
            fg=fg_color, bg=bg_color,
            borderwidth=1, relief="ridge", justify="center"
        )
        lbl.grid(row=row, column=col, padx=2, pady=2)
        col += 1
        if col >= 8:
            col = 0
            row += 1

def create_grid(parent, mapping, fg_color, bg_color, cols):
    row, col = 0, 0
    for k, v in mapping.items():
        if isinstance(v, tuple):
            tam = v[0] + (" " + v[1] if v[1] else "")
        else:
            tam = v
        text = f"{k}\n{tam}"
        lbl = tk.Label(
            parent, text=text,
            font=("Arial", 10), width=10, height=2,
            fg=fg_color, bg=bg_color,
            borderwidth=1, relief="ridge", justify="center"
        )
        lbl.grid(row=row, column=col, padx=2, pady=2)
        col += 1
        if col >= cols:
            col = 0
            row += 1

# ----------------------------
# GUI Layout
# ----------------------------
root = tk.Tk()
root.title("CHAT GPT AI POWERED PHONETIC TUTOR")
root.geometry("900x800")
root.configure(bg="#f2f2f2")

# Title
tk.Label(
    root,
    text="CHAT GPT AI POWERED PHONETIC TUTOR",
    font=("Arial", 18, "bold"),
    fg="purple",
    bg="#f2f2f2"
).pack(pady=(15, 5))

# About
tk.Label(
    root,
    text="CHAT GPT AI POWERED PHONETIC TUTOR V.1.0\n"
         "Developed by gopalan.bhr@gmail.com with ChatGPT AI assistance",
    font=("Arial", 11, "italic"),
    fg="darkblue",
    bg="#f2f2f2",
    justify="center"
).pack(pady=(0, 15))

# Stage 1: Vowels
stage1_frame = tk.Frame(root, bg="#f2f2f2")
stage1_frame.pack(pady=5)
tk.Label(stage1_frame, text="Vowels + Plus", font=("Arial", 12, "bold"), fg="blue", bg="#f2f2f2").pack()
vowels_grid = tk.Frame(stage1_frame, bg="#f2f2f2")
vowels_grid.pack()
create_grid(vowels_grid, tamil_vowels, "blue", "#e6f0ff", cols=6)

# Stage 2: Consonants
consonants_frame = tk.Frame(root, bg="#f2f2f2")
consonants_frame.pack(pady=10)
tk.Label(consonants_frame, text="Consonants", font=("Arial", 12, "bold"), fg="darkgreen", bg="#f2f2f2").pack()
consonants_grid = tk.Frame(consonants_frame, bg="#f2f2f2")
consonants_grid.pack()
create_consonant_grid(consonants_grid)

# Mode + Action Buttons Row
tamil_mode = [True]
button_row = ttk.Frame(root)
button_row.pack(pady=10)

mode_button = tk.Button(
    button_row, text="Tamil Mode", command=toggle_mode,
    bg="green", fg="white", font=("Arial", 12, "bold"), width=12
)
mode_button.pack(side="left", padx=6)

tk.Button(button_row, text="Copy", command=copy_to_clipboard,
          bg="green", fg="white", width=10, font=("Arial", 10, "bold")).pack(side="left", padx=6)
tk.Button(button_row, text="Save", command=save_to_file,
          bg="blue", fg="white", width=10, font=("Arial", 10, "bold")).pack(side="left", padx=6)
tk.Button(button_row, text="Clear", command=clear_output,
          bg="red", fg="white", width=10, font=("Arial", 10, "bold")).pack(side="left", padx=6)

# Input
ttk.Label(root, text="Type in English (phonetic):", font=("Arial", 12), background="#f2f2f2").pack(pady=5)
input_box = tk.Text(root, font=("Arial", 14), wrap="word", height=5)
input_box.pack(fill="both", expand=True, padx=20, pady=5)
input_box.bind("<KeyRelease>", on_text_change)

# Output
ttk.Label(root, text="Tamil Output:", font=("Arial", 12), background="#f2f2f2").pack(pady=5)
output_box = tk.Text(root, font=("Arial", 14), wrap="word", height=6, state="disabled")
output_box.pack(fill="both", expand=True, padx=20, pady=5)

# Status Bar
status_var = tk.StringVar()
status_var.set("Mode: Tamil")
status_bar = tk.Label(root, textvariable=status_var, bd=1, relief="sunken", anchor="w", bg="#e6e6e6")
status_bar.pack(side="bottom", fill="x")

input_box.focus()
root.mainloop()
