import cd_tools
lgrd = cd_tools.lgrd

def cd_trans(item:'str'):
    nums = ['zero','one','two','three','four','five','six','seven','eight','nine','ten']
    if item.lower() in nums:
        return nums.index(item.lower())
    else:
        return item

def tt_classifer(item_teti_or):
    '''
    :param item_teti_or:
    first Classify the items into 5 different  kinds
    :return: tt_ele_cla = {'Heat': {'timer','heater'}, 'Wait': {}, 'Stir': {}, 'Cool': {}, 'other': {}}
    '''
    tt_ele_cla = {'Heat': {}, 'Wait': {}, 'Add': {}, 'Stir': {}, 'Cool': {}, 'other': {}}
    for tt_ele in item_teti_or:
        if tt_ele['type'] == 'Heat':
            if tt_ele['ope_type'] == 'timer':
                tt_ele_cla['Heat']['timer'] = tt_ele['value']
            if tt_ele['ope_type'] == 'heater':
                tt_ele_cla['Heat']['heater'] = tt_ele['value']

        elif tt_ele['type'] == 'Stir':
            if tt_ele['ope_type'] == 'timer':
                tt_ele_cla['Stir']['timer'] = tt_ele['value']
            if tt_ele['ope_type'] == 'heater':
                tt_ele_cla['Stir']['heater'] = tt_ele['value']

        elif tt_ele['type'] == 'Wait':
            if tt_ele['ope_type'] == 'timer':
                tt_ele_cla['Wait']['timer'] = tt_ele['value']
            if tt_ele['ope_type'] == 'heater':
                tt_ele_cla['Wait']['heater'] = tt_ele['value']

        elif tt_ele['type'] == 'Add':
            if tt_ele['ope_type'] == 'timer':
                tt_ele_cla['Add']['timer'] = tt_ele['value']
            if tt_ele['ope_type'] == 'heater':
                tt_ele_cla['Add']['heater'] = tt_ele['value']

        elif tt_ele['type'] == 'Cool':
            if tt_ele['ope_type'] == 'timer':
                tt_ele_cla['Cool']['timer'] = tt_ele['value']
            if tt_ele['ope_type'] == 'heater':
                tt_ele_cla['Cool']['heater'] = tt_ele['value']

        else:
            if tt_ele['ope_type'] == 'timer':
                tt_ele_cla['other']['timer'] = tt_ele['value']
            if tt_ele['ope_type'] == 'heater':
                tt_ele_cla['other']['heater'] = tt_ele['value']
    return tt_ele_cla


def time_unit_tran(item):
    if 'unit' in item:
        if 'cd' in item:
            item['cd'] = cd_trans(item['cd'])
            if item['unit'] in ['h', 'hour', 'hour']:
                item['unit'] = 'h'

            if item['unit'] in ['day', 'days','d']:
                item['cd'] = int(item['cd']) * 24
                item['unit'] = 'h'

            if item['unit'] in ['week', 'weeks']:
                item['cd'] = int(item['cd']) * 24 * 7
                item['unit'] = 'h'
        else:
            if item['unit'] in ['day', 'days']:
                item['cd'] = ''
                item['unit'] = 'mt_day'

            if item['unit'] in ['week', 'weeks']:
                item['cd'] = ''
                item['unit'] = 'mt_week'
    return item


def heat_unit_tran(item):
    if 'unit' in item:
        if 'cd' in item:
            item['cd'] = cd_trans(item['cd'])
            if item['unit'] in ['K']:
                item['cd'] = float(item['cd']) - 273
                item['unit'] = '°C'
            if item['unit'] in ['°C', 'oC']:

                item['cd'] = float(item['cd'])

                item['unit'] = '°C'
        else:
            if item['unit'] in ['temperature']:
                # most is room temperature
                item['cd'] = '25'
                item['unit'] = '°C'
    return item

class NoTemTimeError(Exception):
    def __str__(self):
        return 'When extract time and temperature, no correct value is found. '
    pass


def ht_ident(ht_item):
    '''
    When extract time and temperature, no correct value is found, an exception NoTemTimeError will raise
    :param ht_item:
    :return: {'temp': '', 'temp_u': '', 'time': '', 'time_u': ''}
    '''
    ht_re = {'temp': '', 'temp_u': '', 'time': '', 'time_u': ''}
    order = ['Heat', 'Wait', 'Add','other']
    for dep in order:
        if dep in ht_item:
            if len(ht_item[dep]) == 2:
                temp_ob = ht_item[dep]['heater']
                temp_ob = heat_unit_tran(temp_ob)
                time_ob = ht_item[dep]['timer']
                time_ob = time_unit_tran(time_ob)
                try:
                    ht_re['temp'] = temp_ob['cd']
                    ht_re['temp_u'] = temp_ob['unit']
                    ht_re['time'] = time_ob['cd']
                    ht_re['time_u'] = time_ob['unit']
                except KeyError:
                    continue
                break
            else:
                if dep == 'other':

                    raise NoTemTimeError(ht_item)



        elif dep == 'other':

            raise NoTemTimeError(ht_item)

        else:
            continue

    return ht_re