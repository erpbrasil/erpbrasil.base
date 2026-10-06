# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from unittest import TestCase, mock

from erpbrasil.base.fiscal.edoc import ChaveEdoc, detectar_chave_edoc
from erpbrasil.base.misc import modulo11

RANDBELOW = "erpbrasil.base.fiscal.edoc.secrets.randbelow"

CAMPOS_NFE = dict(
    codigo_uf=35,
    ano_mes="2103",
    cnpj_cpf_emitente="20.695.448/0001-84",
    modelo_documento="55",
    numero_serie="001",
    numero_documento="000003589",
    forma_emissao=1,
)

# 43 primeiros caracteres sem o cNF: cUF, AAMM, CNPJ, mod, serie, nNF, tpEmis
PREFIXO_NFE = "35210320695448000184550010000035891"


class TestCodigoAleatorio(TestCase):
    def test_codigo_vem_do_secrets_no_tamanho_do_campo(self):
        with mock.patch(RANDBELOW, return_value=4711) as randbelow:
            chave = ChaveEdoc(**CAMPOS_NFE)
        randbelow.assert_called_once_with(10**8)
        self.assertEqual(chave.codigo_aleatorio, "00004711")
        self.assertEqual(
            chave.chave,
            PREFIXO_NFE + "00004711" + str(modulo11(PREFIXO_NFE + "00004711")),
        )

    def test_chave_gerada_e_valida(self):
        chave = ChaveEdoc(**CAMPOS_NFE)
        self.assertEqual(len(chave.chave), 44)
        self.assertEqual(len(chave.codigo_aleatorio), 8)
        self.assertTrue(chave.codigo_aleatorio.isdigit())
        self.assertEqual(chave.chave[:35], PREFIXO_NFE)
        self.assertEqual(int(chave.digito_verificador), modulo11(chave.chave[:43]))
        self.assertEqual(detectar_chave_edoc(chave.chave).chave, chave.chave)

    def test_mesmos_campos_nao_repetem_codigo(self):
        with mock.patch(RANDBELOW, side_effect=[48213907, 70512346]):
            chave_1 = ChaveEdoc(**CAMPOS_NFE)
            chave_2 = ChaveEdoc(**CAMPOS_NFE)
        self.assertEqual(chave_1.codigo_aleatorio, "48213907")
        self.assertEqual(chave_2.codigo_aleatorio, "70512346")
        self.assertNotEqual(chave_1.chave, chave_2.chave)
        # Sem mock: o código não é mais derivado dos campos
        codigos = {ChaveEdoc(**CAMPOS_NFE).codigo_aleatorio for _ in range(20)}
        self.assertGreater(len(codigos), 1)

    def test_codigo_nunca_igual_ao_numero_do_documento(self):
        # Primeira tentativa colide com o nNF 3589: deve ser descartada
        with mock.patch(RANDBELOW, side_effect=[3589, 61724053]) as randbelow:
            chave = ChaveEdoc(**CAMPOS_NFE)
        self.assertEqual(randbelow.call_count, 2)
        self.assertEqual(chave.codigo_aleatorio, "61724053")

    def test_codigo_descarta_valores_da_rejeicao_897(self):
        # NT 2019.001, RV B03-10: digitos iguais e sequencias crescentes
        proibidos = [0, 11111111, 99999999, 12345678, 90123456, 1234567]
        with mock.patch(RANDBELOW, side_effect=[*proibidos, 52806143]) as randbelow:
            chave = ChaveEdoc(**CAMPOS_NFE)
        self.assertEqual(randbelow.call_count, len(proibidos) + 1)
        self.assertEqual(chave.codigo_aleatorio, "52806143")

    def test_codigo_informado_pelo_chamador_nao_muda(self):
        with mock.patch(RANDBELOW) as randbelow:
            chave = ChaveEdoc(codigo_aleatorio="98183992", **CAMPOS_NFE)
        randbelow.assert_not_called()
        self.assertEqual(chave.chave, "35210320695448000184550010000035891981839923")

    def test_calculo_legado_continua_disponivel(self):
        chave = ChaveEdoc(codigo_aleatorio="98183992", **CAMPOS_NFE)
        self.assertEqual(chave.calculo_codigo_aleatorio(PREFIXO_NFE), "98183992")
