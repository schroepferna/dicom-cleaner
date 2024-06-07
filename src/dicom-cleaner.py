from deid.dicom import get_files
from deid.dicom.parser import DicomParser
import os

current_folder = os.path.basename(os.getcwd())
root_dir = os.getcwd()[:os.getcwd().index(current_folder) - 1]

# specify the folder path that contains the dicom images that need to be cleaned in the second argument of os.path.join
unclean_images_dir = os.path.abspath(os.path.join(root_dir, "dicom-images/unclean/humans"))
# save the list of dicom files
dicom_files = list(get_files(unclean_images_dir))

recipe_path = os.path.abspath("deid.dicom")
if not os.path.exists(os.path.abspath(os.path.join(root_dir, "dicom-images/clean"))):
    os.mkdir(os.path.abspath(os.path.join(root_dir, "dicom-images/clean")))

clean_image_dir = os.path.abspath(os.path.join(root_dir, "dicom-images/clean/{folder}").format(folder=os.path.basename(unclean_images_dir)))

for dicom_file in dicom_files:
    # create a parser for each dicom file and parse it using the recipe
    parser = DicomParser(dicom_file, recipe=recipe_path)
    # parse the dicom file and apply the changes defined in deid.dicom
    parser.parse()

    if not os.path.exists(clean_image_dir):
        os.mkdir(clean_image_dir)
    file_path = os.path.abspath(clean_image_dir + "/" + os.path.basename(dicom_file))
    # save the dicom file to a desired dir
    parser.save(file_path)

# check the dicom file is loaded
# print(parser.dicom)

# check the dicom fields, parser.fields will return {} if .parse() hasn't been called
# print(parser.fields)