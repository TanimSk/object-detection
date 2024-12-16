import xml.etree.ElementTree as ET
import sys


"""
python script.py --folder=path/to/images_folder --label=<label_name>
"""


def parse_arguments(arguments):
    args = {}
    for arg in arguments:
        key, value = arg.split("=")
        args[key.strip("-")] = value
    return args


def main() -> None:

    # directory where images and XML files are located
    args = parse_arguments(sys.argv[1:])

    if "folder" not in args or "label" not in args:
        print("Usage: python script.py --folder=<folder_name> --label=<label_name>")
        sys.exit(1)

    image_dir = args["folder"]
    label = args["label"]

    # Process each XML file in the directory
    for filename in os.listdir(image_dir):
        if filename.endswith(".xml"):
            xml_path = os.path.join(image_dir, filename)

            # Parse XML file
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # rename the label            
            root.find(".//name").text = label
            tree.write(xml_path)
            print(xml_path)


if __name__ == "__main__":
    main()
