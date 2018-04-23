import os
import zipfile
import re
'''
Класс архивирует папки рекурсивно с подпапками и файлами, а так же одиночные файлы.
Позволяет указать файлы которые нужно исключить или включить, через регулярные выражения
'''
ZIP_LZMA = zipfile.ZIP_LZMA
ZIP_DEFLATED = zipfile.ZIP_DEFLATED
ZIP_BZIP2 = zipfile.ZIP_BZIP2
ZIP_STORED = zipfile.ZIP_STORED


class zip_arch:
    def __init__(self, compress_type=ZIP_DEFLATED, include=None, exclude=None):
        self.compress_type = compress_type
        self.include = include
        self.exclude = exclude

    def compress(self, path_src, path_dst):
        '''
        Непосредственно архивирует рекурсивно папки и файлы, или одиночный файл
        '''
        dir_path = os.path.split(path_dst)[0]    
        if not os.path.exists(path_src): 
            raise FileNotFoundError(f'path {path_src} not exist')            
        elif not os.path.exists(dir_path):
            raise FileNotFoundError(f'path {dir_path} not exist')
            
        if os.path.isdir(path_src):
            with zipfile.ZipFile(path_dst, 'w') as zip_obj:            
                for folder, subdirs, files in os.walk(path_src):    
                    for file in files:
                        if self.filter(file):
                            fname = os.path.join(folder, file)                            
                            relpath = os.path.relpath(os.path.join(folder, file), os.path.split(path_src)[-1])                                                        
                            zip_obj.write(filename=fname,
                                          arcname=relpath,
                                          compress_type=self.compress_type)
        elif os.path.isfile(path_src):
            with zipfile.ZipFile(path_dst, 'w') as zip_obj:            
                zip_obj.write(filename=path_src,
                              arcname=os.path.split(path_src)[-1],
                              compress_type=self.compress_type)

    def filter(self, fname):
        '''
        Возвращает True или False, для имени заданного файла.
        В зависимости от установленных фильтров include и exclude
        '''
        if self.include and not self.exclude:            
            return re.match(self.include, fname)
        elif self.exclude and not self.include:
            if re.match(self.exclude, fname):
                return False
            else:
                return True
        elif self.include and self.exclude:
            raise Exception('Both exclude and include not possible use')
            return False
        else:
            return True
            

if __name__ == '__main__':
    src = '/home/user/Documents'    
    dst = f'{src}.zip'

    # включить только файлы с расширение *.txt и *.odt
    # тип компрессии ZIP_LZMA, по умолчанию ZIP_DEFLATED
    zip_obj = zip_arch(include='.*txt$|.*odt$', compress_type=ZIP_LZMA)    
    zip_obj.compress(src, dst)
  


   
    



