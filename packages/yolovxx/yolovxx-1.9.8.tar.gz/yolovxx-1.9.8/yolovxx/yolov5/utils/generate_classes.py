import os
import xml.etree.ElementTree as ET


def generate_classes(VOCdevkit_path):
        
    xmlfilepath = os.path.join(
        VOCdevkit_path, 'VOC2007', 'Annotations')
    
    temp_xml = os.listdir(xmlfilepath)
    class_names = set()

    print("Generate labels.txt...")

    for xml in temp_xml:
        if xml.endswith(".xml"):        
            tree = ET.parse(os.path.join(xmlfilepath, xml))
            root = tree.getroot()

            for element in root.findall('object'):
                class_name = element[0].text
                class_names.add(class_name)

    flabels = open('labels.txt', 'w')
    
    for label in class_names:
        
        label = label + '\n'

        flabels.write(label)

    flabels.close()

    print("Generate labels.txt done.")