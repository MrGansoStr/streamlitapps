import numpy as np
import pandas as pd
from scipy.stats import binom

# Define los parámetros
alpha = 0.05
beta = 0.10
NCA = 95
NCL = 5

# Convertir porcentajes a proporciones
p1 = NCA / 100
p2 = NCL / 100

# Calcular Rc
Rc = p2 / p1

# Función para buscar el valor de R más cercano
def buscar_valor_R(tabla, Rc):
    diferencias = np.abs(tabla['Rc'] - Rc)
    min_diff_index = np.argmin(diferencias)
    return tabla.iloc[min_diff_index]

# Crear una tabla simulada
valores_R = np.linspace(0.5, 2.0, 100)  # Ajusta el rango y el número de puntos según sea necesario
valores_c = np.random.randint(1, 50, size=100)  # Simulación de valores de c

tabla = pd.DataFrame({
    'R': valores_R,
    'c': valores_c
})

# Buscar el valor de R más cercano
resultado = buscar_valor_R(tabla, Rc)
print(f"Valor de R más cercano a Rc: {resultado['R']} con c = {resultado['c']}")
