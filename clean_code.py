import logging.config
from settings import logger_config
import json
from pathlib import Path
from datetime import datetime
import os
from typing import NamedTuple
import re


logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.'+ __name__)

class Attribfiles(NamedTuple):
    date_of_change:float
    size_file: int
    f_name:str

def correction_of_the_line(string:str)->str:  # удаляем символы кроме букв,цифр и точки
    reg = re.compile('[^a-zA-Z0-9. -]')
    a = reg.sub('', string)
    return a

def chenge_name(st:str)->str:  # удаляем расширение файла
    if st.rfind('.') > 0:
        return st[0:st.rfind('.')]
    else:
        return st

def attrib(file:Path)->Attribfiles:  # получаем дату изменения  файла и размер
    date_of_change = os.path.getmtime(file)
    size_file = os.path.getsize(file)
    with open(file, 'r') as r:  # только чтение файла
        i = 0
        while i < 3:
            st = r.readline()  # чтение текстового файла построчно
            i += 1
            if ('(' in st) and (')' in st):
                f_name = st[(st.index('(') + 1):(st.index(')'))].strip()
                f_name = correction_of_the_line(f_name).strip()
                break
        else:
            f_name = chenge_name(file.split('\\')[-1])  # если в файле названия нет - берем имя файла
    return Attribfiles(date_of_change, size_file,f_name)

class JsonFile:
    def __init__(self,jsonfile:Path):
        self._jsonfile=jsonfile
        self._init_storage()

    def _init_storage(self)->None:
        if not self._jsonfile.exists():
            logger.debug('file no')
            self._jsonfile.write_text("[]")

    def save(self,pow:Path)->None:
        record=self._read_record()
        record.append({
            'date':str(datetime.now()),
            'f_name':attrib(pow).f_name,
            'path':pow,
            'size':attrib(pow).size_file,
            'date_change':attrib(pow).date_of_change
        })
        self._write(record)

    def _read_record(self):
        with open(self._jsonfile,'r') as f:
            return json.load(f)
    def _write(self,record)->None:
        with open(self._jsonfile,'w') as f:
            json.dump(record,f,ensure_ascii=False,indent=4)

def serch_in_check(path_for_check):
    for adress, dirs, files in os.walk(path_for_check):
        for file in files:
            adress_file_in_check = os.path.join(adress, file)
            yield adress_file_in_check

def main():
    logger.debug(r'это консоль')
    base_path = os.path.dirname(os.path.abspath(__file__))
    jjs=JsonFile(Path.cwd() / 'json.json')
    for a in serch_in_check(os.path.join(base_path, r"81ЦИБ")):
        jjs.save(a)

    # logger.info(r'это консоль и файл')
    # logger.warning(r'это консоль файл телега')
    # logger.error(r'это консоль файл телега мыло')


if __name__ == '__main__':
    main()
    # assert passw_stranght('') == 'Too Weak'
