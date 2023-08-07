import datetime
import hashlib
import os
import re
import shutil
import subprocess
import sys
import turtle

import cv2
import imagehash
import numpy as np
from Levenshtein import distance
from PIL import Image
from screeninfo import get_monitors
import PySimpleGUI as sg


def convert_nan(val):
    return "" if isinstance(val, float) and np.isnan(val) else str(val)


def is_image_product(file_path):
    # Load the image
    image = cv2.imread(file_path)
    # Convert the image from BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Increase the contrast by 50%
    image = np.interp(image, (0, 255), (-0.5, 0.5))
    image = np.clip(image * 1.5 + 0.5, 0, 255).astype(np.uint8)
    # Get the top left and bottom right pixels of the image
    top_left = image[0, 0]
    bottom_right = image[-1, -1]
    # Check if the top left and bottom right pixels are either white or transparent
    is_top_left_white_or_transparent = np.all(top_left >= (230, 230, 230)) or np.all(top_left == (0, 0, 0))
    is_bottom_right_white_or_transparent = np.all(bottom_right >= (230, 230, 230)) or np.all(bottom_right == (0, 0, 0))
    # Return True if both the top left and bottom right pixels are either white or transparent
    return is_top_left_white_or_transparent and is_bottom_right_white_or_transparent


def add_top_level_parent_directory(file_path, folder_ref, folder_suffix="_background"):
    """
    adds a new top level directory to the path, just before the filename

    :param folder_suffix: after the folder name
    :param file_path: string file path
    :param folder_ref: new folder name
    :return: reconstructed file path
    """
    directory, file_name = os.path.split(file_path)
    new_directory = make_filepath_valid(os.path.join(directory, folder_ref + folder_suffix))
    new_file_path = os.path.join(new_directory, file_name)
    return new_file_path


def replace_strange_folder_paths(in_val):
    """Helps make folder path valid"""
    return in_val.replace("\\", "/").replace(" \\", "/").replace(" \\", "/").replace(" /", "/")


def make_filename_valid(filename):
    valid_chars = re.compile(r'[\w.-]+')
    valid_filename = '_'.join(valid_chars.findall(filename))
    invalid_chars = re.compile(r'[^\w.-]+')
    return replace_strange_folder_paths(invalid_chars.sub('_', valid_filename).strip())


def make_filepath_valid(filepath):
    drive, rest = (filepath.split(':', 1) + [''])[:2]
    rest = re.sub(r'[^\w \\/]', '', rest).replace("  ", "-")
    return replace_strange_folder_paths((drive + ':' + rest if drive else rest).strip())


def is_image_match(fl, fl1):
    """
    Checks if two images are visually similar (i.e a match)

    :param fl: file path
    :param fl1: file path
    :return: BOOL if match
    """
    # Load images
    img1 = Image.open(fl)
    img2 = Image.open(fl1)

    # Compute perceptual hashes
    hash1 = imagehash.phash(img1)
    hash2 = imagehash.phash(img2)

    # Compare hashes
    hamming_distance = hash1 - hash2

    # Set a threshold for the hamming distance
    if hamming_distance < 10:
        return True
    else:
        return False


def get_alt_images(filename):
    alternate_files = []
    dir_path = os.path.dirname(filename)
    base_filename = os.path.basename(filename)
    for file in os.listdir(dir_path):
        if file.startswith(base_filename + "_alt"):
            alternate_files.append(os.path.join(dir_path, file))
    return [filename] + alternate_files


def remove_partial_folders_add_match(path):
    return path.replace("partial/", "match/").replace("partial_other/", "match/").replace("folder_match/", "match/")

def get_path_after_val(path, val="match"):
    head, tail = os.path.split(path)
    paths = []
    # Split the head until there's only one directory left
    while head and tail:
        paths.append(tail)
        head, tail = os.path.split(head)
    paths.reverse()

    new_path = ""
    for x in paths:
        new_path += "/" + x
        if paths[paths.index(x) - 1] == val:
            break
def remove_partial_folders_add_to_first_folder_change_ref(path, ref):

    path = path.replace("partial/", "match/").replace("partial_other/", "match/").replace("folder_match/", "match/")
    path, file = os.path.split(path)
    ext = file.split(".")[-1]

    # Split the path into head and tail
    new_path = get_path_after_val(path, "match")

    return os.path.join(new_path, ref + "." + ext), new_path


def get_smallest_window_res():
    sizes = []
    for m in get_monitors():
        sizes.append([m.width * m.height, m.width, m.height])
    largest_resolution = max(sizes, key=lambda x: x[0])
    return largest_resolution[1:]
def open_path(path):
    """opens path to sort files"""
    if os.name == 'nt':  # Windows
        subprocess.run(['explorer', path], check=True)
    elif os.name == 'posix':  # Linux or macOS
        subprocess.run(['xdg-open', path], check=True)
def open_file(path):
    imageViewerFromCommandLine = {'linux': 'xdg-open',
                                  'win32': 'explorer',
                                  'darwin': 'open'}[sys.platform]
    subprocess.Popen([imageViewerFromCommandLine, path])

def show_folder_window(path):
    """ for opening folders """
    layout = [
        [sg.Text("Please click open, sort any images and then click done", font=("Helvetica", 20), text_color='blue')],
        [sg.Button("Open", font=("Helvetica", 20), button_color=('white', 'green'), key="Open"),
         sg.Button("Done", font=("Helvetica", 20), button_color=('white', 'red'), key="Done")]]

    window = sg.Window("Window Title", layout)

    while True:
        event, values = window.read()
        if event == "Open":
            open_path(path)
        elif event == "Done":
            window.close()
            break

def show_image_window(filename, ref, description, move_func):
    # Read the image
    img = cv2.imread(filename)

    # Resize the window to 50% of the screen size
    screen_height, screen_width = get_smallest_window_res()
    window_height = int(screen_height // 1.75)
    window_width = int(screen_width // 1.75)

    # Get the height of the text and buttons
    text_height = 60
    button_height = 60

    # Resize the image to fit in the window
    img_height, img_width = img.shape[:2]
    aspect_ratio = img_width / img_height
    if aspect_ratio > window_width / (window_height - text_height - button_height):
        img_width = window_width
        img_height = int((window_height - text_height - button_height) / aspect_ratio)
    else:
        img_height = window_height - text_height - button_height
        img_width = int(img_height * aspect_ratio)

    # limit the size of the image if it exceeds the size of the window
    if img_width > window_width:
        img_width = window_width
        img_height = int((window_height - text_height - button_height) / aspect_ratio)
    if img_height > window_height - text_height - button_height:
        img_height = window_height - text_height - button_height
        img_width = int(img_height * aspect_ratio)

    img = cv2.resize(img, (int(img_width), int(img_height)))

    # Create the window layout
    layout = [[sg.Text(ref, font=("Helvetica", 20), text_color='blue')],
              [sg.Text(description, font=("Helvetica", 20), text_color='blue')],
              [sg.Button("delete", font=("Helvetica", 20), button_color=('white', 'red')),
               sg.Button("keep", font=("Helvetica", 20), button_color=('white', 'green')),
               sg.Button("view", font=("Helvetica", 20), button_color=("black","yellow")),
               sg.Button("rename", font=("Helvetica", 20), button_color=("black","orange")),
               ],
              [sg.Text('Actual SKU:'),sg.Input(key='input')],
              [sg.Image(data=cv2.imencode(".png", img)[1].tobytes(), key="IMAGE")]
              ]

    # Create the window
    window = sg.Window("Image Window", layout, size=(int(window_width), int(window_height)))

    # Event loop
    while True:
        event, values = window.read()
        if event == "delete":
            os.remove(filename)
            window.close()
            break
        elif event == "keep":
            # Move the file to the desired location
            move_func(filename, remove_partial_folders_add_match(filename), ref)
            window.close()
            break
        elif event == "view":
            # Move the file to the desired location
            open_file(filename)

        elif event == "rename":
            # Move the file to the desired location
            if len(values["input"]) == 0:
                sg.popup("You haven't given a sku", title="Error", button_type=None, auto_close=False, auto_close_duration=None)
            else:

                new_path, sub_path = remove_partial_folders_add_to_first_folder_change_ref(filename, values["input"])
                move_func(filename, new_path, ref)
                window.close()
                return sub_path

    return


def is_file_same(file1, file2):
    """checks if two files are the same """
    # Open the files in binary mode
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        # Calculate the md5 hash of each file
        hash1 = hashlib.sha1(f1.read()).hexdigest()
        hash2 = hashlib.sha1(f2.read()).hexdigest()
    return hash1 == hash2


def add_suffix_to_file(file_path, path="alt", random=True):
    """
    adds a suffix to a file name, preserving the ext
    :param file_path:
    :param path:
    :param random:
    :return:
    """
    base, ext = os.path.splitext(file_path)
    suffix = f"_{path}" + (f"{random.randint(0, 99999)}" if True else "")
    return (base + suffix + ext).strip()


def make_folders_from_filepath(filepath):
    """
    Makes all missing folders in the filepath
    :param filepath: str
    """
    folder = os.path.dirname(filepath)
    if not os.path.exists(folder):
        os.makedirs(folder)


def shrink_stock_ref(nm):
    """Translates the stock reference into something that could be readable"""
    return nm.lower().translate(str.maketrans("", "", " -_.\\/"))


def change_filename(nm):
    """here for compatibility"""
    return shrink_stock_ref(nm)


def count_matches(strings, x, path):
    """
    Takes an array and a string, also the path name of the file. Then checks for 4 match types

    Full Match - any string matches
    Partial match - any String in arrString[:len(inputstring)] == inputstring
    Reverse Partial Match - any String in inputstring[:len(arrString)] == arrString
    Path Match - does the path match the input string - i.e /test/path/8820/front.jpg   == 8820  - True as the path matches the string in top folder
    :param strings:
    :param x:
    :param path:
    :return:
    """
    exact_matches = strings[np.where(strings == x)[0]]

    matches = np.char.startswith(strings, x)
    first_section_matches = strings[np.where(matches)[0]]

    max_len = np.max([len(s) for s in strings])
    repeated_search_term = x.rjust(max_len)
    out = np.array([repeated_search_term[:len(s)] for s in strings])
    partial_matches = strings[np.where(out == strings)[0]]

    path, file = os.path.split(path)
    split_path = path.split("/")[-1].split("\\")

    path_sp = make_filename_valid(shrink_stock_ref(split_path[-1]))
    path_matches = strings[np.where(strings == path_sp)[0]]

    path_matches_one = []
    if len(split_path) > 1:
        path_sp_one = make_filename_valid(shrink_stock_ref(split_path[-2]))
        path_matches_one = strings[np.where(strings == path_sp_one)[0]]

    def closest_match(strings, search_term):
        if len(strings) > 0:
            distances = np.array([distance(string, search_term) for string in strings])
            closest_index = np.argmin(distances)
            return strings[closest_index]
        return None

    return closest_match(exact_matches, x), \
        closest_match(first_section_matches, x), \
        closest_match(partial_matches, x), \
        closest_match(path_matches, x) or closest_match(path_matches_one, x)


def pprint(text, i=None, total=None, start=None):
    nnow = datetime.datetime.now()

    print_str = ""
    if start:
        diff = int((nnow - start).total_seconds())
        hours = diff // 3600
        minutes = (diff % 3600) // 60
        secs = diff % 60
        print_str += "Run Time: " + "{:02d}:{:02d}:{:02d}  ".format(hours, minutes, secs)

    if i and total:
        per = diff / i
        seconds = int(per * total)
        hours_left = seconds // 3600
        minutes_left = (seconds % 3600) // 60
        secs_left = seconds % 60
        print_str += "Time left: " + "{:02d}:{:02d}:{:02d} ".format(hours_left, minutes_left,
                                                                    secs_left) + f" no {i}/{total} "

    print_str += "" if not start or not (i and total) else "  -  "

    print(print_str + text)


def is_large_file(file):
    """
    Check if the file is ok to load into the system

    :param file: path
    :return:
    """
    return 10240 < file.stat().st_size < 10485760 * 1.5


def shrink_stock_ref(ref):
    return ref.lower().replace(" ", "").replace("-", "").replace("_", "").replace(".", "").replace(" /", "/").replace(
        "\\", "").replace("  ", "").strip()


def fix_nan(row):
    for i, row_item in enumerate(row):
        row[i] = convert_nan(row[i])
    return row


def get_alternate_files(filename):
    """finds all files that match """
    alternate_files = []
    dir_path = os.path.dirname(filename)
    base_filename = os.path.basename(filename)
    for file in os.listdir(dir_path):
        if file.startswith(base_filename + "_alt"):
            alternate_files.append(os.path.join(dir_path, file))
    return [filename] + alternate_files
