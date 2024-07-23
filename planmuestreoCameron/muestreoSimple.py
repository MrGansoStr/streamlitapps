import pandas as pd


def calc_razon_operacion(NCA, NCL):
    p1 = NCA / 100
    p2 = NCL / 100

    return p2 / p1


# NCA = 0.4
# alpha = 0.05
# NCL = 2.5
# beta = 0.10

# print(calc_razon_operacion(NCA, NCL))

def buscarElMinimo(thelist, value_to_search):
    newlist = []

    for i in range(0, len(thelist)):
        newlist.append((i, abs(thelist[i] - value_to_search)))
    
    newlist.sort(key=lambda x: x[1])
    return newlist[0]
    

def buscarEnTabla(alpha, beta, NCA_f, NCL_f):
    df = None
    if str(alpha).replace(".", "-") == "0-05":
        df = pd.read_csv("./assets/R1.csv")
    else:
        df = pd.read_csv("./assets/R2.csv")
    beta = str("{:.2f}".format(beta)).replace(".", "-")

    thelist = list(df[beta])
    razon_operacion = calc_razon_operacion(NCA_f, NCL_f)
    # print(alpha, beta, NCA_f, NCL_f, razon_operacion)

    index, dif = buscarElMinimo(thelist, razon_operacion)
    np_value = df.iloc[index, 4]
    c_value = df.iloc[index, 0]
    # print(np_value, c_value, "ga")
    return np_value, c_value

# np_value, c_value = buscarEnTabla(alpha, beta, NCA, NCL)
# print(np_value, c_value)

# size_sample = np_value / (NCA/100)
# print(size_sample)
# print(buscarElMinimo([1, 3, 2, 6, 4, 2, 9, 10], 3))