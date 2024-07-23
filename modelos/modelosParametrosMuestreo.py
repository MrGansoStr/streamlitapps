
# Proporciones

paramNConocidoProporciones = {
    'N': None,
    'Z': None,
    'P': None,
    'Q': None,
    'E': None
}

paramNDesconocidoProporciones = {
    'Z': None,
    'P': None,
    'Q': None,
    'E': None
}

# Con desviaciones

paramNDesconocidoD = {
    'Z': None,
    'S': None,
    'E': None,
}

paramNConocidoD = {
    'N': None,
    'Z': None,
    'S': None,
    'E': None,
}

def verificar_nones(d):
    for key, value in d.items():
        if value is None:
            print(f"El valor para la clave '{key}' es None")
            return False
    return True