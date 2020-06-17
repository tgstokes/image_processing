# %% photo_database.py
# import modules
import os
from exif import Image
import pandas as pd
import collections


def find_images(path, file_types=[".JPG"]):
    file_list = []
    for root, _, files in os.walk(path):
        for file in files:
            for ft in file_types:
                if file.endswith(ft):
                    file_list.append(os.path.join(root, file))
    return file_list


def write_image_df(img_path_list, exif_list=["datetime_original", "gps_latitude"]):
    column_names = ["file_name", "file_path"] + exif_list
    image_list = []
    for img in img_path_list:
        with open(img, 'rb') as fo:
            data_to_write = []
            my_image = Image(fo)
            for exif_flag in column_names:
                if exif_flag == "file_name":
                    exif_write = img.split("\\")[-1]
                elif exif_flag == "file_path":
                    exif_write = img
                else:
                    try:
                        exif_write = eval("my_image." + exif_flag)
                    except:
                        exif_write = "exif_not_found"
                data_to_write.append(exif_write)
        image_list.append(data_to_write)
    print(image_list)
    image_df = pd.DataFrame(image_list, columns=column_names)
    return image_df


def exif_directory(img_path):
    with open(img_path, 'rb') as fo:
        my_img = Image(fo)
    return dir(my_img)


def duplicate_count(listOfTuple):

    flag = False
    val = collections.Counter(listOfTuple)
    uniqueList = list(set(listOfTuple))

    for i in uniqueList:
        if val[i] >= 2:
            flag = True
            print(i, "-", val[i])

    if flag == False:
        print("Duplicate doesn't exist")


# %%
top_path = r"C:\Users\tgsto\OneDrive\Pictures\Saved Pictures"
#top_path = r"C:\Users\tgsto\OneDrive\Documents\Python\Image Processing"
image_list = find_images(top_path)
# %%
exif_available = exif_directory("IMG_2304.JPG")
print(exif_available)

# %%

exif_list = ["datetime_original", "gps_latitude",
             "gps_longitude", "gps_altitude"]
image_df = write_image_df(image_list, exif_list)
image_df.to_csv("PhotoLibrary.csv", sep='\t')
image_df.head()


# %%
