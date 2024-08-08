import re
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# Путь к исходному файлу и к файлу для записи
input_file_path = 'config.cpp'
output_file_path = 'types.xml'

# Регулярное выражение для поиска class и scope
class_pattern = re.compile(r'class\s+(\w+)')
scope_pattern = re.compile(r'scope\s*=\s*2;')
category_pattern = re.compile(r'category\s+name\s*=\s*"([^"]+)"')

# Элементы XML
root = ET.Element('types')

# Чтение файла config.cpp
with open(input_file_path, 'r') as file:
    lines = file.readlines()

# Временные переменные для хранения данных
current_class = None
current_category = None
inside_class = False

for line in lines:
    class_match = class_pattern.search(line)
    scope_match = scope_pattern.search(line)
    category_match = category_pattern.search(line)
    
    if class_match:
        current_class = class_match.group(1)
        current_category = None  # Сбрасываем категорию при нахождении нового класса
        inside_class = True  # Начало нового класса

    if inside_class and scope_match and current_class:
        # Создаем новый элемент type и добавляем в корневой элемент
        type_elem = ET.Element('type', name=current_class)
        nominal = ET.SubElement(type_elem, 'nominal')
        nominal.text = '0'
        lifetime = ET.SubElement(type_elem, 'lifetime')
        lifetime.text = '14400'
        restock = ET.SubElement(type_elem, 'restock')
        restock.text = '0'
        min_elem = ET.SubElement(type_elem, 'min')
        min_elem.text = '0'
        quantmin = ET.SubElement(type_elem, 'quantmin')
        quantmin.text = '-1'
        quantmax = ET.SubElement(type_elem, 'quantmax')
        quantmax.text = '-1'
        cost = ET.SubElement(type_elem, 'cost')
        cost.text = '100'
        flags = ET.SubElement(type_elem, 'flags', count_in_cargo='0', count_in_hoarder='0', count_in_map='1', count_in_player='0', crafted='1', deloot='0')
        
        if current_category:
            category_elem = ET.SubElement(type_elem, 'category', name=current_category)
        else:
            category_elem = ET.SubElement(type_elem, 'category', name='unknown')

        root.append(type_elem)
        current_class = None  # После записи класса сбрасываем его
        inside_class = False  # Закрываем текущий класс

    if inside_class and category_match:
        current_category = category_match.group(1)

# Преобразование в строку для форматирования
xml_str = ET.tostring(root, encoding='utf-8', method='xml')
dom = minidom.parseString(xml_str)
pretty_xml_as_string = dom.toprettyxml(indent="  ")

# Удаление лишней строки декларации XML
pretty_xml_as_string = pretty_xml_as_string.replace('<?xml version="1.0" ?>\n', '')

# Запись в XML файл с добавлением строки кодировки
with open(output_file_path, 'w', encoding='utf-8') as f:
    f.write("<?xml version='1.0' encoding='utf-8'?>\n")
    f.write(pretty_xml_as_string)

print(f"Data has been written to {output_file_path}")
