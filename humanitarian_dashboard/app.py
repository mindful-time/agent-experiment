from flask import Flask, render_template, send_file
import json
import pandas as pd
import folium
from weasyprint import HTML

app = Flask(__name__)

# Load extracted data
with open('data/extracted_data.json') as f:
    data = json.load(f)

@app.route('/')
def index():
    # Prepare data for visualization
    return render_template('index.html', data=data)

@app.route('/download')
def download_pdf():
    # Render the HTML template to a string
    rendered = render_template('index.html', data=data)
    # Convert the HTML to PDF
    pdf = HTML(string=rendered).write_pdf()
    # Send the PDF as a response
    return send_file(
        pdf,
        as_attachment=True,
        download_name='humanitarian_dashboard.pdf',
        mimetype='application/pdf'
    )

def main():
    print("Hey! Welcome to the Humanitarian Dashboard!")

if __name__ == '__main__':
    main()
    app.run(debug=True)
