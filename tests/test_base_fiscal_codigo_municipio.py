# Copyright (C) 2023  Pablo Matos - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import unittest
import re

from erpbrasil.base.fiscal import codigo_municipio

CODIGOS_MUNICIPAIS_VALIDOS = ['2700102', '2700201', '2700300', '2700409', '2700508', '2700607',
                              '2700706', '2700805', '2700904', '2701001', '2701100', '2701209', '2701308']

CODIGOS_MAIORES = ['2700102330', '27002010', '27003000', '270333304090', '27005080', '27006070',
                   '270207060', '2704444444444408050', '27009040', '27044410010', '27011000', '27012090', '27013080']

CODIGOS_MENORES = ['7201', '70300', '700409', '7', '700607',
                   '700706', '70805', '0904', '701001', '7100', '01209', '08']

CODIGOS_UF_INVALIDOS = ['9900102', '9800201', '9700300', '9600409', '6600508', '6700607',
                        '8700706', '8800805', '8500904', '9301001', '0101100', '0701209', '8301308']

CODIGOS_ORDEM_INVALIDOS = ['2700002', '2700001', '2700000', '2700009', '2700008', '2700007',
                           '2700006', '2700005', '2700004', '2700001', '2700000', '2700009', '2700008']

CODIGOS_MUNICIPAIS_INVALIDOS = CODIGOS_MAIORES + CODIGOS_MENORES + \
    CODIGOS_UF_INVALIDOS + CODIGOS_ORDEM_INVALIDOS

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

CODIGOS_MUNICIPAIS_SEM_FORMATACAO = ['2 7 0 0 1 0 2', '2-7-0-0-2-0-1', '270ASD030ASDDA0', '2700409', '2700508', '2700607',
                              '27/00/706', 2700805, '2.7.0.0.9.0.4', '270   1001', '270(1)100', '(2701209)', '2701308']

class Tests(unittest.TestCase):

    def testCodigoValido(self):
        # Caso o codigo seja do tipo String:
        for codigo in CODIGOS_MUNICIPAIS_VALIDOS:
            with self.subTest(codigo=codigo):
                self.assertTrue(
                    codigo_municipio.validar_codigo_municipio(codigo))

        # Caso o codigo seja do tipo Inteiro:
        for codigo in CODIGOS_MUNICIPAIS_VALIDOS:
            with self.subTest(codigo=int(codigo)):
                self.assertTrue(
                    codigo_municipio.validar_codigo_municipio(codigo))

    def testCodigoInvalido(self):
        # Caso o codigo seja do tipo String:
        for codigo in CODIGOS_MUNICIPAIS_INVALIDOS:
            with self.subTest(codigo=codigo):
                self.assertFalse(
                    codigo_municipio.validar_codigo_municipio(codigo))

        # Caso o codigo seja do tipo Inteiro:
        for codigo in CODIGOS_MUNICIPAIS_INVALIDOS:
            with self.subTest(codigo=int(codigo)):
                self.assertFalse(
                    codigo_municipio.validar_codigo_municipio(codigo))

    def testExcecao(self):
        # Caso o codigo seja do tipo String:
        for codigo in EXCECOES.keys():
            with self.subTest(codigo=codigo):
                self.assertTrue(
                    codigo_municipio.validar_codigo_municipio(codigo))

        # Caso o codigo seja do tipo Inteiro:
        for codigo in EXCECOES.keys():
            with self.subTest(codigo=int(codigo)):
                self.assertTrue(
                    codigo_municipio.validar_codigo_municipio(codigo))

    def testCodigoTamanhoValido(self):

        for codigo in CODIGOS_MUNICIPAIS_VALIDOS:
            with self.subTest(codigo=codigo):
                self.assertTrue(codigo_municipio._validar_tamanho(codigo))

    def testCodigoMaior(self):

        for codigo in CODIGOS_MAIORES:
            with self.subTest(codigo=codigo):
                self.assertFalse(codigo_municipio._validar_tamanho(codigo))

    def testCodigoMenor(self):

        for codigo in CODIGOS_MENORES:
            with self.subTest(codigo=codigo):
                self.assertFalse(codigo_municipio._validar_tamanho(codigo))

    def testCodigoDeEstado(self):

        for codigo in CODIGOS_MUNICIPAIS_VALIDOS:
            with self.subTest(codigo=codigo):
                self.assertTrue(
                    codigo_municipio._validar_codigo_de_estado(codigo))

    def testCodigoDeEstadoInvalido(self):

        for codigo in CODIGOS_UF_INVALIDOS:
            with self.subTest(codigo=codigo):
                self.assertFalse(
                    codigo_municipio._validar_codigo_de_estado(codigo))

    def testNumeroDeOrdemValido(self):

        for codigo in CODIGOS_MUNICIPAIS_VALIDOS:
            with self.subTest(codigo=codigo):
                self.assertTrue(
                    codigo_municipio._validar_numero_de_ordem(codigo))

    def testNumeroDeOrdemInvalido(self):

        for codigo in CODIGOS_ORDEM_INVALIDOS:
            with self.subTest(codigo=codigo):
                self.assertFalse(
                    codigo_municipio._validar_numero_de_ordem(codigo))

    def testDigitoDeControleValido(self):

        for codigo in CODIGOS_MUNICIPAIS_VALIDOS:
            with self.subTest(codigo=codigo):
                self.assertTrue(
                    codigo_municipio._validar_digito_de_controle(codigo))
                
    def testFormatarCodigoMunicipio(self):

        for codigo in CODIGOS_MUNICIPAIS_SEM_FORMATACAO:
            with self.subTest(codigo=codigo):
                resultado = codigo_municipio.formatar_codigo_municipio(codigo)
                esperado = re.sub(r"\D", "", str(codigo))
                self.assertEqual(resultado, esperado)

if __name__ == '__main__':
    unittest.main()

