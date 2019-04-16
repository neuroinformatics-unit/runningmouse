from scipy.spatial.distance import euclidean
import os
import numpy as np
from PIL import Image


def get_distances(lista, listb):
    distances = []
    for idx in range(0, len(lista)):
        distances.append(euclidean(lista[idx], listb[idx]))
    return distances


def save_csv(output_dir, name, trace):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, name + ".csv")
    np.savetxt(filename, trace)


def save_movie(output_dir, movie, name, basename='frame'):
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
