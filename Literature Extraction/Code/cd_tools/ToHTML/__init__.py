# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import cd_tools

lgrd= cd_tools.lgrd

def fromCoRe(input_info, output_path, standar_page_path):
    with open(standar_page_path, 'rb') as f:
        ht_ed = f.read()

    ed = BeautifulSoup(ht_ed, 'html5lib')

    core_name = ed.find('h1', class_='core_mof', id='name')
    core_name.string = input_info['core_name']

    core_all_metal = ed.find('div', class_='core_mof', id='core_All_Metals')
    core_all_metal_item = ed.new_tag('p')
    core_all_metal_item.string = input_info['core_All_Metals']
    core_all_metal.append(core_all_metal_item)

    core_Open_Metal_Sites = ed.find('div', class_='core_mof', id='core_Open_Metal_Sites')
    core_Open_Metal_Sites_item = ed.new_tag('p')
    core_Open_Metal_Sites_item.string = input_info['core_Open_Metal_Sites']
    core_Open_Metal_Sites.append(core_Open_Metal_Sites_item)

    try:
        DOI_public = ed.find('div', class_='core_mof', id='DOI_public')
        DOI_public_item = ed.new_tag('p')
        DOI_public_item.string = input_info['DOI_public']
        DOI_public.append(DOI_public_item)
    except:
        lgrd.debug('DOI missing from CoRe MOF Database')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ed.prettify())


def fromCSD(input_path, output_path, standar_page_path):
    with open(input_path, 'rb') as f:
        ht_op = f.read()
    with open(standar_page_path, 'rb') as f:
        ht_ed = f.read()
    op = BeautifulSoup(ht_op, 'html5lib')
    ed = BeautifulSoup(ht_ed, 'html5lib')

    try:
        csd_idf = op.find("div", class_='csd_name')
        csd_idf_noe = ed.find('div', class_="csd", id='csd_ident')
        csd_idf_item = ed.new_tag("p")
        csd_idf_str = csd_idf.get_text()
        csd_idf_item.string = csd_idf_str[:csd_idf_str.find(":")].strip()
        csd_idf_noe.append(csd_idf_item)
    except:
        lgrd.debug('Database Identifier Lost')

    try:
        dp_num = op.find("div", class_="dp_num")
        dp_num_noe = ed.find('div', class_="csd", id="csd_dn")
        dp_num_item = ed.new_tag("p")
        dp_num_item.string = dp_num.string
        dp_num_noe.append(dp_num_item)
    except:
        lgrd.debug('Deposition Number Lost')

    try:
        full_name = op.find('span', attrs={"data-highlight": "Compound"})
        full_name_noe = ed.find('div', class_="csd", id='csd_name')
        full_name.name = 'p'
        full_name_noe.append(full_name)
    except:
        lgrd.debug('Full Name Lost')

    try:
        space_info = op.find("div", class_='csd_name')
        space_info_noe = ed.find('div', class_="csd", id='csd_space')
        space_info_pris = space_info.prettify()
        space_info_item = BeautifulSoup('<p>' + space_info_pris[space_info_pris.find("<br/>") + 5:-6].strip() + '</p>',
                                        'html5lib')
        space_info_noe.append(space_info_item.p)
    except:
        lgrd.debug('Reffrence Lost')

    try:
        # ref will modify the content and remove doi section
        doi = op.find("span", class_='publication-Doi')
        doi_noe = ed.find('div', class_="csd", id='DOI_public')
        doi_item = ed.new_tag("p")
        doi_item.string = doi.string
        doi_noe.append(doi_item)
    except:
        lgrd.debug('DOI Lost')

    try:
        ref = op.find("div", class_='media-body')
        ref_noe = ed.find('div', class_="csd", id='csd_ref')
        ref.name = "p"
        ref_noe.append(ref)
    except:
        lgrd.debug('Reffrence: Lost')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ed.prettify())


def fromCSD_api(input_dict, output_path, standar_page_path):
    '''
    {
        'item_id': item_obj.identifier,
        'item_dp': self.item_dp(item_obj),
        'item_name': self.item_name(item_obj, html=True),
        'item_citation': self.item_citation(item_obj),
        'item_doi': self.item_doi(item_obj),
    }
    '''

    with open(standar_page_path, 'rb') as f:
        ht_ed = f.read()

    ed = BeautifulSoup(ht_ed, 'html5lib')

    try:
        csd_idf_noe = ed.find('div', class_="csd", id='csd_ident')
        csd_idf_item = ed.new_tag("p")
        csd_idf_item.string = input_dict['item_id'].strip()
        csd_idf_noe.append(csd_idf_item)
    except:
        lgrd.debug('Database Identifier Lost')


    dp_num_noe = ed.find('div', class_="csd", id="csd_dn")
    dp_num_item = ed.new_tag("p")

    dp_num_item.string = str(input_dict['item_dp']).strip()

    dp_num_noe.append(dp_num_item)


    try:
        full_name_noe = ed.find('div', class_="csd", id='csd_name')
        full_name_item = BeautifulSoup('<p>' + input_dict['item_name'].strip()+'</p>', 'html5lib')
        full_name_noe.append(full_name_item)
    except:
        lgrd.debug('Full Name Lost')

    try:
        # ref will modify the content and remove doi section
        doi_noe = ed.find('div', class_="csd", id='DOI_public')
        doi_item = ed.new_tag("p")
        doi_item.string = input_dict['item_doi'].strip()
        doi_noe.append(doi_item)
    except:
        lgrd.debug('DOI Lost')

    try:
        ref_noe = ed.find('div', class_="csd", id='csd_ref')
        ref_item = ed.new_tag("p")
        ref_item.string = input_dict['item_citation'].strip()
        ref_noe.append(ref_item)
    except:
        lgrd.debug('Reffrence: Lost')

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ed.prettify())

def FP_publisher(publisher, output_path, standar_page_path):
    with open(standar_page_path, 'rb') as f:
        ht_ed = f.read()

    ed = BeautifulSoup(ht_ed, 'html5lib')

    publisher_name = ed.find('div', class_='cont', id='publisher')
    publisher_name_noe = BeautifulSoup(f"<p>{publisher}</p>", 'html5lib')
    publisher_name.append(publisher_name_noe)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ed.prettify())


def FP_maintext(content_path, output_path, standar_page_path):
    with open(standar_page_path, 'rb') as f:
        ht_ed = f.read()

    with open(content_path, 'rb') as f:
        ht_cont = f.read()

    ed = BeautifulSoup(ht_ed, 'html5lib')
    dish = BeautifulSoup(ht_cont, 'html5lib')

    main_text = ed.find('article', class_='cont', id='fulltext')
    main_text.append(dish)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ed.prettify())


def FP_synpara(content_path, output_path, standar_page_path):
    with open(standar_page_path, 'rb') as f:
        ht_ed = f.read()

    with open(content_path, 'rb') as f:
        ht_cont = f.read()

    ed = BeautifulSoup(ht_ed, 'html5lib')
    dish = BeautifulSoup(ht_cont, 'html5lib')

    main_text = ed.find('div', id='synpara')
    main_text.append(dish)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(ed.prettify())

if __name__ == '__main__':
    pass



