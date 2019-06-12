import os
import sys
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtWidgets import QApplication
from polygon_generator_gui_folder.designer_polygon_generator_gui import Ui_MainWindow
from polygon_generator.polygon_generator import ConcavePolygonGenerator, ConvexPolygonGenerator
from polygon_generator.folder import save_image_to_folder

"""
Overall process of making an executable file starting from designing the application in QtDesigner. this is being run 
on a Windows computer, so a .exe file will be created in the end

Instructions for creating a python file from a .ui file from the QtDesigner application
Use QtDesigner to create an application that you want

Next is to turn the .ui into a .py file; in the terminal run this with whatever the ui path is.
pyuic5 {ui_path}.ui -o {ui_path}.py
so for this:
pyuic5 polygon_generator_gui_folder/designer_polygon_generator_gui.ui -o polygon_generator_gui_folder/designer_polygon_generator_gui.py

for this example, remember that using the terminal from pycharm, most of the path is already there, pointing to the 
root of the project already, so usually only need to add the final part of the path to actually get to the .ui file
if at any point changes need to be made in the QtDesigner, then the pyuic5 line needs to be run in the terminal 
again, and this will completely delete and remake the .py file created from the .ui file

after the .py file is created (the .py file that gets created contains the gui definition. then need to create another 
file that will load the ui file (this file)
in this file, need to import the .py that was created from the .ui file, also need to have imports at the top of the 
file for PyQt. 
Then need to create a class for the app to be made, and it needs to be a subtype of QtWidgets.QMainWindow, 
and also the Ui_MainWindow class from the .py file that was generated from the .ui file. just need to define the 
__init__ method for this class and call the setupUi method. add any other class attributes here too. then add methods 
to the class that have to do with interacting with the added attributes, and that take in input from the GUI to 
perform other tasks. 

in the .py file generated from the .ui file, need to add tool tips and connections between user interaction with the 
gui with code that you want to be run in response (in other words, when the user interacts with the gui, we want to 
link the interaction with some method call to do something else; the method calls are in the class in this file.
this file also needs to include a main method to create a QApplication, an instance of the app class that is defined 
in this file, to show this app, and to be able to exit out of the QApplication.

Finally need to include the call to the main method if __name__ is 'main'

Then to generate a windowed executable application of this run in the terminal:
pyinstaller --windowed {file_name_to_make_executable}.py 
so for this run the following in the 
terminal, which will create a _pycache_ folder, build folder, dist folder, and a polygon_generator_gui.spec file in 
the main folder:
pyinstaller --windowed polygon_generator_gui_folder/polygon_generator_gui.py

inside the dist folder there is a polygon_generator_gui folder, and inside that will be a polygon_generator_gui.exe 
file that will launch the polygon generator gui application  
"""


class PolygonGeneratorApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(PolygonGeneratorApp, self).__init__(parent)
        self.setupUi(self)

        # default values chosen based on the default values in the gui (the .ui file)
        self.generate_convex_polygon = True  # by default set this to true, this is used to decide which of the two
        # generators to use when the generate polygons button is pressed
        self.number_of_images_to_generate = 10
        self.folder_to_save_to = None
        self.file_format = 'jpg'

        # create an instance of both generator types and update them both, since there is no easy way to switch
        # between making convex and concave polygons at the moment
        self.convex_polygon_generator = ConvexPolygonGenerator(image_height=480,
                                                               image_width=480,
                                                               number_of_vertices=5)

        self.concave_polygon_generator = ConcavePolygonGenerator(image_height=480,
                                                                 image_width=480,
                                                                 number_of_vertices=5)

    """
    Define methods here
    The methods here take in the values from the gui and can do thing. So here is where the polygon generator can be 
    altered according to changes that are made in the gui
    """

    def instructions_window(self):
        # print('instructions window')
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Instructions")
        horizontal_layout = QtWidgets.QHBoxLayout(dialog)
        label_instructions = QtWidgets.QLabel(dialog)
        horizontal_layout.addWidget(label_instructions)
        instructions = 'On the left side of the interface choose the settings for the generated polygons. \nPress ' \
                       'the "Draw sample polygon" button to generate a sample polygon with the current settings. ' \
                       '\nThen select the number of randomized images of polygons to' \
                       ' be generated and choose a file format for the images to be saved as.\nLastly, select the ' \
                       'folder for all the images to be saved in and push the "Generate images" button.'
        label_instructions.setText(instructions)
        dialog.exec_()

    def about_window(self):
        url = "https://github.com/vlai3/polygongenerator"
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))

    def set_background_colour(self):
        color = QtWidgets.QColorDialog.getColor()
        # print(f'set background colour in HEX: {color.name()}')
        # print(f'set background colour in RGB: {hex_color.getRgb()}')  # but this has 4 channels; is last one alpha?
        colour_rgba = color.getRgb()
        r_channel = colour_rgba[0]
        g_channel = colour_rgba[1]
        b_channel = colour_rgba[2]

        colour_bgr = (b_channel, g_channel, r_channel)

        self.concave_polygon_generator.set_background_colour(colour=colour_bgr)
        self.convex_polygon_generator.set_background_colour(colour=colour_bgr)
        # print(f'background colour bgr = {colour_bgr}')

        # then colour in the background label to match the colour
        palette = self.label_background_colour.palette()
        palette.setColor(self.backgroundRole(), color)
        self.label_background_colour.setPalette(palette)

    def set_shape_colour(self):
        color = QtWidgets.QColorDialog.getColor()
        # print(f'set shape colour in HEX: {color.name()}')
        # print(f'set shape colour in RGB: {hex_color.getRgb()}')  # but this has 4 channels; is last one alpha?
        colour_rgba = color.getRgb()
        r_channel = colour_rgba[0]
        g_channel = colour_rgba[1]
        b_channel = colour_rgba[2]

        colour_bgr = (b_channel, g_channel, r_channel)

        self.concave_polygon_generator.set_shape_colour(colour=colour_bgr)
        self.convex_polygon_generator.set_shape_colour(colour=colour_bgr)
        # print(f'shape colour bgr = {colour_bgr}')

        # then colour in the shape label to match the colour
        palette = self.label_shape_colour.palette()
        palette.setColor(self.backgroundRole(), color)
        self.label_shape_colour.setPalette(palette)

    def set_generator_to_concave(self):
        self.generate_convex_polygon = False
        # print(f'generator set to convex: {self.generate_convex_polygon}')

    def set_generator_to_convex(self):
        self.generate_convex_polygon = True
        # print(f'generator set to convex: {self.generate_convex_polygon}')

    def set_number_of_vertices(self):
        self.convex_polygon_generator.set_number_of_vertices(self.spinBox_number_of_vertices.value())
        self.concave_polygon_generator.set_number_of_vertices(self.spinBox_number_of_vertices.value())
        # print(f'polygon generator n of vertices: {self.convex_polygon_generator.number_of_vertices}')

    def set_number_of_images_to_generate(self):
        self.number_of_images_to_generate = self.spinBox_number_of_images_to_generate.value()
        # print(f'number of images to generate: {self.number_of_images_to_generate}')

    def select_file_save_format(self, text):
        self.file_format = text
        # print(f'file save format: {self.file_format}')

    def set_image_width(self):
        self.convex_polygon_generator.set_image_width(self.spinBox_image_width.value())
        self.concave_polygon_generator.set_image_width(self.spinBox_image_width.value())
        # print(f'polygon generator image width: {self.concave_polygon_generator.image_width}')

    def set_image_height(self):
        self.convex_polygon_generator.set_image_height(self.spinBox_image_height.value())
        self.concave_polygon_generator.set_image_height(self.spinBox_image_height.value())
        # print(f'polygon generator image height: {self.concave_polygon_generator.image_height}')

    def draw_sample_polygon(self):
        chosen_polygon_generator = None
        if self.generate_convex_polygon is True:
            chosen_polygon_generator = self.convex_polygon_generator
        else:
            chosen_polygon_generator = self.concave_polygon_generator

        number_of_vertices = chosen_polygon_generator.number_of_vertices

        label_height = self.label_sample_polygon_image.height()
        label_width = self.label_sample_polygon_image.width()

        set_height = chosen_polygon_generator.image_height
        set_width = chosen_polygon_generator.image_width

        chosen_polygon_generator.set_image_height(label_height)
        chosen_polygon_generator.set_image_width(label_width)

        generated_sample_image = chosen_polygon_generator.generate_polygon(number_of_vertices=number_of_vertices)

        folder_to_save_to = self.folder_to_save_to
        if folder_to_save_to is None:
            folder_to_save_to = os.getcwd()
        file_format = self.file_format
        image_path = save_image_to_folder(folder_path=folder_to_save_to,
                                          image_name=f'sample_image',
                                          image=generated_sample_image,
                                          file_format=file_format,
                                          )
        pixmap = QtGui.QPixmap(image_path)
        self.label_sample_polygon_image.setPixmap(pixmap)
        self.label_sample_polygon_image.show()

        os.remove(os.path.join(folder_to_save_to, f'sample_image.{file_format}'))
        chosen_polygon_generator.set_image_height(set_height)
        chosen_polygon_generator.set_image_width(set_width)

    def set_folder_to_save_to(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        # print(f'folder to save to: {folder}')
        self.folder_to_save_to = folder

        # then display the folder path on the selected folder to save to label
        self.label_selected_folder_to_save_to.setText(f'{folder}')

    def generate_images(self):
        # print(f'generate images')
        if self.folder_to_save_to is None:
            return
        chosen_polygon_generator = None
        if self.generate_convex_polygon is True:
            chosen_polygon_generator = self.convex_polygon_generator
        else:
            chosen_polygon_generator = self.concave_polygon_generator

        folder_to_save_to = self.folder_to_save_to
        number_of_vertices = chosen_polygon_generator.number_of_vertices
        image_name = 'generated_polygon'
        file_format = self.file_format

        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Download progress")
        dialog.resize(350, 100)
        horizontal_layout = QtWidgets.QHBoxLayout(dialog)
        progress_bar = QtWidgets.QProgressBar()
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(self.number_of_images_to_generate-1)
        progress_bar.setValue(0)
        horizontal_layout.addWidget(progress_bar)
        dialog.show()

        for index in range(self.number_of_images_to_generate):
            generated_polygon_image = chosen_polygon_generator.generate_polygon(number_of_vertices=number_of_vertices)
            save_image_to_folder(folder_path=folder_to_save_to,
                                 image_name=f'{image_name}_{index}',
                                 image=generated_polygon_image,
                                 file_format=file_format,
                                 )
            progress_bar.setValue(index)
            QApplication.processEvents()

        dialog.exec_()


def main():
    app = QApplication(sys.argv)
    form = PolygonGeneratorApp()

    form.show()
    app.exec_()


if __name__ == '__main__':
    main()


"""
while editing and playing around with things, the designer_polygon_generator_gui.py file might be overwritten, 
so a copy of the changes that I have made that will need to go into the file will be stored here

these changes go between self.retranslateUi(MainWindow) and QtCore.QMetaObject...
"""

# """
# tool tips
# """
# self.label_image_width.setToolTip("Set the width (0-1000) of the images that will be generated")
# self.label_image_height.setToolTip("Set the height (0-1000) of the images that will be generated")
# self.label_number_of_images_to_generate.setToolTip("Set the number of images (up to 1000) to be generated")
# self.label_file_save_format.setToolTip("Select the file format for the generated images to be saved as")
# self.button_select_folder_to_save_images_to.setToolTip("Select a folder for the generated images to be saved")
# self.pushButton_generate_images.setToolTip("Generate and save images of polygons to the selected folder in")
# self.button_draw_sample_polygon.setToolTip("Draw a sample polygon with the current settings")
# self.label_number_of_vertices.setToolTip("Select the number (1-99) of vertices for the polygon to have")
# self.label_polygon_type.setToolTip("Select the type of polygon to generate")
# self.button_select_shape_colour.setToolTip('Select polygon colour')
# self.button_select_background_colour.setToolTip('Select image background colour')
#
# """
# Do connections here
# So for this, need to link what happens when there is some change in the gui to a method that is in the
# MainWindow class, and in the MainWindow class, the methods are able to reference the values from the gui that
# come from buttons and the like
# """
#
# self.actionInstructions.triggered.connect(MainWindow.instructions_window)
# self.actionAbout.triggered.connect(MainWindow.about_window)
#
# self.button_select_background_colour.clicked.connect(MainWindow.set_background_colour)
# self.button_select_shape_colour.clicked.connect(MainWindow.set_shape_colour)
#
# self.radioButton_concave.toggled.connect(MainWindow.set_generator_to_concave)
# self.radioButton_convex.toggled.connect(MainWindow.set_generator_to_convex)
#
# self.spinBox_number_of_vertices.valueChanged.connect(MainWindow.set_number_of_vertices)
# self.spinBox_image_width.valueChanged.connect(MainWindow.set_image_width)
# self.spinBox_image_height.valueChanged.connect(MainWindow.set_image_height)
# self.spinBox_number_of_images_to_generate.valueChanged.connect(MainWindow.set_number_of_images_to_generate)
# self.comboBox_files_save_format.activated[str].connect(MainWindow.select_file_save_format)
#
# self.button_draw_sample_polygon.clicked.connect(MainWindow.draw_sample_polygon)
#
# self.button_select_folder_to_save_images_to.clicked.connect(MainWindow.set_folder_to_save_to)
#
# self.pushButton_generate_images.clicked.connect(MainWindow.generate_images)


