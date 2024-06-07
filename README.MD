## About This Project

### /dicom-images
This directory contains 2 folders: clean and unclean.  
The unclean folder stores the DICOM images that haven't been clean.
If you want to test this project, save your test DICOM images to the unclean folder.  
After running main.py, cleaned DICOM images will be stored in the clean folder. The clean folder will get created if it doesn't already exist.
<br>
<br>
### /src/dicom-cleaner.py
This is the file that does the job of processing DICOM images.
<br>
<br>
### /src/dicom-fields.py
This file contains explanation about DICOM fields. It's not needed to run main.py.
I created this file in case I need to refer to the knowledge later when I actually clean the DICOM images for OAI.
<br>
<br>
### /src/deid.dicom
This file contains the configuration for manipulating DICOM images.
Currently, this file tells the DICOM parser to blank out patient name, patient birthdate, and patient ID.
<br>
<br>
### About Reading DICOM Images
To read the header information of a DICOM image, open the image using File Viewer Plus, and then click File Info.
It should open up a panel on the left. The header information is under Image Metadata.  
You can find information like the patient's name under Image Metadata. 
If you configure deid.dicom to blank out the patient's name, then after running main.py and opening the cleaned version of the image, you should no longer see the patient's name.
