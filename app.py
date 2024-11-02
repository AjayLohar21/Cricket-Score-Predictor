import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

model = pickle.load(open('model.pkl','rb'))

#  teams = ['Bangladesh', 'England', 'Sri Lanka', 'India', 'South Africa',
#        'Afghanistan', 'West Indies', 'Pakistan', 'New Zealand',
#        'Australia']

# cities = ['Mirpur', 'London', 'Auckland', 'Dubai', 'Cardiff', 'Pallekele',
#        'Mumbai', 'Centurion', 'Colombo', 'St Lucia', 'Durban',
#        'Manchester', 'Abu Dhabi', 'Kolkata', 'Nagpur', 'Johannesburg',
#        'Barbados', 'Chittagong', 'Nottingham', 'Wellington', 'Melbourne',
#        'Adelaide', 'Christchurch', 'Lauderhill', 'Cape Town', 'Bangalore',
#        'Mount Maunganui', 'Sydney', 'Chandigarh', 'Lahore', 'Trinidad',
#        'Hamilton', 'Southampton', 'Delhi', 'St Kitts']

team_mapping = {
    'Bangladesh': 0, 'England': 1, 'Sri Lanka': 2, 'India': 3, 'South Africa': 4,
    'Afghanistan': 5, 'West Indies': 6, 'Pakistan': 7, 'New Zealand': 8, 'Australia': 9
}

city_mapping = {
    'Mirpur': 0, 'London': 1, 'Auckland': 2, 'Dubai': 3, 'Cardiff': 4, 'Pallekele': 5,
    'Mumbai': 6, 'Centurion': 7, 'Colombo': 8, 'St Lucia': 9, 'Durban': 10,
    'Manchester': 11, 'Abu Dhabi': 12, 'Kolkata': 13, 'Nagpur': 14, 'Johannesburg': 15,
    'Barbados': 16, 'Chittagong': 17, 'Nottingham': 18, 'Wellington': 19, 'Melbourne': 20,
    'Adelaide': 21, 'Christchurch': 22, 'Lauderhill': 23, 'Cape Town': 24, 'Bangalore': 25,
    'Mount Maunganui': 26, 'Sydney': 27, 'Chandigarh': 28, 'Lahore': 29, 'Trinidad': 30,
    'Hamilton': 31, 'Southampton': 32, 'Delhi': 33, 'St Kitts': 34
}


st.title('Cricket Score Predictor')

col1,col2 = st.columns(2)

with col1:
    batting_team = st.selectbox('Select batting team',sorted(team_mapping.keys()))
with col2:
    bowling_team = st.selectbox('Select bowling team',sorted(team_mapping.keys()))

city = st.selectbox('Select City',sorted(city_mapping.keys()))

col3,col4,col5 = st.columns(3)

with col3:
    current_score = st.number_input('Current score')
with col4:
    overs = st.number_input('Overs done(works for over>5)')
with col5:
    wickets = st.number_input('Wickets out') 

last_five = st.number_input('Runs scored in last 5 overs')

if st.button('Predict Score'):
    balls_left = 120 - (overs*6)
    wickets_left = 10 - wickets
    crr = current_score/overs

    input_df = pd.DataFrame(
        {'current_score':[current_score],
         'balls_left':[balls_left],
         'wickets_left':[wickets_left],
         'last_five':[last_five],
         'crr':[crr],
         'batting_team': [team_mapping[batting_team]],
         'bowling_team': [team_mapping[bowling_team]],
         'city': [city_mapping[city]]
         }
    )

     # Label Encoding for categorical columns
    # label_encoders = {}
    # for column in ['batting_team', 'bowling_team', 'city']:
    #     le = LabelEncoder()
    #     input_df[column] = le.fit_transform(input_df[column])
    #     label_encoders[column] = le

    result = model.predict(input_df)

    st.header("Predicted Score "+ str(int((result[0]))))

