# ********************* Step 01: Import the required libraries and packages *******************

# Streamlit for user interface
import streamlit as st
# Numpy for numerical calculations
import numpy as np
# To use the saved and downloaded model, scaler and lebel encoder
import joblib
# To interact with operating system
import os
# *********************************************************************************************

# ********************* Step 02: Load the downloaded model and scaler *************************

# Load the downloaded model
model = joblib.load('lin_reg.pkl')

# Load the downloaded scaler
scaler = joblib.load('scaler.pkl')


# Also binary mapping for (yes, no)
binary_map = {'yes': 1, 'no': 0}

# Furnishing status mapping (must match LabelEncoder fit order)
furnishing_map = {'furnished': 1, 'semi-furnished': 2, 'unfurnished': 0}

# *********************************************************************************************

# ********************* Step 03: Build the streamlit app **************************************

# App title
st.title("🏠 House Price Prediction App")

st.markdown("Enter the data to predict price of a house")

# Difine columns for user inputs to show it side by side in streamlit
col1, col2 = st.columns(2)

# User inputs in column 1
with col1:
    area = st.number_input("Area (sq. ft.)", min_value=200, max_value=10000, step=50)
    bedrooms = st.selectbox("Bedrooms", [1,2,3,4,5,6,7,8,9,10])
    bathrooms = st.selectbox("Bathrooms", [1,2,3,4,5,6,7,8,9,10])
    stories = st.selectbox("Stories", [1,2,3,4,5])
    mainroad = st.selectbox("Man Road Access", ["Yes", "No"])
    guestroom = st.selectbox("Have a Guest Room", ["Yes", "No"])
   
# User inputs in column 2
with col2:
   
    basement = st.selectbox("Have a Basement", ["Yes", "No"])
    hotwaterheating = st.selectbox("Hot Water System", ["Yes", "No"])
    airconditioning = st.selectbox("Have Air Condition", ["Yes", "No"])
    parking = st.selectbox("Parking Places", [0,1,2,3,4])
    prefarea = st.selectbox("Preferred Area", ["Yes", "No"])
    furnishingstatus = st.selectbox("Furnishing Status", ['furnished', 'semi-furnished', 'unfurnished'])

# Button for Prediction
if st.button("Predict Price"):
    # Transforming area into log_area using 'Log Transformation' as  we applied it during model training
    log_area = np.log1p(area)
    # Create an input array
    input_data = np.array([[
        log_area,
        bedrooms,
        bathrooms,
        stories,
        binary_map[mainroad.lower()],
        binary_map[guestroom.lower()],
        binary_map[basement.lower()],
        binary_map[hotwaterheating.lower()],
        binary_map[airconditioning.lower()],
        parking,
        binary_map[prefarea.lower()],
        furnishing_map[furnishingstatus]
    ]])

    # Scale the input because we trained the model with scaled data, so it will conpare scaled input with scaled features
    input_scaled = scaler.transform(input_data)

    # Predict the price (but it will predict the log_price as we applied 'Log Transformation' on it during model training)
    log_price = model.predict(input_scaled)[0]
    # Now reverse transforming the log_price into original value
    price = np.expm1(log_price)             # np.expm1(x)   which returns (exp(x) - 1)

    st.success(f"🏡 Estimated House Price: $ {price:,.0f}")

# ********************************************************************************************

############ Just for background (Optional) ###################################################

# Custom CSS to set background image
def set_background(image_file):
    with open(image_file, "rb") as image:
        encoded = image.read()
    base64_image = base64.b64encode(encoded).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpeg;base64,{base64_image}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Usage
import base64
set_background("Images\image1.jpeg")

###############################################################################################
