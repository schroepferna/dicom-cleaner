from deid.dicom import get_identifiers
import os
import csv
from dicom_parser import Image
import pathlib

# this program get the metadata in dicom images and write the metadata to a cvs file

# fetch a list of dicom files
dicom_file_paths = []
for root, dirs, files in os.walk('C:/Users/schroepferna/OAI/OAI_iMorphics_Extracted/9902757-9993846'):
    for file in files:
        file_path = os.path.abspath(os.path.join(root, file))
        if 'DICOM' in file_path:
            dicom_file_paths.append(file_path)

# retrieve metadata information
# it's a dictionary that has dicom file paths as keys
metadata = get_identifiers(dicom_file_paths)

image_name_col = "Image Name"

# csv_columns contains all the columns for all the dicom files
csv_columns = [image_name_col]

# csv_data_list contains metadata in all dicom files
# each element in this list is a dictionary that represents all the metadata in a dicom file
csv_data_list = []

# collection all the metadata into csv_data_list
for file_path in dicom_file_paths:
    file_data = metadata[file_path]

    # the first column is the name of the image
    # might need to change it to the s3 path of the image later
    csv_data_dict = {image_name_col: os.path.basename(file_path)}
    image = Image(file_path)

    for key in file_data:
        field = file_data[key]
        field_name = field.name

        if field_name is None or field_name == '':
            field_name = field.element.name
        if '[' in field_name:
            field_name = field_name[1:-1]
        if ' ' in field_name:
            field_name = field_name.replace(' ', '')

        field_value = ''
        try:
            field_value = image.header.get(field_name, parsed=True)
        except:
            field_value = field.element.value

        if field_value is None or field_value == '':
            field_value = field.element.value

        if field_name == 'MedComHistoryInformation' and field_value is not None and field_value != '':
            field_value = field_value.decode('utf_16')

        if field_name is not None and field_name != '' and field_value is not None and field_value != '':
            if field_name not in csv_columns:
                csv_columns.append(field_name)
            csv_data_dict[field_name] = field_value
    csv_data_list.append(csv_data_dict)

# create the csv file
dicom_csv_dir = os.path.abspath('C:/dicom-csv')
csv_file_path = os.path.abspath(dicom_csv_dir + '/OAI_iMorphics_Complete_9902757-9993846_Fields.csv')

# write to the csv file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns, restval='')
    writer.writeheader()
    writer.writerows(csv_data_list)
