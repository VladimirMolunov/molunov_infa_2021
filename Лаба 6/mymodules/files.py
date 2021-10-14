import pathlib
from pathlib import Path

custom_path = Path('custom_parameters.txt')
playerdata_path = Path('mymodules', 'playerdata.txt')
default_path = Path('mymodules', 'default')
playerdata = open(playerdata_path, 'r')

names = ('TPS', 'max_radius')
numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '.')


def getparameter(string, param_names, param_numbers):
    """
    Считывает значение переменной из файла
    :param string: строка файла, которая может содержать переменную
    :param param_names: кортеж названий переменных, которые необходимо определить
    :param param_numbers: кортеж из цифр, точки и запятой в символьном формате
    """
    for j in param_names:
        exec('global ' + j)
    for j in param_names:
        if string.find(j) == 0:
            k = len(j)
            line = ''
            while string[k] not in param_numbers and k < len(string):
                k += 1
            while string[k] in param_numbers and k < len(string):
                if string[k] == ',':
                    string[k] = '.'
                line += string[k]
                k += 1
            if line != '':
                exec(j + ' = ' + line, globals())
            break


def getdefault(varnames):
    with open(default_path, 'r') as file:
        """
        Считывание переменных из файла default.txt
        :param varnames: кортеж названий переменных
        """
        var = file.readlines()
        for j in var:
            getparameter(j, varnames, numbers)


def getcustom(varnames):
    with open(custom_path, 'r') as file:
        """
        Считывание переменных из файла custom_parameters.txt
        :param varnames: кортеж названий переменных
        """
        var = file.readlines()
        for j in var:
            getparameter(j, varnames, numbers)


def reset_custom():
    with open(custom_path, 'w') as custom_parameters:
        with open(default_path, 'r') as default_parameters:
            for j in default_parameters.readlines():
                print(j, file=custom_parameters, end='')


data = playerdata.readlines()
getdefault(names)
playerdata.close()
playerdata = open('playerdata.txt', 'w')

for i in data:
    print(i, file=playerdata, end='')
