import streamlit as st
import pandas as pd
import pickle
# Load the model and label encoders
model = pickle.load(open('model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
batting_team_encoder = pickle.load(open('batting_team_encoder.pkl', 'rb'))
bowling_team_encoder = pickle.load(open('bowling_team_encoder.pkl', 'rb'))
city_encoder = pickle.load(open('city_encoder.pkl', 'rb'))

# Team and city options for selection
teams = ['Bangladesh', 'England', 'Sri Lanka', 'India', 'South Africa',
         'Afghanistan', 'West Indies', 'Pakistan', 'New Zealand',
         'Australia']
cities = ['Mirpur', 'London', 'Auckland', 'Dubai', 'Cardiff', 'Pallekele',
          'Mumbai', 'Centurion', 'Colombo', 'St Lucia', 'Durban',
          'Manchester', 'Abu Dhabi', 'Kolkata', 'Nagpur', 'Johannesburg',
          'Barbados', 'Chittagong', 'Nottingham', 'Wellington', 'Melbourne',
          'Adelaide', 'Christchurch', 'Lauderhill', 'Cape Town', 'Bangalore',
          'Mount Maunganui', 'Sydney', 'Chandigarh', 'Lahore', 'Trinidad',
          'Hamilton', 'Southampton', 'Delhi', 'St Kitts']

# Title for the app
st.title('Cricket Score Predictor')

# Input fields for the app
col1, col2 = st.columns(2)
with col1:
    batting_team = st.selectbox('Select batting team', sorted(teams))
with col2:
    bowling_team = st.selectbox('Select bowling team', sorted(teams))

city = st.selectbox('Select City', sorted(cities))

col3, col4, col5 = st.columns(3)
with col3:
    current_score = st.number_input('Current score')
with col4:
    overs = st.number_input('Overs done (works for over > 5)')
with col5:
    wickets = st.number_input('Wickets out')

last_five = st.number_input('Runs scored in last 5 overs')

# Prediction button
if st.button('Predict Score'):
    # Feature engineering
    balls_left = 120 - (overs * 6)
    wickets_left = 10 - wickets
    crr = current_score / overs

    # Create input DataFrame
    input_df = pd.DataFrame({
        'current_score': [current_score],
        'balls_left': [balls_left],
        'wickets_left': [wickets_left],
        'last_five': [last_five],
        'crr': [crr],
        'batting_team': [batting_team],
        'bowling_team': [bowling_team],
        'city': [city]
    })

    # Transform categorical features using loaded encoders
    input_df['batting_team'] = batting_team_encoder.transform(input_df['batting_team'])
    input_df['bowling_team'] = bowling_team_encoder.transform(input_df['bowling_team'])
    input_df['city'] = city_encoder.transform(input_df['city'])

    input_df[['current_score', 'balls_left', 'wickets_left', 'last_five', 'crr']] = scaler.transform(
        input_df[['current_score', 'balls_left', 'wickets_left', 'last_five', 'crr']]
    )



    # Make prediction
    result = model.predict(input_df)

    # Display the predicted score
    st.header("Predicted Score: " + str(int(result[0])))
