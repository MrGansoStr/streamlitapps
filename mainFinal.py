import streamlit as st
# import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from scipy import stats

from planmuestreoCameron.muestreoSimple import buscarEnTabla
from planmuestreoCameron.curvaOperacion import generateOperationCurve
from planmuestreoCameron.tablaCameron import showtable

from planmuestreoMIL.manageTableOne import getM_Value, getP_ZTable, getLevelInspect
from planmuestreoMIL.showTables import showTable

from cartas_control.main import hotelling_t2_control_chart, calculate_LCS

from taguchi.main_taguchi import *


def main():
    st.title("Control de Calidad y Muestreo")

    menu = ["Plan de muestreo para atributo",
            "Plan de muestreo para variable",
            "Curva de Operacion",
            "Tabla Cameron",
            "Tablas MIL STD",
            "Carta de control multivariado",
            "Filosofía de Taguchi"]
    
    choice = st.sidebar.selectbox("Seleccione una opción", menu)
        # Inicializar el historial global en session_state si no existe
    if 'historial_global' not in st.session_state:
        st.session_state.historial_global = []

    def agregar_a_historial(resultados):
        st.session_state.historial_global.append(resultados)

    def mostrar_historial():
        if st.session_state.historial_global:
            st.subheader("Historial")
            for i, resultado in enumerate(st.session_state.historial_global, 1):
                st.write(f"Resultado {i}: {resultado}")
        else:
            st.write("No hay resultados en el historial.")

    def eliminar_item(index):
        if 0 <= index < len(st.session_state.historial_global):
            st.session_state.historial_global.pop(index)
            st.success(f"Ítem {index + 1} eliminado exitosamente.")
        else:
            st.error("Ítem no encontrado.")
        
    main_col1, main_col2 = st.columns([4, 1], gap="large")
    with main_col1:
        if choice == "Plan de muestreo para atributo":
            st.subheader("Diseño de plan de muestreo para atributo (método de Cameron)")
            
            col1, col2 = st.columns(2)
            
            with col1:
                NCA = st.number_input("NCA %", min_value=0.0, max_value=100.0, value=1.0, step=1.0)
                NCL = st.number_input("NCL %", min_value=0.0, max_value=100.0, value=1.0, step=1.0)
            
            with col2:
                alpha = st.number_input("Alpha", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
                beta = st.number_input("Beta", min_value=0.0, max_value=1.0, value=0.10, step=0.01)
    
            if st.button("Calcular n y c"):
                n_calc, c_calc = buscarEnTabla(alpha, beta, NCA, NCL)
                # print(n_calc, c_calc)
                st.session_state['n_calc'] = n_calc
                st.session_state['c_calc'] = c_calc
                st.write(f"Tamaño de muestra calculado (n): {n_calc}")
                st.write(f"Número de aceptación calculado (c): {c_calc}")
                resultados = f"Plan de muestreo para atributo - NCA: {NCA}, NCL: {NCL}, Alpha: {alpha}, Beta: {beta}, n: {n_calc}, c: {c_calc}"
                agregar_a_historial(resultados)
                # agregar_a_historial(resultados)
    
        if choice == "Curva de Operacion":
            col1, col2 = st.columns(2)
            with col1:
                NCA = st.number_input("NCA %", min_value=0.0, max_value=100.0, value=1.0, step=1.0)
                NCL = st.number_input("NCL %", min_value=0.0, max_value=100.0, value=1.0, step=1.0)
                p = st.number_input("P (probabilidad de defectuosos)", min_value=0.0, max_value=1.0, value=0.10, step=0.001)
            
            with col2:
                alpha = st.number_input("Alpha", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
                beta = st.number_input("Beta", min_value=0.0, max_value=1.0, value=0.10, step=0.01)
            st.write("Ajuste manual de n y c:")
            n = st.slider("Tamaño de muestra (n)", min_value=1, max_value=1000, value=60)
            c = st.slider("Número de aceptación (c)", min_value=0, max_value=25, value=0)
    
            generateOperationCurve(n, c, p, beta, NCA/100, NCL/100, alpha=alpha)
        if choice == "Tabla Cameron":
            showtable()
        if choice == "Plan de muestreo para variable":
            st.subheader("Diseño de plan de muestreo para variable (método MIL STD 414)")
            col1, col2 = st.columns(2)
            with col1:
                size_lote = st.number_input("Tamaño de Lote ", min_value=0)
                NCA_levels = ["0-040","0-065","0-100","0-150","0-250","0-400","0-650","1-000","1-500","2-500","4-000","6-500","10-000","15-000"]
                NCA_L = st.selectbox(
                    "Seleccionar NCA",
                    NCA_levels,
                )
                st.write("Seleccionaste", NCA_L)
    
                level_inspeccion = ["I", "II", "III", "IV", "V"]
                lvl_insp =st.selectbox(
                    "Seleccionar un nivel de inspeccion",
                    level_inspeccion,
                )
                st.write("Seleccionaste", lvl_insp)
    
                tipo_inspeccion = ["normal", "severa"]
                type_inspection = st.selectbox(
                    "Seleccionar el nivel de inspeccion",
                    tipo_inspeccion,
                )
                st.write("Selecciono inspeccion ", type_inspection)
    
                if st.button(
                    "Calcular M y N"
                ):
                    M, N = getM_Value(getLevelInspect(size_lote, lvl_insp), NCA_L, type_inspection)
                    st.write("El valor M es: ", M)
                    st.write("El tamaño de muestra es : ", N)
                    agregar_a_historial(f"M: {M} y N: {N}")
    
                
                # NCA = st.number_input("NCA %", min_value=0.0, max_value=100.0, value=1.0, step=1.0)
            with col2:
                ES = st.number_input(
                    "Especificacion superior"
    
                )
                EI = st.number_input(
                    "Especificacion Inferior"
                )
    
                media = st.number_input(
                    "Media"
                )
    
                desviacion = st.number_input(
                    "Desviacion"
                )
    
                if st.button(
                    "Calcular Zes y Zei"
                ):
                    if ES == 0 and EI == 0 and media == 0 and desviacion == 0:
                        st.error('Todos los campos son obligatorios. Por favor, introduce valores en todos los campos.')
                    Zes = (ES - media) / desviacion
                    Zei = (media - EI) / desviacion
                    st.write("Zes ", Zes)
                    st.write("Zei ", Zei)
                    agregar_a_historial(f"Zes: {Zes} y Zei: {Zei}")
    
                size_n = st.number_input(
                    "Tamaño de muestra"
                )
                Zto_find = st.number_input(
                    "Valor z a buscar en tabla"
                )
    
                if st.button(
                    "Buscar Z en tabla"
                ):
                    if ES == 0 and EI == 0 and media == 0 and desviacion == 0:
                        st.error('Todos los campos son obligatorios. Por favor, introduce valores en todos los campos.')
                    valuep = getP_ZTable(int(size_n), Zto_find)
                    st.write("El valor es: ", valuep)
                    agregar_a_historial(f"Valor z encontrado en tabla{valuep}")
        if choice == "Tablas MIL STD":
    
            name_table = st.selectbox(
                "Seleccionar Tabla",
                ["LVL_INSP", "normal", "severa", "size_sample"]
            )
    
            if st.button("Mostrar tabla"):
                showTable(name_table)
        elif choice == "Carta de control multivariado":
            st.subheader("Cartas de control multivariado (método T2 de Hotelling)")
            uploaded_file = st.file_uploader("Cargar datos CSV", type="csv")
            alpha = st.number_input("alpha", value=0.01)
            
            if uploaded_file is not None:
                data = pd.read_csv(uploaded_file)
                with st.form('form'):
                    sel_column = st.multiselect('Selecciona las columnas', data.columns,
                       help='Selecciona las columnas para procesar')
                    
                    # drop_na = st.checkbox('Drop rows with missing value', value=True)
                    submitted = st.form_submit_button("Submit")
                    t2 = None
                    lcs = None
                    lcsv2 = None
                    media = None
                    if submitted:
                        newDataframe = pd.DataFrame(data[sel_column])
                        # print(newDataframe)
                        t2, lcs, media = hotelling_t2_control_chart(data.values, 1 - alpha)
                        lcsv2 = calculate_LCS(newDataframe, alpha)
                        # print(media)
    
                    # print(lcs, lcsv2)
                    st.write("LCS: ", lcsv2)
                    agregar_a_historial(f"LCS: {lcsv2}")
                    st.write("LCI: ", 0)
                    st.dataframe(t2)
                    fig, ax = plt.subplots()
                    ax.plot(t2["T2"])
                    ax.axhline(y=lcs, color='r', linestyle='--')
                    ax.axhline(y=0, color='g', linestyle='--')
                    ax.axhline(y=media, color='0', linestyle='--')
                    ax.set_title("Carta de control T2 de Hotelling")
                    ax.set_xlabel("Muestra")
                    ax.set_ylabel("T2")
                    st.pyplot(fig)
        elif choice == "Filosofía de Taguchi":
            num_factors = st.number_input("Número de factores", min_value=2, max_value=10, value=3)
            num_levels = st.number_input("Número de niveles por factor", min_value=2, max_value=5, value=3)
            matrix = generate_taguchi_matrix(num_factors, num_levels)
            if matrix is not None:
                st.subheader("Matriz ortogonal de Taguchi")
                st.dataframe(matrix)
            results = []
            for i in range(len(matrix)):
                result = st.number_input(f"Resultado del experimento {i+1}", value=0.0, key=f"result_{i}")
                results.append(result)
            quality_characteristic = st.selectbox(
                "Seleccione la característica de calidad",
                ("Nominal es mejor", "Menor es mejor", "Mayor es mejor")
            )
            if st.button("Calcular efectos y relación S/N"):
                effects = calculate_main_effects(matrix, results, num_factors, num_levels)
                sn_ratio = calculate_sn_ratio(results, quality_characteristic)
                
                st.subheader("Efectos principales")
                for i, effect in enumerate(effects):
                    st.write(f"Factor {i+1}: {effect}")
                
                st.subheader("Relación Señal-Ruido (S/N)")
                st.write(f"{quality_characteristic}: {sn_ratio:.2f} dB")
            
                # Calcular el mejor nivel para cada factor
                best_levels = []
                for effect in effects:
                    if quality_characteristic in ["Mayor es mejor", "Nominal es mejor"]:
                        best_level = np.argmax(effect) + 1
                    else:  # Menor es mejor
                        best_level = np.argmin(effect) + 1
                    best_levels.append(best_level)
                
                st.subheader("Niveles óptimos")
                for i, level in enumerate(best_levels):
                    st.write(f"Factor {i+1}: Nivel {level}")

    # Mostrar el historial global en una sección separada
    with main_col2:

        st.sidebar.subheader("Historial")
        mostrar_historial()
        
        if st.sidebar.checkbox("Eliminar ítem específico del historial"):
            if st.session_state.historial_global:
                index = st.sidebar.number_input("Ítem a eliminar (número)", min_value=1, max_value=len(st.session_state.historial_global), step=1) - 1
                if st.sidebar.button("Eliminar ítem seleccionado"):
                    eliminar_item(index)
            else:
                st.error("No hay ítems para eliminar.")    


            

if __name__ == "__main__":
    main()