#!/usr/bin/env python3
# -*- config: utf-8 -*-
# Использовать словарь, содержащий следующие ключи: фамилия, имя; номер телефона;
# дата рождения. Написать программу, выполняющую следующие
# действия: ввод с клавиатуры данных в список, состоящий из словарей заданной структуры;
# записи должны быть упорядочены по трем первым цифрам номера телефона; вывод на
# экран информации о человеке, чья фамилия введена с клавиатуры; если такого нет, выдать
# на дисплей соответствующее сообщение.
# Выполнить индивидуальное задание 2 лабораторной работы 14, добавив аннтотации типов.
# Выполнить проверку программы с помощью утилиты mypy.

from dataclasses import dataclass, field
import logging
import sys
from typing import List
import xml.etree.ElementTree as ET


class IllegalTimeError(Exception):

    def __init__(self, time, message="Запрещенное время :"):
        self.time = time
        self.message = message
        super(IllegalTimeError, self).__init__(message)

    def __str__(self):
        return f"{self.year} -> {self.message}"


class UnknownCommandError(Exception):

    def __init__(self, command, message="Неизвестная команда"):
        self.command = command
        self.message = message
        super(UnknownCommandError, self).__init__(message)

    def __str__(self):
        return f"{self.command} -> {self.message}"


@dataclass(frozen=True)
class poez:
    name: str
    num: str
    time: str


@dataclass
class Staff:
    poezd: List[poez] = field(default_factory=lambda: [])

    def add(self, name, num, time): -> None:

        if "." not in num:
            raise IllegalTimeError(time)

        self.poezd.append(
            poez(
                name=name,
                num=num,
                time=time
            )
        )


        self.poezd.sort(key=lambda poez: poez.num)

    def __str__(self):
        table = []
        l line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 17
        )
        table.append(line)
        table.append(
            '| {:^4} | {:^30} | {:^20} | {:^17} |'.format(
                "№",
                "Пункт назначения",
                "Номер поезда",
                "Время отправления"
            )
        )
        table.append(line)

        for idx, poez in enumerate(self.poezd, 1):
            table.append(
                '| {:>4} | {:<30} | {:<20} | {:>17} |'.format(
                    idx,
                    poez.name,
                    poez.num,
                    poez.time
                )
            )

        table.append(line)

        return '\n'.join(table)

    def select(self, name) -> List[Poez]:
        parts = command.split(' ', maxsplit=2)
        nam = (parts[1])
        result = []

        for poez in self.poezd:
            if poezd.name == name:
                result.append(poez)

        return result

    def load(self, filename):
        with open(filename, 'r', encoding='utf8') as fin:
            xml = fin.read()
        parser = ET.XMLParser(encoding="utf8")
        tree = ET.fromstring(xml, parser=parser)
        self.poezd = []

        for poez_element in tree:
            name, num, time = None, None, None

            for element in poez_element:
                if element.tag == 'name':
                    name = element.text
                elif element.tag == 'num':
                    num = element.text
                elif element.tag == 'time':
                    time = element.text

                if name is not None and num is not None \
                        and time is not None and time is not None:
                    self.poezd.append(
                        poez(
                            name=name,
                            num=int(num),
                            time=time
                        )
                    )


    def save(self, filename):
        root = ET.Element('poezd')
        for poez in self.poezd:
            poez_element = ET.Element('poez')

            name_element = ET.SubElement(poez_element, 'name')
            name_element.text = poez.name

            num_element = ET.SubElement(poez_element, 'num')
            num_element.text = poez.num

            time_element = ET.SubElement(poez_element, 'time')
            time_element.text = str(poez.time)

            root.append(poez_element)

    tree = ET.ElementTree(root)
    with open(filename, 'wb') as fout:
        tree.write(fout, encoding='utf8', xml_declaration=True)


if __name__ == '__main__':

    logging.basicConfig(
        filename='poezd.log',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s:%(message)s'
    )
    staff = Staff()

    while True:

            command = input(">>> ").lower()
            if command == 'exit':
                break


            elif command == 'add':
                name = input("Название пункта назначения: ")
                num = input("Номер поезда: ")
                time = input("Время отправления: ")

                staff.add(name, num, time)
                logging.info(f"Добавлено название: {name}, "
                f"Добавлен номер: {num}, "
                f"Добавлено время {time}. "
                )


            elif command == 'list':
                print(staff)
                logging.info("Отображен список поездов.")

            elif command.startswith('select '):
                parts = command.split(' ', maxsplit=2)
                selected = staff.select(parts[1])

                if selected:
                    for c, poez in enumerate(selected, 1):
                        print(
                            ('Название:', poez.name),
                            ('Номер :', poez.num,)),
                            ('Время:', poez.time)
                    )
                    logging.info(
                    f"Найден путь с названием {poez.name}"
                )

                else:
                    print("Таких названий нет!")
                    logging.warning(
                        f"Путь с названием {poez.name} не найден."
                    )

            elif command.startswith('load '):
                parts = command.split(' ', maxsplit=1)
                staff.load(parts[1])
                logging.info(f"Загружены данные из файла {parts[1]}.")

            elif command.startswith('save '):
                parts = command.split(' ', maxsplit=1)
                staff.save(parts[1])
                logging.info(f"Сохранены данные в файл {parts[1]}.")

            elif command == 'help':

                print("Список команд:\n")
                print("add - добавить поезд;")
                print("list - вывести список поездов;")
                print("select <номер поезда> - запросить информацию о выбранном времени;")
                print("help - отобразить справку;")
                print("load <имя файла> - загрузить данные из файла;")
                print("save <имя файла> - сохранить данные в файл;")
                print("exit - завершить работу с программой.")
            else:
                raise UnknownCommandError(command)

        except Exception as exc:
            logging.error(f"Ошибка: {exc}")
            print(exc, file=sys.stderr)
            
