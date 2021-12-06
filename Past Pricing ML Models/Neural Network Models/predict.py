import numpy as np
import tensorflow as tf
from joblib import load




explanatory_variables = {}

explanatory_variables['sqft'] = 950
explanatory_variables['property_type'] = 'Condo Apartment'
explanatory_variables['style'] = 'Apartment'
explanatory_variables['bedrooms' ] = 2
explanatory_variables['dens'] = 0
explanatory_variables['bathrooms'] = 1 
explanatory_variables['kitchens'] = 1
explanatory_variables['rooms'] = 5
explanatory_variables['parking'] = 1.0


def predict(input_data):

    keys_for_categorical_data = {'Type': {'Co-op / Co-Ownership Apartment': 0, 'Condo Apartment': 1, 'Condo Townhouse': 2, 'Det Condo': 3, 'Detached': 4, 'Multiplex': 5, 'Other': 6, 'Semi-Detached': 7, 'Store W/Apt/Offc': 8, 'Townhouse': 9}, 'Style': {'1 1/2 Storey': 0, '2 1/2 Storey': 1, '2-Storey': 2, '3-Storey': 3, 'Apartment': 4, 'Bachelor/Studio': 5, 'Backsplit': 6, 'Bungalow': 7, 'Loft': 8, 'Sidesplit': 9, 'Stacked Townhouse': 10}}

    test_input = np.array([input_data['sqft'], input_data['property_type'], input_data['style'], input_data['bedrooms' ], input_data['dens'], input_data['bathrooms'], input_data['kitchens'], input_data['rooms'], input_data['parking']], dtype = 'object' )

    test_input[1] = keys_for_categorical_data['Type'][test_input[1]]
    test_input[2] = keys_for_categorical_data['Style'][test_input[2]]

    test_input = test_input.reshape(1,9)

    test_input = np.asarray(test_input).astype(np.float32)

    load_model_from_file = tf.keras.models.load_model("./models/mvp_model")


    scaler = load('scaler_filename.joblib')
    


    result = load_model_from_file.predict(test_input)

    predicted = scaler.inverse_transform(result)

    return predicted

print(predict(explanatory_variables))