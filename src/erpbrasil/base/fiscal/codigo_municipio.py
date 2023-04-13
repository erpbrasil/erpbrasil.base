# Copyright (C) 2023  Pablo Matos - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re

CODIGOS_DE_ESTADO = {
    '11': 'Rondônia',
    '12': 'Acre',
    '13': 'Amazonas',
    '14': 'Roraima',
    '15': 'Pará',
    '16': 'Amapá',
    '17': 'Tocantins',
    '21': 'Maranhão',
    '22': 'Piauí',
    '23': 'Ceará',
    '24': 'Rio Grande do Norte',
    '25': 'Paraíba',
    '26': 'Pernambuco',
    '27': 'Alagoas',
    '28': 'Sergipe',
    '29': 'Bahia',
    '31': 'Minas Gerais',
    '32': 'Espírito Santo',
    '33': 'Rio de Janeiro',
    '35': 'São Paulo',
    '41': 'Paraná',
    '42': 'Santa Catarina',
    '43': 'Rio Grande do Sul',
    '50': 'Mato Grosso do Sul',
    '51': 'Mato Grosso',
    '52': 'Goiás',
    '53': 'Distrito Federal'
}

EXCECOES = {
    '9999999': 'EXTERIOR',
    '4305871': 'Coronel Barros/RS',
    '2201919': 'Bom Princípio do Piauí/PI',
    '2202251': 'Canavieira/PI',
    '2201988': 'Brejo do Piauí/PI',
    '2611533': 'Quixaba/PE',
    '3117836': 'Cônego Marinho/MG',
    '3152131': 'Ponto Chique/MG',
    '5203939': 'Buriti de Goiás/GO',
    '5203962': 'Buritinópolis/GO'
}

def _validar_tamanho(codigo_municipal):

    if len(codigo_municipal) != 7:
        return False

    return True

def _validar_codigo_de_estado(codigo_municipal):

    codigo_de_estado = codigo_municipal[:2]
    if codigo_de_estado not in CODIGOS_DE_ESTADO.keys():
        return False

    return True

def _validar_numero_de_ordem(codigo_municipal):

    numero_de_ordem = int(codigo_municipal[2:6])
    if numero_de_ordem == 0:
        return False

    return True

def _validar_digito_de_controle(codigo_municipal):

    '''
    -Dígito de Controle: módulo 10 (pesos 2 e 1)
    -Se o resto da divisão for zero, considerar o 
        dígito verificador igual a zero.
    '''

    pesos = [1, 2, 1, 2, 1, 2]
    soma = 0

    for i in range(len(pesos)):
        ponderacao = int(codigo_municipal[i]) * pesos[i]
        soma += (ponderacao // 10) + (ponderacao % 10)

    resto = soma % 10
    if resto == 0:
        digito_verificador = 0
        return int(codigo_municipal[-1]) == digito_verificador

    else:
        digito_verificador = 10 - resto

    return int(codigo_municipal[-1]) == digito_verificador

def validar_codigo_municipio(codigo_municipal):

    codigo_municipal = str(codigo_municipal)

    if codigo_municipal in EXCECOES.keys():
        return True

    if not (_validar_tamanho(codigo_municipal)):
        return False

    if not (_validar_codigo_de_estado(codigo_municipal)):
        return False

    if not (_validar_numero_de_ordem(codigo_municipal)):
        return False

    if not (_validar_digito_de_controle(codigo_municipal)):
        return False

    return True

def formatar_codigo_municipio(codigo_municipal):

    codigo_municipal = str(codigo_municipal)

    return re.sub(r"\D", "", codigo_municipal)

