# -*- coding: utf-8 -*-
import logging.config
from settings import logger_config
from typing_extensions import TypeAlias
from typing import Literal,Iterable
from pathlib import Path
from abc import abstractmethod, ABC
from dataclasses import dataclass

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.'+ __name__)

SRC_DIR = Path(__file__).parent / "src"

BaseFolder: TypeAlias = Literal["components", "pages"]

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class Element:
    full_path:Path
    name:str

class FileCreator(ABC):
    def __init__(self,element:Element):
        self._element=element

    def create(self)->None:
        """Creates empty file and then fill with contents"""
        self._create_empty_file()
        self._write_file_contents()

    def get_relative_filename(self)->str:
        """Returns relative filename as str for logging"""
        relative_path_start_index=1+len(str(SRC_DIR.resolve()))
        logger.debug(f'ff={len(str(SRC_DIR.resolve()))}')
        logger.debug(f'relative_path_start_index={relative_path_start_index}')
        result = str(self.get_absolute_filename().resolve())[relative_path_start_index:]
        logger.debug(f'res={result}')
        return result

    def _create_empty_file(self):
        """Init file if not exists"""
        self.get_absolute_filename().parent.mkdir(parents=True,exist_ok=True)
        # logger.debug(f'_create_empty_file {str(self.get_absolute_filename().parent)}')
        self.get_absolute_filename().touch(exist_ok=True)

    @abstractmethod
    def get_absolute_filename(self) -> Path:
        """Returns file in Path format"""
        pass

    @abstractmethod
    def _write_file_contents(self) -> None:
        """Fill file with contents"""
        pass

class TSXFileCreator(FileCreator):
    def get_absolute_filename(self) -> Path:
        return self._element.full_path/(self._element.name+'.tsx')

    def _write_file_contents(self) -> None:
        self.get_absolute_filename().write_text( f"""import styles from "./{self._element.name}.module.css"

interface {self._element.name}Props {{
  
}}
const {self._element.name} = ({{}}: {self._element.name}Props) => (
  <div>{self._element.name}</div>
)
export default {self._element.name}
        """.strip()
                                                 )

class CSSFileCreator(FileCreator):
    def get_absolute_filename(self) -> Path:
        return self._element.full_path/(self._element.name+'.module.css')

    def _write_file_contents(self) -> None:
        pass

class IndexFileCreator(FileCreator):
    """Optional index.ts file creator"""
    def get_absolute_filename(self) -> Path:
        return self._element.full_path / "index.ts"

    def _write_file_contents(self):
        current_file_contents = self.get_absolute_filename().read_text()
        if current_file_contents.strip():
            logger.debug(f'{current_file_contents}')
            return
        self.get_absolute_filename().write_text(
            f"""export {{default}} from "./{self._element.name}";"""
        )

class AskParams:
    """Ask params from user, parse it and create Element structure"""
    def __init__(self):
        self._element:Element

    def ask(self)->Element:
        """Ask all parameters — element folder and name"""
        base_folder=self._ask_base_folder()
        self._element=self._parse_as_element(self._ask_element(base_folder),base_folder)
        return self._element

    def _parse_as_element(self,element_str:str,base_folder:BaseFolder)->Element:
        element_as_list=element_str.split('/')
        logger.debug(f'element_as_list={element_as_list}')
        element_name=element_as_list[-1]
        logger.debug(f'element_name= {element_name}')
        if len(element_as_list)>1:
            relative_path="/".join(element_as_list[:-1])
        else:
            relative_path=element_name
        logger.debug(f'relative_path={relative_path}')
        return Element(
            full_path=SRC_DIR/base_folder/relative_path,
            name=element_name
        )

    def _ask_base_folder(self)->BaseFolder:
        while True:
            a = input('c-comp,p-pages:').strip().lower()
            if a == 'c':
                return "components"
            elif a == 'p':
                return "pages"
            else:
                print('repeat')


    def _ask_element(self,base_folder:BaseFolder)->str:
        return input(f"There input?{base_folder}/").strip()

    def ask_ok(self,filenames:Iterable[str])->None:
        filenames="\n\t".join(filenames)
        while True:
            print(f'\nИтак, создаём файлы:\n'
                  f"{Colors.HEADER}\t{filenames} {Colors.ENDC}\n\n"
                  )
            a = input("Ок? [Y]/N: ").strip().lower()
            if a == 'y':
                return
            elif a == 'n':
                exit("Ок, выходим, ничего не создал.")
            else:
                print('repeat eee')

class ElementFilesCreator:
    def __init__(self,element:Element):
        self._element=element
        self._file_creators:list[FileCreator]=[]

    def create(self):
        for file_creator in self._file_creators:
            file_creator.create()

    def register_file_creator(self,*file_creators):
        for fc in file_creators:
            self._file_creators.append(fc(
                element=self._element
            ))

    def get_relative_filenames(self) :
        return tuple(fc.get_relative_filename() for fc in self._file_creators)


# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    asker=AskParams()
    element=asker.ask()

    element_creator = ElementFilesCreator(element)
    element_creator.register_file_creator(
        TSXFileCreator,
        CSSFileCreator,
        IndexFileCreator
    )
    asker.ask_ok(element_creator.get_relative_filenames())
    element_creator.create()
    print(f"Всё создал и весь такой молодец!")


    # s=AskParams.ask_base_folder()
    # asker=AskParams()
    #







# -----------------------------------------------------------------------
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
