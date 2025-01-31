from flask import Flask, render_template, request, send_file
import pandas as pd
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def calculator():
    results = []
    if request.method == 'POST':
        try:
            # Get user inputs
            initial_value = float(request.form['numeric_value'])
            iterations = int(request.form['iterations'])

            # Validate inputs
            if initial_value <= 0 or iterations <= 0:
                raise ValueError("Both Numeric Value and Iterations must be positive numbers.")

            # Perform compounding calculation
            current_value = initial_value
            for i in range(iterations):
                current_value *= 2  # Compound by 100%
                results.append({'Iteration': i + 1, 'Value': current_value})

            # Export to Excel if requested
            if 'export' in request.form:
                # Create a Pandas DataFrame from the results
                df = pd.DataFrame(results)
                
                # Write the DataFrame to an Excel file in memory
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False, sheet_name='Results')
                
                # Prepare the file for download
                output.seek(0)
                return send_file(
                    output,
                    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                    as_attachment=True,
                    download_name='compounding_results.xlsx'
                )

        except ValueError as e:
            return f"<h1>Error: {str(e)}</h1>"

    # Render the calculator page with results (if any)
    return render_template('index.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)