# Importing necessary modules for GUI, HTTP requests, and MySQL database connectivity.
import tkinter as tk  # Tkinter for GUI elements
from tkinter import ttk, messagebox  # Importing specific Tkinter components for styled widgets and message boxes
import requests  # Requests for handling HTTP requests to fetch currency data
import mysql.connector  # MySQL connector for managing MySQL connections
import pymysql  # PyMySQL to facilitate database connections

# Dictionary for storing currency names with their symbols for easy display in the GUI.
currency_names = {
    "AFN": "؋ Afghan Afghani",
    "ALL": "L Albanian Lek",
    "DZD": "د.ج Algerian Dinar",
    "EUR": "€ Euro",
    "AUD": "$ Australian Dollar",
    "AZN": "₼ Azerbaijani Manat",
    "BSD": "$ Bahamian Dollar",
    "BHD": "ب.د Bahraini Dinar",
    "BDT": "৳ Bangladeshi Taka",
    "BTN": "Nu. Bhutanese Ngultrum",
    "BRL": "R$ Brazilian Real",
    "BND": "$ Brunei Dollar",
    "CAD": "$ Canadian Dollar",
    "CVE": "$ Cape Verdean Escudo",
    "KHR": "៛ Cambodian Riel",
    "XAF": "Fr Central African CFA Franc",
    "CLP": "$ Chilean Peso",
    "CNY": "¥ Chinese Yuan Renminbi",
    "COP": "$ Colombian Peso",
    "CUP": "$ Cuban Peso",
    "CZK": "Kč Czech Koruna",
    "DOP": "$ Dominican Peso",
    "USD": "$ United States Dollar",
    "EGP": "£ Egyptian Pound",
    "ERN": "Nfk Eritrean Nakfa",
    "ETB": "Br Ethiopian Birr",
    "FJD": "$ Fijian Dollar",
    "FKP": "£ Falkland Islands Pound",
    "GMD": "D Gambian Dalasi",
    "GEL": "₾ Georgian Lari",
    "GHS": "₵ Ghanaian Cedi",
    "GIP": "£ Gibraltar Pound",
    "GTQ": "Q Guatemalan Quetzal",
    "GYD": "$ Guyanese Dollar",
    "HNL": "L Honduran Lempira",
    "HKD": "$ Hong Kong Dollar",
    "HUF": "Ft Hungarian Forint",
    "ISK": "kr Icelandic Króna",
    "INR": "₹ Indian Rupee",
    "IDR": "Rp Indonesian Rupiah",
    "IRR": "﷼ Iranian Rial",
    "IQD": "ع.د Iraqi Dinar",
    "ILS": "₪ Israeli New Shekel",
    "JMD": "$ Jamaican Dollar",
    "JPY": "¥ Japanese Yen",
    "JOD": "د.ا Jordanian Dinar",
    "KZT": "₸ Kazakhstani Tenge",
    "KES": "Sh Kenyan Shilling",
    "KPW": "₩ North Korean Won",
    "KRW": "₩ South Korean Won",
    "KWD": "د.ك Kuwaiti Dinar",
    "KGS": "лв Kyrgyzstani Som",
    "LAK": "₭ Lao Kip",
    "NOK": "kr Norwegian Krone",
    "OMR": "﷼ Omani Rial",
    "PKR": "₨ Pakistani Rupee",
    "PEN": "S/ Peruvian Sol",
    "PGK": "K Papua New Guinean Kina",
    "PHP": "₱ Philippine Peso",
    "PLN": "zł Polish Zloty",
    "QAR": "﷼ Qatari Rial",
    "RON": "lei Romanian Leu",
    "RUB": "₽ Russian Ruble",
    "RWF": "Fr Rwandan Franc",
    "SAR": "﷼ Saudi Riyal",
    "RSD": "дин Serbian Dinar",
    "SGD": "$ Singapore Dollar",
    "SBD": "$ Solomon Islands Dollar",
    "SOS": "Sh Somali Shilling",
    "ZAR": "R South African Rand",
    "LKR": "₨ Sri Lankan Rupee",
    "SEK": "kr Swedish Krona",
    "SYP": "£ Syrian Pound",
    "TJS": "ЅМ Tajikistani Somoni",
    "TZS": "Sh Tanzanian Shilling",
    "THB": "฿ Thai Baht",
    "TOP": "T$ Tongan Paʻanga",
    "TTD": "$ Trinidad and Tobago Dollar",
    "TND": "د.ت Tunisian Dinar",
    "TRY": "₺ Turkish Lira",
    "TMT": "m Turkmenistani Manat",
    "UGX": "Sh Ugandan Shilling",
    "UAH": "₴ Ukrainian Hryvnia",
    "AED": "د.إ United Arab Emirates Dirham",
    "GBP": "£ British Pound Sterling",
}

# Function to establish a connection to the database.
def connect_db():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="Timepatrol1531",
        database="pti"
    )

# Function to save the selected conversion to the database.
def save_conversion():
    from_currency = from_currency_combo.get().split(" - ")[0]
    to_currency = to_currency_combo.get().split(" - ")[0]

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO saved_conversion (base_currency, target_currency) VALUES (%s, %s)", (from_currency, to_currency))
        db.commit()
        messagebox.showinfo("Success", "Conversion saved successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        db.close()

# Function to fetch all saved conversions from the database.
def fetch_saved_conversions():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT base_currency, target_currency FROM saved_conversion")
        conversions = cursor.fetchall()
        db.close()
        return [f"{base} to {target}" for base, target in conversions]
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        return []

# Function to delete the selected conversion from the database.
def delete_conversion(conversion):
    if not conversion:
        messagebox.showerror("Selection Error", "Please select a conversion to delete.")
        return

    from_currency_code, to_currency_code = conversion.split(" to ")

    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM saved_conversion WHERE base_currency = %s AND target_currency = %s", (from_currency_code, to_currency_code))
        db.commit()
        messagebox.showinfo("Success", "Selected conversion deleted successfully.")
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
    finally:
        db.close()

    saved_window.destroy()
    display_saved_conversions(fetch_saved_conversions())

# Function to display saved conversions in a new window.
def display_saved_conversions(conversions):
    global saved_window
    saved_window = tk.Toplevel(root)
    saved_window.title("Saved Conversions")
    saved_window.configure(bg="DarkOrange4")

    listbox = tk.Listbox(saved_window, font=("Algerian", 14))
    for conversion in conversions:
        listbox.insert(tk.END, conversion)
    listbox.pack(padx=20, pady=20)

    apply_button = tk.Button(saved_window, text="Apply Selected Conversion", command=lambda: set_conversion(listbox.get(tk.ACTIVE)))
    apply_button.pack(pady=10)

    delete_button = tk.Button(saved_window, text="Delete Selected Conversion", command=lambda: delete_conversion(listbox.get(tk.ACTIVE)))
    delete_button.pack(pady=10)

# Function to fetch currency data from the API.
def fetch_currencies():
    try:
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        currencies = list(data['rates'].keys())
        return [f"{code} - {currency_names[code]}" for code in currencies if code in currency_names]
    except requests.exceptions.RequestException:
        messagebox.showerror("Connection Error", "Failed to retrieve currency data.")
        return []

# Global list to track the last 10 conversions.
recent_conversions = []

# Function to update the conversion result based on user input and selected currencies.
def update_conversion():
    from_currency = from_currency_combo.get().split(" - ")[0]
    to_currency = to_currency_combo.get().split(" - ")[0]

    try:
        amount = float(amount_entry.get())  # Get the amount entered by the user and convert it to float.
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for the amount.")  # Handle invalid input.
        return

    try:
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")  # Fetch conversion rate.
        response.raise_for_status()
        data = response.json()

        if to_currency in data['rates']:  # Check if the target currency is available in the response.
            rate = data['rates'][to_currency]
            converted_amount = amount * rate  # Convert the amount based on the fetched rate.
            result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")  # Display the result.

            recent_conversions.append(f"{amount} {from_currency} to {converted_amount:.2f} {to_currency}")  # Store conversion in history.
            if len(recent_conversions) > 10:
                recent_conversions.pop(0)  # Keep only the last 10 conversions.
        else:
            messagebox.showerror("Conversion Error", f"Conversion rate for {to_currency} not available.")  # Handle missing rate.
    except requests.exceptions.HTTPError as http_err:
        messagebox.showerror("HTTP Error", f"HTTP error occurred: {http_err}")  # Handle HTTP errors.
    except requests.exceptions.RequestException:
        messagebox.showerror("Connection Error", "Failed to fetch conversion rate.")  # Handle connection errors.

# Function to display the last 10 conversion history in a new window.
def show_conversion_history():
    history_window = tk.Toplevel(root)  # Create a new window.
    history_window.title("Conversion History")
    history_window.configure(bg="DarkOrange4")
    history_window.geometry("600x400")

    tk.Label(history_window, text="Last 10 Conversions", font=("Algerian", 14), bg="DarkOrange4").pack(pady=10)

    listbox = tk.Listbox(history_window, font=("Arial", 12), height=15, width=50)
    for conversion in recent_conversions:
        listbox.insert(tk.END, conversion)  # Display each conversion in the listbox.
    listbox.pack(padx=20, pady=20, fill="both", expand=True)

# Function to swap the selected currencies in the combo boxes.
def switch_currencies():
    from_currency = from_currency_combo.get()  # Get the selected currencies.
    to_currency = to_currency_combo.get()
    from_currency_combo.set(to_currency)  # Swap the values.
    to_currency_combo.set(from_currency)

# Function to set the selected conversion in the combo boxes based on the history.
def set_conversion(conversion):
    from_currency_code, to_currency_code = conversion.split(" to ")
    from_currency_full = currency_names[from_currency_code]
    to_currency_full = currency_names[to_currency_code]

    from_currency_combo.set(f"{from_currency_code} - {from_currency_full}")  # Set the combo boxes to the selected conversion.
    to_currency_combo.set(f"{to_currency_code} - {to_currency_full}")

# Initialize the Tkinter window and set its properties.
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()  # Main window for the application.
root.title("Currency Converter")
root.geometry("1500x700")

# List of popular conversions for quick access in the sidebar.
popular_conversion = [
    "USD to INR", "USD to EUR", "USD to GBP", "EUR to INR",
    "USD to JPY", "USD to AUD", "USD to CAD", "USD to CNY",
    "EUR to GBP", "EUR to JPY", "GBP to JPY"
]

# Sidebar section at the bottom of the window to display popular conversions.
sidebar_bottom = tk.Frame(root, width=120, bg="saddle brown")
sidebar_bottom.pack(side="bottom", fill="x")
sidebar_title = tk.Label(sidebar_bottom, text="Popular Conversion", bg="LightYellow4", font=("Algerian", 16, "bold"), fg="black")
sidebar_title.pack(side="left", padx=10)

# Add buttons for each popular conversion.
for conversion in popular_conversion:
    button = tk.Button(sidebar_bottom, text=conversion, bg="gold", font=("Algerian", 10),
                       command=lambda c=conversion: set_conversion(c))  # Set conversion when button clicked.
    button.pack(side="left", padx=5)

# Set the background image for the main window.
bg_image = Image.open(r"img/bkg.jpg") # Replace with your image path
bg_image = bg_image.resize((1500, 700), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(root, width=1500, height=700)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Add title label to the canvas.
center_x = 750
center_y = 350
title_label = tk.Label(root, text="Real-Time Currency Converter", font=("Algerian", 24, "bold"), bg="saddle brown")
canvas.create_window(center_x, 40, window=title_label)

# Create frames for the amount entry and result label.
f1 = tk.Frame(root, bg="#082357")
canvas.create_window(center_x, 120, window=f1)
result_label = tk.Label(f1, text="Result will be shown here", font=("Algerian", 20, "bold"), bg="saddle brown", fg="black")
result_label.pack(pady=10)

# Create input field for the amount.
amount_label = tk.Label(root, text="Enter Amount:", font=("Algerian", 18, "bold"), bg="saddle brown")
canvas.create_window(center_x, 220, window=amount_label)

amount_entry = tk.Entry(root, bg="goldenrod", font=("Times New Roman", 16))
canvas.create_window(center_x, 255, window=amount_entry)

# Frame for the currency combo boxes.
f2 = tk.Frame(root, borderwidth=3, bg="DarkOrange4")
canvas.create_window(center_x, 350, window=f2)

# Fetch available currencies and populate the combo boxes.
currencies = fetch_currencies()
from_currency_combo = ttk.Combobox(f2, values=currencies, font=("Times New Roman", 14))
from_currency_combo.set("USD - United States Dollar")
from_currency_combo.pack(pady=10, padx=20)

# Button to switch the selected currencies.
switch_button = tk.Button(f2, text="🔁", command=switch_currencies, font=("Times New Roman", 16), bg="LightYellow4")
switch_button.pack()

to_currency_combo = ttk.Combobox(f2, values=currencies, font=("Times New Roman", 14))
to_currency_combo.set("INR - Indian Rupee")
to_currency_combo.pack(pady=10, padx=20)

# Button to perform the conversion.
convert_button = tk.Button(root, text="Convert", font=("Algerian", 16, "bold"), command=update_conversion, width=20, bg="saddle brown", fg="black")
canvas.create_window(center_x, 460, window=convert_button)

# Create options menu with save and view commands.
options_menu_button = tk.Menubutton(root, text="Options", relief="raised", font=("Algerian", 14, "bold"), bg="#8B0000", fg="black")
canvas.create_window(center_x, 510, window=options_menu_button)

conversion_menu = tk.Menu(options_menu_button, tearoff=0)
options_menu_button.config(menu=conversion_menu)

conversion_menu.add_command(label="Save Conversion", font=("Impact", 10), command=save_conversion)
conversion_menu.add_command(label="View Saved Conversions", font=("Impact", 10), command=lambda: display_saved_conversions(fetch_saved_conversions()))

# Create history menu to view the last 10 conversions.
menubar = tk.Menu(root)
root.config(menu=menubar)

history_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="History", menu=history_menu)
history_menu.add_command(label="View Last 10 Conversions", font=("Impact", 10), command=show_conversion_history)

# Start the Tkinter main loop.
root.mainloop()
