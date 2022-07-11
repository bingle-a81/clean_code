# -*- coding: utf-8 -*-
import logging.config
from settings import logger_config
import random
from dataclasses import dataclass
import copy
# from typing_extensions import TypeAlias
# from typing import Literal

logging.config.dictConfig(logger_config)
logger = logging.getLogger('app_logger.' + __name__)

@dataclass
class Attempt:
    pile:int
    stone:int


def lay_out_the_stones()->int:
    ferst_pile=random.randint(1,20)
    logger.debug(f'pile={ferst_pile}')
    return ferst_pile

def take_from_the_pile()->Attempt:
    while True:
        print(f'Из какой кучи брать? \n 1-2-3?')
        a = input(": ").strip().lower()
        if (a.isdigit()) and (0<int(a)<4) :
            pile=int(a)
            break
        else:
            print('ниче не понял . введи от 1 до 3')
    while True:
        b = input("f'Сколько камней брать?': ")
        if b.isdigit() and (0<int(b)<11) :
            stone=int(b)
            break
        else:
            print('ниче не понял . введи числа!')
    return Attempt(pile=pile,stone=stone)


def find_out_the_position_of_the_stones(three_piles:dict,att:Attempt)->dict:
    k=three_piles[att.pile]-att.stone
    logger.debug(f'k {k}')
    if k<0:
        print("повтори")
    else:
        three_piles[att.pile]=k
        logger.debug(f'three_piles={three_piles}')
    return three_piles


def check_the_victory(three_piles:dict)->bool:
    if all([three_piles[x] == 0 for x in three_piles]):
        return False
    else:
        return True
# ***********************************************************************
# -----------------------------------------------------------------------
#
def main():
    logger.debug("Start ")
    # three_piles={}
    three_piles={k:lay_out_the_stones() for k in range(1,4)}
    logger.debug(f'three_piles={three_piles}')
    player=1
    flag=True
    while flag==True:
        three_piles_copy=copy.deepcopy(three_piles)
        if player%2==0:
            print('Игроку 2 приготовиться!')
        else:
            print('Игроку 1 приготовиться!')
        player_attempt=take_from_the_pile()
        logger.debug(player_attempt)
        three_piles=find_out_the_position_of_the_stones(three_piles,player_attempt)
        logger.debug(f'after change {three_piles}')
        if any([three_piles[x] != three_piles_copy[x] for x in three_piles]):
            player+=1
        else:
            print('Попробуй еще раз!!')
        flag=check_the_victory(three_piles)
        logger.debug(f'flag={flag}')
    else:
        if player%2==0:
            print('Игроку 1 победа!')
        else:
            print('Игроку 2 победа!')

    logger.debug("End")


# -----------------------------------------------------------------------
if __name__ == '__main__':
    main()
