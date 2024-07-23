import numpy as np
import pandas as pd
from scipy import stats

def hotelling_t2_control_chart(data, alpha = 0.9973):
    mean = np.mean(data, axis=0)
    cov = np.cov(data.T)
    t2 = []
    for row in data:
        t2.append(np.dot(np.dot((row - mean), np.linalg.inv(cov)), (row - mean).T))
    ucl = stats.f.ppf(alpha, len(mean), len(data) - len(mean)) * \
          ((len(data) - 1) * len(mean) / (len(data) - len(mean))) * \
          ((len(data) + 1) / len(data))
    listTvalues = pd.DataFrame(t2, columns=["T2"])
    # listTvalues["T2"] = t2
    return listTvalues, ucl, np.mean(mean)
"""
fuente https://www.redalyc.org/journal/404/40471792002/html/
"""
def calculate_LCS(data_frame: pd.DataFrame, alpha):
    p = len(data_frame.columns) # Numero de variables
    size_sample = data_frame.shape[0]
    F_value = stats.f.isf(0.01, p, size_sample - p)
    LCS = ((p * (size_sample + 1)) * (size_sample - 1)) / (size_sample * (size_sample - p))
    # print(F_value, LCS  )
    return LCS * F_value


