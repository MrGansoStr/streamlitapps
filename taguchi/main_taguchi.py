import numpy as np
import itertools
import pandas as pd
import streamlit as st

def generate_taguchi_matrix(num_factors, num_levels):
    if num_levels == 2 and num_factors <= 4:
        return pd.DataFrame(np.array(list(itertools.product([1, 2], repeat=num_factors))))
    elif num_levels == 3 and num_factors <= 4:
        return pd.DataFrame(np.array([[1,1,1],[1,2,2],[1,3,3],[2,1,2],[2,2,3],[2,3,1],[3,1,3],[3,2,1],[3,3,2]]))
    else:
        st.error("Combinación de factores y niveles no soportada en este ejemplo simplificado.")
        return None

def calculate_sn_ratio(results, characteristic):
    if characteristic == "Nominal es mejor":
        mean = np.mean(results)
        variance = np.var(results)
        return 10 * np.log10((mean**2) / variance)
    elif characteristic == "Menor es mejor":
        return -10 * np.log10(np.mean(np.array(results)**2))
    elif characteristic == "Mayor es mejor":
        return -10 * np.log10(np.mean(1 / np.array(results)**2))

def calculate_main_effects(matrix, results, num_factors, num_levels):
    effects = []
    for factor in range(num_factors):
        effect = []
        for level in range(1, num_levels + 1):
            mask = matrix[factor] == level
            effect.append(np.mean([r for m, r in zip(mask, results) if m]))
        effects.append(effect)
    return effects
