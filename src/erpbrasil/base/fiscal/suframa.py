# Copyright (C) 2023  Breno Dias - KMEE
# License MIT - See https://opensource.org/license/mit

def validar(suframa):
    if not suframa.isdigit():
        return False
    if len(suframa) < 8:
        suframa.zfill(8)

    suframa = [int(suframaList) for suframaList in str(suframa)]

    if suframa[0:2] == [0, 0]:
        return False

    return VerifDig(suframa)


def VerifDig(suframa):
    verificador = 0
    pesos = [9, 8, 7, 6, 5, 4, 3, 2]

    for x, cod in enumerate(suframa[:-1]):
        verificador += pesos[x] * cod
    resto = verificador % 11

    if (resto == 1 or resto == 0):
        verificador = 0
    else:
        verificador = 11 - resto
    if verificador == suframa[-1]:
        return True
    else:
        return False

