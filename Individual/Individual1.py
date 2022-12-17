#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
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
    Вывести список студентов
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
                "Успеваемость"
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


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("students")
    parser.add_argument(
        "--version",
        action="version",
        help="The main parser",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления студента.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new student"
    )
    add.add_argument(
        "-n",
        "--name",
        action="store",
        required=True,
        help="The student's name"
    )
    add.add_argument(
        "-g",
        "--group",
        type=int,
        action="store",
        help="The student's group"
    )
    add.add_argument(
        "-gr",
        "--grade",
        action="store",
        required=True,
        help="The student's grade"
    )

    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all students"
    )

    # Создать субпарсер для выбора студентов.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the students"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех студентов из файла, если файл существует.
    is_dirty = False
    if os.path.exists(args.filename):
        students = load_students(args.filename)
    else:
        students = []

    # Добавить студента.

    if args.command == "add":
        students = add_student(
            students,
            args.name,
            args.group,
            args.grade
        )
        is_dirty = True
    # Отобразить всех студентов.
    elif args.command == "display":
        show_list(students)
    # Выбрать требуемых студентов.
    elif args.command == "select":
        selected = show_selected(students)
        show_list(selected)

    # Сохранить данные в файл, если список студентов был изменен.
    if is_dirty:
        save_students(args.filename, students)


if __name__ == '__main__':
    main()
