#%% tested code
## import modules
import os
import glob
from exif import Image
from datetime import datetime

## define functions
def find_files(path, file_types):
    found_files = []
    for type in file_types:
        for file in glob.glob(type):
            found_files.append(file)
    return found_files

def create_file_path(source_dir,files):
    file_path = []
    for file in found_files:
        file_path.append(os.path.join(source_dir, file))
    return file_path

def get_date(path):
    file_dates = {}
    for file in path:
        with open(file, 'rb') as fo:
            my_image = Image(fo)
            try:
                date = my_image.datetime_original
            except:
                date = "DateNotFound"
            datatowrite = {file: date}
            file_dates.update(datatowrite)
    return file_dates

def convert_date_strings(dict):
    for key in dict:
        dict[key] = dict[key].replace(":","-")
        dict[key] = dict[key].replace(" ","_")
    return dict

## define and navigate to directory
source_dir = r"C:\Users\tgsto\OneDrive\Documents\Python\Image Processing"
os.chdir(source_dir)

## find image files
file_types = ["*.jpg"]
found_files = find_files(source_dir,file_types)

## Turn file names into paths
#file_path = create_file_path(source_dir,found_files)

## Find datetime_original of each filepath
file_dates = get_date(found_files)
print("Scanned for filedates, found: ")

## Convert datetimes to strings
file_dates = convert_date_strings(file_dates)
print(file_dates)

# Start renaming images
for key in file_dates:
    if file_dates[key] is not "DateNotFound":
        suffix = 0
        while os.path.isfile(str(file_dates[key])+".jpg") is True:
            print("File " + file_dates[key] + ".jpg already exists... adding suffix")
            suffix = suffix + 1
            file_dates[key] = [file_dates[key] + "_" + str(suffix)]
            print(key)
        else:
            print("Renaming file " + str(file_dates[key][0]) + ".jpg")
    else:
        print("File " + key + " will not be renamed as no date was found")


# %%