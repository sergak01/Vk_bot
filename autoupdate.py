# -*- coding: utf-8 -*-
import requests
import subprocess
import os
import re
import sys
import zipfile

update_parameters = []
version = [str, int, int, int]
last_version = [str, int, int, int]
text_last_version = ""

def main(update=False):
    get_version()
    version = get_version_from_text(update_parameters[0])
    print("Текущая версия бота: " + str(version))
    last_version = get_last_version(version)
    print("Последняя версия бота: " + str(last_version))
    if version[0] == last_version[0] and (
            version[1] < last_version[1] or
            version[2] < last_version[2] or
            version[3] < last_version[3]
        ):
        if "-Autoupdate" in update_parameters or update == True or version[1] == 0:
            print("Запускаю автообновление!")
            get_update_zip(last_version)
            if zipfile.is_zipfile('update.zip'):
                print("Открываем архив обновления")
                z = zipfile.ZipFile('update.zip', 'r')
                print("Архив открыт")
                print("Распаковываем архив")
                extract_zip(z)
                z.close()
                print("Удаляем архив обновления")
                os.remove("update.zip")
                print("Обновление закончено. Запускаю бота...")
                subprocess.Popen("python.exe .\start.py")
        else:
            print("Доступно обновление бота. Это обновление не будет установлено автоматически. Для установки выполните команду 'python autoupdate.py -update'")
    else:
        print("Бот не нуждаеться в обновлении.")
        quit()
    quit()

def get_version():
    global update_parameters
    try:
        with open("Version.txt", "r") as version_file:
            print("Файл версий открыт")
            first_line = version_file.readline()
            if first_line[0] == "":
                raise FileNotFoundError
            update_parameters = first_line.split()
    except FileNotFoundError:
        print("Файл версий не найден! Будет скачана последння Alpha версия")
        update_parameters = str("[Ver.-Alpha(0.00.00)] -Autoupdate").split()

def get_last_version(version):
    global update_parameters
    if version[0] == "Alpha":
        ver_file = requests.get("https://raw.githubusercontent.com/sergak01/Vk_bot/Ver.-Alpha/Version.txt")
        first_line = ver_file.content.decode("utf-8").split('\n', 1)[0]
        update_parameters = first_line.split()
        return get_version_from_text(update_parameters[0])
    elif version[0] == "Beta":
        pass
    elif version[0] == "Stable":
        pass
    else:
        print("Данные о версии повреждены или не получены!")
        quit()

def get_version_from_text(version_text):
    temp_version = [str, int, int, int]
    rexp_parser = re.compile(r'\[Ver\.-([^\(]+)\((\d+)\.(\d+)\.(\d+)[^$]+')
    if rexp_parser.sub("", version_text) == "":
        temp_version[0] = str(rexp_parser.sub(r'\1', version_text))
        temp_version[1] = int(rexp_parser.sub(r'\2', version_text))
        temp_version[2] = int(rexp_parser.sub(r'\3', version_text))
        temp_version[3] = int(rexp_parser.sub(r'\4', version_text))
        return temp_version
    else:
        print("Версия программы имеет неверный формат. Закрываюсь...")
        quit()

def get_update_zip(version):
    global text_last_version
    text_last_version = "Ver.-" + version[0] + "(" + \
        (str(version[1])) + \
        "." + ("0" + str(version[2]) if len(str(version[2])) < 2 else str(version[2])) + \
        "." + ("0" + str(version[3]) if len(str(version[3])) < 2 else str(version[3])) + ")"
    path_to_web_zip = "https://github.com/sergak01/Vk_bot/archive/" + text_last_version + ".zip"
    try:
        with open("update.zip", "wb") as zipfile:
            print("Пытаюсь скачать архив обновления...")
            byte_data = requests.get(path_to_web_zip)
            print("Архив обновления получен. Сохраняю...")
            zipfile.write(byte_data.content)
            print("Архив обновления сохранен")
    except Exception as e:
        print(e)

def extract_zip(zipfile):
    root = os.path.abspath('.')
    name_list = zipfile.namelist()
    new_files_path = {}
    directory_tree = {}
    print("Получаю имена файлов и директорий...")
    for name in name_list:
        if name.split('/')[-1] != "":
            new_files_path.update({name.split('/')[-1]: name.split('/')})
        elif len(name.split('/')) > 2:
            directory_tree.update({name.split('/')[-2]: name.split('/')})
    print("Создаю дерево директорий...")
    for name, path in directory_tree.items():
        temp_path = ""
        for i in range(1, len(path)):
            temp_path += path[i] + "\\"
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
    print("Создаю файлы...")
    for name, path in new_files_path.items():
        temp_path = ""
        for i in range(1, len(path) - 1):
            temp_path += path[i] + "\\"
        temp_path += path[-1]
        with open(temp_path, "wb") as file:
            f_path_temp = ""
            for i in range(0, len(path) - 1):
                f_path_temp += path[i] + "/"
            f_path_temp += path[-1]
            file.write(zipfile.read(f_path_temp))
    print("Файлы успешно созданы")

if __name__ == "__main__":
    if len (sys.argv) > 1:
        for param in sys.argv:
            if param == "-update" or param == "-u":
                main(update=True)
    else:
        main()