from deid.dicom import get_files
from deid.dicom import get_identifiers
import os
import csv
import random

# this file get the metadata in dicom images and write the metadata to a cvs file

# fetch a list of dicom files
current_folder = os.path.basename(os.getcwd())
root_path = os.getcwd()[:os.getcwd().index(current_folder) - 1]
unclean_images_dir = os.path.abspath(os.path.join(root_path, "dicom-images/unclean/humans"))
dicom_file_paths = list(get_files(unclean_images_dir))

# retrieve metadata information
# it's a dictionary that has dicom file paths as keys
metadata = get_identifiers(dicom_file_paths)

image_name_col = "Image Name"
csv_columns = [image_name_col]
csv_data_list = []

# collection all the metadata into csv_data_list
for file_path in dicom_file_paths:
    file_data = metadata[file_path]
    csv_data_dict = {image_name_col: os.path.basename(file_path)}

    for key in file_data:
        field = file_data[key]
        column_name = field.element.name

        if column_name not in csv_columns:
            csv_columns.append(column_name)
        csv_data_dict[column_name] = field.element.value

    csv_data_list.append(csv_data_dict)

# create the csv file
dicom_csv_dir = os.path.abspath("C:/dicom-csv")
csv_file_path = os.path.abspath(dicom_csv_dir + "/dicom-" + random.randint())
os.mkdir(csv_file_path)

# write to the csv file
with open(csv_file_path, 'w') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
    writer.writeheader()

    for csv_data in csv_data_list:
        writer.writerows(csv_data)
