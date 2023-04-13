# coding=utf-8
# @ 2017 Akretion - www.akretion.com.br -
#   Clément Mombereau <clement.mombereau@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from unittest import TestCase

from erpbrasil.base.fiscal import ie

# Create a dictionary with a list of invalid inscr_est for each state
invalid_ie = {
    "ac": [
        "0102190200161",
        "0101296300282",
        "0100258700141",
        "0101296300101",
        "0101613200121",
        "0100662000131",
        "01006620001310",
    ],
    "al": [
        "241065551",
        "248501412",
        "240916422",
        "248540982",
        "248429982",
        "246014341",
        "2460143410",
    ],
    "am": [
        "042933681",
        "041330181",
        "042357072",
        "042338961",
        "042215381",
        "042201621",
        "0422016210",
    ],
    "ap": ["030380341", "030317542", "030273465", "030132818", "030069281"],
    "ba": ["41902652", "77893322", "51153772", "14621861", "09874625", "098746250"],
    "ce": [
        "063873771",
        "061876641",
        "062164251",
        "061970361",
        "061880991",
        "069108591",
        "0691085910",
    ],
    "df": [
        "0732709900171",
        "0730562700171",
        "0751504400161",
        "0744409300181",
        "0748774800131",
        "0747987900101",
        "07479879001010",
        "0803592300143",
    ],
    "es": [
        "082376121",
        "082106021",
        "082467671",
        "082169711",
        "082585301",
        "082588571",
        "0825885710",
    ],
    "go": [
        "103450591",
        "104197631",
        "104345191",
        "104455571",
        "104555271",
        "1045552710",
    ],
    "ma": [
        "121498291",
        "122045040",
        "123214281",
        "123110131",
        "123170521",
        "121530061",
        "1215300610",
    ],
    "mg": [
        "2615950220091",
        "7000547460061",
        "3519900270001",
        "0621828520091",
        "5780297160001",
        "0620297160291",
        "06202971602910",
    ],
    "ms": [
        "283370641",
        "283238931",
        "283235561",
        "283167161",
        "283267081",
        "283352121",
        "2833521210",
    ],
    "mt": [
        "00133337411",
        "00133110021",
        "00132040541",
        "00133095611",
        "00132390321",
        "00131235461",
        "00132465711",
        "001324657110",
    ],
    "pa": [
        "151925940",
        "152336261",
        "152355651",
        "151386350",
        "153646720",
        "152346911",
        "1523469110",
    ],
    "pb": [
        "161435941",
        "161462711",
        "161455741",
        "161349241",
        "161427451",
        "160506321",
        "1605063210",
    ],
    "pr": [
        "4100161411",
        "9020581251",
        "1011473550",
        "1010586971",
        "9053527171",
        "90535271710",
    ],
    "pe": [
        "027693361",
        "18171203059321",
        "029748001",
        "18171001920080",
        "030374521",
        "0303745210",
    ],
    "pi": [
        "169609151",
        "194549991",
        "194661051",
        "194507681",
        "194010401",
        "1940104010",
    ],
    "rj": [
        "78890161",
        "78724991",
        "78205351",
        "85190880",
        "78860051",
        "78873651",
        "788736510",
    ],
    "rn": [
        "200887891",
        "200395141",
        "200653011",
        "201199350",
        "2074337761",
        "2010665161",
        "2075778441",
        "20757784410",
    ],
    "rs": [
        "0240130110",
        "0963376211",
        "0290289001",
        "1240237331",
        "0570120201",
        "0962655441",
        "0962003671",
        "09620036710",
    ],
    "ro": [
        "00000001656551",
        "00000001499391",
        "00000001727111",
        "00000002999271",
        "00000001765930",
        "000000017659301",
    ],
    "rr": [
        "240151301",
        "240042101",
        "240128121",
        "240146371",
        "240018111",
        "240106211",
        "240003911",
        "2400039110",
    ],
    "sc": [
        "255830691",
        "253952661",
        "253967621",
        "254086581",
        "252625081",
        "251083111",
        "251130481",
        "2511304810",
    ],
    "sp": [
        "692015742111",
        "645274188111",
        "645169551111",
        "649005952110",
        "645098352111",
        "6450983521110",
    ],
    "se": [
        "271126971",
        "271233641",
        "271200631",
        "270622021",
        "271307981",
        "2713079810",
    ],
    "to": [
        "290921014",
        "293799491",
        "290737544",
        "990655293",
        "693742782",
        "6937427820",
    ],
}

# Create a dictionary with a list of valid inscr_est for each state
valid_ie = {
    "ac": [
        "0102190200165",
        "0101296300289",
        "0100258700145",
        "0101296300106",
        "0101613200122",
        "0100662000133",
    ],
    "al": [
        "241065550",
        "248501410",
        "240916425",
        "248540980",
        "248429981",
        "246014342",
    ],
    "am": [
        "042933684",
        "041330188",
        "042357071",
        "042338964",
        "042215382",
        "042201624",
    ],
    "ap": ["030380340", "030317541", "030273455", "030131818", "030069381"],
    "ba": ["41902653", "77893325", "51153771", "14621862", "09874624"],
    "ce": [
        "063873770",
        "061876640",
        "062164252",
        "061970360",
        "061880990",
        "069108595",
    ],
    "df": [
        "0732709900174",
        "0730562700176",
        "0751504400168",
        "0744409300183",
        "0748774800134",
        "0747987900103",
        "0803592300140",
    ],
    "es": [
        "082376123",
        "082106029",
        "082467676",
        "082169713",
        "082585300",
        "082588570",
    ],
    "go": ["103450599", "104197633", "104345195", "104455578", "104555270"],
    "ma": [
        "121498298",
        "122045041",
        "123214289",
        "123110130",
        "123170524",
        "121530060",
    ],
    "mg": [
        "2615950220092",
        "7000547460067",
        "3519900270005",
        "0621828520097",
        "5780297160005",
        "0620297160299",
    ],
    "ms": [
        "283370645",
        "283238933",
        "283235560",
        "283167165",
        "283267089",
        "283352124",
    ],
    "mt": [
        "00133337413",
        "00133110028",
        "00132040549",
        "00133095614",
        "00132390329",
        "00131235460",
        "00132465710",
    ],
    "pa": [
        "151925941",
        "152336265",
        "152355650",
        "151386358",
        "153646721",
        "152346910",
    ],
    "pb": [
        "161435947",
        "161462715",
        "161455743",
        "161349242",
        "161427456",
        "160506328",
    ],
    "pr": ["4100161414", "9020581252", "1011473551", "1010586972", "9053527172"],
    "pe": ["027693368", "18171203059328", "029748003", "18171001920081", "030374529"],
    "pi": ["169609154", "194549992", "194661059", "194507688", "194010406"],
    "rj": ["78890169", "78724994", "78205350", "85190881", "78860057", "78873655"],
    "rn": [
        "200887890",
        "200395149",
        "200653016",
        "201199351",
        "2074337760",
        "2010665163",
        "2075778442",
    ],
    "rs": [
        "0240130111",
        "0963376217",
        "0290289009",
        "1240237330",
        "0570120209",
        "0962655449",
        "0962003670",
    ],
    "ro": [
        "00000001656554",
        "00000001499394",
        "00000001727117",
        "00000002999277",
        "00000001765931",
    ],
    "rr": [
        "240151303",
        "240042104",
        "240128125",
        "240146373",
        "240018116",
        "240106210",
        "240003910",
    ],
    "sc": [
        "255830696",
        "253952662",
        "253967627",
        "254086586",
        "252625080",
        "251083110",
        "251130487",
    ],
    "sp": [
        "692015742119",
        "645274188118",
        "645169551117",
        "649005952111",
        "645098352117",
    ],
    "se": ["271126973", "271233648", "271200634", "270622020", "271307986"],
    "to": ["290021014", "293799490", "290707544", "290655293", "293742782"],
}


class ValidateIETest(TestCase):
    def test_inscr_invalid(self):
        for est in invalid_ie:
            for inscr_est in invalid_ie[est]:
                self.assertFalse(
                    ie.validar(est, inscr_est), "Error on validate %s inscr_est" % est
                )

    def test_inscr_valid(self):
        for est in valid_ie:
            for inscr_est in valid_ie[est]:
                self.assertTrue(
                    ie.validar(est, inscr_est), "Error on validate %s inscr_est" % est
                )
