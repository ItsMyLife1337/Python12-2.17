#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import click
import os.path


def add_student(students, name, group, grade):
    """
    Добавить данные о студенте
    """
    students.append(
        {
            'name': name,
            'group': group,
            'grade': grade,
        }
    )
    return students


def show_list(students):
    """
    Вывести список с тудентов
    """
    # Заголовок таблицы.
    if students:

        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 15
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^15} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Успеваемость "
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('grade', 0)
                )
            )
        print(line)
    else:
        print("Список студентов пуст.")


def show_selected(students):
    # Проверить сведения студентов из списка.
    result = []
    for student in students:
        grade = [int(x) for x in (student.get('grade', '').split())]
        if sum(grade) / max(len(grade), 1) >= 4.0:
            result.append(student)
    return result


def help_1():
    print("Список команд:\n")
    print("add - добавить студента;")
    print("display - вывести список студентов;")
    print("select - запросить студентов с баллом выше 4.0;")
    print("save - сохранить список студентов;")
    print("load - загрузить список студентов;")
    print("exit - завершить работу с программой.")


def save_students(file_name, students):
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students, fout, ensure_ascii=False, indent=4)


def load_students(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        return json.load(fin)


@click.command()
@click.argument('filename')
@click.option('--command', '-c', help="Commands")
@click.option('--name', '-n', help="The students name")
@click.option('--group', '-gr', type=int, help="The plane's numer")
@click.option('--grade', '-g', help="The plane's type")
def main(command, name, group, grade, filename):
    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(filename):
        students = load_students(filename)
    else:
        students = []

    # Добавить студента.

    if command == "add":
        students = add_student(students, name, group, grade)
        is_dirty = True

    # Отобразить всех студентов.
    elif command == "display":
        show_list(students)

    # Выбрать требуемых студентов.
    elif command == "select":
        selected = show_selected(students)
        show_list(selected)

    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(filename, students)


if __name__ == '__main__':
    main()
