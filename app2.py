# app.py
from flask import Flask, render_template, request, send_file
from openpyxl import Workbook
from io import BytesIO

app = Flask(__name__)

def calculate_compounded_values(initial, iterations):
    data = []
    for i in range(1, iterations + 1):
        value = initial * (2 ** i)
        data.append({'iteration': i, 'value': value})
    return data

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            initial = float(request.form['initial'])
            iterations = int(request.form['iterations'])
            data = calculate_compounded_values(initial, iterations)
            return render_template('calculator.html', 
                                 data=data,
                                 initial=initial,
                                 iterations=iterations)
        except ValueError:
            return render_template('calculator.html', error="Invalid input values")
    return render_template('calculator.html')

@app.route('/export', methods=['POST'])
def export():
    try:
        initial = float(request.form['initial'])
        iterations = int(request.form['iterations'])
        data = calculate_compounded_values(initial, iterations)
        
        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Compound Results"
        ws.append(['Iteration', 'Compounded Value'])
        
        for entry in data:
            ws.append([entry['iteration'], entry['value']])
        
        # Save workbook to bytes buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        
        return send_file(buffer,
                        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                        download_name='compound_results.xlsx',
                        as_attachment=True)
    except ValueError:
        return render_template('calculator.html', error="Invalid export values")

if __name__ == '__main__':
    app.run(debug=True)