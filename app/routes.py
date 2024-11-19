import sqlite3
from flask import render_template, request, redirect, url_for
from app import app
import main

@app.route('/', methods=['GET', 'POST'])
def index():
    db_path = main.get_db_path()
    printers = main.get_all_printers()
    selected_printer = request.form.get('printer') or request.args.get('printer')
    out_of_stock_toners = main.get_out_of_stock_toners()

    # Handle quantity update requests
    toner_name = request.form.get('toner_name')
    action = request.form.get('action')

    if toner_name and action:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()

            # Update quantity based on action
            if action == 'add':
                cursor.execute("UPDATE toner_table SET Toner_Qty = Toner_Qty + 1 WHERE Toner_Name = ?", (toner_name,))
            elif action == 'subtract':
                cursor.execute("UPDATE toner_table SET Toner_Qty = Toner_Qty - 1 WHERE Toner_Name = ? AND Toner_Qty > 0", (toner_name,))
            conn.commit()

        # Redirect to refresh the page, maintaining the selected printer view if one is selected
        if selected_printer:
            return redirect(url_for('index', printer=selected_printer))
        else:
            return redirect(url_for('index'))


    # Display toners based on selected printer
    if selected_printer:
        selected_toners, printer_ip, location = main.get_selected_toners(selected_printer)
        return render_template('index.html', toners=None, printers=printers, selected_toners=selected_toners, selected_printer=selected_printer, printer_ip=printer_ip, location=location, out_of_stock_toners=out_of_stock_toners)

    # Show all toners by default
    toners = main.get_all_toners()
    return render_template('index.html', toners=toners, printers=printers, selected_toners=None, selected_printer=None, printer_ip=None, location=None, out_of_stock_toners=out_of_stock_toners)


@app.route('/toner-details')
def toner_details():
    db_path = main.get_db_path()
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Toner_Name, Toner_Qty, Toner_Url_Single, Toner_Url_Double, Toner_Url_Multi FROM toner_table")
        toners = cursor.fetchall()
    return render_template('toner_details.html', toners=toners)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=3000)