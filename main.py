import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

def plan_muestreo_atributo():
    st.subheader("Plan de muestreo para atributo (método de Cameron)")
    
    # Inputs
    aql = st.number_input("AQL (Nivel de Calidad Aceptable)", min_value=0.01, max_value=10.0, value=1.0, step=0.1)
    ltpd = st.number_input("LTPD (Porcentaje Tolerable de Defectuosos)", min_value=0.1, max_value=20.0, value=5.0, step=0.1)
    alpha = st.number_input("Riesgo del productor (α)", min_value=0.01, max_value=0.1, value=0.05, step=0.01)
    beta = st.number_input("Riesgo del consumidor (β)", min_value=0.01, max_value=0.1, value=0.1, step=0.01)

    if st.button("Calcular plan de muestreo"):
        # Cálculos del método de Cameron (simplificado)
        n = int(np.log(beta / alpha) / (np.log((1 - aql/100) / (1 - ltpd/100))))
        c = int(n * aql/100 + stats.norm.ppf(1-alpha) * np.sqrt(n * aql/100 * (1 - aql/100)))

        st.write(f"Tamaño de muestra (n): {n}")
        st.write(f"Número de aceptación (c): {c}")

        # Gráfica de la curva OC
        p = np.linspace(0, ltpd*2/100, 100)
        pa = stats.binom.cdf(c, n, p)

        fig, ax = plt.subplots()
        ax.plot(p*100, pa)
        ax.set_xlabel("Porcentaje de defectuosos")
        ax.set_ylabel("Probabilidad de aceptación")
        ax.set_title("Curva Característica de Operación (OC)")
        ax.axvline(aql, color='r', linestyle='--', label='AQL')
        ax.axvline(ltpd, color='g', linestyle='--', label='LTPD')
        ax.legend()
        st.pyplot(fig)

def plan_muestreo_variable():
    st.subheader("Plan de muestreo para variable (método MIL STD 414)")
    
    # Inputs
    aql = st.number_input("AQL (Nivel de Calidad Aceptable)", min_value=0.01, max_value=10.0, value=1.0, step=0.1)
    inspection_level = st.selectbox("Nivel de Inspección", ["II", "III", "IV", "V"])
    
    # Simplificación del método MIL STD 414
    sample_sizes = {"II": 10, "III": 15, "IV": 20, "V": 25}
    n = sample_sizes[inspection_level]
    
    k = stats.norm.ppf(1 - aql/100)
    
    st.write(f"Tamaño de muestra (n): {n}")
    st.write(f"Factor de aceptación (k): {k:.3f}")
    
    # Gráfica de la distribución normal con límites
    x = np.linspace(-4, 4, 100)
    y = stats.norm.pdf(x)
    
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.fill_between(x, y, where=(x > k), alpha=0.3)
    ax.axvline(k, color='r', linestyle='--', label='k')
    ax.set_xlabel("Desviaciones estándar")
    ax.set_ylabel("Densidad de probabilidad")
    ax.set_title("Distribución Normal con límite de aceptación")
    ax.legend()
    st.pyplot(fig)

def cartas_control_multivariado():
    st.subheader("Cartas de control multivariado (T2 de Hotelling)")
    
    # Inputs
    n_variables = st.number_input("Número de variables", min_value=2, max_value=10, value=3, step=1)
    n_samples = st.number_input("Número de muestras", min_value=10, max_value=100, value=20, step=1)
    
    # Generamos datos de ejemplo
    data = np.random.randn(n_samples, n_variables)
    
    # Cálculo de T2 de Hotelling
    mean = np.mean(data, axis=0)
    cov = np.cov(data.T)
    t2 = []
    for sample in data:
        diff = sample - mean
        t2.append(np.dot(np.dot(diff, np.linalg.inv(cov)), diff.T))
    
    ucl = ((n_variables * (n_samples - 1)) / (n_samples - n_variables)) * stats.f.ppf(0.9973, n_variables, n_samples - n_variables)
    
    # Gráfica de control T2
    fig, ax = plt.subplots()
    ax.plot(range(1, n_samples + 1), t2, marker='o')
    ax.axhline(ucl, color='r', linestyle='--', label='UCL')
    ax.set_xlabel("Número de muestra")
    ax.set_ylabel("T2 de Hotelling")
    ax.set_title("Carta de control T2 de Hotelling")
    ax.legend()
    st.pyplot(fig)

def filosofia_taguchi():
    st.subheader("Filosofía de Taguchi para el control fuera de línea")
    
    st.write("""
    La filosofía de Taguchi se centra en la mejora de la calidad a través del diseño de productos y procesos. 
    Algunos conceptos clave incluyen:
    
    1. Función de pérdida de calidad
    2. Diseño robusto
    3. Diseño de parámetros
    4. Relación señal-ruido (S/N)
    """)
    
    # Ejemplo de función de pérdida de calidad
    target = st.number_input("Valor objetivo", value=10.0)
    k = st.number_input("Coeficiente de pérdida", value=1.0)
    
    x = np.linspace(target-5, target+5, 100)
    loss = k * (x - target)**2
    
    fig, ax = plt.subplots()
    ax.plot(x, loss)
    ax.set_xlabel("Valor")
    ax.set_ylabel("Pérdida")
    ax.set_title("Función de pérdida de calidad de Taguchi")
    ax.axvline(target, color='r', linestyle='--', label='Objetivo')
    ax.legend()
    st.pyplot(fig)

def main():
    st.title("Aplicación de Estadística Industrial")

    menu = ["Inicio", 
            "Plan de muestreo para atributo (Cameron)", 
            "Plan de muestreo para variable (MIL STD 414)", 
            "Cartas de control multivariado (T2 de Hotelling)",
            "Filosofía de Taguchi"]

    choice = st.sidebar.selectbox("Menú", menu)

    if choice == "Inicio":
        st.subheader("Bienvenido a la aplicación de Estadística Industrial")
        st.write("Seleccione una opción del menú para comenzar.")

    elif choice == "Plan de muestreo para atributo (Cameron)":
        plan_muestreo_atributo()

    elif choice == "Plan de muestreo para variable (MIL STD 414)":
        plan_muestreo_variable()

    elif choice == "Cartas de control multivariado (T2 de Hotelling)":
        cartas_control_multivariado()

    elif choice == "Filosofía de Taguchi":
        filosofia_taguchi()

if __name__ == "__main__":
    main()