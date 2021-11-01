from pathlib import Path

custom_path = Path('custom_parameters.txt')
vars_path = Path('mymodules', 'vars.txt')
default_path = Path('mymodules', 'default.txt')

numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '.')


class Var:
    """
    Класс изменяемых переменных
    :param name: имя переменной
    :param value: значение переменной
    :param default: стандартное значение переменной из файла (строка)
    :param custom: пользовательское значение переменной из файла (строка)
    :param vartype: требуемый тип переменной: 0 - любой числовой, 1 - целочисленный
    :param restriction: дополнительные ограничения для переменной:
        0 - нет ограничений
        1 - положительное (в случае целочисленного типа - большее или равное 1)
        (names, sizes) - больше, чем сумма каждой переменной из names, умноженной на соответствующее значение sizes
    """
    def __init__(self, name, value, default, custom, vartype, restriction):
        self.name = name
        self.value = value
        self.default = default
        self.custom = custom
        self.vartype = vartype
        self.restriction = restriction


def getvars():
    """
    Считывает названия переменных и их типы из файла vars
    """
    varlist = []
    with open(vars_path, 'r') as file:
        lines = file.readlines()
        for i in lines:
            templist = i.split('; ')
            varlist.append(Var(templist[0], 0, '', '', int(templist[1]), templist[2]))
    return varlist


def getparameter(string, varlist, param_numbers, is_default):
    """
    Считывает значение переменной из файла
    :param string: строка файла, которая может содержать переменную
    :param varlist: список объектов переменных, которые необходимо определить
    :param param_numbers: кортеж из цифр, точки и запятой в символьном формате
    :param is_default: определяет, является ли полученное значение стандартным (True) или пользовательским (False)
    """
    for var in varlist:
        if string.find(var.name) == 0:
            k = len(var.name)
            line = ''
            while string[k] not in param_numbers and k < len(string) and string[k] != '#':
                k += 1
            while string[k] in param_numbers and k < len(string):
                if string[k] == ',':
                    string[k] = '.'
                line += string[k]
                k += 1
            if line != '':
                if is_default:
                    var.default = line
                else:
                    var.custom = line
            break


def getdefault(varlist):
    """
    Считывание переменных из файла default.txt
    :param varlist: список объектов переменных
    """
    with open(default_path, 'r') as file:
        lines = file.readlines()
        for j in lines:
            getparameter(j, varlist, numbers, True)


def getcustom(varlist):
    """
    Считывание переменных из файла custom_parameters.txt
    :param varlist: список объектов переменных
    """
    with open(custom_path, 'r') as file:
        lines = file.readlines()
        for j in lines:
            getparameter(j, varlist, numbers, False)


def reset_custom():
    """
    Сбрасывает пользовательские настройки изменяемых переменных до стандартных значений
    """
    with open(custom_path, 'w') as custom_parameters:
        with open(default_path, 'r') as default_parameters:
            for j in default_parameters.readlines():
                print(j, file=custom_parameters, end='')


def check(varlist):
    """
    Проверяет тип и размер переменных, введённых пользователем
    В случае несоответствия преобразует их или присваивает стандартное значение
    :param varlist: список объектов переменных
    """
    for var in varlist:
        if var.vartype == 1:
            if var.custom == '':
                var.value = int(var.default)
            else:
                var.value = int(var.custom)
        elif var.vartype == 0:
            if var.custom == '':
                var.value = float(var.default)
            else:
                var.value = float(var.custom)
    for var in varlist:
        if not var.restriction[0] == '\\':
            rest = int(float(var.restriction))
            if rest == 1:
                if var.value <= 0:
                    if var.vartype == 1:
                        var.value = int(var.default)
                    else:
                        var.value = float(var.default)
    for var in reversed(varlist):
        if var.restriction[0] == '\\':
            line = var.restriction.replace('\\', '', 1)
            rest = line.split(', ')
            names = rest[0].split(' / ')
            sizes = rest[1].split(' / ')
            s = 0
            for j in range(0, len(names), 1):
                for i in varlist:
                    if i.name == str(names[j]):
                        if sizes[j].isdigit():
                            s += i.value * int(sizes[j])
                        else:
                            for k in varlist:
                                if k.name == sizes[j]:
                                    s += i.value * k.value
                    break
            if var.value <= s:
                    if var.vartype == 1:
                        var.value = int(var.default)
                    else:
                        var.value = float(var.default)


def get():
    """
    Получает значения изменяемых переменных
    :return: список объектов переменных
    """
    varlist = getvars()
    getdefault(varlist)
    getcustom(varlist)
    check(varlist)
    return varlist
