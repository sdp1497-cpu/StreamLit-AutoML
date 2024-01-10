import streamlit as st
import pandas as pd
import os 
from ydata_profiling import profile_report
import pandas_profiling
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import requests
from streamlit.components.v1 import html
from streamlit_lottie import st_lottie
#from pycaret.regression import setup , compare_models , pull , save_model
from pycaret.classification import setup , compare_models , pull , save_model




with st.sidebar:
    url = requests.get( 
    "https://lottie.host/761cd9e2-08d2-404d-8c78-a9ce943ef91b/7l7U3FKU8W.json") 
    url_json = dict() 
    if url.status_code == 200: 
        url_json = url.json() 
    else: 
        print("Error in URL") 
  
  
    #st.image("https://lottie.host/761cd9e2-08d2-404d-8c78-a9ce943ef91b/7l7U3FKU8W.json")
    st.title("Welcome to Auto ML App")
    st_lottie(url_json,key="AI")
    choice = st.radio("NAVIGATION : " , ["Upload File","Profiling" ,"Machine Learning","Download"])
    st.info("This web application allows you to build automated Machine Learning Model with ease using StreamLit , Pnadas Profoling and PyCaret.Try it out Yourself !")

if os.path.exists("sourcedata.csv"):
    df = pd.read_csv("sourcedata.csv", index_col=None)


if choice == 'Upload File':
    st.title("Upload Your Data for Modelling")
    uploaded_file = st.file_uploader("Upload your Dataset here ", type=['csv','xlsx'])
    if uploaded_file:
        df = pd.read_csv(uploaded_file, index_col=None)
        df.to_csv("sourcedata.csv", index=None)
        st.dataframe(df)

if choice=="Profiling":
    st.title("Automated Exploratory Data Analysis ")
    profile_report = df.profile_report()
    st_profile_report(profile_report)
    
    #profile_report = df.profile_report()
    #html(profile_report.to_html())
    #profile_report = ProfileReport(df, explorative=True)
    #html(profile_report.to_html(), height=900)

if choice=='Machine Learning':
    st.title("Machine Learning Starts:")
    target =st.selectbox("Select Your Target" , df.columns)
    if st.button("Train Model"):
        setup(df, target=target)
        setup_df = pull()
        st.info("This is the ML Experiment Settings ")
        st.dataframe(setup_df)
        best_model = compare_models()
        comapre_df = pull()
        st.info("This is the ML Model ")
        st.dataframe(comapre_df)
        best_model
        save_model(best_model,'best_model')

if choice == "Download":
    with open("best_model.pkl",'rb')as f : 
        st.download_button("Download the Model ", f ,"trained_model.pkl")

