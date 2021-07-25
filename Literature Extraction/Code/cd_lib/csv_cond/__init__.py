import spacy
from spacy.tokens import Span


def dep_r_a(doc):
    # dependency relation adjust:
    for ent in doc.ents:
        if ent.root.head.ent_type_ == 'QUANTITY':
            ent.root.head = ent.root.head.head
    return doc


def mod_unit_ent(doc):
    new_ents = []
    for ent in doc.ents:
        if ent.label_ == 'CARDINAL' and ent.start != 0:
            # ml quantity
            if ent.root.head.text in ('mL', 'ml', 'L', 'l'):
                # to identify the ml quantity
                for unit_item in doc[ent.start: ent.start + 5]:
                    # check the
                    if unit_item.text in ('mL', 'ml', 'L', 'l'):
                        new_ent = Span(doc, ent.start, unit_item.i + 1, label="QUANTITY")
                        new_ents.append(new_ent)

            # degree C
            if ent.root.head.text == 'C' and ent.root.head.head.text == 'at':
                # to identify the degree C
                for unit_item_idx in range(ent.start + 5):
                    if doc[unit_item_idx].text == "°" and doc[unit_item_idx + 1].text == "C":
                        new_ent = Span(doc, ent.start, unit_item_idx + 2, label="TEMPERATURE_C")
                        new_ents.append(new_ent)

            # K
            if ent.root.head.text == "K":
                # to identify the degree C
                for unit_item_idx in range(ent.start + 2):
                    if doc[unit_item_idx].text == "K":
                        new_ent = Span(doc, ent.start, unit_item_idx + 1, label="TEMPERATURE_K")
                        new_ents.append(new_ent)

        else:
            new_ents.append(ent)
    doc.ents = new_ents
    return doc


def froot(ent):
    def dig(rootf):
        try:
            return rootf.head
        except:
            return False

    rootf = ent.root.head
    digging = 0
    while rootf.pos_ != 'VERB' and dig(rootf):
        if digging < 8:
            rootf = dig(rootf)
            digging += 1
        else:
            return False
    return rootf.lemma_


def out_put(recs):
    rec_m = {}
    record = {}
    for rec in recs:
        if rec['id'] not in record:
            record[rec['id']] = [len(rec_m), 0]
        rec_pos = record[rec['id']][0]

        if rec['ent.label_'] == 'QUANTITY' and rec['ent_anc'] != 'wash':
            if record[rec['id']][1] == 0:
                record[rec['id']][1] += 1
                rec_m[rec_pos] = {'process': 'ADD', 'cont_dic': {'name': rec['ent.root.head'], 'full_name': "",
                                                                 'QUANT': [rec['ent.text']]}}

            else:
                record[rec['id']][1] += 1
                rec_m[rec_pos]['cont_dic']['QUANT'].append(rec['ent.text'])

        if rec['ent.label_'] == 'QUANTITY' and rec['ent_anc'] == 'wash':
            if record[rec['id']][1] == 0:
                record[rec['id']][1] += 1
                rec_m[rec_pos] = {'process': 'WASH', 'cont_dic': {'name': rec['ent.root.head'], 'full_name': "",
                                                                  'QUANT': [rec['ent.text']]}}

            else:
                record[rec['id']][1] += 1
                rec_m[rec_pos]['cont_dic']['QUANT'].append(rec['ent.text'])

        if rec['ent.label_'] == 'TEMPERATURE_C':
            rec_m[rec_pos] = {'process': 'AT', 'cont_dic': {'cond': rec['ent.text']}}
        if rec['ent.label_'] == 'TEMPERATURE_K':
            rec_m[rec_pos] = {'process': 'AT', 'cont_dic': {'cond': rec['ent.text']}}

    return rec_m


def rep_ori(doc):
    reciepe = []
    count = 0
    record = doc.ents[0].root.head.i
    record_tem = 0
    for ent in doc.ents:

        record_tem = ent.root.head.i
        if record_tem != record:
            count += 1
            record = record_tem
        ent_anc = froot(ent)

        reciepe.append({'id': count, 'ent.start': ent.start, 'ent.text': ent.text, 'ent.root.head.i': ent.root.head.i,
                        'ent.root.head': ent.root.head, 'ent.label_': ent.label_, 'ent_anc': ent_anc})

    return reciepe


def csv_list(rec_m, item_name):
    csv_title = ['item_name', 'temperature', 'time', 'wash_1_name', 'wash_1_name_quant', 'wash_2_name',
                 'wash_2_name_quant', 'chemical_1_name', 'chemical_1_fname', 'chemical_1_name_quant', 'chemical_2_name',
                 'chemical_2_fname', 'chemical_2_name_quant', 'chemical_3_name', 'chemical_3_fname',
                 'chemical_3_name_quant', 'chemical_4_name', 'chemical_4_fname', 'chemical_4_name_quant',
                 'chemical_5_name', 'chemical_5_fname', 'chemical_5_name_quant', 'chemical_6_name', 'chemical_6_fname',
                 'chemical_6_name_quant']
    cond_dic = {}
    for name in csv_title:
        cond_dic[name] = ""
    cond_dic['item_name'] = item_name

    chemical = 0
    wash = 0
    for i in range(len(rec_m)):

        cont = rec_m[i]

        if cont['process'] =='ADD':
            chemical += 1
            cond_dic['chemical_'+str(chemical)+'_name'] = cont['cont_dic']['name']
            cond_dic['chemical_'+str(chemical)+'_fname'] = cont['cont_dic']['full_name']
            cond_dic['chemical_'+str(chemical)+'_name_quant'] = cont['cont_dic']['QUANT'][0]
        if cont['process'] =='AT':
            cond_dic['temperature'] = cont['cont_dic']['cond']
        if cont['process'] =='WASH':
            wash += 1
            cond_dic['wash_'+str(wash)+'_name'] = cont['cont_dic']['name']
            cond_dic['wash_'+str(wash)+'_fname'] = cont['cont_dic']['full_name']
            cond_dic['wash_'+str(wash)+'_name_quant'] = cont['cont_dic']['QUANT'][0]

    cond_row = []
    for i in csv_title:
        cond_row.append(cond_dic[i])
    return cond_row


def flow(ctext, item_name: str):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(ctext)

    doc = dep_r_a(doc)

    doc = mod_unit_ent(doc)

    recs = rep_ori(doc)
    rec_m = out_put(recs)

    csv_row = csv_list(rec_m, item_name)

    csv_title = ['item_name', 'temperature', 'time', 'wash_1_name', 'wash_1_name_quant', 'wash_2_name',
                 'wash_2_name_quant', 'chemical_1_name', 'chemical_1_fname', 'chemical_1_name_quant', 'chemical_2_name',
                 'chemical_2_fname', 'chemical_2_name_quant', 'chemical_3_name', 'chemical_3_fname',
                 'chemical_3_name_quant', 'chemical_4_name', 'chemical_4_fname', 'chemical_4_name_quant',
                 'chemical_5_name', 'chemical_5_fname', 'chemical_5_name_quant', 'chemical_6_name', 'chemical_6_fname',
                 'chemical_6_name_quant']


    print(csv_row)