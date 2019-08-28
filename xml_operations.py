import time
import xml.etree.ElementTree as ET
from shutil import copyfile
import os
import logging

class XmlOperator:

    def __init__(self):
        pass
        logging.debug('XmlOperator object created')

    def output(self, type, **kwargs):

        template_file_destination = 'xml_templates/' + type + '.xml'

        output_file_name = type + '_output_' + str(kwargs['id']) + '-' + str(round(time.time())) + '.xml'
        output_directory_name = type + '_outputs'
        output_file_destination = 'xml_outputs/' + output_directory_name + '/' + output_file_name

        if os.path.exists('xml_outputs/' + output_directory_name) == False:
            os.mkdir('xml_outputs/' + output_directory_name)
            logging.debug('xml_outputs/' + output_directory_name + ' was created')

        copyfile(template_file_destination, output_file_destination)
        logging.debug('Template file copied: ' + template_file_destination + ' to ' + output_file_destination)

        tree = ET.parse(output_file_destination)
        root = tree.getroot()

        for key, value in kwargs.items():
            # changing the elem text
            for elem in root.iter(key.upper()):
                elem.text = str(value)
                break

        tree.write(output_file_destination)
        logging.debug(output_file_destination + ' generated. Attributes changed: ' + str(kwargs))