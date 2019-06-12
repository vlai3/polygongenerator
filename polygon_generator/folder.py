import os
import shutil
import cv2
import tkinter
from tkinter import messagebox


class Folder:
    """
    Class to create and store a folder hierarchy and to easily create folders and access paths to save files and
    folders in
    """

    def __init__(self,
                 folder_name: str,
                 folder_path: str,
                 ):
        """
        A folder can have files and folders in it, but for now just care about it containing folders. The name of the
        folder should be the same as the last part of the folder path.

        :param str, folder_path: path to save the folder on disk
        :param str, folder_name: Should be the same as the last part of the folder path
        """
        self.name = folder_name
        self.path = folder_path
        self.children = set()

        try:
            self.save_to_disk()
        except FileExistsError as error:
            root = tkinter.Tk()
            yes_or_no_result = tkinter.messagebox.askyesno(
                'Folder manager',
                'File or folder already exists. Would you like to create one with "_copy_(#)" appended to the '
                'end of the file name?')
            if yes_or_no_result is True:
                # rename the file something else
                for i in range(20):  # randomly put 20 here, just assuming there won't already be more
                    try:
                        old_name = self.get_name()
                        old_path = self.get_path()
                        new_name = old_name + f'_copy_({i})'
                        new_path = old_path + f'_copy_({i})'
                        self.set_name(name=new_name)
                        self.set_path(path=new_path)
                        self.save_to_disk()
                        root.destroy()
                        break
                    except FileExistsError as error:
                        self.set_name(name=old_name)
                        self.set_path(path=old_path)
                        pass
            else:
                raise error

    def get_name(self):
        return self.name

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def set_name(self,
                 name: str,
                 ):
        self.name = name

    def save_to_disk(self):
        os.makedirs(
            name=self.path,
        )

    def delete_from_disk(self):
        shutil.rmtree(path=self.path)

    def get_children(self):
        return self.children

    def add_child(self,
                  child,
                  ):
        """
        Add a child to the set of children

        :return:
        """
        self.children.add(child)

    def save_image_to_folder(self,
                             image_name: str,
                             image,
                             ):
        """
        Save an image to disk using cv2
        :param str, image_name: name of the file to save the image as in the folder
        :param image: image to save

        :return: str, path_to_save_image: the path the image was saved to
        """
        image_name = f'{image_name}.jpg'
        path_to_save_image = os.path.join(self.path, image_name)
        cv2.imwrite(path_to_save_image, image)

        return path_to_save_image


def save_image_to_folder(folder_path: str,
                         image_name: str,
                         image,
                         file_format: str = 'jpg',
                         ):
    """
    Save an image to disk using cv2
    :param str, folder_path: folder to save the image to
    :param str, image_name: name of the file to save the image as in the folder
    :param image: image to save
    :param str, file_format:

    :return: str, path_to_save_image: the path the image was saved to
    """
    image_name = f'{image_name}.{file_format}'
    path_to_save_image = os.path.join(folder_path, image_name)
    cv2.imwrite(path_to_save_image, image)

    return path_to_save_image
