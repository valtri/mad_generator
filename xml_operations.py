import time
import xml.etree.ElementTree as ET
from shutil import copyfile

class XmlOperator:

    def __init__(self):
        pass

    def outputVm(self, **kwargs):

        output_file_name = 'vm_output_' + str(kwargs['id']) + '-' + str(round(time.time())) + '.xml'
        output_file_destination = 'xml_outputs/' + output_file_name

        copyfile('xml_templates/vm.xml', output_file_destination)

        for key, value in kwargs.items():

            tree = ET.parse(output_file_destination)
            root = tree.getroot()

            # changing the elem text
            for elem in root.iter(key.upper()):
                elem.text = str(value)
                break

            tree.write(output_file_destination)