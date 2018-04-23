import read_cfg_class
import hash_class
import send_file_class
import archive_file_class
import logging
import sys
import os

CFG_FILE = sys.argv[1]

def main():
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    is_change = False
    cfg_obj = read_cfg_class.rw_cfg(CFG_FILE)
    cfg_dict = cfg_obj.read_cfg()

    hash_obg = hash_class.hash_fl()
    send_obj = send_file_class.send_fl_tg(chat_ids=cfg_dict['chat_ids'],
                                          token_bot=cfg_dict['token_bot'],
                                          proxy_url=cfg_dict['proxy_url'])
    

    for i, file in enumerate(cfg_dict['files']):

        # Если указанный путь это директория
        if os.path.isdir(file['path']):
            src = file['path']
            dst = f'{src}.zip'
            
            # установлен ли фильтр
            if 'include' in file and file['include']:                
                zip_obj = archive_file_class.zip_arch(include=file['include'],
                                                          compress_type=archive_file_class.ZIP_LZMA)
                zip_obj.compress(src, dst)
            elif 'exclude' in file and file['exclude']:                
                zip_obj = archive_file_class.zip_arch(exclude=file['exclude'],
                                                          compress_type=archive_file_class.ZIP_LZMA)
                zip_obj.compress(src, dst)
            else:
                zip_obj = archive_file_class.zip_arch(compress_type=archive_file_class.ZIP_LZMA)            
                zip_obj.compress(src, dst)

            # считаем хеш архива, это и будет хеш каталога
            hash_dir = hash_obg.get_hash(dst)
            # сравниваем хеш архива каталога с хешем который записан в файле настроек
            if hash_dir.lower() != file['hash'].lower():
                # меняем старый хеш на новый в конфиге
                cfg_dict['files'][i]['hash'] = hash_dir
                try:
                    # Отправляем zip файл в телеграм
                    send_obj.send_fl(dst)
                    # флаг означающий что конфиг нужно перезаписать новыми данными                                         
                    is_change = True
                except Exception as e:
                    logging.info(f'Error send file:{dst}')
                else:
                    # Удаляем отправленный файл
                    logging.info(f'File {dst} send to tg')
                    os.remove(dst)
                    logging.info(f'File {dst} removed')

        # Если указанный путь это файл
        elif os.path.isfile(file['path']):
            # считаем хеш файла и кладем в переменную
            hash_fl = hash_obg.get_hash(file['path'])

            # сравниваем хеш файла с хешем который записан в файле настроек               
            if hash_fl.lower() != file['hash'].lower():
                logging.info(f'hash_old:{cfg_dict["files"][i]["hash"]}')
                logging.info(f'hash_new:{hash_fl}')
                cfg_dict['files'][i]['hash'] = hash_fl
                logging.info(f'file_path_to_send:{file["path"]}')

                # Если указана опция архивировать, архивируем
                if cfg_dict['archive'].lower() == 'true':
                    zip_obj = archive_file_class.zip_arch(compress_type=archive_file_class.ZIP_LZMA)
                    zip_obj.compress(file['path'], f'{file["path"]}.zip')
                    
                    try:
                        # Отправляем zip файл в телеграм
                        send_obj.send_fl(f'{file["path"]}.zip')
                        # флаг означающий что конфиг нужно перезаписать новыми данными                                         
                        is_change = True
                    except Exception as e:
                        logging.info(f'Error send file:{file["path"]}')
                    else:
                        # Удаляем отправленный файл
                        os.remove(f'{file["path"]}.zip')

                # Если не указана опция архивировать, просто отправляем файл в телеграм
                else:
                    try:
                        send_obj.send_fl(file['path'])
                        # флаг означающий что конфиг нужно перезаписать новыми данными                
                        is_change = True
                    except Exception as e:
                        logging.info(f'Error send file:{file["path"]}')
                
            
    
    if is_change:
        # запись конфига в файл
        cfg_obj.write_cfg(cfg_dict)
    else:
        logging.info('Not Change Files')

if __name__ == '__main__':
    main()