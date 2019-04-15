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


def save_movie(output_dir, movie, name):
    output_dir = os.path.join(output_dir, name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for t in range(0, movie.shape[2]):
        filename = os.path.join(output_dir, "frame_" + str(t) + ".tiff")
        im = Image.fromarray(movie[:, :, t])
        im.save(filename)


def stamp_im(im, points):
    max_val = np.max(im)
    # "Stamp' point onto images
    for t in range(0, im.shape[2]):
        im_x = int(round(points[t][0]))
        im_y = int(round(points[t][1]))

        im[im_x, im_y, t] = 2 * max_val

    return im
