import ccdc
from ccdc.search import TextNumericSearch

class csd_obj(object):
    def __init__(self):
        self.__entry_reader = ccdc.io.EntryReader('CSD')

    def item_exsit(self, item: str):
        try:
            item_obj = self.__entry_reader.entry(item)
        except RuntimeError:
            return False, None
        else:
            if item_obj.identifier != item:
                return False, None
            else:
                return True, item_obj

    def item_dp(self, item_obj):
        return item_obj.ccdc_number

    def item_name(self, item_obj, *arg, html=False):
        if html:
            return item_obj.chemical_name_as_html
        else:
            return item_obj.chemical_name

    def item_citation(self, item_obj):
        '''
        "Citation(authors='%s', journal='%s', volume='%s', year=%d, first_page='%s', doi=%s)" % (citation.authors, citation.journal,
        citation.volume, citation.year, citation.first_page, 'None' if citation.doi is None else '\'%s\'' % citation.doi)
        '''
        p_obj = item_obj.publication
        raw = [p_obj.authors,p_obj.journal.name,p_obj.volume,p_obj.year,p_obj.first_page,self.item_doi(item_obj)]

        return ", ".join([str(x) for x in raw]).strip()

    def item_doi(self, item_obj):
        item_doi = item_obj.publication.doi
        if item_doi == 'None' or item_doi is None:
            return ''
        else:
            return str(item_doi).strip()

    def simple_return(self, item_obj):

        return {
            'item_id':          item_obj.identifier,
            'item_dp':          self.item_dp(item_obj),
            'item_name':   self.item_name(item_obj, html=True),
            'item_citation':    self.item_citation(item_obj),
            'item_doi':         self.item_doi(item_obj),
        }

    def doi_search(self,doi_str:str):
        searcher = TextNumericSearch()
        searcher.add_doi(doi_str.strip())
        return searcher.search()

    def doi_search_res(self,doi_search_raw:list):
        temp = []
        temp.append(str(len(doi_search_raw)))
        if doi_search_raw:
            for i in doi_search_raw:
                temp.append(f'{str(i.entry.identifier)},_,{str(i.entry.ccdc_number)}')
        return "|".join(temp)

if __name__ == '__main__':
    csd_d = csd_obj()

    def retur_pure_name(inp_name):
        if inp_name.find('_') == -1:
            oup_name = inp_name
        else:
            oup_name = inp_name[:inp_name.find('_')]
        return [inp_name, oup_name]


    # exist, item_obj = csd_d.item_exsit('ADATAC')
    # if not exist:
    #     print('No')
    #
    # print(csd_d.simple_return(item_obj))

    # from cd_tools import osvalkyrie as osv
    # from cd_tools.ToHTML import fromCSD_api
    # import os
    #
    # csd_d = csd_obj()
    # exist, item_obj = csd_d.item_exsit('ADATAC')
    # if not exist:
    #     print('No')
    # else:
    #     fromCSD_api(csd_d.simple_return(item_obj),os.path.join(osv.project_path(),'111.html'),os.path.join(osv.project_path(),'_CommonRedist','standards.html'))
    search_re = csd_d.doi_search('10.1038/nchem.2430')
    if search_re:
        print(csd_d.doi_search_res(search_re))