from flask import Flask, render_template, request
import pickle

app = Flask(__name__, template_folder='templates')

dct_of_cities_in_order = {
    'Avon': 0, 'Berlin': 0, 'Bethel': 0, 'Branford': 0,
    'Bridgeport': 0, 'Bristol': 0, 'Cheshire': 0, 'Danbury': 0,
    'Darien': 0, 'East Hartford': 0, 'East Haven': 0,
    'East Lyme': 0, 'Enfield': 0, 'Fairfield': 0, 'Farmington': 0,
    'Glastonbury': 0, 'Greenwich': 0, 'Groton': 0, 'Guilford': 0,
    'Hamden': 0, 'Hartford': 0, 'Killingly': 0, 'Madison': 0,
    'Manchester': 0, 'Meriden': 0, 'Middletown': 0, 'Milford': 0,
    'Monroe': 0, 'Naugatuck': 0, 'New Britain': 0, 'New Canaan': 0,
    'New Haven': 0, 'New London': 0, 'New Milford': 0,
    'Newington': 0, 'Newtown': 0, 'North Haven': 0, 'Norwalk': 0,
    'Norwich': 0, 'Ridgefield': 0, 'elton': 0, 'Simsbury': 0,
    'South Windsor': 0, 'Southbury': 0, 'Southington': 0,
    'Stamford': 0, 'Stonington': 0, 'Stratford': 0, 'Torrington': 0,
    'Trumbull': 0, 'Vernon': 0, 'Wallingford': 0, 'Waterbury': 0,
    'Waterford': 0, 'West Hartford': 0, 'West Haven': 0,
 'Westport': 0, 'Wethersfield': 0, 'Windsor': 0
}

dct_of_p_type_in_order = {
    'Condo': 0, 'Four Family': 0,
    'Residential': 0, 'Single Family': 0,
    'Three Family': 0, 'Two Family': 0
}

dct_of_r_type_in_order = {
    'Condo': 0, 'Four Family': 0,
    'Single Family': 0, 'Three Family': 0,
    'Two Family': 0
}

def update_dict(key, dct):
    if key in dct:
        dct[key] = 1

def get_prediction(form_data):
    listYear = int(form_data['listYear'])
    yearRecorded = int(form_data['yearRecorded'])
    assessedValue = int(form_data['assessedValue'])
    salesRatio = float(form_data['salesRatio'])
    town = form_data['town']
    propertyType = form_data['propertyType']
    residentialType = form_data['residentialType']
    update_dict(town, dct_of_cities_in_order)
    update_dict(propertyType, dct_of_p_type_in_order)
    update_dict(residentialType, dct_of_r_type_in_order)

    with open('site\model.pkl', 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([[
        listYear, yearRecorded, assessedValue, salesRatio,
        *dct_of_cities_in_order.values(),
        *dct_of_p_type_in_order.values(),
        *dct_of_r_type_in_order.values()
    ]])

    return prediction[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    prediction = get_prediction(request.form)
    return render_template('/index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
