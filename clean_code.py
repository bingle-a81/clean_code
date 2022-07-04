import logging.config
from settings import logger_config
from datetime import datetime
from pathlib import Path
from contextlib import contextmanager
import os
import json

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.'+ __name__)

@contextmanager
def managed_file(name):
    try:
        f = open(name, 'w')
        yield f
    finally:
        f.close()

def serch_in_check(path_for_check):  # ищем файл в папке  со станков
    for adress, dirs, files in os.walk(path_for_check):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check  # возвращаем адрес файла


class JsonF:
    def __init__(self,jsonfile: Path) -> None:
        self._jsonfile=jsonfile
        self._init_storage()
    
    def _init_storage(self)->None:
        if not self._jsonfile.exists():
            self._jsonfile.write_text('[]')

    
    def save(self,fi:str)->None:
        history=self._read_history()
        history.append({
            'date1':str(datetime.now()),
            'file':fi
            }) 
        self._write(history)   


    def _read_history(self):
        with open(self._jsonfile,'r') as f:
            return json.load(f)

    def _write(self,history)->None:
        with open(self._jsonfile,'w') as f:
            json.dump(history,f,ensure_ascii=False,indent=4)

# def save_weather(weather: Path, storage: WeatherStorage) -> None:
#     """Saves weather in the storage"""
#     storage.save(weather)


def main():
    logger.debug(r'это консоль')
    BASE_DIR = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR = BASE_DIR.joinpath(r'Компания МК')
    jjs=JsonF(Path.cwd() / 'hist.json')
    for a in serch_in_check(TEMPLATES_DIR):
        print(a)
        # logger.debug(a)
        jjs.save(a)


    
    # with open('text.txt','w+') as f:
    #     for a in serch_in_check(TEMPLATES_DIR):
    #         print((a+'\n'))
    #         f.write(a+'\n')
    # logger.info(r'это консоль и файл')
    # logger.warning(r'это консоль файл телега')
    # logger.error(r'это консоль файл телега мыло')





if __name__ == '__main__':
    main()
    # assert passw_stranght('') == 'Too Weak'
