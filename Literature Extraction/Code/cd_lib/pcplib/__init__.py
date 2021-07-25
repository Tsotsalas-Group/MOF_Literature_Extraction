import pubchempy as pcp
import pandas as pd
from cd_tools import osvalkyrie as osv
import os
import re

elementTable = {'H': [1, 'hydrogen'], 'He': [2, 'helium'], 'Li': [3, 'lithium'], 'Be': [4, 'beryllium'],
                'B': [5, 'boron'], 'C': [6, 'carbon'], 'N': [7, 'nitrogen'], 'O': [8, 'oxygen'], 'F': [9, 'fluorine'],
                'Ne': [10, 'neon'], 'Na': [11, 'sodium'], 'Mg': [12, 'magnesium'], 'Al': [13, 'aluminium'],
                'Si': [14, 'silicon'], 'P': [15, 'phosphorus'], 'S': [16, 'sulfur'], 'Cl': [17, 'chlorine'],
                'Ar': [18, 'argon'], 'K': [19, 'potassium'], 'Ca': [20, 'calcium'], 'Sc': [21, 'scandium'],
                'Ti': [22, 'titanium'], 'V': [23, 'vanadium'], 'Cr': [24, 'chromium'], 'Mn': [25, 'manganese'],
                'Fe': [26, 'iron'], 'Co': [27, 'cobalt'], 'Ni': [28, 'nickel'], 'Cu': [29, 'copper'],
                'Zn': [30, 'zinc'], 'Ga': [31, 'gallium'], 'Ge': [32, 'germanium'], 'As': [33, 'arsenic'],
                'Se': [34, 'selenium'], 'Br': [35, 'bromine'], 'Kr': [36, 'krypton'], 'Rb': [37, 'rubidium'],
                'Sr': [38, 'strontium'], 'Y': [39, 'yttrium'], 'Zr': [40, 'zirconium'], 'Nb': [41, 'niobium'],
                'Mo': [42, 'molybdenum'], 'Tc': [43, 'technetium'], 'Ru': [44, 'ruthenium'], 'Rh': [45, 'rhodium'],
                'Pd': [46, 'palladium'], 'Ag': [47, 'silver'], 'Cd': [48, 'cadmium'], 'In': [49, 'indium'],
                'Sn': [50, 'tin'], 'Sb': [51, 'antimony'], 'Te': [52, 'tellurium'], 'I': [53, 'iodine'],
                'Xe': [54, 'xenon'], 'Cs': [55, 'caesium'], 'Ba': [56, 'barium'], 'La': [57, 'lanthanum'],
                'Ce': [58, 'cerium'], 'Pr': [59, 'praseodymium'], 'Nd': [60, 'neodymium'], 'Pm': [61, 'promethium'],
                'Sm': [62, 'samarium'], 'Eu': [63, 'europium'], 'Gd': [64, 'gadolinium'], 'Tb': [65, 'terbium'],
                'Dy': [66, 'dysprosium'], 'Ho': [67, 'holmium'], 'Er': [68, 'erbium'], 'Tm': [69, 'thulium'],
                'Yb': [70, 'ytterbium'], 'Lu': [71, 'lutetium'], 'Hf': [72, 'hafnium'], 'Ta': [73, 'tantalum'],
                'W': [74, 'tungsten'], 'Re': [75, 'rhenium'], 'Os': [76, 'osmium'], 'Ir': [77, 'iridium'],
                'Pt': [78, 'platinum'], 'Au': [79, 'gold'], 'Hg': [80, 'mercury'], 'Tl': [81, 'thallium'],
                'Pb': [82, 'lead'], 'Bi': [83, 'bismuth'], 'Po': [84, 'polonium'], 'At': [85, 'astatine'],
                'Rn': [86, 'radon'], 'Fr': [87, 'francium'], 'Ra': [88, 'radium'], 'Ac': [89, 'actinium'],
                'Th': [90, 'thorium'], 'Pa': [91, 'protactinium'], 'U': [92, 'uranium'], 'Np': [93, 'neptunium'],
                'Pu': [94, 'plutonium'], 'Am': [95, 'americium'], 'Cm': [96, 'curium'], 'Bk': [97, 'berkelium'],
                'Cf': [98, 'californium'], 'Es': [99, 'einsteinium'], 'Fm': [100, 'fermium'],
                'Md': [101, 'mendelevium'], 'No': [102, 'nobelium'], 'Lr': [103, 'lawrencium'],
                'Rf': [104, 'rutherfordium'], 'Db': [105, 'dubnium'], 'Sg': [106, 'seaborgium'],
                'Bh': [107, 'bohrium'], 'Hs': [108, 'hassium'], 'Mt': [109, 'meitnerium'], 'Ds': [110, 'darmstadtium'],
                'Rg': [111, 'roentgenium'], 'Cn': [112, 'copernicium'], 'Nh': [113, 'nihonium'],
                'Fl': [114, 'flerovium'], 'Mc': [115, 'moscovium'], 'Lv': [116, 'livermorium'],
                'Ts': [117, 'tennessine'], 'Og': [118, 'oganesson']}

ET_n2s = {'hydrogen': 'H', 'helium': 'He', 'lithium': 'Li', 'beryllium': 'Be', 'boron': 'B', 'carbon': 'C',
          'nitrogen': 'N', 'oxygen': 'O', 'fluorine': 'F', 'neon': 'Ne', 'sodium': 'Na', 'magnesium': 'Mg',
          'aluminium': 'Al', 'silicon': 'Si', 'phosphorus': 'P', 'sulfur': 'S', 'chlorine': 'Cl', 'argon': 'Ar',
          'potassium': 'K', 'calcium': 'Ca', 'scandium': 'Sc', 'titanium': 'Ti', 'vanadium': 'V', 'chromium': 'Cr',
          'manganese': 'Mn', 'iron': 'Fe', 'cobalt': 'Co', 'nickel': 'Ni', 'copper': 'Cu', 'zinc': 'Zn',
          'gallium': 'Ga', 'germanium': 'Ge', 'arsenic': 'As', 'selenium': 'Se', 'bromine': 'Br', 'krypton': 'Kr',
          'rubidium': 'Rb', 'strontium': 'Sr', 'yttrium': 'Y', 'zirconium': 'Zr', 'niobium': 'Nb', 'molybdenum': 'Mo',
          'technetium': 'Tc', 'ruthenium': 'Ru', 'rhodium': 'Rh', 'palladium': 'Pd', 'silver': 'Ag', 'cadmium': 'Cd',
          'indium': 'In', 'tin': 'Sn', 'antimony': 'Sb', 'tellurium': 'Te', 'iodine': 'I', 'xenon': 'Xe',
          'caesium': 'Cs', 'barium': 'Ba', 'lanthanum': 'La', 'cerium': 'Ce', 'praseodymium': 'Pr', 'neodymium': 'Nd',
          'promethium': 'Pm', 'samarium': 'Sm', 'europium': 'Eu', 'gadolinium': 'Gd', 'terbium': 'Tb',
          'dysprosium': 'Dy', 'holmium': 'Ho', 'erbium': 'Er', 'thulium': 'Tm', 'ytterbium': 'Yb', 'lutetium': 'Lu',
          'hafnium': 'Hf', 'tantalum': 'Ta', 'tungsten': 'W', 'rhenium': 'Re', 'osmium': 'Os', 'iridium': 'Ir',
          'platinum': 'Pt', 'gold': 'Au', 'mercury': 'Hg', 'thallium': 'Tl', 'lead': 'Pb', 'bismuth': 'Bi',
          'polonium': 'Po', 'astatine': 'At', 'radon': 'Rn', 'francium': 'Fr', 'radium': 'Ra', 'actinium': 'Ac',
          'thorium': 'Th', 'protactinium': 'Pa', 'uranium': 'U', 'neptunium': 'Np', 'plutonium': 'Pu',
          'americium': 'Am', 'curium': 'Cm', 'berkelium': 'Bk', 'californium': 'Cf', 'einsteinium': 'Es',
          'fermium': 'Fm', 'mendelevium': 'Md', 'nobelium': 'No', 'lawrencium': 'Lr', 'rutherfordium': 'Rf',
          'dubnium': 'Db', 'seaborgium': 'Sg', 'bohrium': 'Bh', 'hassium': 'Hs', 'meitnerium': 'Mt',
          'darmstadtium': 'Ds', 'roentgenium': 'Rg', 'copernicium': 'Cn', 'nihonium': 'Nh', 'flerovium': 'Fl',
          'moscovium': 'Mc', 'livermorium': 'Lv', 'tennessine': 'Ts', 'oganesson': 'Og'}

MET_n2s = {'lithium': 'Li', 'beryllium': 'Be', 'sodium': 'Na', 'magnesium': 'Mg', 'aluminium': 'Al', 'potassium': 'K',
           'calcium': 'Ca', 'scandium': 'Sc', 'titanium': 'Ti', 'vanadium': 'V', 'chromium': 'Cr', 'manganese': 'Mn',
           'iron': 'Fe', 'cobalt': 'Co', 'nickel': 'Ni', 'copper': 'Cu', 'zinc': 'Zn', 'gallium': 'Ga', 'germanium':
               'Ge', 'arsenic': 'As', 'rubidium': 'Rb', 'strontium': 'Sr', 'yttrium': 'Y', 'zirconium': 'Zr',
           'niobium': 'Nb', 'molybdenum': 'Mo', 'technetium': 'Tc', 'ruthenium': 'Ru', 'rhodium': 'Rh',
           'palladium': 'Pd', 'silver': 'Ag', 'cadmium': 'Cd', 'indium': 'In', 'tin': 'Sn', 'antimony': 'Sb',
           'caesium': 'Cs', 'barium': 'Ba', 'lanthanum': 'La', 'cerium': 'Ce', 'praseodymium': 'Pr', 'neodymium': 'Nd',
           'promethium': 'Pm', 'samarium': 'Sm', 'europium': 'Eu', 'gadolinium': 'Gd', 'terbium': 'Tb',
           'dysprosium': 'Dy', 'holmium': 'Ho', 'erbium': 'Er', 'thulium': 'Tm', 'ytterbium': 'Yb', 'lutetium': 'Lu',
           'hafnium': 'Hf', 'tantalum': 'Ta', 'tungsten': 'W', 'rhenium': 'Re', 'osmium': 'Os', 'iridium': 'Ir',
           'platinum': 'Pt', 'gold': 'Au', 'mercury': 'Hg', 'thallium': 'Tl', 'lead': 'Pb', 'bismuth': 'Bi',
           'polonium': 'Po', 'francium': 'Fr', 'radium': 'Ra', 'actinium': 'Ac', 'thorium': 'Th', 'protactinium': 'Pa',
           'uranium': 'U', 'neptunium': 'Np', 'plutonium': 'Pu', 'americium': 'Am', 'curium': 'Cm', 'berkelium': 'Bk',
           'californium': 'Cf', 'einsteinium': 'Es', 'fermium': 'Fm', 'mendelevium': 'Md', 'nobelium': 'No',
           'lawrencium': 'Lr', 'rutherfordium': 'Rf', 'dubnium': 'Db', 'seaborgium': 'Sg', 'bohrium': 'Bh', 'hassium':
               'Hs', 'meitnerium': 'Mt', 'darmstadtium': 'Ds', 'roentgenium': 'Rg', 'copernicium': 'Cn',
           'nihonium': 'Nh', 'flerovium': 'Fl', 'moscovium': 'Mc', 'livermorium': 'Lv'}

nonmetal_table = ['F', 'S', 'H', 'O', 'P', 'N', 'Br', 'Kr', 'B', 'At', 'I', 'Og', 'Ts', 'He', 'Rn', 'Ar', 'Se', 'Te',
                  'Xe', 'Cl', 'C', 'Ne', 'Si']
metal_table = ['Li', 'Be', 'Na', 'Mg', 'Al', 'K', 'Ca', 'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn', 'Ga',
               'Ge', 'As', 'Rb', 'Sr', 'Y', 'Zr', 'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn', 'Sb',
               'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd', 'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu',
               'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg', 'Tl', 'Pb', 'Bi', 'Po', 'Fr', 'Ra', 'Ac', 'Th',
               'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm', 'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh',
               'Hs', 'Mt', 'Ds', 'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv']


def cid_find(chemical_name: 'str'):
    chemical_name = chemical_name.strip()
    # 通过搜索化合物名字的Compound identification number，详见https://pubchem.ncbi.nlm.nih.gov/
    chemical_name = chemical_name.replace(',N′-', ',N-')

    abv_dict = {
        "DEE": "ethoxyethane",
        "DCM": "dichloromethane",
        "MTBE": "2-Methoxy-2-methylpropane",
        "DMK": "acetone",
        "TCM": "trichloromethane",
        "THF": "oxolane",
        "DIPE": "2-[(Propan-2-yl)oxy]propane",
        "EA": "ethyl ethanoate",
        "EtOH": "ethanol",
        "CAN": "ethanenitrile",
        "DME": "dimethoxyethane",
        "DCE": "1,2-dichloroethane",
        "TEA": "N,N-Diethylethanamine",
        "DMF": "N,N-dimethylformamide",
        "DMSO": "dimethyl sulfoxide",
        "NMP": "N-Methyl-2-pyrrolidone",
        "DMA": "N,N-Dimethylacetamide",
        "DMAc": "N,N-Dimethylacetamide",
        'TFE': "2,2,2-trifluoroethanol",
        'ETA': "2-Aminoethan-1-ol",
        'DEA':'Diethanolamine',
        '(±)-2-amino-1-butanol':'2-Aminobutan-1-ol',
        'DEF': 'N,N-diethylformamide',
        'DMPU' : '1,3-Dimethyl-3,4,5,6-tetrahydro-2(1H)-pyrimidinone'
    }
    if chemical_name.strip() in abv_dict:
        chemical_name = abv_dict[chemical_name.strip()]

    cids = pcp.get_compounds(chemical_name, 'name')
    if len(cids) == 1:
        return cids[0].cid
    else:
        return None


class cid_find2:
    def __init__(self):
        self.__name_dict = {}

    def check(self, name: str):
        if name not in self.__name_dict:
            check_res = cid_find(name)
            if check_res is not None:
                self.__name_dict[name] = check_res
            else:
                return None
        return self.__name_dict[name]


def solvent_list():
    root = osv.project_path()
    solvent_list = pd.read_csv(os.path.join(root, '_CommonRedist', 'local_solvents_cids.csv'))
    return solvent_list['solvent_cid'].to_list()


def add_list():
    root = osv.project_path()
    add_list = pd.read_csv(os.path.join(root, '_CommonRedist', 'local_addtives_cids.csv'))
    return add_list['addtive_cid'].to_list()


def cid_name_smiles(cid: int):
    c = pcp.Compound.from_cid(cid)
    return (int(cid), c.iupac_name, c.canonical_smiles)


class chemical_base(object):
    def __init__(self):
        solvent_list = pd.read_csv(os.path.join(osv.project_path(), '_CommonRedist', 'local_addtives_cids.csv'))
        solvent_list.columns = ['cid', 'name', 'smiles']
        addtive_list = pd.read_csv(os.path.join(osv.project_path(), '_CommonRedist', 'local_solvents_cids.csv'))
        addtive_list.columns = ['cid', 'name', 'smiles']
        self.__chemical_list = pd.concat([solvent_list, addtive_list], ignore_index=True)

    def in_cid(self, cid: int):
        return self.__chemical_list.loc[self.__chemical_list.cid == cid]['cid'].tolist()

    def from_cid(self, cid: int):
        if self.in_cid(cid):
            return cid, self.__chemical_list.loc[self.__chemical_list.cid == cid]['name'].tolist()[0], \
                   self.__chemical_list.loc[self.__chemical_list.cid == cid]['smiles'].tolist()[0]
        else:
            return cid_name_smiles(cid)



class chem_role(object):
    def __init__(self, cc_table):
        self.__solvent_list = solvent_list()
        self.__addtive_list = add_list()
        self.__cc_table = cc_table
        for i in self.__cc_table:
            if i['cid'] is not None and int(i['cid']) in self.__solvent_list:
                i['chem_role'] = 'Sol'
                continue
            elif i['cid'] is not None and int(i['cid']) in self.__addtive_list:
                i['chem_role'] = 'Addt'
                continue
            else:
                i['chem_role'] = ''
                i = self.metal_iden(i)
                continue

    def metal_iden(self, i: dict):
        # If the English name
        item_name = i['name']
        item_name_tokens = item_name.split(" ")
        for token in item_name_tokens:
            if token.lower() in MET_n2s:
                i['chem_role'] = MET_n2s[token.lower()]
                return i

        # If it is the chemical formula?

        # import re
        # re.split('\W','Cu[NO3(Pttyr)2(asfasf) Tb2O3(Ba)4]')
        # OUTPUT:['Cu', 'NO3', 'Pttyr', '2', 'asfasf', '', 'Tb2O3', 'Ba', '4', '']

        item_chemical_tokens = re.findall(r'[A-Z][a-z]{0,1}(?=[0-9A-Z\W]+?)', item_name)

        if item_chemical_tokens:
            for token in item_chemical_tokens:
                if token in metal_table:
                    i['chem_role'] = token
                    return i

        # If none of both
        i['chem_role'] = ""
        return i

    def cc_table(self):
        return self.__cc_table


if __name__ == "__main__":
    pcp.get_compounds()
    pass




