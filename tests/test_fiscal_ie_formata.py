# coding=utf-8
# @ 2019 Akretion - www.akretion.com.br -
#   Clément Mombereau <clement.mombereau@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import TestCase

from erpbrasil.base.fiscal import ie

# IEs sem formação
ies_sem_formatacao = {
    'ac': ['0102190200165', '0101296300289', '0100258700145', '0101296300106',
           '0101613200122', '0100662000133'],
    'al': ['241065550', '248501410', '240916425', '248540980', '248429981',
           '246014342'],
    'am': ['042933684', '041330188', '042357071', '042338964', '042215382',
           '042201624'],
    'ap': ['030380340', '030317541', '030273455', '030131818', '030069381'],
    'ba': ['41902653', '77893325', '51153771', '14621862', '09874624'],
    'ce': ['063873770', '061876640', '062164252', '061970360', '061880990',
           '069108595'],
    'df': ['0732709900174', '0730562700176', '0751504400168', '0744409300183',
           '0748774800134', '0747987900103'],
    'es': ['082376123', '082106029', '082467676', '082169713', '082585300',
           '082588570'],
    'go': ['103450599', '104197633', '104345195', '104455578', '104555270'],
    'ma': ['121498298', '122045041', '123214289', '123110130', '123170524',
           '121530060'],
    'mg': ['2615950220092', '7000547460067', '3519900270005', '0621828520097',
           '5780297160005', '0620297160299'],
    'ms': ['283370645', '283238933', '283235560', '283167165', '283267089',
           '283352124'],
    'mt': ['00133337413', '00133110028', '00132040549', '00133095614',
           '00132390329', '00131235460', '00132465710'],
    'pa': ['151925941', '152336265', '152355650', '151386358', '153646721',
           '152346910'],
    'pb': ['161435947', '161462715', '161455743', '161349242', '161427456',
           '160506328'],
    'pr': ['4100161414', '9020581252', '1011473551', '1010586972',
           '9053527172'],
    'pe': ['027693368', '18171203059328', '029748003', '18171001920081',
           '030374529'],
    'pi': ['169609154', '194549992', '194661059', '194507688', '194010406'],
    'rj': ['78890169', '78724994', '78205350', '85190881', '78860057',
           '78873655'],
    'rn': ['200887890', '200395149', '200653016', '201199351', '2074337760',
           '2010665163', '2075778442'],
    'rs': ['0240130111', '0963376217', '0290289009', '1240237330',
           '0570120209', '0962655449', '0962003670'],
    'ro': ['00000001656554', '00000001499394', '00000001727117',
           '00000002999277', '00000001765931'],
    'rr': ['240151303', '240042104', '240128125', '240146373', '240018116',
           '240106210', '240003910'],
    'sc': ['255830696', '253952662', '253967627', '254086586', '252625080',
           '251083110', '251130487'],
    'sp': ['692015742119', '645274188118', '645169551117', '649005952111',
           '645098352117'],
    'se': ['271126973', '271233648', '271200634', '270622020', '271307986'],
    'to': ['290021014', '293799490', '290707544', '290655293', '293742782']
}

ies_formatadas = {
    'ac': ['01.021.902/001-65', '01.012.963/002-89', '01.002.587/001-45',
           '01.012.963/001-06', '01.016.132/001-22', '01.006.620/001-33'],
    'al': ['24.106.555-0', '24.850.141-0', '24.091.642-5', '24.854.098-0',
           '24.842.998-1', '24.601.434-2'],
    'am': ['04.293.368-4', '04.133.018-8', '04.235.707-1', '04.233.896-4',
           '04.221.538-2', '04.220.162-4'],
    'ap': ['03.038.034-0', '03.031.754-1', '03.027.345-5', '03.013.181-8',
           '03.006.938-1'],
    'ba': ['041.902.653', '077.893.325', '051.153.771', '014.621.862',
           '009.874.624'],
    'ce': ['06.387377-0', '06.187664-0', '06.216425-2', '06.197036-0',
           '06.188099-0', '06.910859-5'],
    'df': ['07-327.099/001-74', '07-305.627/001-76', '07-515.044/001-68',
           '07-444.093/001-83', '07-487.748/001-34', '07-479.879/001-03'],
    'es': ['082.376.12-3', '082.106.02-9', '082.467.67-6', '082.169.71-3',
           '082.585.30-0', '082.588.57-0'],
    'go': ['10.345.059-9', '10.419.763-3', '10.434.519-5', '10.445.557-8',
           '10.455.527-0'],
    'ma': ['12.149.829-8', '12.204.504-1', '12.321.428-9', '12.311.013-0',
           '12.317.052-4', '12.153.006-0'],
    'mg': ['261.595.022/00-92', '700.054.746/00-67', '351.990.027/00-05',
           '062.182.852/00-97', '578.029.716/00-05', '062.029.716/02-99'],
    'ms': ['28.337.064-5', '28.323.893-3', '28.323.556-0', '28.316.716-5',
           '28.326.708-9', '28.335.212-4'],
    'mt': ['00.13.33.3741-3', '00.13.31.1002-8', '00.13.20.4054-9',
           '00.13.30.9561-4', '00.13.23.9032-9', '00.13.12.3546-0',
           '00.13.24.6571-0'],
    'pa': ['15.192.594-1', '15.233.626-5', '15.235.565-0', '15.138.635-8',
           '15.364.672-1', '15.234.691-0'],
    'pb': ['16.143.594-7', '16.146.271-5', '16.145.574-3', '16.134.924-2',
           '16.142.745-6', '16.050.632-8'],
    'pr': ['410.0161-41', '902.0581-25', '101.1473-55', '101.0586-97',
           '905.3527-17'],
    'pe': ['027693368', '18171203059328', '029748003', '18171001920081',
           '030374529'],
    'pi': ['16.960.915-4', '19.454.999-2', '19.466.105-9', '19.450.768-8',
           '19.401.040-6'],
    'rj': ['78.890.16-9', '78.724.99-4', '78.205.35-0', '85.190.88-1',
           '78.860.05-7', '78.873.65-5'],
    'rn': ['20.088.789-0', '20.039.514-9', '20.065.301-6', '20.119.935-1',
           '207.433.776-0', '201.066.516-3', '207.577.844-2'],
    'rs': ['024/013.011-1', '096/337.621-7', '029/028.900-9', '124/023.733-0',
           '057/012.020-9', '096/265.544-9', '096/200.367-0'],
    'ro': ['00000001656554', '00000001499394', '00000001727117',
           '00000002999277', '00000001765931'],
    'rr': ['24.015.130-3', '24.004.210-4', '24.012.812-5', '24.014.637-3',
           '24.001.811-6', '24.010.621-0', '24.000.391-0'],
    'sc': ['255.830.696', '253.952.662', '253.967.627', '254.086.586',
           '252.625.080', '251.083.110', '251.130.487'],
    'se': ['27.112.697-3', '27.123.364-8', '27.120.063-4', '27.062.202-0',
           '27.130.798-6'],
    'sp': ['692015742119', '645274188118', '645169551117', '649005952111',
           '645098352117'],
    'to': ['29.002.101-4', '29.379.949-0', '29.070.754-4', '29.065.529-3',
           '29.374.278-2']
}


class ValidateIETest(TestCase):

    def test_ie_formata(self):
        """Testa a formatação das IEs"""
        for uf in ies_sem_formatacao:
            for i in ies_sem_formatacao[uf]:
                self.assertTrue(
                    ie.formata(uf, i) in ies_formatadas[uf],
                    'Erro ao formatar inscrição estadual para a UF: %s' % uf)
