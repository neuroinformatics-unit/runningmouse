import av
from datetime import datetime
import numpy as np
import scipy.signal
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter

import tools.plot as ps_plot
import tools.tools as tools


def main():
    """
    Takes a video, crops the left half, calculates the v(t) - v(t-1)
    difference, saves this as a new video, and saves the resulting mean
    difference over time
    """
    start_time = datetime.now()
    args = parse()

    container = av.open(args.video_file)

    len_t = container.streams.video[0].duration
    len_y = container.streams.video[0].codec_context.coded_height
    len_x = container.streams.video[0].codec_context.coded_width

    dev_t = int(round(len_t/10))

    # TODO: generalise cropping
    half_len_x = int(round(len_x / 2))
    video_array = np.empty((len_y, half_len_x, len_t), dtype=float)
    t = 0

    print('Loading video')
    for frame in container.decode(video=0):
        array = frame.to_ndarray(format='rgb24')
        # get mouse
        video_array[:, :, t] = array[:, 0:half_len_x, 0]
        if args.dev:
            if t > dev_t:
                break
        t += 1

    if args.dev:
        video_array = video_array[:, :, 0:dev_t]
        video_array = video_array[0::4, 0::4, 0::4]

    if args.med_filt_kernel:
        print('Filtering')
        video_array = scipy.signal.medfilt(
            video_array, kernel_size=[1, 1, args.med_filt_kernel])

    print('Calculating difference')
    difference = abs(np.diff(video_array))

    print('Calculate mean_trace')
    mean_trace = np.mean(difference, axis=(0, 1))

    if args.plot:
        ps_plot.plot_1d(mean_trace, x_label='Time (frames)',
                        y_label='Difference (a.u.)',
                        title='Video difference over time')

    if args.save_movie:
        print('Saving')
        tools.save_movie(args.output_dir, difference)

    if args.save_csv:
        tools.save_csv(args.output_dir, 'mean_trace', mean_trace)

    print('Finished. Total time taken: %s', datetime.now() - start_time)


def parse():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('-v', '--video-file', dest='video_file', type=str,
                        required=True, help='Movies')
    parser.add_argument( '-o', dest='output_dir', type=str,
                         help='Output directory')
    parser.add_argument('--save-csv', dest='save_csv', action='store_true',
                        help='Save .csv?')
    parser.add_argument('--save-movie', dest='save_movie', action='store_true',
                        help='Save difference movie frames?')
    parser.add_argument('--plot', dest='plot', action='store_true',
                        help='Plot?')
    parser.add_argument('--med-filt-kernel', dest='med_filt_kernel',
                        type=int, default=5, help='Smoothing sigma')
    parser.add_argument('--dev', dest='dev', action='store_true',
                        help='Process fraction of data (for development')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    main()
