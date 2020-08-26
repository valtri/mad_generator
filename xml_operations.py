import time
import xml.etree.ElementTree as ET
from shutil import copyfile
import os
import logging
import random


class XmlOperator:
    def __init__(self):
        pass
        logging.debug("XmlOperator object created")
        self.output_base_directory_name = (
            "xml_output-"
            + str(round(time.time()))
            + "-"
            + str(random.randint(1, 1000000))
        )
        if not os.path.exists("xml_outputs/" + self.output_base_directory_name):
            os.mkdir("xml_outputs/" + self.output_base_directory_name)
            logging.debug(
                "xml_outputs/" + self.output_base_directory_name + " was created"
            )

    def output(self, instance):

        type = instance.__class__.__name__.lower()

        template_file_destination = "xml_templates/" + type + ".xml"

        output_file_name = (
            type
            + "_output_"
            + str(instance.id)
            + "-"
            + str(round(time.time()))
            + ".xml"
        )
        output_directory_name = type + "_outputs"
        output_file_destination = (
            "xml_outputs/"
            + self.output_base_directory_name
            + "/"
            + output_directory_name
            + "/"
            + output_file_name
        )

        if (
            os.path.exists(
                "xml_outputs/"
                + self.output_base_directory_name
                + "/"
                + output_directory_name
            )
            == False
        ):
            os.mkdir(
                "xml_outputs/"
                + self.output_base_directory_name
                + "/"
                + output_directory_name
            )
            logging.debug(
                "xml_outputs/"
                + self.output_base_directory_name
                + "/"
                + output_directory_name
                + " was created"
            )

        copyfile(template_file_destination, output_file_destination)
        logging.debug(
            "Template file copied: "
            + template_file_destination
            + " to "
            + output_file_destination
        )

        tree = ET.parse(output_file_destination)
        root = tree.getroot()

        for key, value in instance.__dict__.items():
            # changing the elem text
            for elem in root.iter(key.upper()):
                elem.text = str(value)
                break

        tree.write(output_file_destination)
        logging.debug(
            output_file_destination
            + " generated. Attributes changed: "
            + str(instance.__dict__)
        )
