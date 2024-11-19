import sqlite3
import os
import sys

# Function to get the path to the database file
def get_db_path():
    return os.path.join(os.getcwd(), 'toner_stock.db')


# Function to get all toners
def get_all_toners():
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Toner_Name, Toner_Qty FROM toner_table ORDER BY Toner_Name ASC")
        toners = cursor.fetchall()
    return toners


# Function to get selected toners and printer details by printer name
def get_selected_toners(printer_name):
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Printer_ID, Printer_Model, Printer_IP, Printer_Location, Toner_ID_Black, Toner_ID_Yellow, Toner_ID_Cyan, Toner_ID_Magenta
            FROM printer_table
            WHERE Printer_Name = ?
        """, (printer_name,))
        printer = cursor.fetchone()

        selected_toners = []
        printer_ip = None
        location = None
        if printer:
            printer_ip = printer[2]  # Printer_IP
            location = printer[3]    # Location
            toner_ids = [printer[4], printer[5], printer[6], printer[7]]
            for toner_id in toner_ids:
                if toner_id:
                    cursor.execute("SELECT Toner_Name, Toner_Qty FROM toner_table WHERE Toner_ID = ?", (toner_id,))
                    toner = cursor.fetchone()
                    if toner:
                        selected_toners.append(toner)
    return selected_toners, printer_ip, location



# Function to get all printers
def get_all_printers():
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Printer_Name, Printer_Model FROM printer_table ORDER BY Printer_Name ASC")
        printers = cursor.fetchall()
    return printers


# Function to get out-of-stock toners
def get_out_of_stock_toners():
    db_path = get_db_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Toner_Name FROM toner_table WHERE Toner_Qty = 0")
        out_of_stock_toners = cursor.fetchall()
    return [toner[0] for toner in out_of_stock_toners]