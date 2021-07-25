import cd_tools
lgrd = cd_tools.lgrd

def yield_out(yield_item):
    '''

    :param yield_item: form chemtgxml.yield_list()
    :return:if there is no  yield information, return None,else return string of the yield number

            __yield_item = {
                        'exist': False,
                        'sent_no': [],
                        'sent': obj,
                        'perc_num':str
                        }

                        there state:
                        'exist': False,
                        'exist': True, 'perc_num':str
                        'exist': True, 'perc_num':None
    '''

    #不能用调试来直接写程序，要不然着个错误会直接反映到顶层

    if yield_item['exist']:
        if isinstance(yield_item['perc_num'], str):
            return yield_item['perc_num']
        else:
            return None
    else:
        return None