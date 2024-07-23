import pandas as pd
import streamlit as st

def showTable(name_table):
    df = None
    if name_table == "LVL_INSP":
        df = pd.read_csv("./assets/MILSTD414.csv")
    if name_table == "normal":
        df = pd.read_csv("./assets/inspeccion_normal.csv")
    if name_table == "severa":
        df = pd.read_csv("./assets/inspeccion_normal.csv")
    if name_table == "size_sample":
        df = pd.read_csv("./assets/tabla_muestra_desviacion.csv")
    st.dataframe(df)




