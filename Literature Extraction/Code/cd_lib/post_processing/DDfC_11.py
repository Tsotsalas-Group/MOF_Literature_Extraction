import shutil
import csv
from cd_tools.osvalkyrie import project_path, sub_floders
import cd_tools
import os, time, shutil
import pandas as pd
from cd_tools import lgrd, iden_njs_resu, retur_pure_name

logger = lgrd


class CSDInternetError(Exception):
    def __str__(self):
        return 'CSD_internet_error'


class DOIError(Exception):
    def __str__(self):
        return 'DOI wrong or not in CCDC'


def ddfc(doi_str, debug=False):
    if debug:
        headless = 'false'
    else:
        headless = 'true'

    node_loaction = os.path.join(project_path(), 'DDfC_1.0.js')
    try_count = 0;
    delay_time = 1000
    while try_count < 3:
        logger.debug('Stat for DDfC')
        logger.debug(
            r'node {} --delay {} --headless {}  "{}"'.format(str(node_loaction), delay_time, headless, doi_str))
        with os.popen(
                r'node {} --delay {} --headless {}  "{}"'.format(str(node_loaction), delay_time, headless, doi_str),
                'r') as f:
            # popen返回文件对象，跟open操作一样
            text = f.read()
        doi_item = iden_njs_resu(text)
        logger.debug(doi_item.result())

        if doi_item.result()[0]:
            re_raw = doi_item.result()[1].strip().split('|')
            # 判断条目是否完整
            if len(re_raw) == int(re_raw[0]) + 1:
                logger.info(f'\t{doi_str} everyting is geted')
                return [True, re_raw]
            else:
                if try_count == 2:
                    logger.critical(f'\t{doi_str}: doi_error')
                    return [False, 'doi_error']
                time.sleep(3)
                continue
        else:
            if doi_item.result()[1].strip() == 'Name is not inside CSD':
                logger.info(f'{doi_str}: not_in_csd')
                return [False, 'not_in_csd']
            elif doi_item.result()[1].strip() == 'No node found for selector: #Doi.form-control':
                logger.critical(f'\t connection_error')
                return [False, 'connection_error']
            elif doi_item.result()[1].strip() == 'Web page error.':
                if try_count == 2:
                    logger.warn(f'\t{doi_str}: webpage_error')
                    return [False, 'webpage_error']
                try_count += 1
                delay_time += 1000
                time.sleep(3)
                continue
            if try_count == 2:
                logger.critical(f'\t{doi_str}: webpage_error')
                return [False, 'webpage_error']
            try_count += 1
            delay_time += 1000
            continue


def process_row(ddfc_return_r, doi):
    ddfc_result = [ddfc_return_r[i].split(',_,') for i in range(1, len(ddfc_return_r))]

    for single in ddfc_result:
        single[1] = int(single[1])
        single.append(doi)

    def take_dp(elem):
        return elem[1]

    ddfc_result.sort(key=take_dp)
    project_path()
    return [
        {'item_name': ddfc_result[i][0], 'dep_num': ddfc_result[i][1], 'num_sum': len(ddfc_result), 'item_ind': i,
         'doi': ddfc_result[i][2]} for i in range(len(ddfc_result))]


class doi_list_gener(object):
    def __init__(self):
        self._doi_map = pd.read_csv(os.path.join(project_path(), '_CommonRedist', 'DOI_map.csv'), sep='|',
                                    encoding='utf-8', dtype={'dep_num': str, 'num_sum': int, 'item_ind': int})
        self._continuous_error = []

    def map_refresh(self, new_map):
        self._doi_map = new_map

    def name_selector(self, item_name: str):
        return item_name.count('.') > 1

    def to_local(self):
        norepeat_df = self._doi_map.drop_duplicates(subset=['item_name', 'doi'], keep='first')
        norepeat_df.reset_index(drop=True, inplace=True)
        norepeat_df.to_csv(os.path.join(project_path(), '_CommonRedist', 'DOI_map.csv'), sep='|', encoding='utf-8',
                           index=False)

    def exist_doi(self, doi):
        '''
        :param doi:
        :return: [] or [int()]

        since if [] return False
        the judgement can be done
        '''
        return self._doi_map[self._doi_map['doi'].isin([doi])].index.tolist()

    def exist_item_name(self, pure_item_name):
        print(pure_item_name)
        print(self._doi_map)
        return self._doi_map[self._doi_map['item_name'].isin([pure_item_name])].index.tolist()

    def check_item(self, item_name):
        pure_item_nanme = retur_pure_name(item_name)[1]
        item_index = self.exist_item_name(pure_item_nanme)
        if item_index:
            return True
        else:
            return False

    def check_item_order(self, item_name):
        pure_item_name = retur_pure_name(item_name)[1]
        search_re = self._doi_map.loc[self._doi_map.item_name == pure_item_name]['item_ind'].tolist()
        if search_re:
            return search_re[0]
        else:
            return None

    def item_order(self, item_name, doi):
        if self.name_selector(item_name):
            return None
        else:
            pass
        order = self.check_item_order(item_name)
        if order is None:
            try:
                self.adding_item(doi)
            except Exception as e:
                raise e
            else:
                return self.check_item_order(item_name)
        else:
            return order

    def adding_item(self, doi):
        try:
            calwer_re = self.get_doi_orders(doi, debug=False)
            result_list = process_row(calwer_re, doi)
            self._doi_map = self._doi_map.append(result_list)
        except Exception as e:
            raise e
        else:
            self._doi_map.reset_index(drop=True, inplace=True)

    def get_doi_orders(self, doi, debug=False):
        '''
        :param doi:
        :param debug:
        :return: list(list(item_pure_name,dp_num,doi))
        '''
        while self._continuous_error.count(1) < 5:
            ddfc_return = ddfc(doi, debug)
            if ddfc_return[0]:
                self._continuous_error.append(0)
                if len(self._continuous_error) > 10:
                    self._continuous_error = []
                return ddfc_return[1]
            else:
                if ddfc_return[1] == 'not_in_csd' or ddfc_return[1] == 'wrong_name':
                    raise DOIError
                if ddfc_return[1] == 'connection_error':
                    raise CSDInternetError
                if ddfc_return[1] == 'webpage_error':
                    self._continuous_error.append(1)
                    continue
        if self._continuous_error.count(1) > 4:
            logger.critical('Too much _continuous_error')
            raise CSDInternetError

    def doi_map_print(self):
        return self._doi_map

    def doi_repot(self, doi_check: str):
        '''
        :param doi_check: DOI to check 
        '''

    def check_doi_sum_order(self,doi_check:str):
        search_re = self._doi_map.loc[self._doi_map.doi == doi_check]['num_sum'].tolist()
        if search_re:
            return search_re[0]
        else:
            return None

    def check_item_sum_order(self, item_name):
        pure_item_name = retur_pure_name(item_name)[1]
        search_re = self._doi_map.loc[self._doi_map.item_name == pure_item_name]['num_sum'].tolist()
        if search_re:
            return search_re[0]
        else:
            return None


def test_ddfc():
    shutil.copy(os.path.join(project_path(), '_CommonRedist', 'DOI_map.csv'),
                os.path.join(project_path(), '_CommonRedist',
                             'DOI_map' + time.strftime("_%Y%m%d_%H%M%S", time.localtime()) + '.csv'))
    doi_list = doi_list_gener()
    try:
        print('{}:{}'.format('SUNLAP', doi_list.item_order('SUNLAP', '10.1002/anie.200806227')))
        print('{}:{}'.format('ADASUV', doi_list.item_order('ADASUV', '10.1002/anie.201201202')))
        print('{}:{}'.format('ADASUV', doi_list.item_order('ADASUV', '10.1002/anie.2012asfdasf01202')))
        print('{}:{}'.format('ADASssUV', doi_list.item_order('ADASssUV', '10.1002/anie.2012asfdasf01202')))
    except DOIError:
        print('DOI is wrong')
        doi_list.to_local()
    except CSDInternetError:
        print('Internet is something wrong')
        doi_list.to_local()


def item_oder_subfolder(testmode=False):
    if testmode:
        dir_path = os.path.join(project_path(), 'test')
    else:
        dir_path = os.path.join(project_path(), 'data_base')  #

    shutil.copy(os.path.join(project_path(), '_CommonRedist', 'DOI_map.csv'),
                os.path.join(project_path(), '_CommonRedist',
                             'DOI_map' + time.strftime("_%Y%m%d_%H%M%S", time.localtime()) + '.csv'))
    doi_list = doi_list_gener()

    with open(os.path.join(project_path(), '_CommonRedist', 'c2985_doi.csv')) as csvfile:
        csv_r = csv.reader(csvfile, delimiter=' ', quotechar='|')
        csv_rows = [x for x in csv_r]
    for row in csv_rows:
        item_name = row[0]
        item_doi = row[1]
        if item_name.count('_') >= 2 and len(item_name) > 14:
            continue

        # row_item = cd_tools.from_html(dir_path, item_name)
        #
        # core_doi = row_item.core_item('DOI_public')
        # csd_doi = row_item.csd_item('DOI_public')
        #
        # if core_doi != '':
        #     item_doi = core_doi
        # elif csd_doi != '':
        #     item_doi = csd_doi
        # else:
        #     continue

        item_doi = item_doi.strip()

        try:
            print('{}:{}'.format(item_name, doi_list.item_order(item_name, item_doi)))
        except DOIError:
            print('{}:{}'.format(item_name, 'DOI is wrong'))
            continue
        except CSDInternetError:
            print('Internet is something wrong')
            doi_list.to_local()
            break
        except Exception:
            print('Some other Errors')
            doi_list.to_local()
    doi_list.to_local()


def item_oder_subtest(testmode=True):
    if testmode:
        dir_path = os.path.join(project_path(), 'test')
    else:
        dir_path = os.path.join(project_path(), 'data_base')

    shutil.copy(os.path.join(project_path(), '_CommonRedist', 'DOI_map.csv'),
                os.path.join(project_path(), '_CommonRedist',
                             'DOI_map' + time.strftime("_%Y%m%d_%H%M%S", time.localtime()) + '.csv'))
    doi_list = doi_list_gener()

    with open(os.path.join(project_path(), '_CommonRedist', 'test_doi.csv')) as csvfile:
        csv_r = csv.reader(csvfile, delimiter=' ', quotechar='|')
        csv_rows = [x for x in csv_r]
    for row in csv_rows:
        item_name = row[0]
        item_doi = row[1]
        if item_name.count('_') >= 2 and len(item_name) > 14:
            continue

        # row_item = cd_tools.from_html(dir_path, item_name)
        #
        # core_doi = row_item.core_item('DOI_public')
        # csd_doi = row_item.csd_item('DOI_public')
        #
        # if core_doi != '':
        #     item_doi = core_doi
        # elif csd_doi != '':
        #     item_doi = csd_doi
        # else:
        #     continue

        item_doi = item_doi.strip()

        try:
            print('{}:{}'.format(item_name, doi_list.item_order(item_name, item_doi)))
        except DOIError:
            print('{}:{}'.format(item_name, 'DOI is wrong'))
            continue
        except CSDInternetError:
            print('Internet is something wrong')
            doi_list.to_local()
            break
        except Exception:
            print('Some other Errors')
            doi_list.to_local()
    doi_list.to_local()


if __name__ == "__main__":
    item_oder_subtest()
