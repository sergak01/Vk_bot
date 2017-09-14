# -*- coding: utf-8 -*-
import requests

update_parameters = []
version = [str, int, int, int]
last_version = [str, int, int, int]

def main():
    get_version()

def get_version():
    with open("Version.txt", "r") as version_file:
        print("Файл версий открыт")
        first_line = version_file.readline()
        print(first_line)
        update_parameters = first_line.split()
        print(update_parameters)

def get_last_version(version):
    if version[0] == "Alpha":
        ver_file = requests.get("https://raw.githubusercontent.com/sergak01/Vk_bot/Ver.-Alpha/Version.txt")
        print(ver_file)
    elif version[0] == "Beta":
        pass
    elif version[0] == "Stable":
        pass
    else:
        print("Данные о версии повреждены или не получены!")
        quit()


if __name__ == "__main__":
    main()