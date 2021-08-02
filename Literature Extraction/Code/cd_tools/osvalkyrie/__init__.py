import os
import shutil


def sub_floders(path):
    list = []
    if os.path.exists(path):
        files = os.listdir(path)
        for file in files:
            m = os.path.join(path, file)
            if os.path.isdir(m):
                h = os.path.split(m)
                list.append(h[-1])
        return list
    else:
        return list

def sub_files(root_dic,ext):
    assert os.path.exists(root_dic)
    return [x for x in files(root_dic,ext)]



def project_path():
    curPath = os.path.abspath(os.path.dirname(__file__))
    rootPath = curPath[:curPath.find("Code") + len("Code")]
    return rootPath


def dir_path_str(test_mode):
    if test_mode:
        dir_path = os.path.join(project_path(), 'test')
    else:
        dir_path = os.path.join(project_path(), 'data_base')
    return dir_path

"""
Use wildcards, get all files, or perform operations.
"""
import glob
import os


def files(curr_dir='.', ext='*.exe'):
    """Files in the current directory"""
    for i in glob.glob(os.path.join(curr_dir, ext)):
        yield i


def all_sub_files(rootdir, ext):
    """Files in the current directory and subdirectories"""
    for name in os.listdir(rootdir):
        if os.path.isdir(os.path.join(rootdir, name)):
            try:
                for i in all_sub_files(os.path.join(rootdir, name), ext):
                    yield i
            except:
                pass
    for i in files(rootdir, ext):
        yield i


def remove_files(rootdir,*args, ext = '', show=False):
    if ext == '':
        if os.path.exists(rootdir):
            os.remove(rootdir)
    else:
        """删除rootdir目录下的符合的文件/Delete the matching files in the rootdir directory"""
        for i in files(rootdir, ext):
            if show:
                print(f'{i} is deleted')
            os.remove(i)


def remove_all_subfiles(rootdir, ext, show=False):
    """删除rootdir目录下以及子目录下符合的文件/Delete the matching files in the rootdir directory and subdirectories"""
    for i in all_sub_files(rootdir, ext):
        if show:
            print(f'{i} is deleted')
        os.remove(i)

def transf(source_path, target_path):
    if not os.path.exists(source_path):
        raise RuntimeError(f'{source_path} is not there!')
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):

            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)




if __name__ == '__main__':
    pass
