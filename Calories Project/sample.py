import requests
import json
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import openpyxl
from openpyxl import Workbook, load_workbook
from datetime import datetime

app = Flask(__name__)
book = load_workbook('FoodTracker.xlsx')
sheet = book.active
#print(sheet['A1'].value)
#book.save('Food_Tracker.xlsx')
#sheet.append(data)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/addFood/<query>/<float:serving_size>', methods=['POST'])
def add_food(query, serving_size):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': '3AbZ8I219IopLDx85grrcQ==bTiIx38uJXM8Te1o'})
    data = response.json()
    #Get the name and all the information
    name = data[0]["name"]
    serving_g = float(data[0]["serving_size_g"])
    protein = float(data[0]["protein_g"]) * serving_size/serving_g
    fat = float(data[0]["fat_total_g"]) * serving_size/serving_g
    carbohydrates = float(data[0]["carbohydrates_total_g"]) * serving_size/serving_g
    calories = float(data[0]["calories"]) * serving_size/serving_g 
    current_date = datetime.now()
    formatted_date = current_date.strftime("%d-%m-%Y")

    sheet.append([name, formatted_date, serving_size, protein, fat, carbohydrates, calories])
    print("Data has been appended")
    book.save('FoodTracker.xlsx')
    return data

@app.route('/getFood/<query>', methods=['GET'])
def get_food(query):
    api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
    response = requests.get(api_url, headers={'X-Api-Key': '3AbZ8I219IopLDx85grrcQ==bTiIx38uJXM8Te1o'})
    data = response.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)