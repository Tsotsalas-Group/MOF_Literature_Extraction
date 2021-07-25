import os,re
import xml.etree.ElementTree as ET
from cd_lib.chetg.tt_id import *
from cd_lib.chetg.yield_id import *
from cd_lib.chetg.c_id import *
from cd_tools.osvalkyrie import project_path
from cd_lib.chetg.yield_id import yield_out


def chemtgp(text_location, *args, text='', chemtg_location='', test_mode=False,
            opt_put='chemtg'):
    '''
    :param text_location: str without \n
    :param text: if no text_location is given, text in UtF-8, in a pragrapgh
    :param args:
    :param chemtg_location:
    :param test_mode:
    :param file_writing:
    :param file_title:
    :return:
In order to improve the accuracy of recognition, the following processing is done in the input file:
    the strange blank space in utf-8 is removed
    remove expressoion ' without stirring'

    '''

    def blank_re2(in_str: 'str'):
        # since utf-8 has a 0xC2 0xA0. it is a space but will display ? in unicode.
        # so here is to replace the character with the normal space
        temp = in_str.split('\n')
        in_str2 = ' '.join(temp)
        in_str2 = re.sub(r'\s',' ',in_str2)
        temp = in_str2.split(' ')
        temp2 = ' '.join(temp)
        temp3 = temp2.split(' ')
        half_done = ' '.join(temp3)
        return half_done.replace('°С', '°C').replace(' °', ' °').replace(' %', ' %').replace('⋅', '·')

    def inp_normal(in_stir: 'str'):
        tem = in_stir
        tem = tem.replace('without stirring', '')
        tem = tem.replace('distilled water', 'water')
        tem = tem.replace('aqueous', 'water')
        tem = tem.replace('°C/', '°C for ')
        tem = tem.replace('· ','·')
        tem = tem.replace('is about', 'is ')
        tem = tem.replace('. The yield',', the yield')
        tem = tem.replace('methanolic','methanol')
        tem = tem.replace(' DMA ', ' Dimethylacetamide ')
        tem = tem.replace(' DMAc ', ' Dimethylacetamide ')
        tem = tem.replace('pH≈', 'pH ≈ ')
        tem = tem.replace('pH=','pH = ')
        tem = tem.replace(' N ,N', ' N,N')      
        tem = tem.replace('·2.5 H2O','·2.5H2O')

        if re.findall(r'\·[0-9]\s{1}(?=[A-Z]{1})', tem):
            for i in re.findall(r'\·[0-9]\s{1}(?=[A-Z]{1})', tem):
                tem = tem.replace(i, i.strip())

        return tem

    if not chemtg_location == '':
        chemtg_location = os.path.abspath(chemtg_location)
    else:
        chemtg_location = os.path.join(project_path(), '_CommonRedist',
                                       'chemicalTagger-1.6-SNAPSHOT-jar-with-dependencies-file.jar')

    if text == '':
        o_t_name = os.path.basename(text_location)
        m_t_name = 'mod_' + o_t_name

        mod_t_loc = os.path.join(os.path.dirname(text_location), m_t_name)
        out_put_loc = os.path.join(os.path.dirname(text_location), opt_put + '.xml')

        with open(text_location, 'rt', encoding='utf8') as f:
            text = f.read()

        text = blank_re2(text)
        text = inp_normal(text)

        with open(mod_t_loc, 'w', encoding='utf8') as f:
            f.write(text)
        try:
            with os.popen(r'java -jar {} {} {}'.format(str(chemtg_location), str(mod_t_loc), str(out_put_loc),
                                                       'r')) as f:  # popen返回文件对象，跟open操作一样
                info_r = f.read()
        except:
            lgrd.warn(info_r)
        with open(out_put_loc, 'rt', encoding='utf8') as f:
            result = f.read()
    else:
        result = ""
    if test_mode:
        print(result)
    return result


class chemtgxml():

    def findallsub(self, xml_item, tag):
        tag_list = []
        for i in xml_item.iter(tag):
            tag_list.append(i)
        return tag_list

    def __init__(self, xml_item):
        '''
        For all of the items, they will be accepted as they are initialized, and nothing will be deleted.
         :param xml_item: xml-object that is read through
        '''
        self.xml_item = xml_item
        self.__root = ET.fromstring(self.xml_item)

        self.__ope_list = []
        self.__token_list = {}  # start with 0
        self.__molecular_list = []
        self.__yield_item = {'exist': False, 'sent_no': []}
        '''
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
        
        __molecular_list = [{
                        'chemical_no':int
                        'sent_no':'int',
                        'type':'str',
                        'after_heat':'Boolean',
                        'after_yeild':'Boolean'
                        'molec_role':'str',
                        'item':'object',
                        'name_list':[name1,name2,name3],
                        'mixture':'Boolean'
                        'mixture_no':int
                        'QUANTITY':[[{'type':'','cd':'','unit':''}]]
                        }]

        ope_list = [{
                    'sent_no':'int',
                    'part_no':'int',
                    'type':'str',
                    'ope_type': 'heater'|'timer',
                    'item': 'object',
                    'value':dic()
                    }]
        '''

        sent_no = 0
        part_no = 0
        token = 0

        chemical_no = 0

        after_heat = False
        heat = False

        after_yield = False
        yield_ap = False

        for i in self.__root.iter():
            if i.text is not None:
                self.__token_list[token] = [i.text]
                token += 1

            if i.tag == 'Sentence':
                sent_no += 1
                part_no = 0
                parents_name = None

            if i.tag == 'ActionPhrase':
                parents_name = i.attrib['type']

                if parents_name == 'Heat':
                    heat = True

            if i.tag == 'TempPhrase':
                self.__ope_list.append(
                    {'sent_no': sent_no - 1, 'part_no': part_no, 'type': parents_name, 'ope_type': 'heater', 'item': i})

            if i.tag == 'TimePhrase':
                self.__ope_list.append(
                    {'sent_no': sent_no - 1, 'part_no': part_no, 'type': parents_name, 'ope_type': 'timer', 'item': i})

            if i.tag == 'MOLECULE':
                try:
                    molec_role = i.attrib['role']
                except:
                    molec_role = ''

                molec = {'chemical_no': str(chemical_no), 'sent_no': sent_no - 1, 'type': parents_name,
                         'after_heat': after_heat,
                         'after_yeild': after_yield,
                         'molec_role': molec_role, 'item': i}
                self.__molecular_list.append(molec)

                chemical_no += 1

            if i.tag == 'NN-YIELD' and not yield_ap:
                self.__yield_item['exist'] = True
                self.__yield_item['sent_no'] = sent_no - 1
                yield_ap = True

            # below muast be put in the end.
            if i.tag == 'ActionPhrase' and heat:
                after_heat = True

            if yield_ap:
                after_yield = True

            part_no = part_no + 1

    def sentences(self):
        return list(self.__root.findall('Sentence'))

    def yieldit(self):
        def percent_pra(percent_item):
            number = percent_item.find('CD')
            if number is not None:
                return number.text
            else:
                return None

        if self.__yield_item['exist']:
            self.__yield_item['sent'] = self.sentences()[self.__yield_item['sent_no']]
        else:
            return self.__yield_item

        y_sent = self.__yield_item['sent']

        yeild_list = self.findallsub(y_sent, 'YIELD')
        if yeild_list != []:
            percent = yeild_list[0].find('PERCENT')
            perc_num = percent_pra(percent)
            self.__yield_item['perc_num'] = perc_num

        else:  # YIELD is not recognized
            NNYIELD = False
            for i in y_sent.iter():
                if i.tag == 'NN-YIELD':
                    NNYIELD = True
                if i.tag == 'PERCENT' and NNYIELD:
                    perc_num = percent_pra(i)
                    self.__yield_item['perc_num'] = perc_num
                    break
            if not 'perc_num' in self.__yield_item:
                self.__yield_item['perc_num'] = None

        return self.__yield_item

    def yield_list(self):
        self.yieldit()
        return self.__yield_item

    def nameit(self):
        '''
        Process each object in __molecular_list,
         Extract name from

        :return:
        '''
        for i in self.__molecular_list:
            item = i['item']

            # how many OSCARCM inside?
            # every time only 1 OSCARCM inside, but many OSCAR-CM inside OSCARCM
            osc_f = self.findallsub(item, 'OSCARCM')
            if len(osc_f)>0:
                m = osc_f[0]
                name_item = ['']
                for n in m.iter():
                    if n.tag == 'OSCAR-CM':
                        name_item[-1] = name_item[-1] + ' ' + n.text
                    if n.tag == 'DASH':
                        name_item.append('')
                name_item = [x.strip() for x in name_item]
            else:
                i['name_list'] = ['']
            i['name_list'] = name_item
        return self.__molecular_list

    def quantit(self):
        def quant_list_p(item):
            # For each molecule, we believe there is only one QUANTITY
            quant_items = item.findall('QUANTITY')
            quant_list = []
            for quant_item in quant_items:
                quant_table = []
                for m in quant_item.iter():
                    if m.tag == 'VOLUME':
                        quant_table.append({'type': 'VOLUME', 'cd': m.find('CD').text, 'unit': m.find('NN-VOL').text})
                    if m.tag == 'MASS':
                        quant_table.append({'type': 'MASS', 'cd': m.find('CD').text, 'unit': m.find('NN-MASS').text})
                    if m.tag == 'AMOUNT':
                        quant_table.append(
                            {'type': 'AMOUNT', 'cd': m.find('CD').text, 'unit': m.find('NN-AMOUNT').text})
                quant_list.append(quant_table)
            return quant_list

        for i in self.__molecular_list:
            item = i['item']

            # is it MIXTURE?
            # we believe there is only one inside each mixture
            mixture_item = item.find('MIXTURE')

            if mixture_item is not None:
                i['mixture'] = True
                # determine the radio and some thing else
                ratio_item = mixture_item.find('RATIO')
                ratio = []
                mixture_no = 0

                if ratio_item is not None:
                    for m in ratio_item.iter():
                        if m.tag == 'CD':
                            # error may come here!!!
                            ratio.append(float(m.text))
                            mixture_no = 1 + mixture_no
                    ratio_sum = sum(ratio)
                    ratio_f = []
                    for ra in ratio:
                        ratio_f.append(ra / ratio_sum)
                    ratio = ratio_f

                    # For each molecule, we believe there is only one QUANTITY
                    quant_list_or = quant_list_p(item)
                    quant_list = []
                    for sub_ratio in ratio:
                        quant_sub_ratio = []
                        try:
                            quant_list_or[0]
                        except IndexError:
                            quant_list_or = [[{'type': 'error', 'cd': '0', 'unit': 'error'}]]

                        for quant_dic in quant_list_or:
                            for sub_quant_dic in quant_dic:
                                qsr_itme = sub_quant_dic.copy()
                                sub_value = float(sub_ratio) * float(qsr_itme['cd'])
                                qsr_itme['cd'] = sub_value
                                quant_sub_ratio.append(qsr_itme)
                        quant_list.append(quant_sub_ratio)

                    i['mixture_no'] = mixture_no
                    i['QUANTITY'] = quant_list

                    continue

                else:
                    i['mixture'] = False

            else:
                i['mixture'] = False

            if not i['mixture']:
                # For each molecule, we believe there is only one QUANTITY
                quant_list = quant_list_p(item)
                i['mixture_no'] = 0
                i['QUANTITY'] = quant_list

        return self.__molecular_list

    def molecular_list(self):
        # print(self.__molecular_list)
        # print()
        self.nameit()
        # print(self.__molecular_list)
        # print()
        self.quantit()
        # print(self.__molecular_list)
        # print()
        return self.__molecular_list

    def teti(self):
        for item in self.__ope_list:
            if item['ope_type'] == 'heater':
                item_dic = {}
                for i in item['item'].iter():
                    if i.tag == 'CD':
                        item_dic['cd'] = i.text
                    if i.tag == 'NN-TEMP':
                        item_dic['unit'] = i.text
                item['value'] = item_dic
            if item['ope_type'] == 'timer':
                item_dic = {}
                for i in item['item'].iter():
                    if i.tag == 'CD':
                        item_dic['cd'] = i.text
                    if i.tag == 'NN-TIME':
                        item_dic['unit'] = i.text
                item['value'] = item_dic
        return self.__ope_list

    def ope_list(self):
        self.teti()
        return self.__ope_list

    def token_l(self):
        return self.__token_list

    def chemical_out(self):
        return


def ctg_xml_par(xml_str, *args, xml_loaction=''):
    if not xml_loaction == '':
        with open(xml_loaction, 'rt', encoding='utf8') as f:
            xml_str = f.read()
    return chemtgxml(xml_str)


if __name__ == "__main__":
    xml_str = chemtgp(r'D:\c_reader_local\test\MAZSOX_clean\pot_sny_para0.txt')


    print(xml_str)
    a = ctg_xml_par(xml_str)

    tt_ele_cla = tt_classifer(a.ope_list())
    print(tt_ele_cla)
    tt_re = ht_ident(tt_ele_cla)
    print(tt_re)
    #
    print()
    # print(a.ope_list())
    # print(a.yield_list())
    for i in a.molecular_list():
        print(i)
        print()
    print(yield_out(a.yield_list()))


