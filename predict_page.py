import streamlit as st
import pickle
import numpy as np

# Function to load the pre-trained model and associated encoders
def load_saved_model():
    with open('saved_steps.pkl', 'rb') as file:
        loaded_data = pickle.load(file)
    return loaded_data

# Function to extract model and encoders from loaded data
def preprocess_country_education(data):
    regressor = data["model"]
    le_country = data["le_country"]
    le_education = data["le_education"]
    return regressor, le_country, le_education

# Function to predict salary based on user inputs
def predict_salary(regressor, le_country, le_education, country, education, experience):
    # Prepare user inputs in the format expected by the model
    X_sample = np.array([[country, education, experience]])
    X_sample[:, 0] = le_country.transform(X_sample[:,0])
    X_sample[:, 1] = le_education.transform(X_sample[:,1])
    X_sample = X_sample.astype(float)

    # Make the salary prediction
    salary_prediction = regressor.predict(X_sample)
    return salary_prediction

# Main function to display the prediction interface
def show_predict_page():
    # Set title and prompt for information
    st.title("Software Developer Salary Prediction")
    st.write("""### We need some information to predict the salary""")

    # Define options for country and education level
    countries_list = (
        "United States", "India", "United Kingdom", "Germany", "Canada",
        "Brazil", "France", "Spain", "Australia", "Netherlands", "Poland",
        "Italy", "Russian Federation", "Sweden", "Switzerland", "Turkey"
    )

    education_levels = (
        "Less than a Bachelors", "Bachelor’s degree", "Master’s degree", "Post grad",
    )

    # Load model and encoders
    data = load_saved_model()
    regressor, le_country, le_education = preprocess_country_education(data)

    # Display dropdowns and slider for user input
    selected_country = st.selectbox("Country", countries_list)
    selected_education = st.selectbox("Education Level", education_levels)
    years_experience = st.slider("Years of Experience", 0, 50, 3)

    # Perform salary calculation when button is clicked
    calculate_salary = st.button("Calculate Salary")
    if calculate_salary:
        predicted_salary = predict_salary(regressor, le_country, le_education, selected_country, selected_education, years_experience)
        st.subheader(f"The estimated salary is ${predicted_salary[0]:.2f}")

