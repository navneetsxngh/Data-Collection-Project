import os
import csv
from flask import Flask, request, jsonify, render_template
from datetime import datetime

app = Flask(__name__)

# CSV Configuration
CSV_FILE = 'student_data.csv'
HEADERS = [
    'serial_id', 'full_name', 'phone', 'email', 
    'income', 'city', 'acquisition', 'gender', 
    'department', 'timestamp'
]

def save_to_csv(data_dict):
    file_exists = os.path.isfile(CSV_FILE)
    
    # Open in append mode ('a')
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        
        # Write header only if the file is being created for the first time
        if not file_exists:
            writer.writeheader()
            
        writer.writerow(data_dict)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.json
        
        # Map incoming JSON to CSV columns
        entry = {
            'serial_id': data.get('studentId'),
            'full_name': data.get('fullName'),
            'phone': data.get('phone'),
            'email': data.get('email'),
            'income': data.get('income'),
            'city': data.get('city'),
            'acquisition': data.get('acquisition'),
            'gender': data.get('gender'),
            'department': data.get('department'),
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        save_to_csv(entry)
        
        return jsonify({"status": "success", "message": "Record saved to CSV"}), 201
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)