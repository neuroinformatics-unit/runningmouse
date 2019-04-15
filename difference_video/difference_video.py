import av
from datetime import datetime
from PIL import Image
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import os

start_time = datetime.now()

save_movie = True
save_csv = False

dev = True
dev_t = 400

med_filt_kernel = 5


video_file = '/media/adam/SATA/runningmouse/difference_video/CA_392_2_locovestrec2.avi'
output_dir = '/media/adam/SATA/runningmouse/difference/video/output3'
container = av.open(video_file)

len_t = container.streams.video[0].duration
len_y = container.streams.video[0].codec_context.coded_height
len_x = container.streams.video[0].codec_context.coded_width

half_len_x = int(round(len_x / 2))
video_array = np.empty((len_y, half_len_x, len_t), dtype=float)
t = 0

print('Loading video')
for frame in container.decode(video=0):
    array = frame.to_ndarray(format='rgb24')
    # get mouse
    video_array[:, :, t] = array[:, 0:half_len_x, 0]
    if dev:
        if t > dev_t:
            break
    t += 1


if dev:
    video_array = video_array[:, :, 0:dev_t]
    video_array = video_array[0::4, 0::4, 0::4]


print('Filtering')
video_array = scipy.signal.medfilt(
    video_array, kernel_size=[1, 1, med_filt_kernel])

print('Calculating difference')
difference = abs(np.diff(video_array))

print('Calculate mean_trace')
mean_trace = np.mean(difference, axis=(0, 1))

plt.figure()
plt.plot(mean_trace)
plt.xlabel('Time (frames)')
plt.ylabel('Difference (a.u.)')
plt.title('Video difference over time')

if save_movie:
    print('Saving')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for t in range(0, difference.shape[2]):
        filename = os.path.join(output_dir, "Image_" + str(t) + ".tiff")
        im = Image.fromarray(difference[:, :, t])
        im.save(filename)

if save_csv:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    filename = os.path.join(output_dir, "Mean_trace" + ".csv")
    np.savetxt(filename, mean_trace)

print('Finished. Total time taken: %s', datetime.now() - start_time)
