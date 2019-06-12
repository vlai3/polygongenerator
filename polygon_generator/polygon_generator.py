import os
import cv2
import random
import numpy as np
from polygon_generator.folder import Folder

"""
For opencv: image.shape = (height, width, channels). colours are by default bgr
"""

white = (255, 255, 255)
black = (0, 0, 0)
red = (0, 0, 255)
green = (0, 255, 0)
blue = (255, 0, 0)


class PolygonGenerator:
    def __init__(self,
                 image_height: int,
                 image_width: int,
                 number_of_vertices: int,
                 ):
        # create a white image
        self.image_height = image_height
        self.image_width = image_width

        self.background_colour = white
        self.shape_colour = black
        self.line_type = cv2.LINE_AA

        # if you dont want randomly generated points within n pixels of either the width edges or height edges of the
        #  image, set these numbers
        self.height_bezels = 0
        self.width_bezels = 0

        # initially set white canvas as image
        self.image = self.reset_image()

        self.number_of_vertices = number_of_vertices

        self.polygon_vertices = []

    def reset(self):
        self.reset_image()
        self.polygon_vertices = []

    def reset_image(self):
        self.image = np.zeros((self.image_height, self.image_width, 3), np.uint8)

        channel_one_value = self.background_colour[0]
        channel_two_value = self.background_colour[1]
        channel_three_value = self.background_colour[2]

        for height_idx, col in enumerate(self.image):
            for row_idx, pixel in enumerate(col):
                self.image[height_idx][row_idx][0] = channel_one_value
                self.image[height_idx][row_idx][1] = channel_two_value
                self.image[height_idx][row_idx][2] = channel_three_value

        empty_image = self.image

        return empty_image

    def set_shape_colour(self,
                         colour: tuple,
                         ):
        """

        :param tuple, colour: shape colour to set, as (b, g, r)
        :return:
        """
        self.shape_colour = colour

    def set_background_colour(self,
                              colour: tuple,
                              ):
        """

        :param tuple, colour: shape colour to set, as (b, g, r)
        :return:
        """
        self.background_colour = colour

    def set_number_of_vertices(self,
                               number_of_vertices: int,
                               ):
        self.number_of_vertices = number_of_vertices

    def set_image_height(self,
                         height: int,
                         ):
        self.image_height = height

    def set_image_width(self,
                        width: int,
                        ):
        self.image_width = width

    def set_height_bezels(self,
                          height: int,
                          ):
        self.height_bezels = height

    def set_width_bezels(self,
                         width: int,
                         ):
        self.width_bezels = width

    def generate_n_random_points(self,
                                 number_of_vertices: int = None,
                                 ):
        """
        :param int, number_of_vertices:
        :return:
        """

        if number_of_vertices is None:
            number_of_vertices = self.number_of_vertices

        for number in range(number_of_vertices):
            random_x = random.randint(1, self.image_width-self.width_bezels)
            random_y = random.randint(1, self.image_height-self.height_bezels)
            self.polygon_vertices.append([random_x, random_y])

        self.polygon_vertices = np.array(self.polygon_vertices, np.int32)
        # reshape from being (n, 2) to (n, 1, 2) where n is the number of vertices, and 2 symbolizes having an x and
        #  y coordinate
        self.polygon_vertices = self.polygon_vertices.reshape((-1, 1, 2))

        return self.polygon_vertices

    def draw_polygon(self,
                     polygon_vertices,
                     number_of_vertices: int,
                     ):
        """
        Draw an image of a polygon with a certain number of vertices. polygon_vertices is a numpy array of the
        polygon vertices with shape (n, 1, 2). Where there are n number of vertices, and the coordinates are x and
        y for each point.

        Example of an array:
        array([[[x1, y1]],
              [[x2, y2]],
              [[x3, y3]],
              [[x4, y4]],
              [[x5, y5]],
              [[x6,  y6]],
              [[x7, y7]]]
             )

        :param number_of_vertices:
        :param polygon_vertices: np.ndarray
        :return:

        """

        raise NotImplementedError

    def generate_polygon(self,
                         number_of_vertices: int = None,
                         ):
        self.reset()

        if number_of_vertices is None:
            number_of_vertices = self.number_of_vertices

        polygon_vertices = self.generate_n_random_points(number_of_vertices=number_of_vertices)
        generated_image = self.draw_polygon(number_of_vertices=number_of_vertices,
                                            polygon_vertices=polygon_vertices)
        return generated_image

    def invert_image_colours(self,
                             image,
                             ):
        inverted_image = ~image
        return inverted_image


class ConvexPolygonGenerator(PolygonGenerator):
    def __init__(self,
                 image_height: int,
                 image_width: int,
                 number_of_vertices: int
                 ):
        super().__init__(image_height=image_height,
                         image_width=image_width,
                         number_of_vertices=number_of_vertices,
                         )

    def draw_polygon(self,
                     polygon_vertices,
                     number_of_vertices: int = None,
                     ):

        if number_of_vertices is None:
            number_of_vertices = self.number_of_vertices

        self.reset()

        image = self.image

        hull = cv2.convexHull(points=polygon_vertices)
        # for drawing n sided polygon, length of points hull needs is one more than n
        needed_hull_length = number_of_vertices + 1

        while True:
            if len(hull) is needed_hull_length:
                break
            if len(hull) < needed_hull_length:
                number_of_points_needed = needed_hull_length - len(hull)
                for number in range(number_of_points_needed):
                    random_x = random.randint(1, self.image_width)
                    random_y = random.randint(1, self.image_height)
                    polygon_vertices = np.append(polygon_vertices, [random_x, random_y])
                    polygon_vertices = polygon_vertices.reshape((-1, 1, 2))
                hull = cv2.convexHull(points=polygon_vertices)

        # works to draw convex hull
        cv2.drawContours(image=image,
                         contours=[hull],
                         contourIdx=-1,
                         color=self.shape_colour,
                         thickness=-1,  # set to -1 to colour in polygon
                         lineType=self.line_type,
                         )

        self.image = image

        return image


class ConcavePolygonGenerator(PolygonGenerator):
    def __init__(self,
                 image_height: int,
                 image_width: int,
                 number_of_vertices: int,
                 ):
        super().__init__(image_height=image_height,
                         image_width=image_width,
                         number_of_vertices=number_of_vertices,
                         )

    def draw_polygon(self,
                     polygon_vertices,
                     number_of_vertices: int = None,
                     ):
        # help from https://stackoverflow.com/questions/13935324/sorting-clockwise-polygon-points-in-matlab/13935419
        # #13935419
        if number_of_vertices is None:
            number_of_vertices = self.number_of_vertices

        self.reset()

        image = self.image

        def clockwise(points):
            x = np.array([item[0][0] for item in points])
            y = np.array([item[0][1] for item in points])
            cx = np.mean(x)
            cy = np.mean(y)
            a = np.arctan2(y - cy, x - cx)
            order = a.ravel().argsort()[::-1]
            x = x[order]
            y = y[order]
            return_points = []

            for number in range(number_of_vertices):
                return_points.append([x[number], y[number]])
            return_points = np.array(return_points, np.int32)
            return_points = return_points.reshape((-1, 1, 2))

            return return_points

        points_sorted_clockwise = clockwise(polygon_vertices)

        image = cv2.fillPoly(img=image,
                             pts=[points_sorted_clockwise],
                             color=self.shape_colour,
                             lineType=self.line_type,
                             )

        self.image = image

        return image


def test():
    concave_polygon_generator = ConcavePolygonGenerator(image_width=125,
                                                        image_height=170,
                                                        number_of_vertices=9)

    convex_polygon_generator = ConvexPolygonGenerator(image_width=125,
                                                      image_height=170,
                                                      number_of_vertices=9)

    root_folder_path = os.getcwd()

    nine_sided_polygon_folder_name = 'nine_sided_folder'
    nine_sided_polygon_folder = Folder(folder_name=nine_sided_polygon_folder_name,
                                       folder_path=os.path.join(root_folder_path, nine_sided_polygon_folder_name))

    for i in range(2):
        generated_image = concave_polygon_generator.generate_polygon(number_of_vertices=9)
        nine_sided_polygon_folder.save_image_to_folder(image_name=f'nine_sided_polygon_{i}',
                                                       image=generated_image)
    for i in range(2, 4):
        generated_image = convex_polygon_generator.generate_polygon(number_of_vertices=9)
        nine_sided_polygon_folder.save_image_to_folder(image_name=f'nine_sided_polygon_{i}',
                                                       image=generated_image)


def generate_n_sided_polygons(number_of_vertices: int):
    concave_polygon_generator = ConcavePolygonGenerator(image_width=125,
                                                        image_height=170,
                                                        number_of_vertices=number_of_vertices)
    concave_polygon_generator.set_height_bezels(10)
    concave_polygon_generator.set_height_bezels(10)

    concave_polygon_generator.set_background_colour(white)
    concave_polygon_generator.set_shape_colour(black)

    root_folder_path = os.getcwd()

    n_sided_polygon_folder_name = f'polygon_with_{number_of_vertices}_points'
    n_sided_polygon_folder = Folder(folder_name=n_sided_polygon_folder_name,
                                    folder_path=os.path.join(root_folder_path, n_sided_polygon_folder_name))

    for i in range(120):
        generated_image = concave_polygon_generator.generate_polygon(number_of_vertices=number_of_vertices)
        n_sided_polygon_folder.save_image_to_folder(image_name=f'polygon{i}',
                                                    image=generated_image)

