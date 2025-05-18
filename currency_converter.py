
import tkinter as tk
from tkinter import ttk, messagebox

# Exchange rates
usd_rates = {
    "USD": 1.0, "INR": 83.50, "EUR": 0.92, "GBP": 0.80, "JPY": 134.50,
    "CHF": 0.91, "CAD": 1.34, "AUD": 1.50, "NZD": 1.63, "ZAR": 18.70,
    "CNY": 7.15, "SGD": 1.35, "MXN": 17.70, "SEK": 10.20, "NOK": 10.60,
    "BRL": 5.15, "RUB": 90.00, "TRY": 26.0
}

conversion_history = []

def get_exchange_rate(base_currency, target_currency):
    if base_currency not in usd_rates or target_currency not in usd_rates:
        return None
    return (1 / usd_rates[base_currency]) * usd_rates[target_currency]

def convert_currency():
    base_currency = base_currency_var.get()
    target_currency = target_currency_var.get()
    amount = amount_entry.get()
    try:
        amount = float(amount)
        if amount < 0:
            raise ValueError
    except ValueError:
        original_value_label.config(text="")
        result_value_label.config(text="Enter a valid amount.")
        return

    exchange_rate = get_exchange_rate(base_currency, target_currency)
    decimals = int(decimal_precision.get())
    if exchange_rate is not None:
        converted = amount * exchange_rate
        original_value_label.config(text=f"{amount:.{decimals}f} {base_currency}")
        result_value_label.config(text=f"{converted:.{decimals}f} {target_currency}")
        entry = f"{amount:.{decimals}f} {base_currency} → {converted:.{decimals}f} {target_currency}"
        if not conversion_history or conversion_history[-1] != entry:
            conversion_history.append(entry)
            update_history()
    else:
        original_value_label.config(text="")
        result_value_label.config(text="Conversion failed.")

def update_history():
    history_listbox.delete(0, tk.END)
    for item in conversion_history[-5:][::-1]:
        history_listbox.insert(tk.END, item)

def toggle_theme():
    global is_dark
    is_dark = not is_dark
    apply_theme(dark_theme if is_dark else light_theme)

def apply_theme(theme):
    root.configure(bg=theme["bg"])
    container.configure(bg=theme["bg"], highlightbackground=theme["border"])
    for widget in theme_widgets:
        if isinstance(widget, (tk.Label, tk.Button, tk.Listbox)):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, (tk.Frame, tk.LabelFrame)):
            widget.configure(bg=theme["bg"])
    convert_btn.configure(bg=theme["accent"], fg=theme["button_fg"])
    theme_btn.configure(bg=theme["accent"], fg=theme["button_fg"])
    history_listbox.configure(selectbackground=theme["accent"], selectforeground=theme["button_fg"])

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TCombobox", fieldbackground=theme["combo_bg"], background=theme["combo_bg"], foreground=theme["fg"])

def auto_refresh():
    convert_currency()
    root.after(2000, auto_refresh)  # refresh every 2 seconds

# GUI Setup
root = tk.Tk()
root.title("Currency Converter")
root.geometry("750x420")
is_dark = False

light_theme = {
    "bg": "#f0f8ff", "fg": "#000000", "accent": "#1976d2",
    "button_fg": "#ffffff", "border": "#aaaaaa", "combo_bg": "#ffffff"
}
dark_theme = {
    "bg": "#2e3440", "fg": "#eceff4", "accent": "#88c0d0",
    "button_fg": "#2e3440", "border": "#4c566a", "combo_bg": "#3b4252"
}

currency_codes = sorted(usd_rates.keys())

container = tk.Frame(root, bg="#f0f8ff", bd=2, relief="groove")
container.place(relx=0.5, rely=0.5, anchor="center", width=700, height=390)

header_label = tk.Label(container, text="💱 Currency Converter", font=("Segoe UI", 20, "bold"), bg="#f0f8ff")
header_label.pack(pady=(15, 10))

form_frame = tk.Frame(container, bg="#f0f8ff")
form_frame.pack()

tk.Label(form_frame, text="Amount:", font=("Segoe UI", 12), bg="#f0f8ff").grid(row=0, column=0, padx=8, pady=5, sticky="e")
amount_entry = tk.Entry(form_frame, font=("Segoe UI", 12), width=15)
amount_entry.grid(row=0, column=1, padx=8, pady=5)

tk.Label(form_frame, text="From:", font=("Segoe UI", 12), bg="#f0f8ff").grid(row=1, column=0, padx=8, pady=5, sticky="e")
base_currency_var = tk.StringVar(value="USD")
base_currency_menu = ttk.Combobox(form_frame, textvariable=base_currency_var, values=currency_codes, state="readonly", width=12)
base_currency_menu.grid(row=1, column=1, padx=8, pady=5)

tk.Label(form_frame, text="To:", font=("Segoe UI", 12), bg="#f0f8ff").grid(row=2, column=0, padx=8, pady=5, sticky="e")
target_currency_var = tk.StringVar(value="INR")
target_currency_menu = ttk.Combobox(form_frame, textvariable=target_currency_var, values=currency_codes, state="readonly", width=12)
target_currency_menu.grid(row=2, column=1, padx=8, pady=5)

tk.Label(form_frame, text="Decimals:", font=("Segoe UI", 12), bg="#f0f8ff").grid(row=3, column=0, padx=8, pady=5, sticky="e")
decimal_precision = tk.StringVar(value="2")
decimal_menu = ttk.Combobox(form_frame, textvariable=decimal_precision, values=["0", "1", "2", "3", "4"], state="readonly", width=5)
decimal_menu.grid(row=3, column=1, padx=8, pady=5)

convert_btn = tk.Button(container, text="Convert 💹", command=convert_currency, font=("Segoe UI", 12, "bold"), padx=10, pady=5)
convert_btn.pack(pady=(10, 5))

result_frame = tk.Frame(container, bg="#f0f8ff")
result_frame.pack()
original_value_label = tk.Label(result_frame, text="", font=("Segoe UI", 12), bg="#f0f8ff")
original_value_label.pack()
result_value_label = tk.Label(result_frame, text="", font=("Segoe UI", 16, "bold"), bg="#f0f8ff", fg="#388e3c")
result_value_label.pack()

theme_btn = tk.Button(container, text="Toggle Theme 🎨", command=toggle_theme, font=("Segoe UI", 10))
theme_btn.pack(pady=5)

history_frame = tk.LabelFrame(container, text="Recent Conversions", font=("Segoe UI", 10, "bold"), bg="#f0f8ff")
history_frame.pack(pady=5)
history_listbox = tk.Listbox(history_frame, width=60, height=5)
history_listbox.pack()

theme_widgets = [
    container, header_label, form_frame, original_value_label,
    result_value_label, theme_btn, history_frame, history_listbox
]

apply_theme(light_theme)
auto_refresh()

root.mainloop()
