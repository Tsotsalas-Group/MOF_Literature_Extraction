import pubchempy as pcp
import pandas as pd
from cd_tools import osvalkyrie as osv
import os


def cid_find(chemical_name: 'str'):
    # 通过搜索化合物名字的Compound identification number，详见https://pubchem.ncbi.nlm.nih.gov/
    cids = pcp.get_compounds(chemical_name, 'name')
    if len(cids) == 1:
        return cids[0].cid
    else:
        return None


def solvent_list():
    root = osv.project_path()
    solvent_list = pd.read_csv(os.path.join(root, '_CommonRedist/local_solvents_cids.cvs'))
    return solvent_list['solvent_cid'].to_list()


class chem_role(object):
    def __init__(self, cc_table):
        self.__solvent_list = solvent_list()
        self.__cc_table = cc_table
        for i in self.__cc_table:
            if i['cid'] is None:
                i['chem_role'] = ''
                continue
            if int(i['cid']) in self.__solvent_list:
                i['chem_role'] = 'Sol'
            else:
                i['chem_role'] = ''

    def cc_table(self):
        return self.__cc_table
