'''Функція сканування папок'''

import shutil
import sys
import normalize
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import time

'''створюємо списки відповідно до розширення файлів'''
jpeg_files = list()
doc_files = list()
video_files = list()
music_files = list()
folders = list()
archives = list()
others = list()
unknown = set()
extensions = set()

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
    "MPEG": video_files,
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
def get_extensions(file_name):
    return Path(file_name).suffix[1:].upper()

'''сканування папок'''
def scan(folder):
    for item in folder.iterdir():
        if item.is_dir():
            if item.name not in ('IMAGES', 'DOCUMENTS', 'AUDIO', 'VIDEO', 'ARCHIVES', 'OTHERS'):
                folders.append(item)
                scan(item)
            continue
        # else:
        #     extension = get_extensions(file_name=item.name)
        #     new_name = folder / item.name
        extension = get_extensions(file_name=item.name)  #працюємо з розширенням (відділяємо)

        new_name = folder / item.name   

        if not extension:
            others.append(new_name)
        else:
            try:
                container = registered_extensions[extension]
                extensions.add(extension)
                container.append(new_name)
            except KeyError:
                unknown.add(extension)
                others.append(new_name)
 #друкуємо те що зберегли в контейнерах
    # print(f'IMAGES jpeg, jpg, png, svg: {jpeg_files}\n')    
    # print(f'VIDEO mp4, avi, mov, mkv, mpeg : {video_files}\n')
    # print(f'DOCS docs, doc, txt, xlsx, pptx, pdf : {doc_files}\n')
    # print(f'MUSIC mp3, ogg, wav, amr: {music_files}\n')
    # print(f'ARCHIVES zip, gz, rar: {archives}\n')
    # print(f'others: {others}\n')
    # print(f'All extensions: {extensions}')
    # print(f'unknown extentions: {unknown}\n')


def hande_file(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)
    path.replace(target_folder/normalize.normalize(path.name))

def handle_archive(path, root_folder, dist):
    target_folder = root_folder / dist
    target_folder.mkdir(exist_ok=True)

    new_name = normalize.normalize(path.name.replace(".zip", ''))
    archive_folder = target_folder / new_name
    archive_folder.mkdir(exist_ok=True)

    try:
        shutil.unpack_archive(str(path.resolve()), archive_folder)
    except shutil.ReadError:
        archive_folder.rmdir()
        return
    except FileNotFoundError:
        archive_folder.rmdir()
        return
    path.unlink()

def remove_empty_folders(path):
    for item in path.iterdir():
        if item.is_dir():
            remove_empty_folders(item)
            try:
                item.rmdir()
            except OSError:
                pass

def get_folder_objects(root_path):
    for folder in root_path.iterdir():
        if folder.is_dir():
            remove_empty_folders(folder)
            try:
                folder.rmdir()
            except OSError:
                pass

def main(folder_path):
    scan(folder_path)
    start_time = time.time()  # Фіксуємо початковий час виконання програми
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        for item in folder_path.iterdir():
            executor.submit(scan, item)
            print('Executor FOLDERS is working...')

    with ThreadPoolExecutor(max_workers=5) as executor:
        for file in jpeg_files:
            executor.submit(hande_file, file, folder_path, "IMAGES")
            print('Executor FILES is working...')

        for file in doc_files:
            executor.submit(hande_file, file, folder_path, "DOCUMENTS")

        for file in video_files:
            executor.submit(hande_file, file, folder_path, "VIDEO")

        for file in music_files:
            executor.submit(hande_file, file, folder_path, "AUDIO")

        for file in archives:
            executor.submit(handle_archive, file, folder_path, "ARCHIVES")

        for file in unknown:
            executor.submit(hande_file, file, folder_path, "OTHERS")

        for file in others:
            executor.submit(hande_file, file, folder_path, "OTHERS")
        
        

    get_folder_objects(folder_path)
    remove_empty_folders(folder_path)

    end_time = time.time()  # Фіксуємо час завершення виконання програми
    elapsed_time = end_time - start_time  # Розраховуємо загальний час виконання
    print(f"Program execution time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    path = sys.argv[1]
    arg = Path(path)

    main(arg.resolve())
