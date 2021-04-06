# Copyright (C) 2015  Base4 Sistemas Ltda ME
# Copyright (C) 2020  Luis Felipe Mileo - KMEE
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

import re

from ..misc import modulo11
from ..misc import punctuation_rm
from . import cnpj_cpf

EDOC_PREFIX = {
    '55': 'NFe',
    '57': 'CTe',
    '58': 'MDFe',
    '59': 'CFe',
    '65': 'NFe',
}


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

        NFe  35 2103 20695448000184 55 001 000003589 1 98183992 3
    """
    CHAVE_REGEX = re.compile(r'^(CFe|NFe|CTe|MDFe)(?P<campos>\d{44})$')

    CUF = slice(0, 2)
    AAMM = slice(2, 6)
    CNPJ = slice(6, 20)
    MODELO = slice(20, 22)
    SERIE = slice(22, 25)
    NUMERO = slice(25, 34)
    FORMA = slice(34, 35)
    CODIGO = slice(35, 43)
    DV = slice(43, None)

    def __init__(self, chave=False, codigo_uf=False, ano_mes=False, cnpj_emitente=False, modelo_documento=False,
                 numero_serie=False, numero_documento=False, forma_emissao=1):

        if not chave:
            if not (codigo_uf and ano_mes and cnpj_emitente and modelo_documento and numero_documento and
                    numero_documento and forma_emissao):
                raise ValueError('Impossível gerar a chave!!')

            campos = str(codigo_uf).zfill(2)

            campos += ano_mes

            campos += str(punctuation_rm(cnpj_emitente)).zfill(14)
            campos += str(modelo_documento).zfill(2)
            campos += str(numero_serie).zfill(3)
            campos += str(numero_documento).zfill(9)

            #
            # A inclusão do tipo de emissão na chave já torna a chave válida
            # também para a versão 2.00 da NF-e
            #
            campos += str(forma_emissao).zfill(1)

            #
            # O código numério é um número aleatório
            #
            # chave += str(random.randint(0, 99999999)).strip().rjust(8, '0')

            #
            # Mas, por segurança, é preferível que esse número não seja
            # aleatório
            #
            soma = 0
            for c in campos:
                soma += int(c) ** 3 ** 2

            codigo = str(soma)
            if len(codigo) > 8:
                codigo = codigo[-8:]
            else:
                codigo = codigo.rjust(8, "0")

            campos += codigo

            soma = 0
            m = 2
            for i in range(len(campos) - 1, -1, -1):
                c = campos[i]
                soma += int(c) * m
                m += 1
                if m > 9:
                    m = 2

            digito = 11 - (soma % 11)
            if digito > 9:
                digito = 0
            campos += str(digito)
            self.campos = campos
            self.prefixo = EDOC_PREFIX[self.modelo_documento]
            self.chave = self.prefixo + self.campos
        else:
            matcher = ChaveEdoc.CHAVE_REGEX.match(chave)
            if matcher:
                campos = matcher.group('campos')
            if not matcher or not campos:
                raise ValueError('Chave de acesso invalida: {!r}'.format(chave))
            self.chave = chave
            self.prefixo, self.campos = self.prefixo_campos(chave)
        self.validar()

    def validar(self):
        digito = modulo11(self.campos[:43])
        if not (digito == int(self.campos[-1])):
            raise ValueError((
                    'Digito verificador invalido: '
                    'chave={!r}, digito calculado={!r}'
                ).format(self.chave, digito))

        # if not br.is_codigo_uf(int(self.campos[ChaveEdoc.CUF])):
        #     raise ValueError((
        #             'Chave de acesso invalida (codigo UF: {!r}): {!r}'
        #         ).format(self.campos[ChaveEdoc.CUF], chave))

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

    @staticmethod
    def prefixo_campos(chave):
        matcher = ChaveEdoc.CHAVE_REGEX.match(chave)
        if matcher:
            campos = matcher.group('campos')
        if not matcher or not campos:
            raise ValueError('Chave de acesso invalida: {!r}'.format(chave))
        return False, campos

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
