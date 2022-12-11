#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os


def get_student(students, name, group, progress):
    # Запросить данные о студенте.
    students.append(
        {
            "name": name,
            "group": group,
            "progress": progress
        }
    )
    return students


def list(students):
    # Заголовок таблицы.
    if students:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "Ф.И.О.",
                "Группа",
                "Оценка"
            )
        )
        print(line)

        # Вывести данные о всех студентах.
        for idx, student in enumerate(students, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('progress', 0)
                )
            )
            print(line)


def show_selected(students):
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
            "Оценка"
        )
    )
    print(line)
    # Инициализировать счетчик.
    count = 0
    # Проверить сведения студентов из списка.
    for student in students:
        if student.get('progress', 0) >= 4.0:
            count += 1
            print(
                '| {:>4} | {:<30} | {:<20} | {:>15} |'.format(
                    count,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('progress', 0)
                )
            )
    print(line)
    if count == 0:
        print("Студенты с оценкой 4.0 и выше не найдены.")


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
        "-g",
        "--group",
        action="store",
        help="The group's post"
    )
    add.add_argument(
        "-p",
        "--progress",
        action="store",
        type=int,
        required=True,
        help="The mark"
    )
    # Создать субпарсер для отображения всех студентов.
    _ = subparsers.add_parser(
        "list",
        parents=[file_parser],
        help="list all students"
    )
    # Создать субпарсер для выбора студентов с оценкой >= 4-рём.
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
            args.group,
            args.progress
        )
        is_dirty = True
    elif args.command == "list":
        list(students)
    elif args.command == "select":
        show_selected(students)
    if is_dirty:
        save_students(args.filename, students)


if __name__ == '__main__':
    main()
