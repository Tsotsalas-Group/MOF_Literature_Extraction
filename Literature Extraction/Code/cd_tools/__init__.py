# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import os
import logging
import sys


def retur_pure_name(inp_name):
    if inp_name.find('_') == -1:
        oup_name = inp_name
    else:
        oup_name = inp_name[:inp_name.find('_')]
    return [inp_name, oup_name]


class Logger(object):
    def __init__(self, log_file_name, log_level, logger_name):

        # 创建一个logger
        # Create a logger
        self.__logger = logging.getLogger(logger_name)

        # 指定日志的最低输出级别，默认为WARN级别
        # Specify the minimum output level of the log, the default is WARN level
        self.__logger.setLevel(log_level)

        # 创建一个handler用于写入日志文件
        # Create a handler for writing to the log file
        file_handler = logging.FileHandler(log_file_name, encoding='utf-8')

        # 创建一个handler用于输出控制台
        # Create a handler for output to the console
        console_handler = logging.StreamHandler(sys.stdout)

        # 定义handler的输出格式
        # Define the output format of the handler
        formatter = logging.Formatter(
            '[%(asctime)s] - [%(name)s] - [%(filename)s file line:%(lineno)d] - %(levelname)s: %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 给logger添加handler
        # Add handler to logger
        self.__logger.addHandler(file_handler)
        self.__logger.addHandler(console_handler)

    def get_log(self):
        return self.__logger


lgrd = Logger(log_file_name='log.txt', log_level=logging.INFO, logger_name="C&C").get_log()


class iden_njs_resu(object):
    levels = {'error', 'warn', 'info', 'http', 'verbose', 'debug', 'silly'}

    def __init__(self, njs_dirc_cont):
        items = njs_dirc_cont.split('\n')

        def maker_obt(input):
            return input[input.find('<') + 1:input.find('>')]

        def cont_obt(input):
            return input[input.find('>') + 1:]

        self.error = []
        self.warn = []
        self.info = []
        self.http = []
        self.verbose = []
        self.debug = []
        self.silly = []
        for item in items:
            if maker_obt(item) == "error":
                self.error.append(cont_obt(item))
            if maker_obt(item) == "warn":
                self.warn.append(cont_obt(item))
            if maker_obt(item) == "info":
                self.info.append(cont_obt(item))
            if maker_obt(item) == "http":
                self.http.append(cont_obt(item))
            if maker_obt(item) == "verbose":
                self.verbose.append(cont_obt(item))
            if maker_obt(item) == "debug":
                self.debug.append(cont_obt(item))
            if maker_obt(item) == "silly":
                self.silly.append(cont_obt(item))
                # levels = {'error': 0, 'warn': 1, 'info': 2, 'http': 3, 'verbose': 4, 'debug': 5, 'silly': 6}
                #
                # def maker_obt(input):
                #     return input[input.find('<') + 1:input.find('>')]
                #
                # def cont_obt(input):
                #     return input[input.find('>') + 1:]
                #
                # for level in levels:
                #     print(f'self.{level} = []')
                # print('for item in items:')
                # for level in levels:
                #     print(f'\tif self.maker_obt(item)== "{level}":')
                #     print(f'\t\tself.{level}.append(self.cont_obt(item))')

    def result(self):
        if len(self.info) > 0:
            return [True, self.info[-1]]
        elif len(self.error) > 0:
            return [False, self.error[-1]]
        elif len(self.warn) > 0:
            return [False, self.warn[-1]]
        elif len(self.info) > 0:
            return [False, self.info[-1]]
        elif len(self.http) > 0:
            return [False, self.http[-1]]
        elif len(self.verbose) > 0:
            return [False, self.verbose[-1]]
        elif len(self.debug) > 0:
            return [False, self.debug[-1]]
        elif len(self.silly) > 0:
            return [False, self.silly[-1]]
        else:
            return [False, 'Unknown Error']

        # levels = {'error': 0, 'warn': 1, 'info': 2, 'http': 3, 'verbose': 4, 'debug': 5, 'silly': 6}
        # for level in levels:
        #     print(f'elif len(self.{level})>0:')
        #     print(f'\treturn [False,self.{level}[-1]]')


class from_html(object):
    '''
    this class is to read the database file.
    '''
    __item_core_txt = {}
    __item_core_html = {}
    __item_csd_txt = {}
    __item_csd_html = {}
    __item_cont_txt = {}
    __item_cont_html = {}

    def __init__(self, data_root, item_name):
        self.__item_path = os.path.abspath(os.path.join(data_root, item_name, 'item_sum.html'))
        with open(self.__item_path, 'rb') as f:
            item_file = f.read()
        self.__item_html__ = BeautifulSoup(item_file, 'html5lib')

        for core_items in self.__item_html__.find_all('div', class_='core_mof'):
            if core_items.p is None:
                self.__item_core_txt[core_items['id']] = ''
                self.__item_core_html[core_items['id']] = ''
                lgrd.debug('{}:No_cont in page_{}'.format(item_name, core_items['id']))
            else:
                self.__item_core_txt[core_items['id']] = core_items.p.get_text("", strip=True)
                self.__item_core_html[core_items['id']] = core_items.p.prettify().replace("\n", "")

        for csd_items in self.__item_html__.find_all('div', class_='csd'):
            if csd_items.p is None:
                self.__item_csd_txt[csd_items['id']] = ''
                self.__item_csd_html[csd_items['id']] = ''
                lgrd.debug('{}:No_cont in page_{}'.format(item_name, csd_items['id']))
            else:
                self.__item_csd_txt[csd_items['id']] = csd_items.p.get_text("", strip=True)
                self.__item_csd_html[csd_items['id']] = csd_items.p.prettify().replace("\n", "")

        for page_items in self.__item_html__.find_all('div', class_='cont'):

            if page_items.p is None:
                self.__item_cont_txt[page_items['id']] = ''
                self.__item_core_html[page_items['id']] = ''
                lgrd.debug('{}:No_cont in page_{}'.format(item_name, page_items['id']))
            else:
                self.__item_cont_txt[page_items['id']] = page_items.p.get_text("", strip=True)
                self.__item_core_html[page_items['id']] = page_items.p.prettify().replace("\n", "")

    def core_ind(self):
        count = []
        for i in self.__item_core_txt:
            if self.__item_core_txt[i] != '':
                count.append(i)
        return count

    def csd_ind(self):
        count = []
        for i in self.__item_csd_txt:
            if self.__item_csd_txt[i] != '':
                count.append(i)
        return count

    def core_item(self, item_name, opt='t'):
        if opt == 't':
            return self.__item_core_txt[item_name]
        else:
            return self.__item_core_html[item_name]

    def csd_item(self, item_name, opt='t'):
        if opt == 't':
            return self.__item_csd_txt[item_name]
        else:
            return self.__item_csd_html[item_name]

    def cont_item(self, item_name, opt='t'):
        if opt == 't':
            return self.__item_cont_txt[item_name]
        else:
            return self.__item_cont_html[item_name]
