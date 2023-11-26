'''Функція normalize - зміна імені файлів з кирилиці на латиницю'''

import re #модуль регулярних обчислень
from pathlib import Path

UKRAINIAN_SYMBOLS = 'абвгдеєжзиіїйклмнопрстуфхцчшщьюя'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "je", "zh", "z", "y", "i", "ji", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "ju", "ja")

TRANS = {}  #створюємо словник

for key, value in zip(UKRAINIAN_SYMBOLS, TRANSLATION):  #ітеруємось: звертання до ключів і значень словника 
    TRANS[ord(key)] = value                             #створення (заповнення) словника TRANS
    TRANS[ord(key.upper())] = value.upper()             #створення (заповнення) словника TRANS великими буквами
    #словник TRANS заповнений малими і великими літерми

def normalize(name):                                #приймає на вхід ім'я файлу та переводить його в нове ім'я new_name
    name,*extension = name.split('.')              #розбиває ім'я файла на дві складові: ім'я та розширення
    new_name = name.translate(TRANS)                #заміна кириличних символів в імені файла
    new_name = re.sub(r'\W', '-', new_name)         #заміна не букв в імені файлу: дужки, пробіли, мінуси і т.д.
    return f"{new_name}.{'.'.join(extension)}"



         