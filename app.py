import numpy as np
import pickle
from flask import Flask, request, render_template

#Consulted: https://github.com/memudualimatou/INSURANCE-CHARGES-WEB-APPLICATION/blob/main/app.py

app = Flask(__name__, template_folder='templates')
model = pickle.load(open("model.pkl", 'rb'))

@app.route('/')
def index():
    return render_template(
        'index.html',
        # Dictionaries for categorical data
        data1=[{'sex': 'Sex'}, {'sex': 'Female'}, {'sex': 'Male'}],
        data2=[{'bp': 'Blood Pressure'}, {'bp': 'High'}, {'bp': 'Low'}, {'bp': 'Normal'}],
        data3=[{'ch': 'Cholesterol'}, {'ch': 'High'}, {'ch': 'Normal'}],
    )

@app.route("/predict", methods=['GET', 'POST'])
def predict():
    input_data = list(request.form.values())

    if input_data[1] == 'Female':
        input_data[1] = 0
    elif input_data[1] == 'Male':
        input_data[1] = 1
    else:
        print(ValueError)

    if input_data[2] == 'High':
        input_data[2] = 0
    elif input_data[2] == 'Low':
        input_data[2] = 1
    elif input_data[2] == 'Normal':
        input_data[2] = 2
    else:
        print(ValueError)

    if input_data[3] == 'High':
        input_data[3] = 0
    elif input_data[3] == 'Normal':
        input_data[3] = 1
    else:
        print(ValueError)

    input_values = [x for x in input_data]
    arr_val = [np.array(input_values)]
    prediction = model.predict(arr_val)

    output = prediction[0]

    return render_template('index.html', prediction_text=" The predicted drug for the patient is {}".format(output),
                           data1=[{'sex': 'Sex'}, {'sex': 'Female'}, {'sex': 'Male'}],
                           data2=[{'bp': 'Blood Pressure'}, {'bp': 'High'}, {'bp': 'Low'}, {'bp': 'Normal'}],
                           data3=[{'ch': 'Cholesterol'}, {'ch': 'High'}, {'ch': 'Normal'}],
                           )

if __name__ == '__main__':
    app.run(debug=True)
