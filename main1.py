import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

def cameron_sampling_plan(AQL, LTPD, alpha, beta):
    n = int(np.ceil((np.log(beta / alpha)) / (np.log((1 - AQL) / (1 - LTPD)))))
    c = int(np.floor(n * (AQL + LTPD) / 2))
    return n, c

def prob_aceptacion(n, c, p):
    return sum([stats.binom.pmf(i, n, p) for i in range(c + 1)])

def mil_std_414_sampling_plan(lot_size, inspection_level, AQL):
    # Implementación simplificada de MIL-STD-414
    # En una implementación real, se usaría una tabla de lookup
    n = int(np.sqrt(lot_size))
    k = stats.norm.ppf(1 - AQL)
    return n, k

def hotelling_t2_control_chart(data):
    mean = np.mean(data, axis=0)
    cov = np.cov(data.T)
    t2 = []
    for row in data:
        t2.append(np.dot(np.dot((row - mean), np.linalg.inv(cov)), (row - mean).T))
    ucl = stats.f.ppf(0.9973, len(mean), len(data) - len(mean)) * \
          ((len(data) - 1) * len(mean) / (len(data) - len(mean))) * \
          ((len(data) + 1) / len(data))
    return t2, ucl

def main():
    st.title("Control de Calidad y Muestreo")

    menu = ["Plan de muestreo para atributo",
            "Plan de muestreo para variable",
            "Carta de control multivariado",
            "Filosofía de Taguchi"]
    
    choice = st.sidebar.selectbox("Seleccione una opción", menu)

    if choice == "Plan de muestreo para atributo":
        st.subheader("Diseño de plan de muestreo para atributo (método de Cameron)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            NCA = st.number_input("NCA", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
            NCL = st.number_input("NCL", min_value=0.0, max_value=1.0, value=0.10, step=0.01)
        
        with col2:
            alpha = st.number_input("Alpha", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
            beta = st.number_input("Beta", min_value=0.0, max_value=1.0, value=0.10, step=0.01)

        if st.button("Calcular n y c"):
            n_calc, c_calc = cameron_sampling_plan(NCA, NCL, alpha, beta)
            st.session_state['n_calc'] = n_calc
            st.session_state['c_calc'] = c_calc
            st.write(f"Tamaño de muestra calculado (n): {n_calc}")
            st.write(f"Número de aceptación calculado (c): {c_calc}")

        st.write("Ajuste manual de n y c:")
        n = st.slider("Tamaño de muestra (n)", min_value=1, max_value=200, value=st.session_state.get('n_calc', 100))
        c = st.slider("Número de aceptación (c)", min_value=0, max_value=n, value=min(st.session_state.get('c_calc', 5), n))

        if st.button("Calcular probabilidades de aceptación"):
            Pa_AQL = prob_aceptacion(n, c, AQL)
            Pa_LTPD = prob_aceptacion(n, c, LTPD)
            
            st.write(f"Probabilidad de aceptación en AQL: {Pa_AQL:.4f}")
            st.write(f"Probabilidad de aceptación en LTPD: {Pa_LTPD:.4f}")
            
            # Gráfica de la curva característica de operación
            p_values = np.linspace(0, 0.2, 100)
            Pa_values = [prob_aceptacion(n, c, p) for p in p_values]
            
            fig, ax = plt.subplots()
            ax.plot(p_values, Pa_values)
            ax.set_title("Curva Característica de Operación")
            ax.set_xlabel("Proporción de defectuosos")
            ax.set_ylabel("Probabilidad de aceptación")
            ax.axvline(x=AQL, color='g', linestyle='--', label='AQL')
            ax.axvline(x=LTPD, color='r', linestyle='--', label='LTPD')
            ax.axhline(y=1-alpha, color='g', linestyle=':', label='1-α')
            ax.axhline(y=beta, color='r', linestyle=':', label='β')
            ax.legend()
            st.pyplot(fig)

    elif choice == "Plan de muestreo para variable":
        st.subheader("Diseño de plan de muestreo para variable (método MIL STD 414)")
        lot_size = st.number_input("Tamaño del lote", min_value=1, value=1000)
        inspection_level = st.selectbox("Nivel de inspección", ["I", "II", "III"])
        AQL = st.number_input("AQL", min_value=0.0, max_value=1.0, value=0.05)

        if st.button("Calcular"):
            n, k = mil_std_414_sampling_plan(lot_size, inspection_level, AQL)
            st.write(f"Tamaño de muestra (n): {n}")
            st.write(f"Factor de aceptación (k): {k:.2f}")

    elif choice == "Carta de control multivariado":
        st.subheader("Cartas de control multivariado (método T2 de Hotelling)")
        uploaded_file = st.file_uploader("Cargar datos CSV", type="csv")
        
        if uploaded_file is not None:
            data = pd.read_csv(uploaded_file)
            t2, ucl = hotelling_t2_control_chart(data.values)
            
            fig, ax = plt.subplots()
            ax.plot(t2)
            ax.axhline(y=ucl, color='r', linestyle='--')
            ax.set_title("Carta de control T2 de Hotelling")
            ax.set_xlabel("Muestra")
            ax.set_ylabel("T2")
            st.pyplot(fig)

    elif choice == "Filosofía de Taguchi":
        st.subheader("Filosofía de Taguchi para el control fuera de línea")
        st.write("Esta sección está en desarrollo. La filosofía de Taguchi se enfoca en la mejora de la calidad a través del diseño de experimentos y la optimización de parámetros.")

if __name__ == "__main__":
    main()