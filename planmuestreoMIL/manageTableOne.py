import pandas as pd

from planmuestreoCameron.muestreoSimple import buscarElMinimo


def search_index(list_f, value):
    index = 0
    for i in range(len(list_f)):
        if value >= list_f[i][0] and value <= list_f[i][1] :
            index = i
            break
    return index


def getLevelInspect(size_l, lvl_inspect):
    df = pd.read_csv("./assets/MILSTD414.csv")

    listMins = list(df["min"])
    listMaxs = list(df["max"])
    thelist = list(zip(listMins, listMaxs))
    theindex = search_index(thelist, size_l)

    level = df.loc[theindex, str(lvl_inspect)]
    return level

def getM_Value(letter: str, NCA:str, type_inspeccion: str):
    df = None
    if type_inspeccion == "normal":
        df = pd.read_csv("./assets/inspeccion_normal.csv", index_col=0)
    else:
        df = pd.read_csv("./assets/inspeccion_severa.csv", index_col=0)
    
    M_value = df.loc[letter, NCA]
    sample_size = df.loc[letter, "size"]
    return M_value, sample_size

def getP_ZTable(size_sample, prob):
    print(size_sample, prob)
    df = pd.read_csv("./assets/tabla_muestra_desviacion.csv")
    # print(df)
    thelist = list(df["z"])
    index, dif = buscarElMinimo(thelist, prob)
    prob_table = None
    try:
        prob_table = df.loc[index, str(size_sample)]
    except Exception as e:
        print("Hay un error en ", str(e))
    return prob_table

# print(getP_ZTable("40", 2.312))






# print(getM_Value("L", "1-000","normal"))

    
        

# print(getLevelInspect(3000,"IV"))

