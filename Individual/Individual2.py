#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import click
import json


def get_student(students_load, name, group, progress, file_name):
    # Запросить данные о студенте.
    students_load.append(
        {
            "name": name,
            "group": group,
            "progress": progress
        }
    )
    with open(file_name, "w", encoding="utf-8") as fout:
        json.dump(students_load, fout, ensure_ascii=False, indent=4)
    return load_students(file_name)


def list(students_load):
    # Заголовок таблицы.
    if students_load:
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
        for idx, student in enumerate(students_load, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    student.get('name', ''),
                    student.get('group', ''),
                    student.get('progress', 0)
                )
            )
            print(line)


def show_selected(students_load):
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
    for i, student in enumerate(students_load, 1):
        if student.get('progress', 0) == 4 or student.get('progress', 0) == 5:
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


def load_students(file_name):
    with open(file_name, "r", encoding="utf-8") as fin:
        loadfile = json.load(fin)
    return loadfile


@click.command()
@click.option("-c", "--command")
@click.argument('file_name')
@click.option("-n", "--name")
@click.option("-g", "--group")
@click.option("-pr", "--progress")
def main(command, name, group, progress, file_name):
    students_load = load_students(file_name)
    if command == 'add':
        get_student(students_load, name, group, progress, file_name)
        click.secho('Данные добавлены')
    elif command == 'display':
        list(students_load)
    elif command == 'select':
        show_selected(students_load)


if __name__ == '__main__':
    main()
