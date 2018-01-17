'''
Чтение, запись файла конфигурации
'''
import json

class rw_cfg:
    def __init__(self, f_path):
        self.f_path = f_path
        self.dict_cfg = ''
        with open(self.f_path, 'rb') as fp:
            self.dict_cfg = json.load(fp)

    def read_cfg(self):        
        return self.dict_cfg

    def write_cfg(self, dict_cfg):
        with open(self.f_path, 'w') as fp:
            json.dump(dict_cfg, fp, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    pass
    