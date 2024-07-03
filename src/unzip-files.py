from zipfile import ZipFile
import os

file_path = os.path.abspath('C:/Users/schroepferna/Downloads/OAI_MR_Pilot_Images.zip')
with ZipFile(file_path, 'r') as file:
    file.extractall(path='C:/Users/schroepferna/Downloads/OAI_MR_Pilot_Images_unzipped')