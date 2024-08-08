# from flask import Flask, request, jsonify, render_template
# import numpy as np
# import pickle
# from datetime import datetime

# app = Flask(__name__)

# # Load the trained model
# try:
#     with open('EnergyPredictor.pkl', 'rb') as file:
#         model = pickle.load(file)
# except (FileNotFoundError, pickle.UnpicklingError) as e:
#     app.logger.error(f"Error loading model: {e}")
#     model = None
# form_to_feature = {
#         'Lighting': 'lights',
#         'Kitchen_temp': 'T1',
#         'Kitchen_Humidity': 'RH_1',
#         'Livingroom_temp': 'T2',
#         'Livingroom_Humidity': 'RH_2',
#         'Laundryroom_temp': 'T3',
#         'Laundryroom_Humidity': 'RH_3',
#         'Officeroom_temp': 'T4',
#         'Officeroom_Humidity': 'RH_4',
#         'Bathroom_temp': 'T5',
#         'Bathroom_Humidity': 'RH_5',
#         'Corridor_temp': 'T6',
#         'Corridor_Humidity': 'RH_6',
#         'Ironingroom_temp': 'T7',
#         'Ironingroom_Humidity': 'RH_7',
#         'Childrenroom_temp': 'T8',
#         'Childrenroom_Humidity': 'RH_8',
#         'Parentroom_temp': 'T9',
#         'Parentroom_Humidity': 'RH_9',
#         'Weatherstation_temp': 'T_out',
#         'Weatherstation_mmhg': 'Press_mm_hg',
#         'Weatherstation_Humidity': 'RH_out',
#         'Weatherstation_windspeed': 'Windspeed',
#         'Weatherstation_dewpoint': 'Tdewpoint',
#         'Time_24hrs': 'hour',
#         'Day_ofthe_week': 'weekday'
#     }
# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded'}), 500

#     app.logger.debug(f"Received form data: {request.form}")

#     # Mapping from form fields to model input features
#     form_to_feature = {
#         'Lighting': 'lights',
#         'Kitchen_temp': 'T1',
#         'Kitchen_Humidity': 'RH_1',
#         'Livingroom_temp': 'T2',
#         'Livingroom_Humidity': 'RH_2',
#         'Laundryroom_temp': 'T3',
#         'Laundryroom_Humidity': 'RH_3',
#         'Officeroom_temp': 'T4',
#         'Officeroom_Humidity': 'RH_4',
#         'Bathroom_temp': 'T5',
#         'Bathroom_Humidity': 'RH_5',
#         'Corridor_temp': 'T6',
#         'Corridor_Humidity': 'RH_6',
#         'Ironingroom_temp': 'T7',
#         'Ironingroom_Humidity': 'RH_7',
#         'Childrenroom_temp': 'T8',
#         'Childrenroom_Humidity': 'RH_8',
#         'Parentroom_temp': 'T9',
#         'Parentroom_Humidity': 'RH_9',
#         'Weatherstation_temp': 'T_out',
#         'Weatherstation_mmhg': 'Press_mm_hg',
#         'Weatherstation_Humidity': 'RH_out',
#         'Weatherstation_windspeed': 'Windspeed',
#         'Weatherstation_dewpoint': 'Tdewpoint',
#         'Time_24hrs': 'hour',
#         'Day_ofthe_week': 'weekday'
#     }

#     input_data = []
#     missing_fields = []
#     form_data = {}

#     # Extract and validate input data from the form
#     for form_field, feature in form_to_feature.items():
#         value = request.form.get(form_field)
#         form_data[form_field] = value
#         if value is None or value.strip() == '':
#             missing_fields.append(form_field)
#             continue

#         try:
#             if feature in ['hour', 'weekday']:
#                 value = int(value)
#             else:
#                 value = float(value)
#             input_data.append(value)
#         except ValueError:
#             app.logger.error(f"Invalid value for {form_field}: {value}")
#             return jsonify({'error': f'Invalid value for {form_field}'}), 400

#     if missing_fields:
#         return jsonify({'error': f'Missing parameters: {", ".join(missing_fields)}'}), 400

#     # Add current month as it's not included in the form
#     input_data.append(datetime.now().month)

#     app.logger.debug(f"Processed input data: {input_data}")

#     # Make prediction
#     try:
#         prediction = model['Model'].predict([input_data])[0]
#     except Exception as e:
#         app.logger.error(f"Prediction error: {e}")
#         return jsonify({'error': f'Error making prediction: {e}'}), 500

#     # Prepare response
#     response = {
#         'prediction': float(np.round(prediction, 2)),
#         'text': f'Predicted Energy Consumption: {np.round(prediction, 2)} Wh',
#         **form_data
#     }

#     return jsonify(response)
# @app.route('/api/predict', methods=['POST'])
# def api_predict():
#     if model is None:
#         return jsonify({'error': 'Model not loaded'}), 500

#     data = request.json
#     if not data:
#         return jsonify({'error': 'No input data provided'}), 400

#     form_to_feature = {
#         'Lighting': 'lights',
#         'Kitchen_temp': 'T1',
#         'Kitchen_Humidity': 'RH_1',
#         'Livingroom_temp': 'T2',
#         'Livingroom_Humidity': 'RH_2',
#         'Laundryroom_temp': 'T3',
#         'Laundryroom_Humidity': 'RH_3',
#         'Officeroom_temp': 'T4',
#         'Officeroom_Humidity': 'RH_4',
#         'Bathroom_temp': 'T5',
#         'Bathroom_Humidity': 'RH_5',
#         'Corridor_temp': 'T6',
#         'Corridor_Humidity': 'RH_6',
#         'Ironingroom_temp': 'T7',
#         'Ironingroom_Humidity': 'RH_7',
#         'Childrenroom_temp': 'T8',
#         'Childrenroom_Humidity': 'RH_8',
#         'Parentroom_temp': 'T9',
#         'Parentroom_Humidity': 'RH_9',
#         'Weatherstation_temp': 'T_out',
#         'Weatherstation_mmhg': 'Press_mm_hg',
#         'Weatherstation_Humidity': 'RH_out',
#         'Weatherstation_windspeed': 'Windspeed',
#         'Weatherstation_dewpoint': 'Tdewpoint',
#         'Time_24hrs': 'hour',
#         'Day_ofthe_week': 'weekday'
#     }

#     input_data = []
#     missing_fields = []

#     for form_field, feature in form_to_feature.items():
#         value = data.get(form_field)
#         if value is None:
#             missing_fields.append(form_field)
#             continue

#         try:
#             if feature in ['hour', 'weekday']:
#                 value = int(value)
#             else:
#                 value = float(value)
#             input_data.append(value)
#         except ValueError:
#             return jsonify({'error': f'Invalid value for {form_field}'}), 400

#     if missing_fields:
#         return jsonify({'error': f'Missing parameters: {", ".join(missing_fields)}'}), 400

#     # Add current month as it's not included in the input data
#     input_data.append(datetime.now().month)

#     # Make prediction
#     try:
#         prediction = model['Model'].predict([input_data])[0]
#     except Exception as e:
#         app.logger.error(f"API prediction error: {e}")
#         return jsonify({'error': f'Error making prediction: {e}'}), 500

#     # Prepare response
#     response = {
#         'prediction': float(np.round(prediction, 2)),
#         'text': f'Predicted Energy Consumption: {np.round(prediction, 2)} Wh'
#     }

#     return jsonify(response)

# if __name__ == '__main__':
#     app.run(debug=True)


# app.py

from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

# In-memory storage for predictions
predictions_storage = defaultdict(list)

# Load the trained model
try:
    with open('EnergyPredictor.pkl', 'rb') as file:
        model = pickle.load(file)
except (FileNotFoundError, pickle.UnpicklingError) as e:
    app.logger.error(f"Error loading model: {e}")
    model = None

form_to_feature = {
    'Lighting': 'lights',
    'Kitchen_temp': 'T1',
    'Kitchen_Humidity': 'RH_1',
    'Livingroom_temp': 'T2',
    'Livingroom_Humidity': 'RH_2',
    'Laundryroom_temp': 'T3',
    'Laundryroom_Humidity': 'RH_3',
    'Officeroom_temp': 'T4',
    'Officeroom_Humidity': 'RH_4',
    'Bathroom_temp': 'T5',
    'Bathroom_Humidity': 'RH_5',
    'Corridor_temp': 'T6',
    'Corridor_Humidity': 'RH_6',
    'Ironingroom_temp': 'T7',
    'Ironingroom_Humidity': 'RH_7',
    'Childrenroom_temp': 'T8',
    'Childrenroom_Humidity': 'RH_8',
    'Parentroom_temp': 'T9',
    'Parentroom_Humidity': 'RH_9',
    'Weatherstation_temp': 'T_out',
    'Weatherstation_mmhg': 'Press_mm_hg',
    'Weatherstation_Humidity': 'RH_out',
    'Weatherstation_windspeed': 'Windspeed',
    'Weatherstation_dewpoint': 'Tdewpoint',
    'Time_24hrs': 'hour',
    'Day_ofthe_week': 'weekday'
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    app.logger.debug(f"Received form data: {request.form}")

    input_data = []
    missing_fields = []
    form_data = {}

    # Extract and validate input data from the form
    for form_field, feature in form_to_feature.items():
        value = request.form.get(form_field)
        form_data[form_field] = value
        if value is None or value.strip() == '':
            missing_fields.append(form_field)
            continue

        try:
            if feature in ['hour', 'weekday']:
                value = int(value)
            else:
                value = float(value)
            input_data.append(value)
        except ValueError:
            app.logger.error(f"Invalid value for {form_field}: {value}")
            return jsonify({'error': f'Invalid value for {form_field}'}), 400

    if missing_fields:
        return jsonify({'error': f'Missing parameters: {", ".join(missing_fields)}'}), 400

    # Add current month as it's not included in the form
    input_data.append(datetime.now().month)

    app.logger.debug(f"Processed input data: {input_data}")

    current_time = datetime.now()
    prediction_time = current_time.replace(hour=int(request.form.get('Time_24hrs', 0)), minute=0, second=0, microsecond=0)

    # Make prediction
    try:
        prediction = model['Model'].predict([input_data])[0]
        rounded_prediction = float(np.round(prediction, 2))

        # Store the prediction
        predictions_storage[prediction_time].append(rounded_prediction)

        # Prepare response
        response = {
            'prediction': rounded_prediction,
            'timestamp': prediction_time.isoformat(),
            'text': f'Predicted Energy Consumption: {rounded_prediction} Wh',
            **form_data
        }

        return jsonify(response)
    except Exception as e:
        app.logger.error(f"Prediction error: {e}")
        return jsonify({'error': f'Error making prediction: {e}'}), 500

@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    # Convert defaultdict to regular dict for JSON serialization
    predictions_dict = {k.isoformat(): v for k, v in predictions_storage.items()}
    return jsonify(predictions_dict)

if __name__ == '__main__':
    app.run(debug=True)