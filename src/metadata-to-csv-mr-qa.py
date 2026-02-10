from deid.dicom import get_identifiers
import os
import csv
from dicom_parser import Image
import pathlib

# this program get the metadata in dicom images and write the metadata to a cvs file

# specify where to put the csv file
csv_file_path = os.path.abspath('C:/dicom-csv/scraped/RMMQs_2010-2014.csv')

# fetch a list of dicom files
dicom_file_paths = []
for root, dirs, files in os.walk('C:/dicom-csv/MR_QA/RMMQs/2010-2014'):
    for file in files:
        file_path = os.path.abspath(os.path.join(root, file))
        if pathlib.Path(file_path).suffix == '.dcm' or pathlib.Path(file_path).suffix == '.dicom':
            dicom_file_paths.append(file_path)

# retrieve metadata information
# it's a dictionary that has dicom file paths as keys
metadata = get_identifiers(dicom_file_paths)

# csv_columns contains all the columns for all the dicom files
csv_columns = []

# csv_data_list contains metadata in all dicom files
# each element in this list is a dictionary that represents all the metadata in a dicom file
csv_data_list = []

# collection all the metadata into csv_data_list
for file_path in dicom_file_paths:
    file_data = metadata[file_path]

    # the first column is the name of the image
    csv_data_dict = {}

    for key in file_data:
        field = file_data[key]
        field_name = field.element.name
        field_value = str(field.element.value).strip()
        clean_field_name = field_name.strip().replace('[', '').replace(']', '').replace(' ', '')
        lower_field_name = clean_field_name.lower()
        lower_field_value = field_value.lower()

        # ignore these columns, don't add them to the csv file
        if (lower_field_name != 'CSASeriesHeaderInfo'.lower() and lower_field_name != 'DateOfLastCalibration'.lower() and lower_field_name != 'DeviceSerialNumber'.lower() and
                lower_field_name != 'ImageComments'.lower() and lower_field_name != 'ImplementationVersionName'.lower() and lower_field_name != 'InstitutionAddress'.lower() and
                lower_field_name != 'InstitutionalDepartmentName'.lower() and lower_field_name != 'InstitutionName'.lower() and lower_field_name != 'MedComHistoryInformation'.lower() and
                lower_field_name != 'Operator\'sName'.lower() and lower_field_name != 'Operators\'Name'.lower() and
                lower_field_name != 'PatientAge'.lower() and lower_field_name != 'Patient\'sAge'.lower() and
                lower_field_name != 'PatientBirthDate'.lower() and lower_field_name != 'Patient\'sBirthDate'.lower() and
                lower_field_name != 'PatientComments'.lower() and lower_field_name != 'Patient\'sComments'.lower() and
                lower_field_name != 'PatientSize'.lower() and lower_field_name != 'Patient\'sSize'.lower() and
                lower_field_name != 'PatientWeight'.lower() and lower_field_name != 'Patient\'sWeight'.lower() and
                lower_field_name != 'PerformedProcedureStepDescription'.lower() and
                lower_field_name != 'PerformingPhysicianName'.lower() and lower_field_name != 'PerformingPhysician\'sName'.lower() and
                lower_field_name != 'PersonName'.lower() and lower_field_name != 'Person\'sName'.lower() and
                lower_field_name != 'PositivePCSDirections'.lower() and lower_field_name != 'PrivateCreator'.lower() and
                lower_field_name != 'ReferringPhysicianName'.lower() and lower_field_name != 'ReferringPhysician\'sName'.lower() and
                lower_field_name != 'RelationshipType'.lower() and lower_field_name != 'RequestingPhysician'.lower() and lower_field_name != 'StationName'.lower() and
                lower_field_name != 'StudyComments'.lower() and lower_field_name != 'TimeofLastCalibration'.lower() and lower_field_name != 'Unknown'.lower()):

            if lower_field_name == 'CSASeriesHeaderType'.lower() or lower_field_name == 'Modality'.lower():
                field_value = 'MR'

            if lower_field_name == 'PatientSex'.lower() or lower_field_name == 'Patient\'sSex'.lower() :
                field_value = 'O'

            if lower_field_name == 'SeriesDescription'.lower() or lower_field_name == 'ProtocolName'.lower():
                if lower_field_value == 'AX TSE 1500 30'.lower() or lower_field_value == 'AX TSE 1750 30'.lower():
                    field_value = 'Axial TSE IW'
                elif lower_field_value == 'Axial T1'.lower() or lower_field_value == 'Axial T1 LG FOV Filter'.lower() or lower_field_value == 'ACR T1'.lower():
                    field_value = 'Axial SE T1W'
                elif (lower_field_value == 'ACR T2'.lower() or lower_field_value == 'TSE(17) T2'.lower() or lower_field_value == 'Axial T2'.lower() or
                      lower_field_value == 'Axial T2 LG FOV Filter'.lower()):
                    field_value = 'Axial SE PD/T2W'
                elif lower_field_value == 'Sag Loc'.lower() or lower_field_value == 'Sag Loc 384'.lower():
                    field_value = 'Localizer Sagittal'
                elif lower_field_value == 'Localizer Isocenter 3plane'.lower():
                    field_value = 'Localizer 3-plane'
                elif lower_field_value == 'SAG TSE 1000 30'.lower() or lower_field_value == 'SAG TSE 1000 30 80% LG FOV'.lower():
                    field_value = 'Sagittal TSE IW'
                elif lower_field_value == 'SE Sagittal'.lower():
                    field_value = 'Sagittal SE T1W'
                elif lower_field_value == 'SE Sagittal LG FOV Filter'.lower():
                    field_value = 'Sagittal SE T1W Large FOV Filter'
                elif (lower_field_value == 'AX TSE 1500 30 left'.lower() or lower_field_value == 'AX TSE 1750 30 left'.lower() or lower_field_value == 'AX TSE 1750 30 LT 101705'.lower() or
                      lower_field_value == 'AX TSE 1750 32 LEFT'.lower() or lower_field_value == 'AX TSE 1500 30'.lower() or lower_field_value == 'AX TSE 1750 30'.lower()):
                    field_value = 'Axial TSE IW LEFT'
                elif (lower_field_value == 'AX TSE 1500 30 Right'.lower() or lower_field_value == 'AX TSE 1750 30 Right'.lower() or lower_field_value == 'AX TSE 1750 30 RT101705'.lower() or
                      lower_field_value == 'AX TSE 1750 32 Right'.lower()):
                    field_value = 'Axial TSE IW RIGHT'
                elif lower_field_value == 'COR TSE 1500 30 left'.lower():
                    field_value = 'Coronal TSE T1W LEFT'
                elif lower_field_value == 'COR TSE 1500 30 Right'.lower():
                    field_value = 'Coronal TSE T1W RIGHT'
                elif lower_field_value == 'SAG 3D DESS ISO Right'.lower() or lower_field_value == 'SAG 3D DESS WE'.lower():
                    field_value = 'Sagittal 3D DESS WE'
                elif (lower_field_value == 'SAG T2_map'.lower() or lower_field_value == 'Sagittal T2 Map 120mmFOV'.lower() or lower_field_value == 'SAG T2 MAP 120MMFOV'.lower() or
                      lower_field_value == 'SAG T2 Map120mmFOV -- new'.lower()):
                    field_value = 'Sagittal SE T2 Map 120mm FOV'
                elif (lower_field_value == 'SAG TSE 1500 30 left'.lower() or lower_field_value == 'SAG TSE 1750 30 left'.lower() or lower_field_value == 'SAG TSE 1750 30 LT 101705'.lower() or
                      lower_field_value == 'SAG TSE 1750 32 LEFT'.lower()):
                    field_value = 'Sagittal TSE IW LEFT'
                elif (lower_field_value == 'SAG TSE 1500 30 Right'.lower() or lower_field_value == 'SAG TSE 1750 30 Right'.lower() or lower_field_value == 'SAG TSE 1750 30 RT101705'.lower() or
                      lower_field_value == 'SAG TSE 1750 32 Right'.lower()):
                    field_value = 'Sagittal TSE IW RIGHT'
                elif lower_field_value == 'Axial T2 Map ACR'.lower():
                    field_value = 'Axial TSE T2'

            if (lower_field_name == 'Patient\'sName'.lower() or lower_field_name == 'PatientName'.lower() or
                    lower_field_name == 'Patient\'sID'.lower() or lower_field_name == 'PatientID'.lower()):
                if lower_field_value == 'MAAA'.lower():
                    field_value = 'AAAA'
                elif lower_field_value == 'RAAA'.lower():
                    field_value = 'BAAA'
                elif lower_field_value == 'OAAA'.lower():
                    field_value = 'CAAA'
                elif lower_field_value == 'PAAA'.lower():
                    field_value = 'DAAA'
                elif lower_field_value == 'MMMM'.lower():
                    field_value = 'AMMM'
                elif lower_field_value == 'RMMM'.lower():
                    field_value = 'BMMM'
                elif lower_field_value == 'OMMM'.lower():
                    field_value = 'CMMM'
                elif lower_field_value == 'PMMM'.lower():
                    field_value = 'DMMM'
                elif lower_field_value == 'MMMQL'.lower():
                    field_value = 'AMMQL'
                elif lower_field_value == 'RMMQL'.lower():
                    field_value = 'BMMQL'
                elif lower_field_value == 'OMMQL'.lower():
                    field_value = 'CMMQL'
                elif lower_field_value == 'PMMQL'.lower():
                    field_value = 'DMMQL'
                elif lower_field_value == 'MMMQR'.lower():
                    field_value = 'AMMQR'
                elif lower_field_value == 'RMMQR'.lower():
                    field_value = 'BMMQR'
                elif lower_field_value == 'OMMQR'.lower():
                    field_value = 'CMMQR'
                elif lower_field_value == 'PMMQR'.lower():
                    field_value = 'DMMQR'

            if field_value is not None and field_value != '':
                if clean_field_name not in csv_columns:
                    csv_columns.append(clean_field_name)

                csv_data_dict[clean_field_name] = field_value
    csv_data_list.append(csv_data_dict)

# write to the csv file
with open(csv_file_path, 'w', newline='') as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=csv_columns, restval='')
    writer.writeheader()
    writer.writerows(csv_data_list)
