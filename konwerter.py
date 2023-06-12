import sys
import xml.etree.ElementTree as ET
import json
import yaml

def convert_xml_to_json(file_path, output_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = {}
    data[root.tag] = parse_element(root)
    with open(output_path, 'w') as output_file:
        json.dump(data, output_file, indent=4)

def parse_element(element):
    if len(element) == 0:
        return element.text
    result = {}
    for child in element:
        child_data = parse_element(child)
        if child.tag in result:
            if type(result[child.tag]) is list:
                result[child.tag].append(child_data)
            else:
                result[child.tag] = [result[child.tag], child_data]
        else:
            result[child.tag] = child_data
    return result

def convert_json_to_xml(file_path, output_path):
    with open(file_path, 'r') as input_file:
        data = json.load(input_file)
    root_element = ET.Element(list(data.keys())[0])
    build_element(root_element, data[list(data.keys())[0]])
    tree = ET.ElementTree(root_element)
    tree.write(output_path)

def build_element(element, data):
    if type(data) is dict:
        for key, value in data.items():
            if type(value) is list:
                for item in value:
                    sub_element = ET.SubElement(element, key)
                    build_element(sub_element, item)
            else:
                sub_element = ET.SubElement(element, key)
                build_element(sub_element, value)
    else:
        element.text = data

def convert_yaml_to_json(file_path, output_path):
    with open(file_path, 'r') as input_file:
        data = yaml.safe_load(input_file)
    with open(output_path, 'w') as output_file:
        json.dump(data, output_file, indent=4)

def convert_json_to_yaml(file_path, output_path):
    with open(file_path, 'r') as input_file:
        data = json.load(input_file)
    with open(output_path, 'w') as output_file:
        yaml.dump(data, output_file, default_flow_style=False)

def convert_data(input_file_path, output_file_path):
    if input_file_path.endswith('.xml'):
        if output_file_path.endswith('.json'):
            convert_xml_to_json(input_file_path, output_file_path)
        elif output_file_path.endswith('.yml') or output_file_path.endswith('.yaml'):
            temp_json_file = 'temp.json'
            convert_xml_to_json(input_file_path, temp_json_file)
            convert_json_to_yaml(temp_json_file, output_file_path)
        else:
            print('Unsupported output format')
    elif input_file_path.endswith('.json'):
        if output_file_path.endswith('.xml'):
            convert_json_to_xml(input_file_path, output_file_path)
        elif output_file_path.endswith('.yml') or output_file_path.endswith('.yaml'):
            convert_json_to_yaml(input_file_path, output_file_path)
        else:
            print('Unsupported output format')
    elif input_file_path.endswith('.yml') or input_file_path.endswith('.yaml'):
        if output_file_path.endswith('.json'):
            convert_yaml_to_json(input_file_path, output_file_path)
        else:
            print('Unsupported output format')
    else:
        print('Unsupported input format')

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Usage: program.exe input_file output_file')
        sys.exit(1)
    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]
    convert_data(input_file_path, output_file_path)
