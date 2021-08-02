import chemdataextractor as cder
# import en_core_web_sm
# from spacy.matcher import Matcher
from chemdataextractor.nlp.tokenize import ChemWordTokenizer

class cde_paras:
    """
    Initialization:
        item = cde_paras(cder obj of an_article_from_cde_reading)
    """

    def __init__(self, body):
        # save and classify the article
        self.__body = body
        self.__sny_para_list = self.selcet_para(body)
        self.__sny_num = len(self.__sny_para_list)

        # # Save all the abvs in the text
        # self__abv_list = {}
        # for item in body.abbreviation_definitions:
        #     self.__abv_list[item[0][0]] = (" ".join(item[1]), item[2])
        # for item in body.records.serialize():
        #     if ('names' in item) and (len(item['names']) > 1):
        #         if len(set([name_item.lower() for name_item in item['names']])) > 1:
        #             '''
        #             abv_name:shortes in names
        #             full_name: longest in names
        #             abv_name = reduce(lambda x, y: x if len(x) < len(y) else y, item['names']) or min(item['names'], key=len)
        #             '''
        #             self.__abv_list[min(item['names'], key=len)] = (max(item['names'], key=len), 'CM')
        #             continue

    def sny_sele(self):
        # whether it be selected or not
        if self.__sny_para_list:
            return True
        else:
            return False

    def sny_cont_num(self):
        # Numbers of the selected paragraphs
        return len(self.__sny_para_list)

    def sny_para_obj(self):
        # Content of the selected paragraphs
        return self.__sny_para_list

    def sny_para_str(self):
        # Content of the selected paragraphs
        return [x.text for x in self.__sny_para_list]

    def select_condition(self):
        """
                a flow kind of method is proposed on the assuption that:
                1) Chemical have a partent

        cde_dic = {'NN': 'noun',
         'CD': 'cardinal number',
         'VBZ': 'verb (third person singular present)',
         'DT': 'determiner',
         'NNS': 'noun plural',
         'IN': 'preposition',
         'JJ': 'adjective',
         'CC': 'coordinating conjunction',
         'CM': 'chemical mention'}


        to analyze a sentens, constituency  tree is need!!!
        how to get the amount?
        Instead of get the chemical first,
        we can start to find the unit first, then follow the constituency  tree to get the chemical head of this unit.

        => the core of the extracting and identification is to find the NEVER-changed things in the colorful world!


                :return: ({'no':int, 'processing': 'IN'|'ADD'|'AT'|'FOR'|'COOL', cont_dic:{}})
                    -ADD    cont_dic = {'name':str, 'full_name':str, 'unit':'mmol'|'mol'|'g'|'kg'|'mL'|'ml','value':float}
                    -IN     cont_dic = { 'item': str} #will start with 'a' or 'an' and end with noun
                    -AT     cont_dic = {'unit': 'K'|'C', 'value': float }
                    -FOR    cont_dic = {'unit': 'min'|'h', 'value' : float}
                    -COOL   cont_dic = {'slow' =Boolean, 'unit': 'min'|'h', 'value' : float}
        """
        return

    def selcet_para(self, html_cde):
        chosen_para = []
        for para in html_cde.paragraphs:
            if syn_para_selector(para):
                chosen_para.append(para)
        return chosen_para






def mod_text(text: str):
    text = text.replace('silica gel plates', 'silica gel')
    text = text.replace('building block', 'building linker')
    text = text.replace('building blocks', 'building linkers')
    return text


def syn_para_selector(html_para):
    # Use cder to judge
    if isinstance(html_para, cder.doc.text.Paragraph):
        def cder_cm_num(cder_html_para):
            cm_nums = 0
            for cder_html_sentence in cder_html_para:
                cm_nums += cder_html_sentence.ner_tags.count('B-CM')
            return cm_nums

        def cry_like(processing_text: str):
            des_for_prod = ['blocks', 'block', 'crystals', 'crystal', 'crystalline', 'plates', 'plate',
                            'single-crystals', 'single-crystal']
            for i in des_for_prod:
                if processing_text.find(i) != -1:
                    return True
            else:
                return False

        def liquid_like_nums(html_para_pos_list_plain):
            num = []
            i = 0
            while i < len(html_para_pos_list_plain):
                if html_para_pos_list_plain[i][1] == 'CD':
                    if i + 1 < len(html_para_pos_list_plain):
                        if html_para_pos_list_plain[i + 1][0].lower() in ('μl', 'ml', 'l', 'm'):
                            num.append(i)
                i += 1
            return num

        def chemical_amount_like_nums(html_para_pos_list_plain):
            num = []
            i = 0
            while i < len(html_para_pos_list_plain):
                if html_para_pos_list_plain[i][1] == 'CD':
                    if i + 1 < len(html_para_pos_list_plain):
                        if html_para_pos_list_plain[i + 1][0].lower() in ('mmol', 'mol', 'mg', 'g'):
                            num.append(i)
                i += 1
            return num

        if len(html_para.sentences) > 1:
            html_para_pos_list_plain = sum(html_para.pos_tagged_tokens, [])
        else:
            html_para_pos_list_plain = html_para.pos_tagged_tokens

        processing_text = mod_text(html_para.text)
        cwt = ChemWordTokenizer()
        # token has a problem! ! !
        plain_tokens_text_lower = [x[:-1].lower() if x[-1] == '.' or x[-1] == "," else x.lower() for x in
                                   cwt.tokenize(processing_text)]

        if (cder_cm_num(html_para) >= 2) and (
                set(plain_tokens_text_lower) & set(['blocks', 'block', 'crystals', 'crystal', 'crystalline', 'plates',
                                                    'plate', 'single-crystals', 'single-crystal'])):
            # print('1 pass')
            # print(chemical_amount_like_nums(html_para_pos_list_plain))
            # print(liquid_like_nums(html_para_pos_list_plain))
            if (len(chemical_amount_like_nums(html_para_pos_list_plain)) >= 1 and len(
                    liquid_like_nums(html_para_pos_list_plain)) >= 1) or (
                    len(liquid_like_nums(html_para_pos_list_plain)) >= 3):
                # print('2 pass')
                return True
            else:
                return False

        else:
            return False
    # Use other judgments
    else:
        return False


# Version 2: Still too slow
# def mod_text(text: str):
#     text = text.replace('silica gel plates', 'silica gel')
#     text = text.replace('building block', 'building linker')
#     text = text.replace('building blocks', 'building linkers')
#     return text
#
#
# def syn_para_selector(html_para):
#     # Use cder to judge
#     if isinstance(html_para, cder.doc.text.Paragraph):
#         def cder_cm_num(cder_html_para):
#             cm_nums = 0
#             for cder_html_sentence in cder_html_para:
#                 cm_nums += cder_html_sentence.ner_tags.count('B-CM')
#             return cm_nums
#
#         def cry_like(processing_text: str):
#             des_for_prod = ['blocks', 'block', 'crystals', 'crystal', 'crystalline', 'plates', 'plate',
#                             'single-crystals', 'single-crystal']
#             for i in des_for_prod:
#                 if processing_text.find(i) != -1:
#                     return True
#             else:
#                 return False
#
#         processing_text = mod_text(html_para.text)
#
#         if (cder_cm_num(html_para) >= 2) and cry_like(processing_text):
#
#             nlp = en_core_web_sm.load()
#
#             doc = nlp(html_para.text)
#
#             matcher = Matcher(nlp.vocab)
#             pattern1 = [[{'LIKE_NUM': True}, {'LOWER': 'μl'}], [{'LIKE_NUM': True}, {'LOWER': 'ml'}],
#                         [{'LIKE_NUM': True}, {'LOWER': 'm'}]]
#             pattern2 = [[{'LIKE_NUM': True}, {'LOWER': 'mmol'}], [{'LIKE_NUM': True}, {'LOWER': 'mol'}],
#                         [{'LIKE_NUM': True}, {'LOWER': 'mg'}], [{'LIKE_NUM': True}, {'LOWER': 'g'}]]
#             # pattern3 = [[{'LEMMA': 'block'}], [{'LEMMA': 'crystal'}], [{'LEMMA': 'plate'}], [{'LEMMA': 'block'}],
#             #             [{'LEMMA': 'crystalline'}]]
#             matcher.add("liquid_volume", pattern1)
#             matcher.add("chemical_amount", pattern2)
#             # matcher.add("crystal_like", pattern3)
#             matches = matcher(doc)
#             matches_r_b = [nlp.vocab.strings[match_id] for match_id, start, end in matches]
#             # print(f"matches_r_b.count(solid_list):{matches_r_b.count('solid_list')}")
#             # print(f"matches_r_b.count('liquid_volume'):{matches_r_b.count('liquid_volume')}")
#             # liquid_list = [match_id for match_id in matches if nlp.vocab.strings[match_id] == 'liquid_volume']
#             # solid_list = [match_id for match_id in matches if nlp.vocab.strings[match_id] == 'chemical_amount']
#             # product_list = [match_id for match_id in matches if nlp.vocab.strings[match_id] == 'crystal_like']
#             if (matches_r_b.count('solid_list') >= 1 and matches_r_b.count('liquid_volume') >= 1) or (
#                     matches_r_b.count('liquid_volume') >= 3):
#
#
#                 return True
#             else:
#                 return False
#
#         else:
#             return False
#     # 利用其他判断
#     else:
#         return False


'''
def mod_text(text:str):
    text = text.replace('silica gel plates','silica gel')
    text = text.replace('building block', 'building linker')
    text = text.replace('building blocks', 'building linkers')
    return text
def syn_para_selector(html_para):
    # 利用cder判断
    if isinstance(html_para, cder.doc.text.Paragraph):
        def cder_cm_num(cder_html_para):
            cm_nums = 0
            for cder_html_sentence in cder_html_para:
                cm_nums += cder_html_sentence.ner_tags.count('B-CM')
            return cm_nums

        plain_tokens_text = []
'''
'''
The following code may need to be asynchronous to be faster,
         At the current speed, an article takes 1-2min
                 # The following codes will seriously slow down the process, but due to the wrong word segmentation method of cder, we can only do this to avoid errors
        
                nlp = en_core_web_sm.load()
        
                doc = nlp(html_para.text)
        
                matcher = Matcher(nlp.vocab)
                pattern1 = [[{'LIKE_NUM': True}, {'LOWER': 'μl'}], [{'LIKE_NUM': True}, {'LOWER': 'ml'}]]
                pattern2 = [[{'LIKE_NUM': True}, {'LOWER': 'mmol'}], [{'LIKE_NUM': True}, {'LOWER': 'mol'}],
                            [{'LIKE_NUM': True}, {'LOWER': 'mg'}], [{'LIKE_NUM': True}, {'LOWER': 'g'}]]
                pattern3 = [[{'LEMMA': 'block'}], [{'LEMMA': 'crystal'}], [{'LEMMA': 'plate'}], [{'LEMMA': 'block'}],
                            [{'LEMMA': 'crystalline'}]]
                matcher.add("liquid_volume", pattern1)
                matcher.add("chemical_amount", pattern2)
                matcher.add("crystal_like", pattern3)
                matches = matcher(doc)
                matches_r_b = [nlp.vocab.strings[match_id] for match_id, start, end in matches]
        
                # liquid_list = [match_id for match_id in matches if nlp.vocab.strings[match_id] == 'liquid_volume']
                # solid_list = [match_id for match_id in matches if nlp.vocab.strings[match_id] == 'chemical_amount']
                # product_list = [match_id for match_id in matches if nlp.vocab.strings[match_id] == 'crystal_like']
                if matches_r_b.count('solid_list') > 1 and matches_r_b.count('liquid_volume') > 1 and (
                        cder_cm_num(html_para) >= 3) and matches_r_b.count('crystal_like') > 0:'''
'''
        processing_text = mod_text(html_para.raw_tokens)
        # The following is the original version,  do with it
        if len(html_para.sentences) > 1:
            plain_tokens_text = sum(processing_text, [])
            # The criterion is the number
        if (plain_tokens_text.count("mmol") > 1 or plain_tokens_text.count("mol") > 1 or plain_tokens_text.count(
                "mg") > 1 or plain_tokens_text.count("g") > 1) \
                and (plain_tokens_text.count("ml") > 0 or plain_tokens_text.count("mL") > 0 or plain_tokens_text.count(
            "μl") > 0 or plain_tokens_text.count("μL") > 0) \
                and (cder_cm_num(html_para) >= 2):
            plain_tokens_text_lower = [x.lower() for x in plain_tokens_text if isinstance(x, str)]
            plain_tokens_text_lower = [x[:-1] if x[-1] == "," or x[-1] == "." else x for x in plain_tokens_text_lower]
            if set(plain_tokens_text_lower) & set(['blocks', 'block', 'crystals', 'crystal', 'crystalline', 'plates',
                                                   'plate','single-crystals','single-crystal']):
                return True
            else:
                return False
        else:
            return False

    # Use other judgments
    else:
        return False
'''
