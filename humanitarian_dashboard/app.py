from flask import Flask, render_template, send_file
import json
import pandas as pd
import folium

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
    # Functionality to generate and download PDF
    pass

def main():
    print("Hey! Welcome to the Humanitarian Dashboard!")

if __name__ == '__main__':
    main()
    app.run(debug=True)
