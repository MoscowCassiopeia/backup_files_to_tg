import read_cfg_class
import hash_class
import send_file_class
import logging
import sys

CFG_FILE = sys.argv[1]

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    is_change = False
    cfg_obj = read_cfg_class.rw_cfg(CFG_FILE)
    cfg_dict = cfg_obj.read_cfg()

    hash_obg = hash_class.hash_fl()
    send_obj = send_file_class.send_fl_tg(chat_ids=cfg_dict['chat_ids'],
                                          token_bot=cfg_dict['token_bot'])
    

    for i, file in enumerate(cfg_dict['files']):
        hash_fl = hash_obg.get_hash(file['path'])                
        if hash_fl.lower() != file['hash'].lower():
            logging.info(f'hash_old:{cfg_dict["files"][i]["hash"]}')
            logging.info(f'hash_new:{hash_fl}')
            cfg_dict['files'][i]['hash'] = hash_fl
            logging.info(f'file_path_to_send:{file["path"]}')
            try:
                ret = send_obj.send_fl(file['path'])                                                
                is_change = True
            except Exception as e:
                logging.info(f'Error send file:{file["path"]}')
            
            
    if is_change:
        cfg_obj.write_cfg(cfg_dict)
    else:
        logging.info('Not Change Files')

if __name__ == '__main__':
    main()