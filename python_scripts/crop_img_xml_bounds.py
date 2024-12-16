import os
import xml.etree.ElementTree as ET
from PIL import Image

# This script crops images according to the xml file bounds
# Directories


# directory where images and XML files are located
image_dir = "../images/all"
output_dir = "../images/cropped_images"

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Process each XML file in the directory
for filename in os.listdir(image_dir):
    if filename.endswith(".xml"):
        xml_path = os.path.join(image_dir, filename)

        # Parse XML file
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # Extract filename and bounding box coordinates
        image_filename = root.find("filename").text
        xmin = int(root.find(".//bndbox/xmin").text)
        ymin = int(root.find(".//bndbox/ymin").text)
        xmax = int(root.find(".//bndbox/xmax").text)
        ymax = int(root.find(".//bndbox/ymax").text)

        # Load and crop the image
        image_path = os.path.join(image_dir, image_filename)
        if os.path.exists(image_path):
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                cropped_img = img.crop((xmin, ymin, xmax, ymax))

                # Save the cropped image
                cropped_image_path = os.path.join(output_dir, image_filename)
                cropped_img.save(cropped_image_path)
                print(f"Cropped and saved: {cropped_image_path}")
        else:
            print(f"Image file does not exist: {image_path}")
