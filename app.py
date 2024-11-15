from flask import Flask, render_template, request, jsonify
from utils import get_suggestions
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/suggest')
def suggest():
    q = request.args.get('q', '')
    suggestions = get_suggestions(q)  # You need to implement this function to search your JSON file.
    return jsonify({"suggestions": suggestions})

@app.route('/get-coordinates', methods=['GET'])
def get_coordinates():
    airport_name = request.args.get('q')
    
    df = pd.read_csv('filtered_airports.csv')
    
    # Find the airport in the DataFrame
    print(airport_name)
    airport = df[df['name'] == airport_name].iloc[0]
    
    return jsonify({
        'latitude': airport['latitude'],
        'longitude': airport['longitude']
    })

if __name__ == '__main__':
    app.run()
