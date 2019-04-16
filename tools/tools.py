from scipy.spatial.distance import euclidean
import os
import numpy as np
from PIL import Image


def get_distances(lista, listb):
    """
    Based on two lists of (x,y) coordinate tuples, calculated the euclidean
    distance between each pair of tuples
    :param lista:
    :param listb:
    :return:
    """

    distances = []
    for idx in range(0, len(lista)):
        distances.append(euclidean(lista[idx], listb[idx]))
    return distances


def save_csv(output_dir, name, trace):
    """
    Saves a 1D array to "output_dir/name.csv"
    :param output_dir:
    :param name:
    :param trace:
    :return:
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, name + ".csv")
    np.savetxt(filename, trace)


def save_movie(output_dir, movie, name=None, basename='frame'):
    """
    Saves a 3D numpy array as a series of 2D tiffs
    :param output_dir:
    :param movie:
    :param name:
    :param basename:
    :return:
    """
    if name:
        output_dir = os.path.join(output_dir, name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for t in range(0, movie.shape[2]):
        filename = os.path.join(output_dir, basename + "_" + str(t) + ".tif")
        im = Image.fromarray(movie[:, :, t])
        im.save(filename)


def stamp_im(im, point):
    """
    "Stamp' point onto images
    :param im: 3D numpy array (x,y,t)
    :param point: The x,y position to overlay
    :return: Image with point stamped onto it
    """
    # TODO: generalise to large images (stamp more than 1x1)
    max_val = np.max(im)

    for t in range(0, im.shape[2]):
        im_x = int(round(point[t][0]))
        im_y = int(round(point[t][1]))

        im[im_x, im_y, t] = 2 * max_val

    return im
