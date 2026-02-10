from deid.dicom import get_identifiers
import os
import csv
from dicom_parser import Image
import pathlib
from datetime import datetime

# this program get the metadata in dicom images and write the metadata to a cvs file
# images are in bucket nda-oai-image-files

# specify where to put the csv file
csv_file_path = os.path.abspath('C:/dicom-csv/scraped/OAI_V12_Images_12C1.csv')

# fetch a list of dicom files
dicom_file_paths = []
for root, dirs, files in os.walk('C:/dicom-csv/V12/12.C.1'):
    for file in files:
        file_path = os.path.abspath(os.path.join(root, file))
        # V12 images don't have .dcm or .dicom suffix
        dicom_file_paths.append(file_path)

# retrieve metadata information
# metadata is a dictionary, where has the file paths as keys, and has the metadata of each dicom file, which is also dictionaries, as values
metadata = get_identifiers(dicom_file_paths)

# csv_columns contains all the columns for all the dicom files
# first column is ImageName
csv_columns = ['ImageName']

# csv_data_list contains a list of extracted dicom data for all files
# each element in this list is a dictionary
csv_data_list = []

# iterate all file paths and collection all the metadata into csv_data_list
for file_path in dicom_file_paths:
    file_data = metadata[file_path]

    csv_data_dict = {'ImageName': file_path.replace('C:\\dicom-csv\\V12\\', '')}
    switch_patient_id = False

    for key in file_data:
        field = file_data[key]
        field_name = field.element.name
        field_value = str(field.element.value).strip()
        clean_field_name = field_name.strip().replace('[', '').replace(']', '').replace(' ', '').replace('"', '')

        if (('StudyDate' == clean_field_name or 'SeriesDate' == clean_field_name or 'AcquisitionDate' == clean_field_name
             or 'ContentDate' == clean_field_name or 'PerformedProcedureStepStartDate' == clean_field_name)
                and field_value):
            dt = datetime.strptime(field_value, "%Y%m%d")
            field_value = dt.strftime("%m/%d/%Y")

        if ('StudyTime' == clean_field_name or 'SeriesTime' == clean_field_name or 'AcquisitionTime' == clean_field_name or 'ContentTime' == clean_field_name) and field_value:
            field_value = round(float(field_value))

        if 'BodyPartExamined' == clean_field_name:
            if field_value == 'LOW_EXM':
                field_value = 'KNEE'

        if 'ClinicalTrialSiteID' == clean_field_name and field_value:
            field_value = field_value.replace('0166', '')

        csv_columns.append(clean_field_name)
        csv_data_dict[clean_field_name] = field_value

        if 'AccessionNumber' == clean_field_name and field_value and not field_value.startswith('0166'):
            switch_patient_id = True

    if switch_patient_id:
        plate_id = csv_data_dict['AccessionNumber']
        csv_data_dict['AccessionNumber'] = csv_data_dict['OtherPatientIDs']
        csv_data_dict['PlateID'] = plate_id

    csv_data_list.append(csv_data_dict)

# write to the csv file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns, restval='')
    writer.writeheader()
    writer.writerows(csv_data_list)
