'''Функція сканування папок'''

import sys
import shutil
from pathlib import Path #Path для ітерування (проходження) по файлам і папкам

'''створюємо списки відповідно до розширення файлів'''
jpeg_files = list()
doc_files = list()
video_files = list()
music_files = list()
folders = list()
archives = list()
others = list()
unknown = set()           #колекція НЕвідомих розширень  
extensions = set()        #колекція відомих розширень  

#словник, в якому ключі - розширення файлів
registered_extensions = {
    "JPEG": jpeg_files,
    "PNG": jpeg_files,
    "JPG": jpeg_files,
    "SVG": jpeg_files,
    "TXT": doc_files,
    "DOCX": doc_files,
    "DOC": doc_files,
    "XLSX": doc_files,
    "PPTX": doc_files,
    "PDF": doc_files,
    "AVI": video_files,
    "MP4": video_files,
    "MOV": video_files,
    "MKV": video_files,
    "MP3": music_files,
    "OGG": music_files,
    "WAV": music_files,
    "AMR": music_files,
    "ZIP": archives,
    "GZ": archives,
    "RAR": archives,
    "TAR": archives
}

#ф-ція обробки розширень
def get_extensions(file_name):                  #отримуємо ім'я файлу
    return Path(file_name).suffix[1:].upper()   #працюємо з суфіксом (беремо розширення) файлу  

'''сканування папок'''
def scan(folder):
    for item in folder.iterdir():                #проходимо по всім елементам папки
        if item.is_dir():                        #перевірка чи є елемент папцкою
            if item.name not in ('IMAGES' , 'DOCUMENTS', 'AUDIO', 'VIDEO', 'ARCHIVES', 'OTHERS'):  #ігноруємо папки для відсортованих файлів
                folders.append(item)             #додаємо назву пройденого каталогу в список
                scan(item)                       #скануємо папку                   
            continue                             #якщо папка зі списку то пропускаємо її

        #блок роботи з файлами  
        extension = get_extensions(file_name=item.name)  #працюємо з розширенням (відділяємо)

        new_name = folder / item.name                    #new_name - шлях. Передаємо шлях до файлу  

        if not extension:                                #перевіряємо чи є у файла розширення
            others.append(new_name)                      #додаємо його в список 'OTHERS'
        
        else:                                            #працюємо з файлами з розширеннями
            try:
                container = registered_extensions[extension]
                extensions.add(extension)                 #зберігаємо відомі розширення в множину (set)
                container.append(new_name)                #додаємо в контейнер ім'я файлу
            except KeyError:                              #KeyError якщо розширення не знайдено  
                unknown.add(extension)                    #зберігаємо НЕвідомі розширення
                others.append(new_name)                   #зберігаємо файли без розширень


    #друкуємо те що зберегли в контейнерах
    # print(f'IMAGES jpeg, jpg, png, svg: {jpeg_files}\n')    
    # print(f'VIDEO mp4, avi, mov, mkv : {video_files}\n')
    # print(f'DOCS docs, doc, txt, xlsx, pptx, pdf : {doc_files}\n')
    # print(f'MUSIC mp3, ogg, wav, amr: {music_files}\n')
    # print(f'ARCHIVES zip, gz, rar: {archives}\n')
    # print(f'others: {others}\n')
    # print(f'All extensions: {extensions}')
    # print(f'unknown extentions: {unknown}\n')

 
