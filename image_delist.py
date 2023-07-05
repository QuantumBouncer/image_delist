import os
import shutil
import cv2

# for json box
import json

########################################################################
# config setting - start
########################################################################

# Image current index
current_image_index = 0

# Directory containing the images
IMAGE_DIR = "./data/input"

# Directory for delisted images
DELISTED_DIR = "./data/delisted_dir"

# json box option (default is False)
json_box = False

########################################################################
# config setting - end
########################################################################

################################
# delist_flag = False
delist_flag_list = []
#delist_string = 'Image to be delisted'
#delist_string = 'UnChanged'
delist_string = {False: 'UnChanged', True: 'Image to be deleted'}
################################

# Read Config file (.json)
configfile = os.getcwd() + "\\config.json"
if os.path.exists(configfile):
    try:
        with open(configfile, 'r') as file:
            config = json.load(file)
        current_image_index = int(config['IMAGE_IDX'])
        IMAGE_DIR = config['IMAGE_DIR']
        DELISTED_DIR = config['COPY_DIR']
        json_box = bool(config['JSON_BOX'])
    except:
        print("An error occurred while reading the config file.")
# current_image_index = int(current_image_index)
# json_box = bool(json_box)

# color
red_color = (0, 0, 255)
green_color = (0, 255, 0)

# Get the list of images in the directory
try:
    image_files = [f for f in os.listdir(IMAGE_DIR) if f.endswith('.jpg')]
    # Sort the list of images by their filenames
    image_files.sort()
except:
    image_read_error_msg = "there are no images in IMAGE_DIR. please check IMAGE_DIR"

# Load the first image
current_image = cv2.imread(os.path.join(IMAGE_DIR, image_files[current_image_index]))
delist_flag_list = [False] * len(image_files)

# Create a window to display the image
cv2.namedWindow("Image")

# Display the image
# 1. print text about current image index
font = cv2.FONT_HERSHEY_SIMPLEX
# cv2.putText(current_image, f"{current_image_index + 1}/{len(image_files)}", (10, 30), font, 1, green_color, 2, cv2.LINE_AA)
cv2.putText(current_image, "{} of {}".format(current_image_index + 1, len(image_files)), (10, 30), font, 1, green_color, 2, cv2.LINE_AA)
cv2.putText(current_image, "{}".format(delist_string[delist_flag_list[current_image_index]]), (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
# 2. print json box
if json_box == True:
    json_filename = image_files[current_image_index][:-4] + '.json'
    json_filename = os.path.join(IMAGE_DIR, json_filename)
    if os.path.exists(json_filename):
        with open(json_filename) as f:
            json_object = json.load(f)
            try:
                height = json_object['info']['event']['object']['height']
                width = json_object['info']['event']['object']['width']
                x = json_object['info']['event']['object']['x']
                y = json_object['info']['event']['object']['y']
                current_image = cv2.rectangle(current_image, (x, y), (x+width, y+height), red_color, 2)
            except KeyError:
                # Display a error message in the image window
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(current_image, "ERROR] json file is damaged ", (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
    else:
        cv2.putText(current_image, f"there is no {image_files[current_image_index][:-4] + '.json'}", (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
# 3. print current image
cv2.imshow("Image", current_image)

while True:   
    # Wait for a key press
    key = cv2.waitKey(0)
    
    if key == ord("e"):
        delist_flag_list[current_image_index] = not delist_flag_list[current_image_index]
        current_image = cv2.imread(os.path.join(IMAGE_DIR, image_files[current_image_index]))
        
        # Write the number of images out of the total number in the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(current_image, "{} of {}".format(current_image_index + 1, len(image_files)), (10, 30), font, 1, green_color, 2, cv2.LINE_AA)
        cv2.putText(current_image, "{}".format(delist_string[delist_flag_list[current_image_index]]), (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
        
        # Display the image
        cv2.imshow("Image", current_image)
    
    elif key == ord("q"):
        # save the progress about the image index
        config['IMAGE_IDX'] = current_image_index
        with open("config.json", 'w') as file:
            json.dump(config, file, indent="\t")
        
        # move
        for i in range(len(delist_flag_list)):
            if delist_flag_list[i] == True:
                source_file = os.path.join(IMAGE_DIR, image_files[i])
                destination_file = os.path.join(DELISTED_DIR, image_files[i])
                shutil.move(source_file, destination_file)
                print(image_files[i] + " 파일 이동 완료")
        
        # Quit the program
        break
    
    elif key == 81 or key == ord("a"):
        # Previous image
        current_image_index = max(0, current_image_index - 1)
        current_image = cv2.imread(os.path.join(IMAGE_DIR, image_files[current_image_index]))
        
        # draw json box
        if json_box == True:
            json_filename = image_files[current_image_index][:-4] + '.json'
            json_filename = os.path.join(IMAGE_DIR, json_filename)
            if os.path.exists(json_filename):
                with open(json_filename) as f:
                    json_object = json.load(f)
                try:
                    height = json_object['info']['event']['object']['height']
                    width = json_object['info']['event']['object']['width']
                    x = json_object['info']['event']['object']['x']
                    y = json_object['info']['event']['object']['y']
                    current_image = cv2.rectangle(current_image, (x, y), (x+width, y+height), red_color, 2)
                except KeyError:
                    # Display a error message in the image window
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(current_image, "ERROR] json file is damaged ", (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
                    continue
            else:
                cv2.putText(current_image, f"there is no {image_files[current_image_index][:-4] + '.json'}", (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
        
        # Write the number of images out of the total number in the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(current_image, "{} of {}".format(current_image_index + 1, len(image_files)), (10, 30), font, 1, green_color, 2, cv2.LINE_AA)
        cv2.putText(current_image, "{}".format(delist_string[delist_flag_list[current_image_index]]), (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
        
        # Display the image
        cv2.imshow("Image", current_image)
        
    elif key == 83 or key == ord("d"):
        # Next image
        current_image_index = min(len(image_files) - 1, current_image_index + 1)
        current_image = cv2.imread(os.path.join(IMAGE_DIR, image_files[current_image_index]))
        
        # draw json box
        if json_box == True:
            json_filename = image_files[current_image_index][:-4] + '.json'
            json_filename = os.path.join(IMAGE_DIR, json_filename)
            if os.path.exists(json_filename):
                with open(json_filename) as f:
                    json_object = json.load(f)
                try:
                    height = json_object['info']['event']['object']['height']
                    width = json_object['info']['event']['object']['width']
                    x = json_object['info']['event']['object']['x']
                    y = json_object['info']['event']['object']['y']
                    current_image = cv2.rectangle(current_image, (x, y), (x+width, y+height), red_color, 2)
                except KeyError:
                    # Display a error message in the image window
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(current_image, "ERROR] json file is damaged ", (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
                    continue
            else:
                cv2.putText(current_image, f"there is no {image_files[current_image_index][:-4] + '.json'}", (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
        
        # Write the number of images out of the total number in the image window
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(current_image, "{} of {}".format(current_image_index + 1, len(image_files)), (10, 30), font, 1, green_color, 2, cv2.LINE_AA)
        cv2.putText(current_image, "{}".format(delist_string[delist_flag_list[current_image_index]]), (10, 50), font, 1, red_color, 2, cv2.LINE_AA)
        
        # Display the image
        cv2.imshow("Image", current_image)
        
    else:
        # Invalid key press
        continue
    
    
# Destroy the window
cv2.destroyAllWindows()
