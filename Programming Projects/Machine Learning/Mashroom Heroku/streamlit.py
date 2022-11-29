import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier

st.write("""
# Safe to eat or deadly poison?
""")

st.sidebar.header('User Input Features')

st.sidebar.markdown("""
""")

def user_input_features():
    gill = ['Close','Crowded','Distant']
    stalk = ["bulbous","club","cup","equal","rhizomorphs","rooted","missing"]
    stalk_above = ["fibrous","scaly","silky","smooth"]
    stalk_below= ["fibrous","scaly","silky","smooth"]
    pop = ["abundant","clustered","numerous","scattered","several","solitary"]
    
    gill_spacing = st.sidebar.selectbox('gill spacing',(gill))
    stalk_root = st.sidebar.selectbox('stalk root',(stalk))
    stalk_surface_above_ring = st.sidebar.selectbox('stalk surface above ring',(stalk_above))
    stalk_surface_below_ring = st.sidebar.selectbox('stalk surface below ring',( stalk_below))
    population = st.sidebar.selectbox('population',(pop))
    ring_number = st.sidebar.slider('ring number', 0,1,2)
    data = {'gill_spacing': gill_spacing,
            'stalk_root': stalk_root,
            'stalk_surface_above_ring': stalk_surface_above_ring,
            'stalk_surface_below_ring': stalk_surface_below_ring,
            'population': population,
            'ring_number': ring_number}
    
    indexes = []
    indexes.append(gill.index(gill_spacing))
    indexes.append(stalk.index(stalk_root))
    indexes.append(stalk_above.index(stalk_surface_above_ring))
    indexes.append(stalk_below.index(stalk_surface_below_ring))
    indexes.append(pop.index(population))
    indexes.append(data["ring_number"])
    
    features = pd.DataFrame(data, index=[0])
    return features, indexes

input_df, values = user_input_features()
st.write(input_df)

load_clf = pickle.load(open("mashrooms_clf.pkl", "rb"))

st.subheader('Prediction Probability')

if load_clf.predict([values]):
    st.write("""
             Holly father waiting for you
             """)
else:
    st.write("""
              You are okey for now
              """)
