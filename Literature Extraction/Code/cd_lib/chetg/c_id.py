import cd_tools
from cd_lib import pcplib as pcpl
from cd_lib.pcplib import chem_role

lgrd = cd_tools.lgrd


class ChemicalListError(Exception):
    def __str__(self):
        return 'When processing the ChemicalListError, error comes'


class EmptyChemicalListError(ChemicalListError):
    def __str__(self):
        return 'Empty chemical list extracted.'


class MixtureFailedError(ChemicalListError):
    def __str__(self):
        return 'Mixture Identification is wrong.'

class NullChemicalNameError(ChemicalListError):
    def __str__(self):
        return 'Mixture Identification is wrong.'


class QuantityIncomplete(ChemicalListError):
    def __str__(self):
        return 'Chemical quantity is missing for one molecular'


def cc_i(molecular_list):
    chemical_list_row = []

    try:
        assert len(molecular_list) > 0
    except EmptyChemicalListError as err:
        lgrd.warn(err)

    # select chemicals
    for c_item_row in molecular_list:
        if not c_item_row['after_heat'] and not c_item_row['after_yeild']:
            if c_item_row['type'] == '':
                continue
            elif c_item_row['type'] == 'ApparatusAction':
                continue
            elif c_item_row['type'] == 'Wash':
                continue
            else:
                chemical_list_row.append(c_item_row)
        else:
            continue
    try:
        assert len(chemical_list_row) > 0
    except ChemicalListError as err:
        lgrd.warn(err)
        return None
    return chemical_list_row


def mixture_iden(chemical_list_row):
    chemical_list = []
    for c_item in chemical_list_row:

        if c_item['mixture']:

            # compound is a mixture
            mix_no = int(c_item['mixture_no'])
            if mix_no == len(c_item['name_list']) and mix_no == len(c_item['QUANTITY']):
                # mixture fit its format
                for i in range(mix_no):
                    item_tem = c_item.copy()
                    item_tem['name_list'] = c_item['name_list'][i]
                    item_tem['QUANTITY'] = [].append(c_item['QUANTITY'][i])
                    item_tem['mixture'] = False
                    item_tem['mixture_no'] = 0
                    chemical_list.append(item_tem)
            else:
                raise MixtureFailedError
        else:
            # compound is not a mixture
            chemical_list.append(c_item)

    return chemical_list


def cc_out(chemical_list):
    '''
    :param chemical_list: as it is
    :return: [{
                'name':str,
                'quant':[{'type':'','cd':'','unit':''}]
            }]
    '''
    # extract name and so on
    chemical_out = []
    for item in chemical_list:
        sub_out = {}
        assert len(item['name_list']) > 0
        sub_out['name'] = item['name_list'][0]

        assert len(item['QUANTITY']) > 0
        assert len(item['QUANTITY'][0]) > 0

        sub_out['quant'] = []

        for i in item['QUANTITY'][0]:
            if len(i) == 3:
                sub_out['quant'].append(i)
        if len(sub_out['quant']) == 0:
            lgrd.warn('Chemical quantity incomplete')
            raise QuantityIncomplete

        chemical_out.append(sub_out)
    return chemical_out


def cc_table(chemical_out):
    '''
    :param chemical_out: full chemical list of the synthesis
    :return: table of the chemical print.

    table= list({'name':str(),
                 'cid':int|Nane,
                 'chem_role':'M'|'L'|'Sol'|'Addi',
                 'quant_type':'AMOUNT'|'VOLUME'|'MASS',
                 'quant_cd':str(),
                 'quant_unit':str()
                 })
    '''
    cc_table = []
    for i in chemical_out:
        sub_t = {'name': i['name'], 'cid': pcpl.cid_find(i['name']), 'quant_type': i['quant'][0]['type'],
                 'quant_cd': str(i['quant'][0]['cd']), 'quant_unit': str(i['quant'][0]['unit'])}
        for quan_dic in i['quant']:
            if quan_dic['type'] == 'AMOUNT':
                sub_t['quant_type'] = quan_dic['type']
                sub_t['quant_cd'] = quan_dic['cd']
                sub_t['quant_unit']: quan_dic['unit']
                break
        cc_table.append(sub_t)
    role_handle = chem_role(cc_table)
    return role_handle.cc_table()


def mixture_iden_no_qua(chemical_list_row):
    chemical_list = []
    for c_item in chemical_list_row:
        if c_item['mixture']:
            # compound is a mixture
            mix_no = int(c_item['mixture_no'])
            if mix_no == len(c_item['name_list']):
                # mixture fit its format
                for i in range(mix_no):
                    item_tem = c_item.copy()
                    item_tem['name_list'] = [c_item['name_list'][i]]
                    item_tem['QUANTITY'] = []
                    item_tem['mixture'] = False
                    item_tem['mixture_no'] = 0
                    chemical_list.append(item_tem)
            else:
                raise MixtureFailedError
        else:
            # compound is not a mixture
            chemical_list.append(c_item)
    return chemical_list

def cc_out_no_qua(chemical_list):
    '''
    :param chemical_list: as it is
    :return: [{
                'name':str,
            }]
    '''
    # extract name and so on
    chemical_out = []

    for item in chemical_list:
        sub_out = {}
        if len(item['name_list']) == 1:
            chemical_out.append({'name':item['name_list'][0]})
        elif len(item['name_list']) > 1:
            for item_sub_name in item['name_list']:
                chemical_out.append({'name':item_sub_name})
        else:
            raise NullChemicalNameError

    return chemical_out

def cc_table_no_qua(chemical_out):
    '''
    :param chemical_out: full chemical list of the synthesis
    :return: table of the chemical print.

    table= list({'name':str(),
                 'cid':int|None,
                 'chem_role':'M'|'L'|'Sol'|'Addi',
                 })
    '''
    cc_table = []
    for i in chemical_out:
        sub_t = {'name': i['name'], 'cid': pcpl.cid_find(i['name'])}
        cc_table.append(sub_t)
    role_handle = chem_role(cc_table)
    return role_handle.cc_table()