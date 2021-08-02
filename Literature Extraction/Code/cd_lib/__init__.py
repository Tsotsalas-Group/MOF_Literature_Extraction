import os
import chemdataextractor as cder
from chemdataextractor.reader import RscHtmlReader, AcsHtmlReader
import cd_tools

lgrd = cd_tools.lgrd


def cde_html(item_name: str, dir_path: str, *args, full_page = True ):
    def html_reader(f, item_publisher: str):
        '''
        :param f: path of the html file
        :param item_publisher: as it is
        :return: obj of the cde with the html
        '''
        # to deal with strange reading function with chemdataextractor
        if item_publisher == 'rsc':
            return cder.Document.from_file(f, readers=[RscHtmlReader()])
        elif item_publisher == 'acs':
            return cder.Document.from_file(f, readers=[AcsHtmlReader()])
        else:
            return cder.Document.from_file(f)

    def html_reading(item_html_root, item_publisher: str):
        with open(item_html_root, 'rb') as f:
            html_cde = html_reader(f, item_publisher)
        return html_cde

    item = cd_tools.from_html(dir_path, item_name)
    item_root = os.path.join(dir_path, item_name)

    if full_page:
        cont_root = os.path.join(item_root, 'full_page.html')
    else:
        cont_root = os.path.join(item_root, 'main_text.html')

    if os.path.exists(cont_root):
        return html_reading(cont_root, item.cont_item('publisher'))
    else:
        lgrd.warn(f'{cont_root} can not find eror')
        return None

def onlystr(item):
    if isinstance(item, float):
        return str(round(item, 2))
    if item is None:
        return ''
    if isinstance(item, int):
        return str(item)
    else:
        return item
