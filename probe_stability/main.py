import av
from datetime import datetime
from skimage.filters import threshold_otsu, gaussian
from scipy.ndimage.measurements import center_of_mass
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import numpy as np

import tools.plot as ps_plot
import tools.tools as tools


def main():
    """
    Takes two movies (of two bright reference points), finds their centers
    and plots the movement over time.
    Assuming equal pixel calibration, the relative distances of these points
    (i.e. do they move together) is calculated and saved
    """

    start_time = datetime.now()
    args = parse()

    video_a, centres_a = run_movie(args.files[0], sigma=args.sigma)
    video_b, centres_b = run_movie(args.files[1], sigma=args.sigma)

    video_a = tools.stamp_im(video_a, centres_a)
    video_b = tools.stamp_im(video_b, centres_b)

    distances = np.array(tools.get_distances(centres_a, centres_b))

    # normalise
    distances = distances - distances[0]

    if args.save_csv:
        tools.save_csv(args.output_dir, 'distances', distances)
    if args.save_movie:
        # TODO: get video filenames
        tools.save_movie(args.output_dir, video_a, name='video_a')
        tools.save_movie(args.output_dir, video_b, name='video_b')
    print('Finished calculations. Total time taken: %s',
          datetime.now() - start_time)

    if args.plot:
        ps_plot.scroll_plot(video_a, video_b, title='Centres')
        ps_plot.plot_1d(distances, x_label='Time (frames)',
                        y_label='Centroid distance drift (pixels)',
                        title='Drift over time')


def parse():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-f', '--movie-files', dest='files', type=str,
                        nargs='+', required=True, help='Movies')
    parser.add_argument('-o', dest='output_dir', type=str,
                        help='Output directory')
    parser.add_argument('--save-csv', dest='save_csv', action='store_true',
                        help='Save .csv?')
    parser.add_argument('--save-movie', dest='save_movie', action='store_true',
                        help='Save overlay movie frames?')
    parser.add_argument('--plot', dest='plot', action='store_true',
                        help='Plot?')
    parser.add_argument('--sigma', dest='sigma', type=int, default=1,
                        help='Smoothing sigma')
    args = parser.parse_args()
    return args


def run_movie(file, sigma=5):
    """
    Loads video, and finds the centre of the (singular) bright spot
    :param file:
    :param sigma:
    :return:
    """
    container = av.open(file)
    centres = []

    len_t = container.streams.video[0].duration
    len_y = container.streams.video[0].codec_context.coded_height
    len_x = container.streams.video[0].codec_context.coded_width

    video_array = np.empty((len_y, len_x, len_t), dtype=float)

    t = 0
    for frame in container.decode(video=0):
        array = frame.to_ndarray(format='rgb24')
        frame_im = array[:, :, 0]
        video_array[:, :, t] = frame_im

        smoothed = gaussian(frame_im, sigma=sigma)
        threshold = threshold_otsu(smoothed)
        thresholded = smoothed > threshold
        centres.append(center_of_mass(thresholded))
        t += 1

    return video_array, centres


if __name__ == '__main__':
    main()
