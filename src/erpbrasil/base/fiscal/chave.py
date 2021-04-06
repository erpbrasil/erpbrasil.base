# Copyright (C) 2015  Base4 Sistemas Ltda ME
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re
from ..misc import modulo11
from . import cnpj_cpf


class ChaveEdoc(object):
    """
    Inspired on

    https://github.com/base4sistemas/satcomum/blob/f45da5b100a63511b9c455cbd6895b630e121866/satcomum/ersat.py


             0  2    6             20  22  25        34 35      43  --> índice
             |  |    |              |  |   |         | |        |
        MDFe 50 1312 48740351011795 58 000 149000153 1 16261964 8
             |  |    |              |  |   |         | |        |
        CTe  32 1712 32438772000104 57 001 000199075 1 39868226 3
             |  |    |              |  |   |         | |        |
        NFe  43 1402 01098983010680 65 796 000000599 1 31447746 1 #NFC-e
             |  |    |              |  |   |         | |        |
        CFe  35 1508 08723218000186 59 900 004019000 0 24111425 7
    """
    CHAVE_REGEX = re.compile(r'^(CFe|NFe|CTe|MDFe)(?P<campos>\d{44})$')

    CUF = slice(0, 2)
    AAMM = slice(2, 6)
    CNPJ = slice(6, 20)
    MODELO = slice(20, 22)
    SERIE = slice(22, 24)
    NUMERO = slice(24, 33)
    FORMA = slice(33, 34)
    CODIGO = slice(34, 43)
    DV = slice(43, None)

    def __init__(self, chave=False):
        if chave:
            self.chave = chave
            self.prefixo, self.campos = self.prefixo_campos(chave)
            self.validar()
        else:
            pass

    @staticmethod
    def prefixo_campos(chave):
        matcher = ChaveEdoc.CHAVE_REGEX.match(chave)
        if matcher:
            campos = matcher.group('campos')
        if not matcher or not campos:
            raise ValueError('Chave de acesso invalida: {!r}'.format(chave))
        return False, campos

    def validar(self):
        digito = modulo11(self.campos[:43])
        if not (digito == int(self.campos[-1])):
            raise ValueError((
                    'Digito verificador invalido: '
                    'chave={!r}, digito calculado={!r}'
                ).format(self.chave, digito))

        # if not br.is_codigo_uf(int(campos[ChaveEdoc.CUF])):
        #     raise ValueError((
        #             'Chave de acesso invalida (codigo UF: {!r}): {!r}'
        #         ).format(campos[ChaveEdoc.CUF], chave))

        if self.campos[ChaveEdoc.MODELO] not in ('55', '57', '58', '59', '65'):
            raise ValueError((
                'Chave de acesso invalida '
                '(Modelos não permitidos: {!r}): {!r}'
                ).format(self.campos[ChaveEdoc.MODELO], self.chave))

        if not cnpj_cpf.validar(self.campos[ChaveEdoc.CNPJ]):
            raise ValueError((
                    'Chave de acesso invalida '
                    '(CNPJ emitente: {!r}): {!r}'
                ).format(self.campos[ChaveEdoc.CNPJ], self.chave))

    def __str__(self):
        return self.chaveMOD

    def __repr__(self):
        return '{:s}({!r})'.format(self.__class__.__name__, self._chave)

    @property
    def chave(self):
        return self._chave

    @chave.setter
    def chave(self, value):
        self._chave = value

    @property
    def campos(self):
        return self._campos

    @campos.setter
    def campos(self, value):
        self._campos = value

    @property
    def codigo_uf(self):
        return int(self._campos[ChaveEdoc.CUF])

    @property
    def ano_mes(self):
        return self._campos[ChaveEdoc.AAMM]

    @property
    def ano_emissao(self):
        return int(self._campos[ChaveEdoc.AAMM][:2]) + 2000

    @property
    def mes_emissao(self):
        return int(self._campos[ChaveEdoc.AAMM][2:])

    @property
    def cnpj_emitente(self):
        return cnpj_cpf.formata(self._campos[ChaveEdoc.CNPJ])

    @property
    def modelo_documento(self):
        return self._campos[ChaveEdoc.MODELO]

    @property
    def numero_serie(self):
        return self._campos[ChaveEdoc.SERIE]

    @property
    def numero_documento(self):
        return self._campos[ChaveEdoc.NUMERO]

    @property
    def forma_emissao(self):
        return self._campos[ChaveEdoc.FORMA]

    @property
    def codigo_aleatorio(self):
        return self._campos[ChaveEdoc.CODIGO]

    @property
    def digito_verificador(self):
        return self._campos[ChaveEdoc.DV]

    def partes(self, num_partes=11):
        assert 44 % num_partes == 0, (
            'O numero de partes nao produz um resultado inteiro (partes '
            'por 44 digitos): num_partes={!r}'
        ).format(num_partes)

        salto = 44 // num_partes
        return [self._campos[n:(n + salto)] for n in range(0, 44, salto)]
