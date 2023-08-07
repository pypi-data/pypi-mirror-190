import datetime
import filecmp
import os
import random
import re
import shutil

import cv2
import imagehash
import numpy as np
import pandas as pd
from Levenshtein import distance
from PIL import Image

from locater.functions import is_large_file, pprint, shrink_stock_ref, fix_nan, make_filename_valid, \
    count_matches, add_suffix_to_file, is_image_match, make_folders_from_filepath, \
    add_top_level_parent_directory, is_image_product, replace_strange_folder_paths


#
# def getRealRow(ref, web=True, sup=False):
#
#     ar = dfpron_look
#
#     search_value = ref
#     index = np.where(ar[:, 0] == search_value)
#     try:
#
#         return ar[index][0][1:]
#     except Exception as e:
#         errors.append(["getRealRow", ref, e])
#
# def get_web_path(row, ref, typ, web):
#     base = get_base(web)
#     paths = [convert_nan(row["Supplier"].to_list()[0]), typ, convert_nan(row["Range"].to_list()[0]),
#              convert_nan(row["Type"].to_list()[0]), ref]
#     path = os.path.join(base, *[x for x in paths if x])
#
#     return path.replace("//", "/").strip().replace(" /", "/").replace(" /", "/")
#
def get_path(ref, typ, sup, web):
    base = get_base(web)
    path = os.path.join(base, sup, typ, ref)
    return path.replace("//", "/").strip().replace(" /", "/").replace(" /", "/")

def get_base(web=True):
    return "C:/Users/ChrisColeman/Desktop/" + ("web" if web else "pro") + "/"

class Locator:
    def __init__(self, search_path: str, out_path: str, data_file: str, *args, **kwargs):
        """Class for locating and organizing files based on search terms.

        :param search_path: Path to search for files.
        :param out_path: Path to output files.
        :param data_file: File consisting of columns in this order: search_term, description, groupingmain, groupingsecondary, etc.
        """

        #source of the files and its length so it doesn't have to be computed each time
        self.files_source = []
        self.files_len = 0
        # list of eventual files once loaded
        self.search_path = search_path  # path to search
        self.out_path = out_path  # output path
        # pandas df of all the data
        self._base_data = self._load_data(data_file)
        self._out_data = self._create_out_data()
        # numpy array to perform matching on
        self.code_data = self._base_data["changedSku"].to_numpy().astype(str)
        # data for getting path etc
        self.lookup_data = self._base_data.to_numpy().astype(str)
        # should print info
        self.verbose = True if "verbose" not in kwargs else True if kwargs["verbose"] else False
        # extra information that could be used later
        self.extra = {"exact_match_paths": [], "search_matches": 0, "search_partials": 0, "search_dupes": 0, "matches_ext": "same", "alt_ext": "alt"}

    def _create_out_data(self):
        df = self._base_data.copy()
        df = df[[df.columns.to_list()[0], df.columns.to_list()[2]]]
        df["matches"] = False
        df["partials"] = False
        return df

    def _load_data(self, file_path):
        # Determine the file extension
        file_extension = file_path[-4:]
        # Choose the appropriate reader function based on the file extension
        if "xls" in file_extension:
            reader = pd.read_excel
        elif "csv" in  file_extension in "csv":
            reader = pd.read_csv

        assert reader, "filetype not supported, please use xls, xlsx, or csv"

        # Load the data into a Pandas DataFrame
        df = reader(file_path)

        # Drop duplicate values in the first column of the DataFrame
        df.drop_duplicates(subset=df.columns[0], inplace=True)

        # Create a new column "changedSku" using the `shrink_stock_ref` function
        df["changedSku"] = df.iloc[:, 0].apply(shrink_stock_ref)

        # Reorder the columns of the DataFrame
        columns = df.columns.tolist()
        new_col_order = [columns[0], "changedSku"] + columns[1:-1]
        df = df[new_col_order]

        # Apply the `fix_nan` function to fill missing values
        df = df.apply(fix_nan, axis=1)

        return df

    def _get_alt_path(self):
        return self.extra["alt_ext"] or "_alt"

    def _get_match_path(self):
        return self.extra["matches_ext"] or "_same"

    def _get_matches(self):
        return self.extra["search_matches"]

    def _get_partials(self):
        return self.extra["search_matches"]

    def _get_dupes(self):
        return self.extra["search_dupes"]

    def _add_match(self, ref=None):
        self.extra["search_matches"] += 1
        if ref:
            self._out_data.loc[self._out_data[self._out_data.columns.tolist()[0]] == ref, "matches"] = True
    def _add_partial(self, ref=None):
        self.extra["search_matches"] += 1
        if ref:
            self._out_data.loc[self._out_data[self._out_data.columns.tolist()[0]] == ref, "partials"] = True
    def _add_dupe(self):
        self.extra["search_dupes"] += 1

    def _get_desc(self, ref):
        """Return the first matching description for the given reference.

        :param ref: The reference to search for.
        :return: The first matching description for the reference.
        """
        return self.lookup_data[np.where(self.lookup_data[:, 0] == ref)[0], 2][0]

    def _get_row(self, ref):
        """Return the first matching row for the given reference.

        :param ref: The reference to search for.
        :return: The first matching row for the reference.
        """
        return self.lookup_data[np.where(self.lookup_data[:, 0] == ref)[0]][0, 3:]

    def _get_path_end(self, ref):
        """Return the path constructed from the attributes in the data.

        :param ref: The reference to use for finding the attributes.
        :return: The path constructed from the attributes.
        """
        return os.path.join(*self._get_row(ref).tolist())

    def _ref_to_shrunk(self, ref):
        """Return the shrunken reference for the given reference.

        :param ref: The reference to shrink.
        :return: The shrunken reference.
        """
        return self.lookup_data[np.where(self.lookup_data[:, 0] == ref)[0], 1][0]

    def _shrunk_to_ref(self, shrunk):
        """Return the original reference for the given shrunken reference.

        :param shrunk: The shrunken reference to expand.
        :return: The original reference.
        """
        return self.lookup_data[np.where(self.lookup_data[:, 1] == shrunk)[0], 0][0]


    def _deal_with_matches_etc(self, dst_file, src_file):
        """
        Handles files with matching names in the same directory as the input file. Checks to see if any match and then keeps the largest one.

        :param filename: The input file name.
        """
        # Get the directory of the input file
        directory = os.path.dirname(dst_file)
        filename = os.path.basename(dst_file)
        ext = filename.split(".")[-1]
        ref = filename.replace(ext, "")

        # Get all the filenames in the directory
        filenames = os.listdir(directory)

        for fn in filenames:
            file_one = os.path.join(directory, filename)


            # Check if the filename matches the input file name or follows the pattern "{filename}_alt*"
            if (fn == filename or fn.startswith(f"{filename}_alt")) and not filecmp.cmp(src_file, dst_file):
                # If a matching filename is found, get the full file path
                matching_file = os.path.join(directory, fn)
                file_two = os.path.join(directory, matching_file)
                # Check if the matching file is an image match with the input file
                if is_image_match(file_one, file_two):
                    # If the matching file is an image match, compare the file sizes
                    if os.path.getsize(file_one) > os.path.getsize(file_two):
                        # If the input file is larger, delete the matching file and keep the input file
                        os.remove(matching_file)
                        shutil.copy2(src_file, matching_file)
                    # End the loop once a match has been found and handled
                    return
        new_filename = f"{ref}_alt_" + str(random.randint(0,99999)) + "." + ext
        shutil.copy2(src_file, os.path.join(directory, new_filename))


    def _copy_file_with_checks(self, src_file: str, dst_file: str, ref: str, *args, **kwargs) -> None:
        """
        Copies a file to a new path while checking for duplicates.

        :param src_file: The source file to be copied.
        :param dst_file: The destination file path.
        :param ref: The reference string used in naming conventions.
        """
        # Replace strange folder paths in the destination file path
        dst_file = replace_strange_folder_paths(dst_file)

        # If the image is a product, amend the destination folder
        if is_image_product(src_file):
            dst_file = add_top_level_parent_directory(dst_file, ref, "_background")

        # Make folders in the file path if they do not exist
        make_folders_from_filepath(dst_file)

        try:
            # If the destination file already exists, check if the image matches the original.
            # If it matches, add a '_same' suffix to the file name. If it doesn't match, add a '_alt' suffix.
            if os.path.exists(dst_file):
                self._deal_with_matches_etc(dst_file, src_file)

            # Copy the source file to the destination file
            shutil.copy2(src_file, dst_file)

        except Exception as e:
            # Catch any errors that occur during the copying process
            print("Error with " + dst_file)

    # def copy_file_with_checks(self, src_file: str, dst_file: str, ref: str, *args, **kwargs) -> None:
    #     """
    #     Copies a file to a new path, if the imege is
    #     :param src_file: Source File to copy
    #     :param dst_file: Destination file path
    #     :param ref: Stock ref
    #     """
    #     global dupes
    #     dst_file = replace_strange_folder_paths(dst_file)
    #
    #     if is_image_product(src_file):
    #         # if the image is a product then amend dst folder
    #         dst_file = add_top_level_parent_directory(dst_file, ref, "_background")
    #     # make folders in path if not exist
    #     make_folders_from_filepath(dst_file)
    #
    #     try:
    #         # if file exists then  - check if the image matches the original, if match then append 'same' to the file
    #         # name, if not image doesn't match and add alt
    #         if os.path.exists(dst_file):
    #             if is_image_match(src_file, dst_file):
    #                 self._add_dupe()
    #                 dst_file = add_suffix_to_file(dst_file, self._get_match_path())
    #             else:
    #                 dst_file = add_suffix_to_file(dst_file, self._get_alt_path())
    #         shutil.copy2(src_file, dst_file)
    #
    #     except Exception as e:
    #         # errors.append(["copy file", ref, e])
    #         print("Error with " + dst_file)

    def _rename_largest_image(filepath: str) -> None:
        # Get the directory and filename without the suffix
        directory, filename = os.path.split(filepath)
        base, ext = os.path.splitext(filename)

        # Find all files with the same base name and the "_same_" suffix
        same_files = [f for f in os.listdir(directory) if f.startswith(base + "_same_")]

        # If there are no such files, return immediately
        if not same_files:
            return

        # Find the file with the largest size
        largest_file = max(same_files, key=lambda f: Image.open(os.path.join(directory, f)).size[0] *
                                                     Image.open(os.path.join(directory, f)).size[1])

        # Rename the largest file to the original name
        os.rename(os.path.join(directory, largest_file), os.path.join(directory, base + ext))

        # Delete the rest of the files
        for f in same_files:
            if f != largest_file:
                os.remove(os.path.join(directory, f))

    def _deal_with_match(self, matchqty, file, filebase, ref):
        """Handle the processing of matched or partially matched files

        :param matchqty: match quantity information
        :param file: file name to be processed
        :param filebase: base file path
        :param ref: reference information

        :return: None
        """
        ext = file.split(".")[-1]
        # convert shunk to real sku
        sku_real = self._shrunk_to_ref(ref)

        if matchqty[0]:
            self._add_match(sku_real)
            typ = "match/"
        elif matchqty[1]:
            typ = "partial/"
            self._add_partial(sku_real)
        elif matchqty[2]:
            typ = "partial_other/"
            self._add_partial(sku_real)
        elif matchqty[3]:
            typ = "folder_match/"
            self._add_partial(sku_real)

        try:
            #get filename
            new_filename = make_filename_valid(sku_real) + "." + ext
            #get new path
            new_path = os.path.join(self.out_path, typ, self._get_path_end(sku_real), new_filename)
            #copy file
            self._copy_file_with_checks(os.path.join(filebase + file), new_path, sku_real)

        except Exception as e:
            pass
            # errors.append(["deal_with_match", ref, e])

    # def load_files(self, path=None):
    #     """
    #     Loads the file into the object, that is, that it searches the file path for all images and stores path etc.
    #
    #     :param path: path to search, defaults to self.search_path if none
    #
    #     :return: on completion
    #     """
    #     if not path:
    #         path = self.search_path
    #
    #     assert path
    #     assert self.out_path
    #     assert type(self._base_data) is pd.DataFrame
    #
    #     for entry in os.scandir(path):
    #         found = sum([1 if x in entry.path else 0 for x in
    #                      ["recyc", "Delivery Notes", "Pick No", "Invoices", ".ipynb_checkpoints"]])
    #         if found == 0:
    #             if entry.is_dir():
    #                 self.load_files(entry.path)
    #             else:
    #                 file = entry.name
    #                 root = entry.path.replace(entry.name, "").replace("\\", "/")
    #                 file_path = os.path.join(root, file)
    #                 image = 1 if file.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif", "webp"] else 0
    #                 if image and is_large_file(entry):
    #                     self.files_source.append([file_path, root, file])
    #
    #                 if self.verbose:
    #                     len(self.files_source) % 10000 == 0 and pprint("Found len" + str(len(self.files_source)))
    #     self.files_len = len(self.files_source)

    # def load_files(self, path=None):
    #     """
    #     Loads the file into the object by searching the file path for all images and storing their paths and related information.
    #
    #     :param path: the path to search for files. If not provided, defaults to `self.search_path`.
    #     :type path: str, optional
    #
    #     :return: None
    #     """
    #     if not path:
    #         path = self.search_path
    #
    #     # Check if `path` and `self.out_path` are provided, and if `self._base_data` is a `pd.DataFrame`
    #     assert path, "Path must be provided"
    #     assert self.out_path, "Output path must be provided"
    #     assert isinstance(self._base_data, pd.DataFrame), "Base data must be a Pandas DataFrame"
    #
    #     # Iterate over all entries in the given `path`
    #     for entry in os.scandir(path):
    #         # Check if the entry path contains any of the following substrings
    #         found = sum([1 if x in entry.path else 0 for x in
    #                      ["recyc", "Delivery Notes", "Pick No", "Invoices", ".ipynb_checkpoints"]])
    #
    #         # If the entry path doesn't contain any of the substrings
    #         if found == 0:
    #             # If the entry is a directory, search it recursively
    #             if entry.is_dir():
    #                 self.load_files(entry.path)
    #             else:
    #                 file = entry.name
    #                 root = entry.path.replace(entry.name, "").replace("\\", "/")
    #                 file_path = os.path.join(root, file)
    #                 # Check if the file is an image
    #                 image = 1 if file.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif", "webp"] else 0
    #                 # If the file is an image, and it's not too large, add its information to `self.files_source`
    #                 if image and is_large_file(entry):
    #                     self.files_source.append([file_path, root, file])
    #
    #                 # If verbose mode is enabled, log progress every 10,000 files found
    #                 if self.verbose and len(self.files_source) % 10000 == 0:
    #                     pprint("Found len" + str(len(self.files_source)))
    #
    #     # Store the number of files found
    #     self.files_len = len(self.files_source)

    def _check_paths(self, path):
        """
        Checks if `path` and `self.out_path` are provided, and if `self._base_data` is a `pd.DataFrame`.

        :param path: the path to search for files. If not provided, defaults to `self.search_path`.
        :type path: str, optional

        :raises AssertionError: if `path` is not provided, `self.out_path` is not provided, or `self._base_data` is not a `pd.DataFrame`.
        """
        assert path, "Path must be provided"
        assert self.out_path, "Output path must be provided"
        assert isinstance(self._base_data, pd.DataFrame), "Base data must be a Pandas DataFrame"

    def _get_files(self, path):
        """
        Iterates over all entries in the given `path` and returns information about the files that are images and not too large.

        :param path: the path to search for files.
        :type path: str

        :return: a list of lists, where each inner list contains information about a file.
        :rtype: list
        """
        files = []
        for entry in os.scandir(path):
            if not any(
                    x in entry.path for x in ["recyc", "Delivery Notes", "Pick No", "Invoices", ".ipynb_checkpoints"]):
                if entry.is_dir():
                    files.extend(self._get_files(entry.path))
                else:
                    file = entry.name
                    root = entry.path.replace(entry.name, "").replace("\\", "/")
                    file_path = os.path.join(root, file)
                    image = 1 if file.split(".")[-1].lower() in ["jpg", "jpeg", "png", "gif", "webp"] else 0
                    if image and is_large_file(entry):
                        files.append([file_path, root, file])

                    if self.verbose and len(files) % 10000 == 0:
                        pprint("Found len" + str(len(files)))
        return files

    def load_files(self, path=None):
        """
        Loads the file into the object by searching the file path for all images and storing their paths and related information.

        :param path: the path to search for files. If not provided, defaults to `self.search_path`.
        :type path: str, optional

        :return: None
        """
        if not path:
            path = self.search_path

        self._check_paths(path)
        self.files_source = self._get_files(path)
        self.files_len = len(self.files_source)

    def match_files(self):
        """
        Actually attempts to match the files, reads the file list, and then searches the list of files,
        checks for matches, and then if found copies the file to the new location

        :return:
        """

        now = datetime.datetime.now()

        for i, listed_file in enumerate(self.files_source):
            #splits file into its parts
            file_path, root, file = listed_file
            # shinks the file name with the same rules as the input data does
            code = shrink_stock_ref(file.replace(file.split(".")[-1], ""))
            # checks for a match of either, full, partial, reverse partial, or directory match
            match = count_matches(self.code_data, code, file_path)
            # gets the match
            check_match = [x for x in list(match) if x]
            # deals with it if one found
            if len(check_match) > 0:
                self._deal_with_match(match, file, root, check_match[0])
            # prints if needed
            if self.verbose and i % 1000 == 0:
                pprint(
                    f"Img {i} checked   Total Matches: {self._get_matches()}  Total Partials {self._get_partials()}  Total Dupes {self._get_dupes()}",
                    i,
                    self.files_len, now)

    def view_matches(self):
        return self._out_data.loc[self._out_data["matches"] > 0]
    def view_partials(self):
        return self._out_data.loc[self._out_data["partials"] > 0]
    def view_missing(self):
        return self._out_data.loc[(self._out_data["partials"] == 0) and (self._out_data["matches"] == 0)]