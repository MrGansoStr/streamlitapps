# from modelos.modelosParametrosMuestreo import  paramNDesconocidoProporciones
# Tamaño Muestra 

# Para proporciones

from scipy import stats

# N Poblacional Conocido

def calcular_n_Proporcion(**kwargs):
    valores = kwargs
    # print(parameters['param2'])
    # print(kwargs.items())
    # N = valores['N']
    n = None
    try: 
        Z = valores['Z']
        P = valores['P']
        Q = valores['Q']
        E = valores['E']
        if 'N' in valores:
            N = valores['N']
            n = (N * pow(Z, 2) * P * Q) / ((N - 1) * pow(E, 2)  + pow(Z, 2) * P * Q)
        else:
            n = ((pow(Z, 2) * P * Q)) / (pow(E, 2))
    except Exception as e:
        print("Hubo un error ", str(e))


    return n


# Para desviaciones


def calcular_n_Desviacion(**kwargs):
    valores = kwargs
    n = None
    try:
        Z = valores['Z']
        E = valores['E']
        desv = valores['desv']
        if 'N' in valores:
            N = valores['N']
            n = (N * pow(Z, 2) * pow(desv, 2)) / ((N - 1) * pow(E, 2) + pow(Z, 2) * pow(desv, 2))
        else:
            n = pow((Z * desv) / E, 2)
    except Exception as e:
        print("Hubo un error en ", str(e))
    return n

# print(calcular_n_Proporcion(Z=1.88, P=0.01, Q=0.99, E=0.03, N=4000))
# print(calcular_n_Desviacion(Z=2.05, E=5, desv=8, N=9000))
# print(stats.binom.cdf(2, 120, 0.04))



