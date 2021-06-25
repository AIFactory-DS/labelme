import json
import os
import shutil
from PIL import Image
import sys


def convert_lg_to_labelme(original_directory='data', new_directory='converted_data',
                 copy_image=True):
    #check if the directory exists
    if not os.path.exists(original_directory):
        raise FileNotFoundError(original_directory+" does not exists.")
    #check if the new directory is available
    if not os.path.exists(new_directory):
        os.mkdir(new_directory)
    elif os.path.isdir(new_directory) and len(os.listdir(new_directory)) > 0:
        raise FileExistsError(new_directory+" is not an empty directory.")

    # variable definition starts
    name_set = os.listdir(original_directory)
    name_set = [name.split(".")[0] for name in name_set]
    name_set = set(name_set)
    # variable definition ends

    for name in name_set:
        image_file_name = name+".jpg"
        json_file_name = name+".json"

        if copy_image is True:
            # copy the original image file into the new one
            shutil.copy(os.path.join(original_directory, image_file_name),
                        os.path.join(new_directory, image_file_name))

        original_json_path = os.path.join(original_directory, json_file_name)
        new_label = {}
        with open(original_json_path) as original_file:
            original_data = json.load(original_file)
            new_label["version"] = "1.0.0"
            new_label["flags"] = {}
            converted_shapes = []
            for object in original_data:
                new_object = {}
                new_object["label"] = object["classification"]["code"]
                new_object["shape_type"] = object["label"]["category"]
                new_object["flags"] = {}
                new_object["group_id"] = None
                new_object["points"] = []
                for point in object["label"]["data"]:
                    new_object["points"].append([point["x"], point["y"]])
                converted_shapes.append(new_object)
            new_label["shapes"] = converted_shapes
            new_label["imagePath"] = image_file_name
            new_label["imageData"] = None

            image = Image.open(os.path.join(original_directory, image_file_name))
            new_label["imageWidth"] = image.size[0]
            new_label["imageHeight"] = image.size[1]

        new_json_path = os.path.join(new_directory, json_file_name)
        with open(new_json_path, 'w') as new_file:
            new_file.write(json.dumps(new_label, indent=2))


if __name__ == "__main__":
    # usage: python converter 'original_directory' 'converted_directory'
    convert_lg_to_labelme(original_directory=sys.argv[1],
                 new_directory=sys.argv[2])
