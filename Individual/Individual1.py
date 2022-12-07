#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
import jsonschema


def get_student(students, name,group,progress):
    # Запросить данные о студенте.
    students.append({
        "name": name,
        "group": group,
        "mark": progress
    })
    if len(students) > 1:
        students.sort(key=lambda item: item.get('group')[::-1])
    return students


def list(students):
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
            ma = student.get('mark', '')
            print(
                '| {:^4} | {:<30} | {:<20} | {}.{}.{}.{}.{:<7} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    ma[0],
                    ma[1],
                    ma[2],
                    ma[3],
                    ma[4]
                )
            )
            print(line)


def select(students):
    # Инициализировать счетчик.
    count = 0
    # Проверить сведения студентов из списка.
    for student in students:
        mark = student.get('mark', '')
        if sum(mark) / max(len(mark), 1) >= 4.0:
            print(
                '{:>4} {}'.format('*', student.get('name', '')),
                '{:>1} {}'.format('группа №', student.get('group', ''))
            )
            count += 1
    if count == 0:
        print("Студенты с баллом 4.0 и выше не найдены.")


def help_1():
    print("Список команд:\n")
    print("add - добавить студента;")
    print("list - вывести список студентов;")
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
    # Список студентов.
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
        help="The students's name"
    )
    add.add_argument(
        "-p",
        "--group",
        action="store",
        help="The group's post"
    )
    add.add_argument(
        "-y",
        "--mark",
        action="store",
        type=int,
        required=True,
        help="The mark"
    )
    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="list all students"
    )
    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the students"
    )
    select.add_argument(
        "-P",
        "--period",
        action="store",
        type=int,
        required=True,
        help="The required period"
    )

    args = parser.parse_args(command_line)

    is_dirty = False
    if os.path.exists(args.filename):
        students = load_students(args.filename)
    else:
        students = []
    if args.command == "add":
        students = get_student(
            students,
            args.name,
            args.progress,
        )
        is_dirty = True
    elif args.command == "list":
        list(students)
    elif args.command == "select":
        list(select(students))

    if is_dirty:
        save_students(args.filename, students)


if __name__ == '__main__':
    main()
