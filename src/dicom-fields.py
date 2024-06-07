from deid.dicom import get_files
from deid.dicom import get_identifiers
import os

# this file gives some information about dicom fields

# fetch a list of dicom files
current_folder = os.path.basename(os.getcwd())
root_path = os.getcwd()[:os.getcwd().index(current_folder) - 1]
unclean_images_dir = os.path.abspath(os.path.join(root_path, "dicom-images/unclean/humans"))
dicom_files = list(get_files(unclean_images_dir))

# get the identifiers of the dicom files
# the identifiers contain sensitive information in the headers
# get_identifiers returns a dictionary
# each key of the dictionary is the absolute path of a dicom file
# each value of the dictionary is another dictionary with expanded strings of tags, a tag looks like (0008, 0005)
ids = get_identifiers(dicom_files)

# for example
# print(ids[dicom_files[0]])
# returns a dictionary with keys like (0010, 0010), and the value is the expanded string of (0010, 0010)
# (0010, 0010) is a tag for PatientName, it's usually present in most dicom images
# print(ids[dicom_files[0]]['(0010, 0010)'])
# returns something like (0010, 0010) Patient's Name                      PN: 'nameless waterfall'  [PatientName]
# note: 'PatientName' is a field name that can be used in a recipe

# check all the field names present in a dicom file, so we can use it in the recipe
# all other dicom files in the same folder usually contain similar fields, so just look at one of them
for key in ids[dicom_files[0]]:
    field = ids[dicom_files[0]][key]
    print(key)
    print(field.element.name, "->", field.element.value)
    print(field.uid, "->", field.name)