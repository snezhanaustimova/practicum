# -*- coding: utf-8 -*-

from pathlib import Path
from TextFeatures import bcolors
import os, shutil
from settings import root


def err_msg(text):

    print(bcolors.FAIL, text, bcolors.ENDC)

# создание пустого каталога
def crdir(current_dir, dir_name):

    new_dir = current_dir/dir_name

    try:
        Path.mkdir(new_dir)

    # на случай, если каталог уже существует
    except FileExistsError:
        err_msg('Directory "{}" already exists'.format(str(new_dir)))


# удаление директории
def deldir(current_dir, dir_name):

    del_dir = current_dir/dir_name

    try:
        # проверяем содержимое каталога
        if len(os.listdir(del_dir)) == 0:
            # и если он пустой, то просто удаляем его средствами Path
            Path.rmdir(del_dir)

        else:
            # если нет, то оповещаем пользователя о том, что директория не пуста и запрашиваем подтверждение
            choose = input(err_msg('Directory "{}" is not empty. Continue? (y/n)'.format(str(del_dir))))

            # если пользователь согласен, то удаляем со всем содержимым
            if choose.lower() == 'y':
                shutil.rmtree(del_dir)
            elif choose.lower() == 'n':
                pass
            else:
                err_msg('Unknown command "{}"'.format(choose))

    # на случай, если введенной папки в принципе не существует
    except FileNotFoundError:
        err_msg('Directory "{}" does not exists'.format(str(del_dir)))


# перемещение в директорию по заданному пути
def go(current_dir, dir_name=''):

    # если не задан путь, то переходим в домашнюю папку
    if not dir_name: return root

    new_dir = current_dir/dir_name

    try:
        if not new_dir.exists():
            err_msg('Path "{}" does not exist'.format(str(new_dir)))
        elif not new_dir.is_dir():
            err_msg('"{}" is not a directory'.format(str(new_dir)))
        else:
            if new_dir.name == '..' and current_dir == root:
                err_msg('Going outside of the root directory is not available')
            else:
                current_dir = new_dir
    except OSError as e:
        err_msg(e)
    return current_dir.resolve()


# создание файла
def crfile(current_dir, file_name):

    new_file = current_dir/file_name
    open(str(new_file), 'w')


# запись текста в файл
def write(current_dir, file_name, text):

    file = current_dir / file_name

    if not file.exists():
        err_msg('File "{}" does not exist'.format(str(file)))
    elif not file.is_file():
        err_msg('{} is not a file'.format(str(file)))
    else:
        with open(file, 'a') as f:
            f.write(text)


# просмотр содержимого каталога
def view(current_dir):

    for f in current_dir.iterdir():
        if f.is_dir():
            print(bcolors.OKBLUE, f.parts[-1:][0], bcolors.ENDC)
        else:
            print(f.parts[-1:][0])


# удаление файла
def delfile(current_dir, file_name):

    file = current_dir / file_name

    if not file.exists():
        err_msg('File "{}" does not exist'.format(str(file)))
    elif not file.is_file():
        err_msg('{} is not a file'.format(str(file)))
    else:
        file.unlink()


# копирование файла
def cpfile(current_dir, file_name, transfer_dir):

    file = current_dir / file_name

    if not file.exists():
        err_msg('File "{}" does not exist'.format(str(file)))
    elif not file.is_file():
        err_msg('{} is not a file'.format(str(file)))
    else:
        if not transfer_dir.exists():
            err_msg('Path "{}" does not exist'.format(transfer_dir))
        elif not transfer_dir.is_dir():
            err_msg('"{}" is not a directory'.format(transfer_dir))
        else:
            shutil.copy(os.path.join(current_dir, file_name), os.path.join(transfer_dir, file_name))


# перемещение файла
def mvfile(current_dir, file_name, transfer_dir):

    file = current_dir/file_name

    if not file.exists():
        err_msg('File "{}" does not exist'.format(str(file)))
    elif not file.is_file():
        err_msg('{} is not a file'.format(str(file)))
    else:
        if not transfer_dir.exists():
            err_msg('Path "{}" does not exist'.format(transfer_dir))
        elif not transfer_dir.is_dir():
            err_msg('"{}" is not a directory'.format(transfer_dir))
        else:
            shutil.move(os.path.join(current_dir, file_name), os.path.join(transfer_dir, file_name))


def rename(current_dir, file_name, new_name):

    file = current_dir / file_name
    new_file = current_dir / new_name

    if not file.exists():
        err_msg('File "{}" does not exist'.format(str(file)))
    elif not file.is_file():
        err_msg('{} is not a file'.format(str(file)))
    else:
        if new_file.exists():
            err_msg('File "{}" is already exist'.format(str(new_file)))
        else:
            Path.replace(file, new_file)


def main():

    current_dir = root

    while True:
        command = input('current_dir:{}$ '.format(current_dir))
        command = command.split()

        if len(command) < 1: continue

        if command[0] == 'crdir':
            if not len(command) == 2:
                err_msg('Wrong number of arguments')
            else:
                crdir(current_dir, command[1])

        elif command[0] == 'deldir':
            if not len(command) == 2:
                err_msg('Wrong number of arguments')
            else:
                deldir(current_dir, command[1])

        elif command[0] == 'go':

            if len(command) == 2:
                current_dir = go(current_dir, command[1])
            elif len(command) == 1:
                current_dir = go(current_dir)
            else:
                if len(command) > 2:
                    path = command[1:]
                    transfer_dir = ''
                    if path[0][0] == '"':
                        path[0] = path[0][1:]
                        path[-1] = path[-1][:-1]
                        for i in path:
                            transfer_dir += i + ' '
                        transfer_dir = transfer_dir[:-1]
                        current_dir = go(current_dir, transfer_dir)
                    else:
                        err_msg('Invalid directory entry format')
                else:
                    err_msg('Wrong number of arguments')

        elif command[0] == 'crfile':
            if len(command) == 1:
                err_msg('Wrong number of arguments')
            else:
                for file in command[1:]:
                    crfile(current_dir, file)

        elif command[0] == 'write':
            if len(command) in [1, 2]:
                err_msg('Wrong number of arguments')
            else:
                file = command[1]
                words = command[2:]
                text = ''
                if words[0][0] == '"':
                    words[0] = words[0][1:]
                    words[-1] = words[-1][:-1]
                for word in words:
                    text += word + ' '
                write(current_dir, file, text)

        elif command[0] == 'view':
            if not len(command) == 1:
                err_msg('view command does not have arguments')
            else:
                view(current_dir)

        elif command[0] == 'delfile':
            if len(command) == 1:
                err_msg('Wrong number of arguments')
            else:
                for file in command[1:]:
                    delfile(current_dir, file)

        elif command[0] == 'cpfile':
            if len(command) in [1, 2]:
                err_msg('Wrong number of arguments')
            elif len(command) > 3 and command[2][0] != '"':
                err_msg('Invalid directory entry format')
            else:
                file = command[1]
                path = command[2:]
                transfer_dir = ''
                if path[0][0] == '"':
                    path[0] = path[0][1:]
                    path[-1] = path[-1][:-1]
                    for i in path:
                        transfer_dir += i + ' '
                    transfer_dir = transfer_dir[:-1]
                else:
                    transfer_dir = current_dir / command[2]
                transfer_dir = Path(transfer_dir)
                cpfile(current_dir, file, transfer_dir)

        elif command[0] == 'mvfile':
            if len(command) in [1, 2]:
                err_msg('Wrong number of arguments')
            elif len(command) > 3 and command[2][0] != '"':
                err_msg('Invalid directory entry format')
            else:
                file = command[1]
                path = command[2:]
                transfer_dir = ''
                if path[0][0] == '"':
                    path[0] = path[0][1:]
                    path[-1] = path[-1][:-1]
                    for i in path:
                        transfer_dir += i + ' '
                    transfer_dir = transfer_dir[:-1]
                else:
                    transfer_dir = current_dir / command[2]
                transfer_dir = Path(transfer_dir)
                mvfile(current_dir, file, transfer_dir)

        elif command[0] == 'rename':
            if len(command) != 3:
                err_msg('Wrong number of arguments')
            else:
                rename(current_dir, command[1], command[2])

        elif command[0] == 'exit':
            break

        else:
            err_msg('Unknown command "{}"'.format(command[0]))


if __name__ == '__main__':
    main()