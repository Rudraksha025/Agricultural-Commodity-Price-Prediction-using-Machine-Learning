from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)


# Load the saved Random Forest model
loaded_model = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/random_forest_model.joblib')

# Load the mapping dictionaries
loaded_commodity_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/commodity_mapping.joblib')

loaded_district_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/District_mapping.joblib')

loaded_market_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/Market_mapping.joblib')

loaded_variety_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/Variety_mapping.joblib')

loaded_month_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/Month_mapping.joblib')

loaded_day_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/Day_mapping.joblib')

loaded_season_mapping = joblib.load('C:/Users/rudra/OneDrive/Desktop/RUNU_PROJECT/Code/Season_mapping.joblib')


def get_season(month):
    if month in ['April', 'May', 'June']:
        return 'Rabi'
    elif month in ['September', 'October', 'November']:
        return 'Kharif'
    return 'Other'

def predict_price(district_name, market_name, commodity, variety, month, day, season):
    # ... (your predict_price function) ...
    user_input = pd.DataFrame({
        'District Name': [district_name],
        'Market Name': [market_name],
        'Commodity': [commodity],
        'Variety': [variety],
        'Month': [month],
        'Day': [day],
        'Season': [season]
    })
    user_input['District Name'] = user_input['District Name'].map(loaded_district_mapping)
    user_input['Market Name'] = user_input['Market Name'].map(loaded_market_mapping)
    user_input['Commodity'] = user_input['Commodity'].map(loaded_commodity_mapping)
    user_input['Variety'] = user_input['Variety'].map(loaded_variety_mapping)
    user_input['Month'] = user_input['Month'].map(loaded_month_mapping)
    user_input['Day'] = user_input['Day'].map(loaded_day_mapping)
    user_input['Season'] = user_input['Season'].map(loaded_season_mapping)
    user_input = user_input.fillna(-1)
    predicted_price = loaded_model.predict(user_input)[0]
    return predicted_price

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        district = request.form['district']
        market = request.form['market']
        commodity = request.form['commodity']
        variety = request.form['variety']
        date_str = request.form['date']

        try:
            date_obj = pd.to_datetime(date_str)
            month = date_obj.strftime('%B')
            day = date_obj.strftime('%d')
            season = get_season(month)

            if season is None:
                return render_template('index.html', error="Could not determine season.")

            prediction = predict_price(district, market, commodity, variety, month, day, season)

            # Determine the image filename based on the commodity
            commodity_image = None
            if commodity == "Bajra(Pearl Millet/Cumbu)":
                commodity_image = "bajra.jpg"
            elif commodity == "Barley (Jau)":
                commodity_image = "jau1.jpg"
            elif commodity == "Groundnut":
                commodity_image = "groundnut1.jpg"
            elif commodity == "Guar":
                commodity_image = "guar.jpg"
            elif commodity == "Onion":
                commodity_image = "onion2.jpg"
            elif commodity == "Potato":
                commodity_image = "potato5.jpg"
            elif commodity == "Soyabean":
                commodity_image = "soya2.jpg"
            elif commodity == "Tomato":
                commodity_image = "tomato4.jpg"
            # Add more conditions for other commodities

            return render_template('result.html', 
                                   prediction=f'Rs. {prediction:.2f}', 
                                   district=district,
                                   market=market,
                                   commodity=commodity,
                                   variety=variety,
                                   date=date_str,
                                   commodity_image=commodity_image)

        except ValueError:
            return render_template('index.html', error="Invalid date format. Please use YYYY-MM-DD.")

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)