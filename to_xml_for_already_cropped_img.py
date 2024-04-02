import xml.etree.ElementTree as ET
import sys
import os
from PIL import Image


"""
python script.py --folder=path/to/images_folder --object_name=one_taka --output_dir=output_xml_folder
"""


def create_xml(folder, filename, path, object_name, width, height):
    annotation = ET.Element("annotation")

    ET.SubElement(annotation, "folder").text = folder
    ET.SubElement(annotation, "filename").text = filename
    ET.SubElement(annotation, "path").text = path

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotation, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"

    ET.SubElement(annotation, "segmented").text = "0"

    obj = ET.SubElement(annotation, "object")
    ET.SubElement(obj, "name").text = object_name
    ET.SubElement(obj, "pose").text = "Unspecified"
    ET.SubElement(obj, "truncated").text = "1"
    ET.SubElement(obj, "difficult").text = "0"

    bndbox = ET.SubElement(obj, "bndbox")
    ET.SubElement(bndbox, "xmin").text = "0"
    ET.SubElement(bndbox, "ymin").text = "0"
    ET.SubElement(bndbox, "xmax").text = str(width)
    ET.SubElement(bndbox, "ymax").text = str(height)

    tree = ET.ElementTree(annotation)
    return tree

def parse_arguments(arguments):
    args = {}
    for arg in arguments:
        key, value = arg.split("=")
        args[key.strip("-")] = value
    return args

def main():
    args = parse_arguments(sys.argv[1:])

    if "folder" not in args or "object_name" not in args or "output_dir" not in args:
        print("Usage: python script.py --folder=<folder_name> --object_name=<object_name> --output_dir=<output_dir>")
        sys.exit(1)

    folder = args["folder"]
    object_name = args["object_name"]
    output_dir = args["output_dir"]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            image_path = os.path.join(folder, filename)
            image = Image.open(image_path)
            width, height = image.size

            xml_tree = create_xml(folder, filename, image_path, object_name, width, height)
            output_filename = os.path.splitext(filename)[0] + ".xml"
            output_path = os.path.join(output_dir, output_filename)
            xml_tree.write(output_path)

if __name__ == "__main__":
    main()
