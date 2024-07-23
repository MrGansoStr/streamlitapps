
import pandas as pd
import streamlit as st


def showtable():
    df = pd.read_csv("./assets/cameronOC.csv", skiprows=1)
    st.dataframe(df)