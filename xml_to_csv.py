# Script to create CSV data file from Pascal VOC annotation files
# Based off code from GitHub user datitran: https://github.com/datitran/raccoon_dataset/blob/master/xml_to_csv.py

import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET


def xml_to_csv(path):
    xml_list = []
    print(f"Processing {path}\n")
    invalid_images = 0

    for xml_file in glob.glob(path + "/*.xml"):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        for member in root.findall("object"):
            xmin = int(member.find("bndbox")[0].text)
            ymin = int(member.find("bndbox")[1].text)
            xmax = int(member.find("bndbox")[2].text)
            ymax = int(member.find("bndbox")[3].text)

            # if bounding box is outside image dimensions, print error
            img_width = int(root.find("size")[0].text)
            img_height = int(root.find("size")[1].text)
            
            if xmin >= xmax:
                # swap values
                xtemp = xmin
                xmin = xmax
                xmax = xtemp

            if ymin >= ymax:
                # swap values
                ytemp = ymin
                ymin = ymax
                ymax = ytemp

            if xmax > img_width or ymax > img_height:
                # clip bounding box to image dimensions
                if xmax > img_width:
                    xmax = img_width
                if ymax > img_height:
                    ymax = img_height            

            # check negative values
            if xmin < 0 or ymin < 0 or xmax < 0 or ymax < 0:
                invalid_images += 1
                print("------------------------------------")
                print(f"Negative value in bounding box in {xml_file}")
                continue

            value = (
                root.find("filename").text,
                int(root.find("size")[0].text),
                int(root.find("size")[1].text),
                member[0].text,
                xmin,
                ymin,
                xmax,
                ymax,
            )
            xml_list.append(value)

    column_name = [
        "filename",
        "width",
        "height",
        "class",
        "xmin",
        "ymin",
        "xmax",
        "ymax",
    ]
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    print(f"\n\nNumber of invalid images: {invalid_images}")
    print(f"\n\nNumber of valid images: {len(xml_list)}")
    return xml_df


def main():
    for folder in ["train", "validation"]:
        image_path = os.path.join(os.getcwd(), ("images/" + folder))
        xml_df = xml_to_csv(image_path)
        path = "data/" + folder + "_labels.csv"
        xml_df.to_csv(path, index=None)
        print(f"Successfully converted xml to csv. path: {path}")


main()
