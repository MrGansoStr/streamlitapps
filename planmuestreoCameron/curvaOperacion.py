from scipy import stats, optimize
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
def prob_aceptacion(n, c, p):
    return stats.binom.cdf(c, n, p)

    # return sum([stats.binom.pmf(i, n, p) for i in range(c + 1)])

# print(stats.binom.cdf(2, 120, 0.04))

def generateOperationCurve(n, c , p, beta, NCA, NCL, cantidad = 10 ,alpha=0.05, step_by = 0.05):
    p_values = np.linspace(0, alpha, 100)
    # p_values = np.arange(0, alpha + step_by, 0.001)
    list_pValues =  [prob_aceptacion(n, c, p) for p in p_values]
    # print(list_pValues)
    # print(p_values)
    fig, ax = plt.subplots()
    ax.plot(p_values, list_pValues)
    ax.set_title("Curva Característica de Operación")
    ax.set_xlabel("Proporción de defectuosos")
    ax.set_ylabel("Probabilidad de aceptación")
    ax.axvline(x=NCA, color='g', linestyle='--', label='NCA')
    ax.axvline(x=NCL, color='r', linestyle='--', label='NCL')
    ax.axhline(y=1-alpha, color='g', linestyle=':', label='1-α')
    ax.axhline(y=beta, color='r', linestyle=':', label='β')
    ax.legend()
    # plt.show()
    
    st.pyplot(fig)


# def generateOperationCurveCameron():

def encontrar_p(n, c, target_cdf):
    # Define una función para la cual queremos encontrar la raíz
    def func(p):
        return prob_aceptacion(n, c, p) - target_cdf
    
    # Usa optimize.bisect para encontrar la raíz de la función
    p = optimize.bisect(func, 0, 1)
    return p

# print(encontrar_p(205,2, 0.005))
# print(stats.binom.isf(2, 205, 0.995))
# NCA = 0.4
# alpha = 0.005
# NCL = 2.5
# beta = 0.10
# print(prob_aceptacion(n=120, c=2, p=0.04))
# generateOperationCurve(n=60, c=1, p=0.04, NCA=NCA/100, NCL=NCL/100, alpha=0.005, beta=0.10)